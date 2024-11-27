#!/usr/bin/python3
import os
import requests
import json
import yaml
import timeit
import pandas as pd

from flask import Flask, request, jsonify, Response
from pymongo import MongoClient, collection, cursor
from pymongo.errors import ConnectionFailure, BulkWriteError, DuplicateKeyError
from pprint import pprint
from bson.json_util import dumps
from json_encoder import JSONEncoder
from datetime import datetime, timedelta


DB_HOST = os.environ['DB_HOST']
DB_PORT = int(os.environ['DB_PORT'])

DB = 'datacube'
COLLS = [
    'solutions', 'AggDocPerSecond_v1','AggDocPerSecond_v2','RawDocPerSecond',
    'attributes','status','cards','hosts','duration'
    ]

LOG_FILE = 'logs/mylog.csv'
FLAG_CALCULATE_TIMES = int(os.environ['FLAG_CALCULATE_TIMES'])


myclient = None

app = Flask(__name__)



def write_to_timelog(operation, service_time):
    if FLAG_CALCULATE_TIMES == 1:
        filename = LOG_FILE
        try:
            if not os.path.exists(filename):
                # make a new file if not
                with open(filename, 'w') as f:
                    line = 'operation,service_time\r\n'
                    f.write(line)
            # append if already exists
            with open(filename, 'a') as f:
                line = operation+','+str(service_time)+'\r\n'
                f.write(line)
        except:
            print('[ERR]: cant write the log file')

@app.route('/times/gather', methods=['GET'])
def gather_times():
    df = pd.read_csv(LOG_FILE)
    json_df = df.to_json(orient='values')
    data = json.loads(json_df)    
    return jsonify({'msg': 'times gatered', 'data': data})

@app.route('/times/clean', methods=['DELETE'])
def clean_times():
    if request.method == 'DELETE':
        filename = LOG_FILE
        try:
            if os.path.exists(filename):
                # clean file if exists
                with open(filename, 'w') as f:
                    line = 'operation,service_time\r\n'
                    f.write(line)
        except:
            print('[ERR]: cant write the log file')
        resp = jsonify({'msg': 'log cleaned'})
    else:
        resp = jsonify({'msg': 'method not allowed'}), 405
    return resp



@app.before_first_request
def before_first_req_fun():
    conn_to_db()
    do_init_cube()

@app.before_request
def before_req_fun():
    conn_to_db()

def conn_to_db():
    global myclient
    # try:
    #     # Python 3.x
    #     from urllib.parse import quote_plus
    # except ImportError:
    #     # Python 2.x
    #     from urllib import quote_plus
    host = 'mongodb://'+DB_HOST+':'+str(DB_PORT)+'/'
    # uri = "mongodb://%s:%s@%s" % (quote_plus(user), quote_plus(password), host)
    try:
        myclient = MongoClient(
            host=host, 
            maxPoolSize=200, # Defaults to 100. Cannot be 0.
            connectTimeoutMS=30000, # Defaults to 20000 (20 seconds)
            # serverSelectionTimeoutMS=10000, # Defaults to 30000 (30 seconds)
            # waitQueueTimeoutMS=10000, # Defaults to None (no timeout). other 100
        )
    except:   
        myclient = None
        app.logger.fatal("Could not connect to db")

def do_init_cube():
    mydb = myclient[DB] # create db
    mycoll = mydb[COLLS[4]] # create collection
    if COLLS[4] not in mydb.list_collection_names():
        # mycoll.drop()
        attributes = [
            { "id": 1, "name": "Reliability"},
            { "id": 2, "name": "Efficiency"}
        ]
        do_insert_to_collection_many(mycoll, attributes)





@app.route('/', methods=['GET'])
def index():
    return 'Indexing module'



"""   DATA CUBE  database handling """
@app.route('/dbs', methods=['GET'])
def listDBs():
    db_list = myclient.list_database_names()
    return jsonify(db_list)

@app.route('/dbs/<string:db_name>/collections', methods=['GET'])
def listCollections(db_name):
    coll_list = myclient[db_name].list_collection_names()
    return jsonify(coll_list)

@app.route('/dbs/<string:db_name>/collections/<string:coll_name>/count_documents', methods=['GET'])
def listDocuments_count(db_name, coll_name):
    mydb = myclient[db_name]
    mycoll = mydb[coll_name]
    ndocs = mycoll.count_documents({}) # this yes
    if ndocs > 0:
        resp = jsonify({'msg':'documents found', 'n': ndocs})
    else:
        resp = jsonify({'msg':'not found'})
        resp.status_code = 400 
    return resp

@app.route('/dbs/<string:db_name>/collections/<string:coll_name>/documents/<int:n>', methods=['GET'])
def listDocuments(db_name, coll_name,n):
    if n > 0: 
        mydb = myclient[db_name]
        mycoll = mydb[coll_name]
        query = {}
        projection = {'_id': 0}
        sort = [
        ('last', -1) #pymongo.DESCENDING)
        ]

        ndocs,find_all = select_docs_in_coll(mycoll,query,projection,n,sort)
        if ndocs > 0:
            documents = parse_docs(find_all,ndocs)
            resp = jsonify({'msg':'documents found', 'n': ndocs, 'data': documents})
        else:
            resp = jsonify({'msg':'not found'})
            resp.status_code = 400
    else:
            resp = jsonify({'msg':'n must be greater than 0'})
            resp.status_code = 400 
    return resp

def parse_docs(result,n):
    docs = []
    for i in range(n):
        try:
            doc = json.loads( JSONEncoder().encode(result[i]) )
        except:
            doc = parse_doc_containing_date_v1_v2(result[i])

        docs.append(doc)
    return docs

def parse_doc_containing_date_v1_v2(doc):
    """
    parse cursor to json, 
    when cursor contains datetime fields in
    first level and second level
    (into an array element)
    """
    new_doc = {}
    for k,v in doc.items():
        if k in ['first','last','creation_time']:
            # convert datetime.datetime to str
            v = parse_RFC3339_datetime_to_str(v)

        # for v1
        if k == 'timestamp':
            if type(v) is list:
                t_stamps = []
                for t in v:
                    # convert datetime.datetime to str
                    t_stamps.append( parse_RFC3339_datetime_to_str(t) )
                v = t_stamps
            else:
                v = parse_RFC3339_datetime_to_str(v)
            
        
        # for v2
        if k == 'samples':
            samples = []
            for sample in v:
                parsed_sample = {}
                for k_s,v_s in sample.items():
                    if k_s == 'timestamp':
                        # convert datetime to str
                        v_s = parse_RFC3339_datetime_to_str(v_s)
                    parsed_sample[k_s] = v_s
                samples.append(parsed_sample)
            v = samples
        
        new_doc[k] = v
    new_doc = json.loads( JSONEncoder().encode(new_doc) )
    return new_doc

def parse_RFC3339_datetime_to_str(date_time):
    return datetime.strftime(date_time, '%Y-%m-%dT%H:%M:%S.%fZ')

def parse_RFC3339_str_to_datetime(date_time):
    return datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S.%fZ')


"""   BEFORE MONITORING   """
@app.route('/hosts', methods=['POST','GET'])
def add_get_hosts():
    """
    (POST) add host metrics to indexing,
    (GET) return query information of all hosts 
    """
    if request.method == 'POST':
        data_r = request.json
        r_count = 0
        if data_r and type(data_r) is list and len(data_r) > 0:
            r_lst = []
            for h in data_r:
                if h.get('location'):
                    resp = do_add_host(h.get('location'),h)
                    if resp:
                        r_lst.append( resp )
                        r_count += 1
                    else:
                        r_lst.append(None) 
                else:
                    r_lst.append(None) 

        if len(data_r) == 0 or r_count == 0:
            msg = {'msg': 'Host was not saved'}
            status = 500
        elif r_count == len(data_r):
            msg = {'msg': 'Host was saved','data': r_lst}
            status = 201
        else:
            msg = {'msg': 'Host was saved, some are duplicated','data': r_lst}
            status = 201

    elif request.method == 'GET':
        mydb = myclient[DB]
        mycoll= mydb[COLLS[7]]
        query = {}
        ndocs,cursor = select_docs_in_coll(mycoll,query)
        if ndocs > 0:
            documents = parse_docs(cursor,ndocs)
            msg = {'msg': 'Hosts found','data': documents}
            status = 200
        else:
            msg = {"msg": "Hosts not found"}
            status = 400

    else:
        msg = {'msg': 'method not allowed'}
        status = 405

    return jsonify(msg),status

def do_add_host(key,data_to_insert):
    mydb = myclient[DB]
    mycoll = mydb[COLLS[7]]
    key_filter = {'location':key}
    update = {'$setOnInsert': data_to_insert}
    res = do_upsert_to_collection_one(mycoll,key_filter,update)
    return res

@app.route('/solutions', methods=['POST','GET'])
def add_get_solutions():
    """
    (POST) add new solution to indexing,
    (GET) return query information of all solutions 
    """
    if request.method == 'POST':
        data_solution = request.json
        s_id = data_solution.get('id')

        resp_add = do_add_solution(s_id,data_solution) # TODO: verify if exists
        
        if resp_add == 'Ok':
            data = {'id': resp_add}
            msg = {'msg': 'Solution was saved','data': data}
            status = 201
        elif resp_add == 'Duplicated':
            msg = {'msg': resp_add}
            status = 400
        else:
            msg = {'msg': 'Solution was not saved'}
            status = 500

    elif request.method == 'GET':
        # TODO: get solutions active,inactive,all
        # currently support only active
        mydb = myclient[DB]
        mycoll= mydb[COLLS[0]]
        query = {'active': True}
        projection = {'_id':0,'full_yml':0} 
        ndocs,cursor = select_docs_in_coll(mycoll,query,projection=projection)
        if ndocs > 0:
            documents = parse_docs(cursor,ndocs)
            msg = {'msg': 'Solutions found','data': documents}
            status = 200
        else:
            msg = {"msg": "Solutions not found"}
            status = 400
    else:
        msg = {'msg': 'method not allowed'}
        status = 405
    return jsonify(msg),status

def do_add_solution(sol_id,data_solution):
    mydb = myclient[DB] # create db
    mycoll = mydb[COLLS[0]] # create collection
    key = {'id':sol_id}
    update = {'$setOnInsert': data_solution}
    res = do_upsert_to_collection_one(mycoll,key,update)
    return res

def do_upsert_to_collection_one(mycoll,filter,update):
    res = None
    try:
        # In python upsert must be passed as a keyword argument
        result = mycoll.update_one(filter=filter, update=update, upsert=True)
        res = result.raw_result
        if res.get('upserted'):
            res = 'Ok'
        elif res.get('updatedExisting') == True:
            res = 'Duplicated'
        else:
            res = 'Error'
    except:
        # pprint(bwe.details)
        res = 'Error'
    return res

@app.route('/solutions/<string:sol_id>', methods=['GET'])
def get_solution(sol_id):
    mydb = myclient[DB]
    mycoll = mydb[COLLS[0]]
    query = {'id': sol_id}
    projection = {'_id': 0}

    ndocs, cursor = select_docs_in_coll(mycoll, query, projection=projection)
    if ndocs > 0:
        msg = {
            'msg': 'Solution found',
            'data': cursor[0]
            }
        resp = jsonify(msg)
    else:
        query = {'name': sol_id}
        ndocs, cursor = select_docs_in_coll(mycoll, query, projection=projection)
        if ndocs > 0:
            msg = {
                'msg': 'Solution found',
                'data': cursor[0]
                }
            resp = jsonify(msg)
        else:
            msg = {"msg": "Solution not found"}
            resp = jsonify(msg)
            resp.status_code = 400
    return resp


""" WHILE MONITORING """
@app.route('/solutions/<string:sol_id>/metrics', methods=['POST'])
def add_solution_metrics(sol_id):
    """
    (POST) add the solution metrics to indexing,
    """
    starttime = timeit.default_timer()

    if request.method == 'POST':
        req = request.json
        # print(f'req: {req}')
        id_sol = req.get('id')
        name_sol = req.get('name')
        n_samples = 0
        first_ts = None
        last_ts = None
        missing_data = 0

        # if there are containers do for each container
        contrs = req.get('containers')
        if contrs:
            for i in range(len(contrs)):
                # validate if container has data
                if contrs[i]:
                    id_cont = contrs[i].get('id')
                    name_cont = contrs[i].get('name')
                    host = contrs[i].get('location')

                    # define stats versions
                    st_v1 = contrs[i].get('stats_v1')
                    st_v2 = contrs[i].get('stats_v2')
                    # st_raw = contrs[i].get('stats_raw')
                    
                    if st_v1:
                        ts = st_v1.get('timestamp')
                        n_samples = 0
                        first_ts = None
                        last_ts = None
                        if ts:
                            n_samples = (len(ts) if type(ts) is list else 0)
                            if n_samples > 0:
                                first_ts = parse_RFC3339_str_to_datetime(ts[0])
                                last_ts = parse_RFC3339_str_to_datetime(ts[-1])
                            else:
                                print(f'ts: {type(ts)}')
                                print(f'ts: {ts}')
                                first_ts = parse_RFC3339_str_to_datetime(ts)
                                last_ts = first_ts
                        sample = {
                            'id_solution': id_sol,
                            'name_solution': name_sol,
                            'id_container': id_cont,
                            'name_container': name_cont,
                            'host': host,
                            'n': n_samples,
                            'first': first_ts,
                            'last': last_ts,
                        }

                        for k,v in st_v1.items():
                            if k == 'timestamp':
                                if type(v) is list:
                                    # convert str timestamp to datetime,
                                    # this allow to query docs by date in mongo
                                    ts_parsed = []
                                    for t in v:
                                        ts_parsed.append( parse_RFC3339_str_to_datetime(t) )
                                else:
                                    ts_parsed = parse_RFC3339_str_to_datetime(ts)
                                sample[k] = ts_parsed
                            else:
                                sample[k] = v
                        
                        mydb = myclient[DB]
                        mycoll = mydb[COLLS[1]]
                        do_insert_to_collection_one(mycoll,sample)
                    
                    if st_v2:
                        samples = []
                        for j in range(len(st_v2)):
                            st = st_v2[j]
                            st['timestamp'] = parse_RFC3339_str_to_datetime( st.get('timestamp') )
                            st['id_container'] = id_cont
                            st['name_container'] = name_cont
                            samples.append(st)
                        
                        sample = {
                            'id_solution': id_sol,
                            'name_solution': name_sol,
                            'n': n_samples,
                            'first': first_ts,
                            'last': last_ts,
                            'samples': samples
                            }
                        mydb = myclient[DB]
                        mycoll = mydb[COLLS[2]]
                        do_insert_to_collection_one(mycoll,sample)

                    # if st_raw:
                    #     for j in range(len(st_raw)):
                    #         sample_raw = st_raw[j]
                    #         sample_raw['id_solution'] = id_sol
                    #         sample_raw['id_container'] = id_cont
                    #         sample_raw['name_container'] = name_cont
                            
                    #         # save each metric with original timestamp
                    #         mydb = myclient[DB]
                    #         mycoll = mydb[COLLS[3]]
                    #         do_insert_to_collection_one(mycoll,sample)
                    
                    # missing_data = 1
                else:
                    missing_data += 1
                    # TODO: request to update container ids to manager
        if missing_data == len(contrs):
            app.logger.error('No container with data')
            resp = jsonify({'msg': 'metrics not added'}), 400
        elif missing_data > 0:
            resp = jsonify({'msg': 'some metrics added'}), 400
        else:
            resp = jsonify({'msg': 'metrics added'})
            
    
    else:
        resp = jsonify({'msg': 'method not allowed'})
        resp.status_code = 405
    
    takentime = timeit.default_timer() - starttime
    write_to_timelog('idx', takentime)

    return resp

@app.route('/solutions/<string:sol_id>/begin-end', methods=['POST'])
def add_solution_begin_end(sol_id):
    if request.method == 'POST':
        rjson = request.json
        if rjson:
            rjson['id'] = sol_id
            if rjson.get('begin'):
                b = rjson.get('begin')
                rjson['begin'] = parse_RFC3339_str_to_datetime(b)
            if rjson.get('end'):
                e = rjson.get('end')
                rjson['end'] = parse_RFC3339_str_to_datetime(e)
            
        resp_add = do_add_begin_end(sol_id,rjson)
        
        if resp_add == 'Ok':
            data = {'id': resp_add}
            msg = {'msg': 'Duration was saved','data': data}
            status = 201
        elif resp_add == 'Duplicated':
            msg = {'msg': resp_add}
            status = 400
        else:
            msg = {'msg': 'Duration was not saved'}
            status = 500
    else:
        msg = {'msg': 'method not allowed'}
        status = 405
    return jsonify(msg),status

def do_add_begin_end(sol_id,data):
    mydb = myclient[DB]
    mycoll = mydb[COLLS[8]]
    key = {'id':sol_id}
    update = {'$setOnInsert': data}
    res = do_upsert_to_collection_one(mycoll,key,update)
    return res

@app.route('/solutions/<string:sol_id>/container_ids', methods=['PUT'])
def update_solution_containers(sol_id):
    """
    (PUT) UPDATE the solution container ids to indexing
    """
    if request.method == 'PUT':
        req = request.json

        mydb = myclient[DB] # select db
        mycoll = mydb[COLLS[0]] # select collection
        query = {'id': sol_id}
        updates = {'$set': {'containers': req} }
        
        up = do_update_elem_one(mycoll, query, updates)
            
        if True:
            resp = jsonify({'msg': 'ids updated'})
        else:
            resp = jsonify({'msg': 'ids not updated'}), 404
    
    else:
        resp = jsonify({'msg': 'method not allowed'})
        resp.status_code = 405
    
    return resp



""" AFTER MONITORING """
@app.route('/solutions/status', methods=['POST'])
def add_solution_status():
    """ save status produced by diagnosis

    Returns:
        [type]: [description]
    """
    if request.method == 'POST':
        doc = request.json
        ct = doc.get('creation_time')
        if ct:
            doc['creation_time'] = parse_RFC3339_str_to_datetime(ct)
        mydb = myclient[DB]
        mycoll = mydb[COLLS[5]]
        insrt = do_insert_to_collection_one(mycoll,doc)

        if insrt != 'Duplicated':
            resp = jsonify({'msg': 'status added'})
        else:
            resp = jsonify({'msg': 'status not added'}), 400
    else:
        resp = jsonify({'msg': 'method not allowed'})
        resp.status_code = 405
    return resp

@app.route('/solutions/status/<string:exp_name>', methods=['GET'])
def get_solution_status(exp_name):
    """ get the most recent status with name exp_name

    Args:
        exp_name (str): name to identify the status

    Returns:
        [type]: [description]
    """
    if request.method == 'GET':
        mydb = myclient[DB]
        mycoll = mydb[COLLS[5]]

        query = {'exp_name': exp_name}
        projection = {'_id':0}
        sort = [
            ('creation_time', -1) # descending
        ]
        ndocs,cursor = select_docs_in_coll(mycoll,query,projection=projection,limit=1,sort=sort)
        if ndocs > 0:
            cursor = parse_docs(cursor,ndocs)
            msg = {
                'msg': 'Status found',
                'data': cursor[0]
                }
            resp = jsonify(msg)
        else:
            msg = {"msg": "Status not found"}
            resp = jsonify(msg)
            resp.status_code = 400
    else:
        resp = jsonify({'msg': 'method not allowed'})
        resp.status_code = 405

    return resp

@app.route('/solutions/td-cards', methods=['POST'])
def add_solution_td_cards():
    """
    (POST) save the solution Thing Description cards to indexing,
    """

    if request.method == 'POST':
        doc = request.json
        dtn = datetime.now()
        doc['dt_created'] = dtn
        mydb = myclient[DB]
        mycoll = mydb[COLLS[6]]
        insrt = do_insert_to_collection_one(mycoll,doc)

        if insrt != 'Duplicated':
            resp = jsonify({'msg': 'cards added'})
        else:
            resp = jsonify({'msg': 'cards not added'}), 400

    else:
        resp = jsonify({'msg': 'method not allowed'})
        resp.status_code = 405

    return resp

@app.route('/solutions/<string:sol_id>/td-cards/<int:limit>', methods=['GET'])
def get_solution_td_cards(sol_id,limit):
    mydb = myclient[DB]
    mycoll = mydb[COLLS[6]]

    query = {'sol_id': sol_id}
    projection = {'_id':0}
    sort = [
    ('dt_ini', -1) #pymongo.DESCENDING)
    ]

    ndocs,cursor = select_docs_in_coll(mycoll,query,projection=projection,limit=limit,sort=sort)
    if ndocs > 0:
        msg = {
            'msg': 'Solution found',
            'data': cursor[0]
            }
        resp = jsonify(msg)
    else:
        msg = {"msg": "Solution not found"}
        resp = jsonify(msg)
        resp.status_code = 400

    return resp







"""
INSERTS
"""
def do_insert_to_collection_one(mycoll, document):
    res = None
    try:
        result = mycoll.insert_one(document)
        res = result.inserted_id
    except DuplicateKeyError as bwe:
        # pprint(bwe.details)
        res = 'Duplicated'
    return res

def do_insert_to_collection_many(mycoll, documents):
    res = None
    if len(documents) > 1:
        try:
            result = mycoll.insert_many(documents)
            res = result.inserted_ids
        except DuplicateKeyError as bwe:
            # pprint(bwe.details)
            res = 'Error'
    return res

"""
UPDATES
"""
@app.route('/solutions/<string:sol_id>/update_elem', methods=['PUT'])
def update_elem(sol_id):
    mydb = myclient[DB] # select db
    mycoll = mydb[COLLS[0]] # select collection
    # query = {'name': 'prototype.yml'}
    query = {'id': sol_id}
    updates = {'$set': {'active': False} }
    nupdates = do_update_elem_one(mycoll, query, updates)
    if nupdates > 0:
        status = 200
    else:
        status = 400
    return jsonify({'nModified': nupdates}),status

def do_update_elem_one(mycoll, query, updates):
    result = mycoll.update_one(query, updates)
    if result:
        # options: matched_count, modified_count, raw_result, upserted_id
        result = result.modified_count
    else:
        result = 0
    return result


@app.route('/solutions/<string:sol_id>/update_arrelem', methods=['GET'])
def update_arrelem(sol_id):
    mydb = myclient[DB] # select db
    mycoll = mydb[COLLS[0]] # select collection

    arr_name = 'containers'
    arr_elem = '04456d003c80d4620c8d3e368335b053fcbbe0b71a61ad7d555799d927b4c738'
    field_to_change = 'status'
    value_to_change = 'updating'

    query = {
        'id': sol_id, 
        arr_name: { '$elemMatch': {'id': arr_elem} } 
    }
    updates = { '$set': {arr_name+'.$.'+field_to_change: value_to_change} }

    return do_update_elem_one(mycoll, query, updates)

"""
DELETES
"""
@app.route('/solutions/<string:sol_id_or_name>/metrics/<int:del_metrics>', methods=['DELETE'])
def delete_doc(sol_id_or_name,del_metrics):
    """Remove solution and its metric items

    Args:
        sol_id_or_name (str): [description]
        del_metrics (int): [description]

    Returns:
        json: a message and number of documents deleted
    """
    mydb = myclient[DB] # select db
    mycoll = mydb[COLLS[0]] # select collection
    
    msg = 'Not found'
    status = 500
    mdel = {}

    query = {'id': sol_id_or_name}
    res = do_delete_doc_one(mycoll, query)
    if res and res.get('n'):
        msg = 'solution deleted'
        status = 200
    else:
        query = {'name': sol_id_or_name}
        res = do_delete_doc_one(mycoll, query)
        if res and res.get('n'):
            msg = 'solution deleted'
            status = 200
    
    if del_metrics == 1:
        mycoll = mydb[COLLS[1]]
        query = {'id_solution': sol_id_or_name}
        rid = do_delete_doc_many(mycoll, query)
        if rid and rid.get('n')>0:
            mdel = rid
        else:
            query = {'name_solution': sol_id_or_name}
            rnm = do_delete_doc_many(mycoll, query)
            if rnm and rnm.get('n')>0:
                mdel = rnm

        if not mdel:
            mdel = rid

    if msg == 'Not found':
        status = 404
    
    return jsonify({'msg':msg, 'ndocs_deleted':mdel}), status

def do_delete_doc_one(mycoll, query):
    info = mycoll.delete_one(query)
    # print(info.raw_result)
    return info.raw_result

def do_delete_doc_many(mycoll, query):
    info = mycoll.delete_many(query)
    # print(info.raw_result)
    return info.raw_result






"""
SELECTS
"""
def select_docs_in_coll(coll, query, projection=None,limit=0,sort=None):
    """Generic find function to perform select query to mongo database. 

    Args:
        coll ([type]): [description]
        query (dict): [description]
        projection (dict, optional): [description]. Defaults to None.
        limit (int, optional): [description]. Defaults to 0.
        sort (int, optional): [description]. Defaults to None.

    Returns:
        [int,Cursor]: [description]
    """
    ndocs = coll.count_documents(query)
    find_all = None

    if ndocs>0:
        newlimit = (ndocs if (limit>0) and (ndocs<limit) else limit)
        if newlimit>0:
            ndocs = newlimit
        # find(filter=None, projection=None, skip=0, limit=0, no_cursor_timeout=False, 
        # cursor_type=CursorType.NON_TAILABLE, sort=None, allow_partial_results=False, 
        # oplog_replay=False, modifiers=None, batch_size=0, manipulate=True, 
        # collation=None, hint=None, max_scan=None, max_time_ms=None, max=None, 
        # min=None, return_key=False, show_record_id=False, snapshot=False, 
        # comment=None, session=None)
        find_all = coll.find(filter=query,projection=projection,limit=newlimit,sort=sort)

    return ndocs, find_all





    

if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0', 
        # debug=True, 
        threaded=True
    )
