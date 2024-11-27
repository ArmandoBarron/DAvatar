from flask import Blueprint, jsonify, request
from flask_api import status
import os
import requests
import json
import yaml
import timeit

from .constants import MTR_PAIR, IDX_PAIR, RPR_PAIR, YML_FOLDER
from .time_measurement import write_to_timelog
from .docker_handler import get_active_docker_containers
from .validations import validate_model_services, validate_model_structure, validate_containers_raw
from .hash_handler import get_SHA3_256
from .indexing_handler import index_add_solution
from .monitoring_handler import monitor_start_monitoring

mgrv2_bp = Blueprint("managerv2", __name__)


@mgrv2_bp.route('/api/v2/solutions', methods=['POST', 'PUT'])
def add_solution_v2():
  msg = 'invalid'
  if request.method not in ['POST', 'PUT']:
    return jsonify({'msg': msg}), status.HTTP_405_METHOD_NOT_ALLOWED
  print(request.method)
  # print(request.data)
  # print(request.args)
  print(request.form)
  print(request.files)
  # print(request.values)
  # print(request.json)
  if 'file' in request.files and request.form:
    print('there are files and params')
    file = request.files['file']
    params = request.form
    msg = 'file and params received'
    try:
      monitor_i = int(params.get('monitor_interval', 3))
    except:
      monitor_i = 3
    monitor_i = (monitor_i if monitor_i > 0 else 3)
    try:
      aggregates_i = int(params.get('aggregates_interval', 10))
    except:
      aggregates_i = 10
    aggregates_i = (aggregates_i if aggregates_i > 0 else 10)
    print('monitor inteval: ', monitor_i)
    status, msg, data = new_solution_w_file_and_params(file, monitor_i, aggregates_i)
    return jsonify({'msg': msg, 'data': data}), status
  return jsonify({'msg': msg})


def new_solution_w_file_and_params(file, monitor_interval, aggregates_interval):
    status = 500
    msg = ''
    solution_obj = None
    modeling_info = None
    full_yml = read_yml_from_file(file.stream)
    if not full_yml:
      msg = 'error yml'
      return status, msg, solution_obj

    # extract services (containers)
    services_dict = full_yml.get('services')
    if not services_dict:
      msg = 'error services'
      return status, msg, solution_obj

    if full_yml.get('x-model-solution'):
        services_model = full_yml.get('x-model-solution').get('x-services')
        if services_model:
            errors = validate_model_services(services_dict, services_model)
            if len(errors) == 0:
                # validate which services has been declared in structure 
                errors = validate_model_structure(services_dict, full_yml.get('x-model-solution').get('structure'))
                if len(errors) == 0:
                  modeling_info = full_yml.get('x-model-solution')

    project_name = file.filename.replace('.yml','')
    # search active containers 
    active_containers_list = get_active_docker_containers()
    # validate which services have active containers in docker
    solution_containers = validate_containers_raw(project_name, services_dict, active_containers_list)
    # index solution structure
    solution_obj = {
        'id': get_SHA3_256(project_name),
        'name': file.filename,
        'active': True,
        'containers': solution_containers,
        'full_yml': full_yml
    }
    if modeling_info:
      solution_obj['x-model-solution'] = modeling_info
    info, status = index_add_solution(solution_obj)
    if info and info.get('msg') == 'Duplicated':
      msg = info.get('msg')

    solution_obj.pop('active')
    solution_obj.pop('containers')
    solution_obj.pop('full_yml')
    if modeling_info:
      solution_obj.pop('x-model-solution')
    
    # begin the monitoring module
    if monitor_interval > 0:
        monitor_start_monitoring(monitor_interval, solution_obj['id'], aggregates_interval)
      
    if msg == '':
      msg = 'ok'

    return status, msg, solution_obj
  
def read_yml_from_file(file_stream):
  y = None
  if file_stream:
    try:
      y = yaml.load(file_stream, Loader=yaml.FullLoader)
    except:
      print('Error: yaml format')
  return y

# @mgrv2_bp.route('/v1/solutions/<string:file_name>', methods=['GET'])
# def temp_send(file_name):
#     file_to_open = os.sep.join([os.getcwd(), YML_FOLDER, file_name])
#     fileobj = open(file_to_open, 'rb')
#     url = 'http://192.168.8.18:22010/v2/solutions'
#     r = requests.post(url, data={"mysubmit":"Go"}, files={"files[]": (file_name, fileobj)})
#     # print(r.json())
#     return jsonify({'msg': 'sended'})