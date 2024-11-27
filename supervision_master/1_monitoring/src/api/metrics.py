from flask import Blueprint, jsonify, json
from flask_api import status
import requests
from multiprocessing import Manager

from .datetime_handler import get_timestamp, get_interval, parse_RFC3339_str_to_datetime, parse_RFC3339_datetime_to_str 
# from .utilization import get_cpu_util, get_mem_util, get_fs_util, get_net_util
from .utilization import get_fs, get_net
from .cadvisor_handler import get_host_metrics_raw, get_containers, get_container_metrics_raw
from .index_handler import index_metrics_of_solution, index_host_list
from .diagnosis_handler import do_aggregates_all
from .constants import JSON_HEADERS, SMGR_PAIR, USER, PASS, T_OUT_LOW, T_OUT_HIGH
from .constants import IDX_PAIR, MTR_PAIR, SMGR_PAIR, DIAG_PAIR, LH_ID
from .settings import hosts_list, active_hosts_list, active_solutions_list, aggregates_flag

metrics_bp = Blueprint("metrics", __name__)

endpoints_list = [
    {'id': 0,
    'name': 'hosts',
    'endpoint': 'api/v1.0/machine'},
    {'id': 1,
    'name': 'host_metrics',
    'endpoint': 'api/v1.0/containers'},
    {'id': 2,
    'name': 'container_metrics',
    'endpoint': 'api/v1.0/containers/docker'}
]
failure_solutions_list = Manager().dict()
last_ts_list = Manager().dict()
begin_end_ts_list = Manager().dict()
seconds_in_day = 24 * 60 * 60


"""   
METRICS EXPOSITION --------------------------------------------
"""
@metrics_bp.route('/hosts', methods=['GET'])
def hosts():
    """
    endpoint: read hosts_list and return all nodes location and 
    general stats from active ones
    """
    global active_hosts_list
    if len(active_hosts_list) < len(hosts_list):
        fill_active_hosts_list()
    
    if len(active_hosts_list) == 0:
        resp = jsonify({'msg': 'No active nodes detected'})
        resp.status_code = 400
    else:
        resp = jsonify(active_hosts_list)
    return resp

@metrics_bp.route('/hosts/reload', methods=['GET'])
def hosts_reload():
    fill_active_hosts_list()
    return jsonify({'msg': 'host updated'}), 200

def fill_active_hosts_list():
    global hosts_list
    global active_hosts_list
    active_hosts_list = []
    for elem in hosts_list:
        elem = host_metrics_fun(elem, elem.get('location'), endpoints_list[0]['endpoint'])
        if elem:
            active_hosts_list.append(elem)
    
    if len(active_hosts_list) > 0:
        index_host_list(active_hosts_list)
    else:
        print('host list 0')



@metrics_bp.route('/hosts/<int:host_id>', methods=['GET'])
def hosts_metrics(host_id):
    """
    enpoint: get the stats about a specified host id
    """
    global hosts_list
    return host_metrics_fun(hosts_list[host_id], hosts_list[host_id]['location'], endpoints_list[0]['endpoint'])

def host_metrics_fun(elem, host_location, endpoint):
    host_m = None
    url = host_location + '/' + endpoint
    data, status = get_host_metrics_raw(url)
    if status == 200:
        host_m = elem
        host_m['num_cores'] = data.get('num_cores')
        host_m['cpu_frequency_khz'] = data.get('cpu_frequency_khz')
        host_m['memory'] = data.get('memory_capacity')
        storage = 0
        overlay = 0
        for fs in data.get('filesystems'):
            storage += fs.get('capacity')
            if fs.get('device') and fs.get('device') == 'overlay':
                overlay += fs.get('capacity')
        host_m['storage'] = storage
        host_m['storage_overlay'] = overlay
        host_m['location'] = host_location
    return host_m




@metrics_bp.route('/hosts/<int:host_id>/containers', methods=['GET'])
def containers(host_id):
    """
    endpoint: get all the containers running in the specified host id
    with their location
    """
    url = hosts_list[host_id]['location']+'/'+endpoints_list[2]['endpoint']
    r = get_containers(url)
    if r and r.status_code == 200:
        subcontainers = r.json()['subcontainers']
        containers = []
        for subc in subcontainers:
            new = subc['name'].replace('/docker/','http://'+MTR_PAIR+'/hosts/'+str(host_id)+'/containers/')
            containers.append(new)
        resp = jsonify(containers)
    else:
        status = (r.status_code if r != None and r.status_code else 500)
        resp = jsonify({'msg': 'not found'}), status
    return resp

@metrics_bp.route('/hosts/<int:host_id>/containers/<string:container_id>', methods=['GET'])
def container_metrics_default(host_id, container_id):
    return container_metrics_fun(host_id,container_id,1)

@metrics_bp.route('/hosts/<int:host_id>/containers/<string:container_id>/<int:interval_time>', methods=['GET'])
def container_metrics(host_id, container_id, interval_time):
    """
    endpoint: get the stats about a specified container hash
    TODO: handle request bigger than 60 seconds
    """
    return container_metrics_fun(host_id, container_id, interval_time)

def container_metrics_fun(host_id, container_id,interval_time):
    c_info = [host_id, container_id,interval_time]
    data_processed = container_metrics_data(c_info)

    # TODO: containers change id while re-run
    if data_processed and len(data_processed)>0:
        resp = jsonify(data_processed)
        resp.status_code = 200
    else:
        resp = jsonify({'msg': 'not found'})
        resp.status_code = 500
    return resp

def container_metrics_data(c_tuple):
    """
    get the metrics of a container
    recives a tuple with the values [host_id,container_id,interval_time]
    process the cv metrics, clean them and
    return one object; the data 
    """
    host_id, container_id, interval_time = c_tuple
    data_processed = []
    status = 500

    if host_id >= 0 and container_id and interval_time:

        # get container metrics
        url = hosts_list[host_id]['location']+'/'+endpoints_list[2]['endpoint']+'/'+container_id
        data_raw, status = get_container_metrics_raw(url, interval_time)

        if status == 200:
            # get machine metrics
            global active_hosts_list
            if len(active_hosts_list) > 0:
                data_totals = active_hosts_list[host_id]

                # clean data
                data_processed, status = get_container_metrics_clean_processed(data_raw)
                if data_processed and len(data_processed) > 0:
                    data_processed['location'] = data_totals.get('location')
            else:
                print('No active hosts')
        else:
            print('No data raw')

    return data_processed

def container_metrics_data_w_lastts(c_tuple):
    """
    get the metrics of a container
    recives a tuple with the values [host_id,container_id,interval_time]
    process the cv metrics, clean them and
    return one object; the data 
    """
    host_id, container_id, service, solution_id, interval_time = c_tuple
    data_processed = []
    new_begin_ts = None
    new_last_ts = None
    status = 500

    if host_id >= 0 and container_id and interval_time:

        # get container metrics
        url = hosts_list[host_id]['location']+'/'+endpoints_list[2]['endpoint']+'/'+container_id
        data_raw, status = get_container_metrics_raw(url, interval_time)


        if status == 200:
            # get machine metrics
            global active_hosts_list
            if len(active_hosts_list) > 0:
                data_totals = active_hosts_list[host_id]
                try:
                    last_ts = last_ts_list.get(container_id)
                except:
                    last_ts = None
                    print('except getting last timestamp')
                # clean data
                data_processed, new_begin_ts, new_last_ts, status = get_container_metrics_clean_processed_w_lastts(data_raw,last_ts)
                if data_processed and len(data_processed) > 0:
                    data_processed['location'] = data_totals.get('location')
                    last_ts_list[container_id] = new_last_ts

            else:
                print('No active hosts')
        else:
            print('No data raw')

    return data_processed, new_begin_ts, new_last_ts




def get_container_metrics_clean_processed(data):
    print(f'data raw len: {len(data)}')
    # more than one means that data has information
    if len(data) >= 1:

        raw_stats = data.get('stats')
        # more than one is requiered to process stats and get actual value
        if raw_stats and len(raw_stats) > 1:
            print(f'stats raw len: {len(raw_stats)}')

            # define data structure to use
            data_processed = {}

            # define resultant stats
            processed_stats = []
            # processed_stats2 = []

            #define elements
            timestamp_list = []
            cpu_util_list = []
            mem_util_list = []
            fs_util_list = []
            net_util_list = []
        
            for i, i_elem in enumerate(raw_stats):
                tsp = i_elem.get('timestamp')
                # print(f'i: {i}, timestamp: {tsp}')
                # clean each metric
                cpu = {
                    'usage_system': i_elem.get('cpu').get('usage').get('system'),
                    'usage_total': i_elem.get('cpu').get('usage').get('total'),
                    'usage_user': i_elem.get('cpu').get('usage').get('user')
                }
                # cpu.pop('per_cpu_usage')
                raw_stats[i]['cpu'] = cpu

                memory = i_elem.get('memory')
                memory['pgfault'] = memory.get('container_data').get('pgfault')
                memory['pgmajfault'] = memory.get('container_data').get('pgmajfault')
                memory.pop('container_data')
                memory.pop('hierarchical_data')
                memory.pop('failcnt')
                raw_stats[i]['memory'] = memory

                diskio = i_elem.get('diskio').get('io_service_bytes')
                if diskio: 
                    for j, j_elem in enumerate(diskio):
                        j_elem['stats']['device'] = j_elem['device'] # i don't know what i was trying to do here
                        diskio[j] = j_elem['stats']
                else:
                    # print('Diskio not found')
                    # print('Diskio not found')
                    diskio = 'Not found'
                raw_stats[i]['diskio'] = diskio

                if i_elem.get('network').get('name') != '':
                    network = i_elem.get('network').get('interfaces')
                else:
                    network = i_elem.get('network')
                    network.pop('tcp')
                    network.pop('tcp6')
                    network.pop('udp')
                    network.pop('udp6')
                raw_stats[i]['network'] = network

                filesystem = i_elem.get('filesystem')
                if filesystem:
                    pass
                else:
                    # print('FS not found')
                    print('FS not found')

                timestamp_list.append(get_timestamp(i_elem.get('timestamp')))
                if not i_elem.get('timestamp'):
                    print('no timestamp 1')

                # cpu # freq in khz
                # u1 = get_cpu_util(t_core_freq,t_cores,cur,prev)
                u1 = i_elem.get('cpu').get('usage_total')
                cpu_util_list.append(u1)

                # memory # bytes i guess
                # u2 = get_mem_util(t_mem,cur)
                u2 = i_elem.get('memory').get('usage')
                mem_util_list.append(u2)

                # filesystem # bytes i guess
                # u3 = get_fs_util(t_fs,cur)
                u3 = get_fs(i_elem)
                fs_util_list.append(u3)

                # network # bytes; usually link speed in bits per second
                # u4 = get_net_util(None,cur,prev) 
                u4 = get_net(i_elem) 
                net_util_list.append(u4)
            print(f'timestamp len: {len(timestamp_list)}')
            print(f'cpu len: {len(cpu_util_list)}')
            if len(timestamp_list) > 0:

                processed_stats = {
                    'timestamp': timestamp_list,
                    'cpu_util': cpu_util_list,
                    'memory_util': mem_util_list,
                    'filesystem_util': fs_util_list,
                    'network_util': net_util_list,
                }
                data_processed = {
                    'id': data.get('id'),
                    'name': data.get('aliases')[0],
                    'image': data.get('spec').get('image'),
                    'creation_time': data.get('spec').get('creation_time'),
                    'stats_v1': processed_stats
                }
                ret = data_processed, 200
            else:
                ret = data_processed, 500
                print('no timestamp 2')
        else:
            ret = None, 500
            print('No raw stats')
    else:
        ret = None, 500
        print('No data or data_totals')
    return ret

def get_container_metrics_clean_processed_w_lastts(data,last_ts):
    data_processed = None
    new_begin_ts = None
    new_last_ts = None
    status = 500
    # more than one means that data has information
    if len(data) >= 1:

        raw_stats = data.get('stats')
        # more than one is requiered to process stats and get actual value
        if raw_stats and len(raw_stats) > 1:

            # define resultant stats
            processed_stats = []
            # processed_stats2 = []

            # define elements
            timestamp_list = []
            cpu_util_list = []
            mem_util_list = []
            fs_util_list = []
            net_util_list = []
        
            for i, i_elem in enumerate(raw_stats):
                ts = None
                if i_elem.get('timestamp'):
                    ts = get_timestamp( i_elem.get('timestamp') )
                    if last_ts:
                        dt_ts = parse_RFC3339_str_to_datetime(ts)
                        if dt_ts > last_ts:
                            timestamp_list.append( ts )
                        else:
                            ts = None
                    else:
                        timestamp_list.append( ts )
                else:
                    # print('no timestamp 1')
                    pass

                if ts:
                    # clean each metric
                    cpu = {
                        'usage_system': i_elem.get('cpu').get('usage').get('system'),
                        'usage_total': i_elem.get('cpu').get('usage').get('total'),
                        'usage_user': i_elem.get('cpu').get('usage').get('user')
                    }
                    # cpu.pop('per_cpu_usage')
                    raw_stats[i]['cpu'] = cpu

                    memory = i_elem.get('memory')
                    memory['pgfault'] = memory.get('container_data').get('pgfault')
                    memory['pgmajfault'] = memory.get('container_data').get('pgmajfault')
                    memory.pop('container_data')
                    memory.pop('hierarchical_data')
                    memory.pop('failcnt')
                    raw_stats[i]['memory'] = memory

                    diskio = i_elem.get('diskio').get('io_service_bytes')
                    if diskio: 
                        for j, j_elem in enumerate(diskio):
                            j_elem['stats']['device'] = j_elem['device'] # i don't know what i was trying to do here
                            diskio[j] = j_elem['stats']
                    else:
                        # print('Diskio not found')
                        diskio = 'Not found'
                    raw_stats[i]['diskio'] = diskio

                    if i_elem.get('network').get('name') != '':
                        network = i_elem.get('network').get('interfaces')
                    else:
                        network = i_elem.get('network')
                        network.pop('tcp')
                        network.pop('tcp6')
                        network.pop('udp')
                        network.pop('udp6')
                    raw_stats[i]['network'] = network

                    filesystem = i_elem.get('filesystem')
                    if not filesystem:
                        print('FS not found')

                    # cpu # freq in khz
                    u1 = i_elem.get('cpu').get('usage_total')
                    cpu_util_list.append(u1)

                    # memory # bytes i guess
                    u2 = i_elem.get('memory').get('usage')
                    mem_util_list.append(u2)

                    # filesystem # bytes i guess
                    u3 = get_fs(i_elem)
                    fs_util_list.append(u3)

                    # network # bytes; usually link speed in bits per second
                    u4 = get_net(i_elem) 
                    net_util_list.append(u4)

            if len(timestamp_list) > 0:
                processed_stats = {
                    'timestamp': timestamp_list,
                    'cpu_util': cpu_util_list,
                    'memory_util': mem_util_list,
                    'filesystem_util': fs_util_list,
                    'network_util': net_util_list,
                }
                data_processed = {
                    'id': data.get('id'),
                    'name': data.get('aliases')[0],
                    'image': data.get('spec').get('image'),
                    'creation_time': data.get('spec').get('creation_time'),
                    'stats_v1': processed_stats
                }
                new_begin_ts = parse_RFC3339_str_to_datetime( timestamp_list[0] )
                new_last_ts = parse_RFC3339_str_to_datetime( timestamp_list[-1] )
                status = 200
            else:
                status = 500
                print('no samples: duplicated data is omited')
                print(f'samples: {len(timestamp_list)}/{len(raw_stats)}')
        else:
            status = 500
            print('No cv raw stats')
    else:
        status = 500
        print('No data or data_totals')
    return data_processed, new_begin_ts, new_last_ts, status
    # return data_processed, new_last_ts, status








"""
SOLUTION METRICS --------------------------------------------
"""
@metrics_bp.route('/solutions/<string:sol_id>', methods=['GET']) 
def solution_metrics(sol_id):
    """
    endpoint: get the stats about a specified solution hash
    without interval time
    """
    return solution_metrics_fun(sol_id, 1)

@metrics_bp.route('/solutions/<string:sol_id>/<int:interval_time>', methods=['GET']) 
def solution_metrics_interval(sol_id, interval_time):
    """
    endpoint: get the stats about a specified solution hash
    with interval time
    """
    return solution_metrics_fun(sol_id, interval_time)

def solution_metrics_fun(sol_id, interval_time):
    data, status = solution_metrics_data(sol_id, interval_time)

    if status == 200:
        resp = jsonify({'msg': 'solution found', 'data': data})
        resp.status_code = status
    else:
        resp = jsonify({'msg': 'not found', 'data': data})
        resp.status_code = 500
    return resp

def solution_metrics_data(sol_id, interval_time):
    # search solution in datacube
    url = 'http://'+IDX_PAIR+'/solutions/'+sol_id
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        # print(e)
        print('Couldnt get solution')
        r = None
    if r and r.status_code == 200:
        rjson = r.json()
        status = 200
        data = get_solution_metrics(rjson['data'], interval_time)
    else:
        status = (r.status_code if r != None and r.status_code else 500)
        data = {}
    return data, status

def get_solution_metrics(rjson, interval_time):
    if rjson.get('containers'):
        sol_id = rjson.get('id')
        sol_name = rjson.get('name')
        sol_containers = rjson.get('containers')

        container_metrics = []
        missing_containers = 0

        for k,v in sol_containers.items():
            ## TODO: get in which host is the solution and change the LH_ID
            ## TODO: error while there is no containers online: update id of containers 
            if v and type(v) is dict and v.get('id'):
                c_info = [LH_ID, v.get('id'), v.get('service'), sol_id, interval_time]
                data_processed = container_metrics_data_w_lastts(c_info)
                if data_processed and len(data_processed) > 0:
                    container_metrics.append(data_processed)
                else:
                    missing_containers += 1
            else:
                print(f'Container does not have id: {v}')
                missing_containers += 1

        if missing_containers == len(sol_containers):
            data = []
            print('No container with metrics')
        else:
            data = {
                'id': sol_id,
                'name': sol_name,
                'containers': container_metrics
            }
        if missing_containers > 0:
            # notify to solution_mgr
            # notify_missing_container(rjson)
            pass
    else:
        print('No containers')
        data = []
    return data

def get_solution_metrics_w_autostop(rjson, interval_time):
    if rjson.get('containers'):
        sol_id = rjson.get('id')
        sol_name = rjson.get('name')
        sol_containers = rjson.get('containers')

        container_metrics = []
        missing_containers = 0

        ## working linear
        for k,v in sol_containers.items():
            ## TODO: get in which host is the solution and change the LH_ID
            ## TODO: error while there is no containers online: update id of containers 
            if v and type(v) is dict and v.get('id'):
                c_info = [LH_ID,v.get('id'),v.get('service'),sol_id,interval_time]
                data_processed, n_begin_ts, n_last_ts = container_metrics_data_w_lastts(c_info)

                if data_processed and len(data_processed) > 0:
                    container_metrics.append(data_processed)

                    # TODO: move into container_metrics_data_w_lastts
                    # calculate the time begin and end time, to get the total execution time
                    if begin_end_ts_list.get(sol_id):
                        b_e = begin_end_ts_list.get(sol_id)
                        if b_e.get('begin') > n_begin_ts:
                            b_e['begin'] = n_begin_ts
                            begin_end_ts_list[sol_id] = b_e
                            # print('begin changed')
                        if b_e.get('end') < n_last_ts:
                            b_e['end'] = n_last_ts
                            begin_end_ts_list[sol_id] = b_e
                            # print('end changed')
                    else:
                        begin_end_ts_list[sol_id] = {'begin': n_begin_ts, 'end': n_last_ts}

                else:
                    missing_containers += 1
            else:
                print(f'Container does not have id: {v}')
                missing_containers += 1

        if missing_containers == len(sol_containers):
            print('No container with metrics')
            data = []
            countfail = failure_solutions_list.get(sol_id)
            if countfail:
                failure_solutions_list[sol_id] = countfail + 1
                if countfail > 2:
                    active_solutions_list.pop(sol_id)
                    failure_solutions_list.pop(sol_id)
                    print(f'Solution with multiple failures: {sol_id}')

                    # save begin, end, and difference time to idx
                    if begin_end_ts_list.get(sol_id):
                        b_e = begin_end_ts_list.get(sol_id)
                        b = b_e.get('begin')
                        e = b_e.get('end')
                        difference = e - b
                        dif_in_mins = divmod(difference.days * seconds_in_day + difference.seconds, 60)
                        b_e['begin'] = parse_RFC3339_datetime_to_str(b)
                        b_e['end'] = parse_RFC3339_datetime_to_str(e)
                        b_e['name'] = sol_name
                        b_e['diff_in_mins'] = dif_in_mins
                        # index difference times
                        url = 'http://'+IDX_PAIR+'/solutions/'+sol_id+'/begin-end'
                        resp = index_metrics_of_solution(url, b_e)
                        # print(f'resp: {resp}')

                        # call for aggregates when solution finish its execution
                        global aggregates_flag
                        if aggregates_flag:
                            resp = do_aggregates_all(url)
                            # print(f'resp: {resp}')
            else:
                failure_solutions_list[sol_id] = 1
        elif missing_containers > 0:
            # TODO: notify to solution_mgr
            # TODO: notify_missing_container(rjson)
            print(f'Missing containers: {missing_containers}/{len(sol_containers)}')
            data = {
                'id': sol_id,
                'name': sol_name,
                'containers': container_metrics
            }
        else:
            data = {
                'id': sol_id,
                'name': sol_name,
                'containers': container_metrics
            }
    else:
        print('error in get containers')
        data = []
    return data

# TODO: put into sol_mgr_handler.py
def notify_missing_container(payload):
    print('notify missing containers')
    url = 'http://'+SMGR_PAIR+'/updatesolution'
    try:
        r = requests.post(url, data=json.dumps(payload), headers=JSON_HEADERS) # , auth=(USER, PASS)
    except requests.exceptions.RequestException as e:
        # print('error')
        r = None
    # TODO: pending
