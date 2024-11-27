#!/usr/bin/python3
# to see resultant data
# http://localhost:54350/{METAWORKFLOW}/stadistics_all_data/
# http://localhost:54350/{METAWORKFLOW}/{label}/
# http://localhost:54350/STUDY-CASE-TEST/stadistics_pollutants/

import os
import requests
import time
import timeit
from flask import Flask, request, Response, json, jsonify
from TPS.Builder import Builder # TPS API BUILDER
from base64 import b64decode,b64encode

LOCALHOST = os.environ['LOCALHOST']

metaworkflow=Builder("STUDY-CASE-TEST",TPS_manager_host="http://"+LOCALHOST+":54350")
# folder = 'Pollutants-data/19RAMA/'
log_path = '.'
list_pollutants =['CO','NO','NO2','NOX','O3','PM10','PM25',"SO2"]
folder1 = 'Pollutants-plots/'
folder2 = 'Pollutants-clust/'

app = Flask(__name__)

@app.errorhandler(500)
def server_error(e):
    app.logger.error('An error occurred during a request. %s', e)
    return jsonify({'msg': 'An internal error occured'}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({'msg': 'API for Study case'})

@app.route('/load-data', methods=['GET'])
def load_data():
    return jsonify({'msg': 'Please use POST'})

@app.route('/load-data', methods=['POST'])
def load_data_p():
    if request.method == 'POST':
        rj = request.json
        folder = rj.get('source-folder')
        if folder and os.path.exists(folder):

            pollutants = []
            times = []
            responses = []

            i = 0
            # read and add dataset in folder
            for d in os.listdir(folder):
                subdir = os.path.join(folder,d)
                if os.path.isdir(subdir):
                    print(f'{d}, {subdir}')
                    pollutants.append([d,subdir])
                    metaworkflow.TPSapi.PutData(subdir,d) # folder, name
                    i+=1
                    # if i > 1: # only load the first two
                    #     break 

            extraction_time = timeit.default_timer() ## <--------------- TIME
            metaworkflow.init_tps() # all the extractor defined are executed
            extraction_time = timeit.default_timer() - extraction_time ## <--------------- TIME

            if len(pollutants) > 0:
                for plltt,subdir in pollutants:
                    
                    # first cleaning
                    fc_time = timeit.default_timer() ## <--------------- TIME
                    query = metaworkflow.TPSapi.format_single_query(plltt) # query
                    res = metaworkflow.TPSapi.TPS(query,"cleaningtools",options={"columns":"all","ReplaceWithNa":['None',-99,-99.0,'NaN','nan'],"DropNa":None,\
                                            "NaReaplace":"interpolate"},label="clean_"+plltt)
                    fc_time = timeit.default_timer() - fc_time ## <--------------- TIME
                    print(res)
                    responses.append(res)

                    # transform columns to records with the label stations
                    tr_time = timeit.default_timer() ## <--------------- TIME
                    query = metaworkflow.TPSapi.format_single_query("clean_"+plltt) # query to a single task
                    res= metaworkflow.TPSapi.TPS(query,"transform",options={"process":"melt","id_vars":['FECHA','HORA'],"var_name":"stations","value_name":plltt },label="T_"+plltt)
                    tr_time = timeit.default_timer() - tr_time ## <--------------- TIME
                    print(res)
                    responses.append(res)

                    # group all the records which has the same FECHA and station values. 
                    # This help us to reduce data. data producen in a single day by the same station is grouped by mean.
                    gr_time = timeit.default_timer() ## <--------------- TIME
                    query = metaworkflow.TPSapi.format_single_query("T_"+plltt) # query to a single task
                    res= metaworkflow.TPSapi.TPS(query,"transform",options={"process":"group","group":['FECHA','stations'],"variable":plltt,"group_by":"mean" },label="group_"+plltt)
                    gr_time = timeit.default_timer() - gr_time ## <--------------- TIME
                    print(res)
                    responses.append(res)

                    times.append((plltt,extraction_time,fc_time,tr_time,gr_time))
            save_times_to_file(log_path,times)
            res = {'msg': 'Data loaded', 'data': responses}
            status = 200
        else:
            res = {'msg': 'invalid or missing params'}
            status = 400
    else:
        res = {'msg': 'method not allowed'}
        status = 405
    return jsonify(res), status


@app.route('/group-all-data', methods=['GET'])
def group_all_data():
    """al final este script agrupa todas las columnas de los contaminantes en una sola tabla llamada pollutants
    """
    responses = []
    init_time = timeit.default_timer() ## <--------------- TIME
    query = metaworkflow.TPSapi.format_query("group_CO","group_NO",keygroups=["FECHA-FECHA","stations-stations"])
    res = metaworkflow.TPSapi.TPS(query,"getdata",label="pollutants")
    list_data = ["NO2","NOX","O3","PM10","PM25","PMCO","SO2"]
    for pollutant in list_data:
        query = metaworkflow.TPSapi.format_query("pollutants","group_"+pollutant,keygroups=["FECHA-FECHA","stations-stations"])
        res = metaworkflow.TPSapi.TPS(query,"getdata",label="pollutants")
        print(res)
        responses.append(res)
    end_time = timeit.default_timer() - init_time ## <--------------- TIME

    save_times_to_file(log_path,end_time)
    return jsonify({'msg': 'Data grouped', 'data': responses}), 200

@app.route('/statistics-by-column', methods=['GET'])
def statistics_by_column():
    query = metaworkflow.TPSapi.format_single_query("pollutants") #query to a single task
    result_desc = metaworkflow.TPSapi.TPS(query,"describe",options={'columns':'all'},label="stadistics_pollutants")
    print(result_desc)
    return jsonify({'msg': 'Statistics by column', 'data': result_desc}), 200


@app.route('/histograms-by-variable', methods=['GET'])
def histograms_by_variable():
    results = []
    create_subfolders_777(folder1)
    # Create a histogram of each pollutant
    for poll in list_pollutants:
            query = metaworkflow.TPSapi.format_single_query("pollutants") # query to a single task
            res= metaworkflow.TPSapi.TPS(query,"graphics",options={"kind":"hist","variables":[poll],"alpha":.25,"bins":20 })
            results.append(res['filename'])
            with open(folder1+poll+"_"+res['filename'],"wb") as file:
                    file.write(res['result'])
    return jsonify({'msg': 'plots saved', 'data': results}), 200


@app.route('/perform-clustering', methods=['GET'])
def perform_clustering():
    responses = []
    create_subfolders_777(folder2)
    # get some clusters ange make a graphic
    # we use a clustering alghoritm to see the behavior of this difference
    for poll in list_pollutants:
        query = metaworkflow.TPSapi.format_single_query("pollutants") # query to a single task
        res = metaworkflow.TPSapi.TPS(query,"clustering",options={"k":3,"alghoritm":"kmeans","variables":poll},label="clust_"+poll)
        print(res)
        responses.append(res)
        
        query = metaworkflow.TPSapi.format_single_query("pollutants") # query to a single task
        res = metaworkflow.TPSapi.TPS(query,"clustering",options={"alghoritm":"silhouette","variables":poll})
        print('saved clust silhouette')
        responses.append(res['result']['filename'])
        with open(folder2+res['result']['filename'],"wb") as file:
                file.write(b64decode(res['result']['image'].encode()))
    return jsonify({'msg': 'plots saved', 'data': responses}), 200



def create_subfolders_777(path):
    cr = 0
    access_rights = 0o777 # octal prefix (0o)
    try:
        if not os.path.exists(path):
            os.makedirs(path, access_rights)
            cr = 1
    except OSError:
        print (f'Creation of the directory {path} failed')
    return cr

def save_times_to_file(log_path,times):
    if type(times) is list: 
        logfile = open(log_path+"/log1-load.txt", "a+")
        for plltt,extraction_time,fc_time,tr_time,gr_time in times:
            logfile.write( "%s,%s,%s,%s,%s\r\n" %(plltt,extraction_time,fc_time,tr_time,gr_time) )
        logfile.close()
    else:
        logfile = open(log_path+"/log2-join.txt", "a+")
        logfile.write("%s\n" %(times))
        logfile.close()

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True, threaded=True)
