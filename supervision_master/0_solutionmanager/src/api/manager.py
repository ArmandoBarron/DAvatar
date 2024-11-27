from flask import Blueprint, jsonify, request
from flask_api import status
import os
import requests
import json
import yaml
import timeit

from .constants import IDX_PAIR, MTR_PAIR, RPR_PAIR, YML_FOLDER
from .time_measurement import write_to_timelog
from .docker_handler import get_active_docker_containers
from .validations import validate_model_services, validate_model_structure, validate_containers_raw
from .hash_handler import get_SHA3_256
from .requests_handler import do_get, do_post, do_put, do_delete
from .indexing_handler import index_add_solution, index_remove_solution, index_update_containerids
from .monitoring_handler import monitor_start_monitoring

mgr_bp = Blueprint("manager", __name__)

# aggregates_flag = None

@mgr_bp.route('/addsolution/<string:file_name>/<int:monitor_flag>/<int:ignore_model_info>/<int:agg_flag>', methods=['GET'])
def add_solution(file_name, monitor_flag, ignore_model_info, agg_flag):
    """
    read yml file and get two objects 
    one with the full yml content
    two only the components of this yml
    """
    starttime = timeit.default_timer()

    # global aggregates_flag
    # if agg_flag:
    #     aggregates_flag = 1
    # else:
    #     aggregates_flag = None

    status, solution_struc = add_solution_fun(file_name, monitor_flag, ignore_model_info, agg_flag)

    if status == 201:
        # prepare response
        resp = {
            'msg': 'Solution was saved',
            'data': solution_struc,
        }
    elif status == 400 and solution_struc and solution_struc == 'Duplicated':
        resp = {
            'msg': 'Solution was not saved, duplicated',
            }
    elif status == 400: # and type(solution_struc) == list:            
        resp = {
            'msg': 'Solution was not saved, probable missing model information',
        }
    else:
        status = (status if status else 500)
        resp = {'msg': 'Cant read the file'}
    
    takentime = timeit.default_timer() - starttime
    write_to_timelog('mgr1', takentime)
    return jsonify(resp), status

@mgr_bp.route('/replacesolution/<string:file_name>/<int:monitor_flag>/<int:ignore_model_info>/<int:agg_flag>', methods=['GET'])
def replace_solution(file_name, monitor_flag, ignore_model_info, agg_flag):
    starttime = timeit.default_timer()

    # global aggregates_flag
    # if agg_flag:
    #     aggregates_flag = 1
    # else:
    #     aggregates_flag = None

    index_remove_solution(file_name, 1)

    status, solution_struc = add_solution_fun(file_name, monitor_flag, ignore_model_info, agg_flag)
    if status == 201:
        # prepare response
        resp = {
            'msg': 'Solution was saved',
            'data': solution_struc,
        }
    elif status == 400 and solution_struc and solution_struc == 'Duplicated':
        resp = {
            'msg': 'Solution was not saved, duplicated',
            }
    elif status == 400: # and type(solution_struc) == list:
        resp = {
            'msg': 'Solution was not saved, probable missing model information',
            }
    else:
        status = (status if status else 500)
        resp = {'msg': 'Cant read the file'}
    
    takentime = timeit.default_timer() - starttime
    write_to_timelog('mgr2', takentime)
    return jsonify(resp), status

@mgr_bp.route('/updatecids', methods=['POST'])
def update_solution_ids():
    if request.method == 'POST':

        # search active containers 
        active_containers_list = get_active_docker_containers()

        solution = request.json
        sol_id = solution.get('id')
        sol_conts = solution.get('containers')

        for i in range(len(sol_conts)):
            name_yml = sol_conts[i].get('name_yml')
            if name_yml:

                # validate which services have active containers in docker
                for j in range(len(active_containers_list)):
                    # replicas = []
                    if name_yml in active_containers_list[j]['name']:
                        updated_cont = active_containers_list[j]
                        updated_cont['name_yml'] = name_yml
                        sol_conts[i] = updated_cont
        
        # update container ids to indexing
        info, status = index_update_containerids(sol_id, sol_conts)

        if status == 200:
            resp = jsonify({'msg': 'ok'})
        else:
            resp = jsonify({'msg': 'error'}), status
    else:
        resp = jsonify({'msg': 'method not allowed'}), 405

    return resp


def add_solution_fun(file_name, monitor_flag, ignore_model_info, aggregates_flag):
    full_yml = read_yml(file_name)
    status = 500
    solution_obj = None
    if not full_yml:
        return status, solution_obj

    # extract services (containers)
    services_dict = full_yml.get('services')
    if not services_dict:
        return status, solution_obj

    if not ignore_model_info:
        modeling_info = full_yml.get('x-model-solution')
        services_model = None
        if modeling_info:
            services_model = modeling_info.get('x-services')
            if services_model:
                services_model_error = validate_model_services(services_dict, services_model)
                if len(services_model_error)==0:
                    # validate which services has been declared in structure 
                    structure_list = modeling_info.get('structure')
                    invalid_services = validate_model_structure(services_dict, structure_list)

                    if len(invalid_services) > 0:
                        status = 400
                        solution_obj = invalid_services    
                else:
                    status = 400
                    solution_obj = services_model_error
        else:
            status = 400
        if status == 400:
            return status, solution_obj

    project_name = file_name.replace('.yml','')
    s_key = get_SHA3_256( project_name ) # json.dumps(full_yml)
    # search active containers 
    active_containers_list = get_active_docker_containers()
    # validate which services have active containers in docker
    solution_containers = validate_containers_raw(project_name,services_dict, active_containers_list)
    # index solution structure
    solution_obj = {
        'id': s_key,
        'name': file_name,
        'active': True,
        'containers': solution_containers,
        'full_yml': full_yml
    }
    info, status = index_add_solution(solution_obj)
    solution_obj.pop('active')
    solution_obj.pop('containers')
    solution_obj.pop('full_yml')
    if info and info.get('msg') == 'Duplicated':
        solution_obj = info.get('msg')
    # begin the monitoring module
    if monitor_flag > 0:
        monitor_start_monitoring(monitor_flag, s_key, aggregates_flag)

    return status, solution_obj


def read_yml(file_name):
    file_to_open = os.sep.join([os.getcwd(), YML_FOLDER, file_name])
    fyml = None
    if os.path.exists(file_to_open):
        with open(file_to_open, 'r') as ymlfile:
            try:
                fyml = yaml.load(ymlfile, Loader=yaml.FullLoader)
            except:
                fyml = None
                print('yaml format')
    else:
        print('cant open the file')

    return fyml

