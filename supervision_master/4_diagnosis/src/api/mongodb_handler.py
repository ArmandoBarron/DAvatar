from pymongo import MongoClient
from .constants import DB_PAIR, DB_DATACUBE, CL_RESOURCES

myclient = None
try:
  myclient = MongoClient('mongodb://'+DB_PAIR+'/',
  waitQueueTimeoutMS=100, maxPoolSize=200)
  print("Connected successfully!")
except:   
  print("Could not connect to db")

def begin_end_idx_date_v1(id_or_name_sol):
    begin_end = ''
    mydb = myclient[DB_DATACUBE]
    mycoll = mydb[CL_RESOURCES[2]]
    query = {'name': id_or_name_sol}
    projection = {'_id': 0}
    sort = [
        ('end', -1) #pymongo.DESCENDING)
    ]
    ndocs, find_all = select_docs_in_coll(mycoll, query, projection, sort=sort)
    
    if ndocs > 0:
        begin_end = find_all[0]
    else:
        print('duration not found, trying bot_top')

        result = get_bot_top_dates(CL_RESOURCES[0], id_or_name_sol)
        if len(result) > 0:
            diff = diff_in_mins(result[0].get('minimumDate'), result[0].get('maximumDate'))
            begin_end = {
                'begin': result[0].get('minimumDate'),
                'end': result[0].get('maximumDate'),
                'diff_in_mins': diff
            }
    
    return begin_end

def get_period_alldocs(name_sol):
    # prepare to access the db
    mydb = myclient[DB_DATACUBE]
    mycoll = mydb[CL_RESOURCES[0]]
    query = {'name_solution': name_sol}
    projection = {'_id': 0}

    # get raw docs in period, from index
    ndocs, result = select_docs_in_coll(mycoll, query, projection)
        
    return ndocs, result

def get_host_info(location):
    mydb = myclient[DB_DATACUBE]
    mycoll = mydb[CL_RESOURCES[1]]
    query = {'location': location}
    projection = {'_id': 0}
    ndocs = mycoll.count_documents(query)
    result = None
    if ndocs > 0:
        result = mycoll.find(query,projection)
    return result, ndocs

def get_bot_top_dates(coll, id_sol):
    """
    lowest and highest dates
    """
    mydb = myclient[DB_DATACUBE]
    mycoll = mydb[coll]
    pipeline = [
        { '$match': {'$or': [ {'name_solution': id_sol }, {'id_solution': id_sol }]} },
        { '$group' : {
                '_id' : -1,
                'minimumDate': { '$min': "$first" },
                'maximumDate': { '$max': "$last" }
            }
        }
    ]
    result = mycoll.aggregate(pipeline)
    result = list(result)
    if len(result) == 0:
        pipeline = [
            { '$match': {'$or': [ {'name_solution': id_sol }, {'id_solution': id_sol }]} },
            { '$group' : {
                    '_id' : -1, 
                    'minimumDate': { '$min': "$timestamp" },
                    'maximumDate': { '$max': "$timestamp" }
                }
            }
        ]
        result = mycoll.aggregate(pipeline)
        result = list(result)
    return result

def get_period_btwn_begin_end(name_sol, begin, end):
    # prepare to access the db
    mydb = myclient[DB_DATACUBE]
    mycoll = mydb[CL_RESOURCES[0]]
    
    # query = {
    #     '$and': [
    #         {'first': {'$gte': begin}},
    #         {'last': {'$lte': end}},
    #         {'$or': [{'name_solution': name_sol},{'id_solution': name_sol}]}
    #     ]
    # }

    query = {
        '$and': [
            {'timestamp': {'$gte': begin}},
            {'timestamp': {'$lte': end}},
            {'name_solution': name_sol}
        ]
    }
    projection = {'_id': 0}
    ndocs = mycoll.count_documents(query)
    result = mycoll.find(query,projection)

    return ndocs, result

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
    result = None

    if ndocs>0:
        newlimit = (ndocs if (limit > 0) and (ndocs < limit) else limit)
        if newlimit > 0:
            ndocs = newlimit
        # find(filter=None, projection=None, skip=0, limit=0, no_cursor_timeout=False, 
        # cursor_type=CursorType.NON_TAILABLE, sort=None, allow_partial_results=False, 
        # oplog_replay=False, modifiers=None, batch_size=0, manipulate=True, 
        # collation=None, hint=None, max_scan=None, max_time_ms=None, max=None, 
        # min=None, return_key=False, show_record_id=False, snapshot=False, 
        # comment=None, session=None)
        result = coll.find(filter=query, projection=projection, limit=newlimit, sort=sort)

    return ndocs, result

def diff_in_mins(init, end):
    difference = end - init
    seconds_in_day = 24 * 60 * 60
    return divmod(difference.days * seconds_in_day + difference.seconds, 60)