from flask import Blueprint, jsonify, request
from flask_api import status
import pandas as pd
import json
import os
import requests
from .constants import LOG_FILE, FLAG_CALCULATE_TIMES
from .constants import IDX_PAIR, MTR_PAIR, RPR_PAIR, DGS_PAIR


time_bp = Blueprint("time_measurement", __name__)


@time_bp.route('/times/gather/<string:to_file>', methods=['GET'])
def gather_times(to_file):
    df = pd.read_csv(LOG_FILE)
    json_df = df.to_json(orient='values')
    data = json.loads(json_df)
    times_wo_titles = []
    for pair in (IDX_PAIR, MTR_PAIR, RPR_PAIR, DGS_PAIR):
        j_req = request_module_times(pair)
        if j_req and j_req.get('data'):
            times_wo_titles.extend(j_req.get('data'))
    times_wo_titles.extend(data)
    df = pd.DataFrame(times_wo_titles,columns=['operation', 'service_time'])
    export_to_csv(to_file,df,False)
    return jsonify({'msg': 'times gatered'})

@time_bp.route('/times/clear', methods=['DELETE'])
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
        for pair in (IDX_PAIR, MTR_PAIR, RPR_PAIR, DGS_PAIR):
            j_req = request_clean_times(pair)
        
        if j_req:
            resp = jsonify({'msg': 'log cleaned'})
        else:
            resp = jsonify({'msg': 'log not cleaned'}), 500
    else:
        resp = jsonify({'msg': 'method not allowed'}), 405
    return resp

def request_module_times(pair):
    url = 'http://'+pair+'/times/gather'
    data = {}
    try:
        r = requests.get(url)
        if r and r.status_code == 200:
            data = r.json()
    except requests.exceptions.RequestException as e:
        print('Couldnt get times')
    return data

def write_to_timelog(operation, service_time):
    if FLAG_CALCULATE_TIMES == 1:
        filename = LOG_FILE
        try:
            if not os.path.exists(filename):
                # make a new file if not exist
                with open(filename, 'w') as f:
                    line = 'operation,service_time\r\n'
                    f.write(line)
            # append if already exists
            with open(filename, 'a') as f:
                line = operation+','+str(service_time)+'\r\n'
                f.write(line)
        except:
            print('[ERR]: cant write the log file')

def request_clean_times(pair):
    url = 'http://'+pair+'/times/clean'
    data = {}
    try:
        r = requests.delete(url)
        if r and r.status_code == 200:
            data = r.json()
    except requests.exceptions.RequestException as e:
        print('Couldnt clean times')
    return data

def export_to_csv(filename,data,flag_idx):
    """save data to csv file

    Args:
        filename (str): the filename to save with
        data (object): could be [dict | list | pd.DataFrame]
        flag_idx (bool): define if save file with the index numbers

    Returns:
        int: 1 if saved -1 if not
    """
    filename = (filename if '.csv' in filename else filename+'.csv')
    saved = 0
    try:
        if data is dict:
            df = pd.read_json(data)
        elif data is list:
            df = pd.DataFrame(data)
        else:
            df = data

        not_svd = df.to_csv(filename, index = flag_idx)
        if not not_svd:
            saved = 1
            print(f'file saved: {filename}')
        else:
            saved = -1
    except:
        print('Error saving csv '+filename)
        saved = -1

    return saved