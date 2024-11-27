from flask import Blueprint, jsonify, json
from flask_api import status
import os
import timeit
import time
from threading import Thread
from multiprocessing import Pool

from .time_measurement import write_to_timelog
from .metrics import get_solution_metrics_w_autostop
from .index_handler import index_metrics_of_solution, get_solution_info
from .constants import JSON_HEADERS
from .constants import IDX_PAIR, LH_ID
from .settings import active_solutions_list, aggregates_flag


monitor_bp = Blueprint("monitor", __name__)


monitor_thread = None
stop_monitor_thread = False
n_samples = None


"""   
BACKGROUND MONITORING --------------------------------------------
"""
@monitor_bp.route('/api/v1/monitor', methods=['GET'])
def background_info():
    return 'Please add an option [start|stop] [interval] [solution] [agg]'

@monitor_bp.route('/api/v1/monitor/<string:option>/<int:interval>/<string:solution_id>/<string:agg_flag>', methods=['GET'])
def control_monitor(option, interval, solution_id, agg_flag):
    global active_solutions_list
    global aggregates_flag
    a = active_solutions_list.get(solution_id)
    if not a:
        active_solutions_list[solution_id] = None
    else:
        print('solution already exists')
        print(a)
    if agg_flag:
        aggregates_flag = 1
    else:
        aggregates_flag = None
    msg, stt = control_monitor_fun(option, interval)
    return jsonify({'msg': msg}), stt

def control_monitor_fun(option, interval):
    """
    allows to handle the monitoring behaviour
    enable, disable, and interval times
    """
    global monitor_thread
    global stop_monitor_thread
    if option == 'start':
        if not monitor_thread:
            stop_monitor_thread = False
            monitor_thread = Thread(target=background_monitor, args=(interval,))
            # monitor_thread.daemon = True
            monitor_thread.start()
            # monitor_thread.join()
            msg = 'started'
        else:
            msg = 'already started'
        ret = msg, 200
    elif option == 'stop':
        if monitor_thread and monitor_thread.is_alive(): 
            stop_monitor_thread = True
            monitor_thread.join()
            monitor_thread = None
            msg = 'stopped'
        elif monitor_thread:
            stop_monitor_thread = True
            monitor_thread.join()
            monitor_thread = None
            msg = 'stopped'
        else:
            msg = 'not running'
        ret = msg, 200
    else:
        msg = 'invalid option'
        ret = msg, 400
    return ret

def background_monitor(interval):
    global n_samples
    n_samples = interval
    while True:
        starttime = timeit.default_timer()

        global stop_monitor_thread
        if stop_monitor_thread:
            break
        
        solutions = []
        if active_solutions_list != None and len(active_solutions_list) == 0:
            pass
            # get solutions from index
            # url = 'http://'+IDX_PAIR+'/solutions'
            # solutions = get_solutions(url)
        if active_solutions_list != None and len(active_solutions_list) > 0:
            # save a copy of solutions in memory
            for s, v in active_solutions_list.items():
                if v:
                    solutions.append(v)
                else:
                    # get solution info
                    print("sending request to idx   ")
                    url = 'http://'+IDX_PAIR+'/solutions/' + s
                    sol = get_solution_info(url)
                    if sol:
                        print("geting response from idx")
                        sol.pop('full_yml')
                        print(sol)
                        solutions.append(sol)
                        active_solutions_list[s] = sol
        

        if len(solutions) > 0:
            print("procsando la solucion")
            # working with multiprocessing
            n_cpus = len(os.sched_getaffinity(0)) # get the number of CPU (cores) the current process can use
            n_cpus = (int(n_cpus / 2) if n_cpus > 1 else n_cpus) # use half cores to avoid saturating the system
            with Pool(processes=n_cpus) as p:
                monitor_and_index = p.map(monitor_solution_and_index, solutions)
        else:
            print('No active solutions founded')

        takentime = timeit.default_timer() - starttime
        write_to_timelog('mon', takentime)

        interval = (n_samples - takentime if n_samples > takentime else 0)
        # print(f'interval: {interval}')
        time.sleep(interval)

def monitor_solution_and_index(mytuple):
    sts = 500
    if mytuple:
        # get metrics by solution
        global n_samples
        data = get_solution_metrics_w_autostop(mytuple, n_samples)
        # dont send request it all containers has no monitoring data
        if data:
            # save metrics by solution
            url = 'http://' + IDX_PAIR + '/solutions/' + mytuple.get('id') + '/metrics'
            sts = index_metrics_of_solution(url, data)
        else:
            # TODO: send request to index for increment not available counter
            # TODO: auto update ids
            # url = 'http://'+IDX_PAIR+'/solutions/'+mytuple.get('id')+'/update_elem'
            # sts = index_active_status_of_solution(url,data)
            pass
            
    return sts





