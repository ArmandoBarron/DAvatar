from flask import Blueprint, jsonify, request
from flask_api import status
import pandas as pd
import json
import os
from .constants import LOG_FILE, FLAG_CALCULATE_TIMES

time_bp = Blueprint("time_measurement", __name__)

@time_bp.route('/times/gather', methods=['GET'])
def gather_times():
  df = pd.read_csv(LOG_FILE)
  json_df = df.to_json(orient='values')
  data = json.loads(json_df)    
  return jsonify({'msg': 'times gatered', 'data': data})

@time_bp.route('/times/clean', methods=['DELETE'])
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
    resp = jsonify({'msg': 'method not allowed'}), status.HTTP_405_METHOD_NOT_ALLOWED
  return resp

def write_to_timelog(operation, service_time):
  if FLAG_CALCULATE_TIMES == 1:
    try:
      if not os.path.exists(LOG_FILE):
        # make a new file if not exist
        with open(LOG_FILE, 'w') as f:
          line = 'operation,service_time\r\n'
          f.write(line)
      # append if already exists
      with open(LOG_FILE, 'a') as f:
        line = operation+','+str(service_time)+'\r\n'
        f.write(line)
    except:
      print('[ERR]: cant write the log file')
