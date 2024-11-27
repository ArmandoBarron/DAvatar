import os
import json
import pandas as pd
import timeit
from flask import Blueprint, jsonify
from flask_api import status
# from bson.json_util import dumps
from .json_encoder import JSONEncoder
from datetime import datetime, timedelta

from .datetime_handler import get_interval, parse_RFC3339_datetime_to_str, parse_RFC3339_str_to_datetime
from .mongodb_handler import get_host_info, get_period_alldocs, get_period_btwn_begin_end, get_bot_top_dates, begin_end_idx_date_v1
from .index_handler import save_status_to_index
from .representation_handler import request_make_model
from .files import make_subfolders, write_json_to_disk, export_to_csv
from .utilization import get_utilization, get_cpu_util, get_net
from .time_measurement import write_to_timelog
from .constants import CL_RESOURCES, THRESHOLDS, DATASETS_FOLDER, FLAG_SAVE_DATASETS

diagnosis_bp = Blueprint("diagnosis", __name__)

global_hosts = {}
ten_megabyte = 10 * 1024*1024
one_megabyte = 1 * 1024*1024
pd.options.mode.chained_assignment = None



@diagnosis_bp.route('/aggregates/<string:sol_id_or_name>/ALL/<string:result_name>', methods=['GET'])
def aggregates_v1(sol_id_or_name, result_name):
    """Calculate utilizations and its aggregates during all the execution time
    aggregates are descriptive statistics min,max,mean,median,std
    and also the status threshold (low,medium,high) depending on 
    the median value.
    Results are saved in indexing
    
    Args:
        sol_id_or_name (str): the name or id of the solution
        result_name (str): the name to save results in idx

    Returns:
        response: 200 if results saved correctly 400 if not
    """
    ndocs,exps_result,payload = agg_v1_fun(sol_id_or_name,result_name)

    if ndocs > 0:
        data = {
            'n':ndocs, 'exps_result':exps_result, 'status': payload
        }
        resp = jsonify({'msg':'documents found', 'data': data})
    else:
        resp = jsonify({'msg':'documents not found'}), 400

    return resp

def agg_v1_fun(sol_id_or_name, result_name):
    
    starttime = timeit.default_timer()

    ndocs = 0
    exp_result = None
    payload = None

    # obtain the begin date if not provided
    begin = begin_end_idx_date_v1(sol_id_or_name)

    if begin != '':
        begin['begin'] = parse_RFC3339_datetime_to_str( begin.get('begin') )
        begin['end'] = parse_RFC3339_datetime_to_str( begin.get('end') )
        
        # create main folder
        ct = parse_RFC3339_datetime_to_str(datetime.today())
        path = os.sep.join([os.getcwd(), DATASETS_FOLDER, sol_id_or_name, ct,])
        if FLAG_SAVE_DATASETS:
            make_subfolders(path)

        df_all = None
        path_file = os.sep.join([path, 'duration.json'])
        write_json_to_disk(begin, path_file)
        
        ndocs, result = get_period_alldocs(sol_id_or_name)
        json_docs = parse_docs(result,ndocs)
        if len(json_docs) > 0:
            arr_docs, arr_utils, cols = structure_docs(json_docs, path=path)

            # save raw datasets, dev only
            # df_all = pd.DataFrame(arr_docs, columns=cols)
            # path_file = os.sep.join([path, 'raw'])
            # export_to_csv(path_file, df_all, True)
            # path_file = os.sep.join([path, 'raw_stats'])
            # desc = df_all.describe()
            # export_to_csv(path_file, desc, True)

            df_all = pd.DataFrame(arr_utils, columns=cols)            

            # first reduce columns
            selected_cols = ['name_solution','name_container','cpu_util','filesystem_util','memory_util','network_util','timestamp']
            df_all = df_all[selected_cols]

            # calculate top network based on max value in period
            max_net = df_all['network_util'].max()
            total_net = top_net_value(max_net)
            

            # calculate network utilization
            df_all['network_util'] = df_all['network_util'].apply( get_utilization, args=[total_net] )
                    
            # convert timestamp str to datetime object
            df_all['timestamp'] = df_all['timestamp'].apply(lambda _: parse_RFC3339_str_to_datetime(_))

            # procces full period
            exp_result, exp_stats_error = process_save_each_vc(df_all)

            # save util datasets, dev only
            if FLAG_SAVE_DATASETS:
                path_file = os.sep.join([path, 'util'])
                export_to_csv(path_file, df_all, True)
                path_file = os.sep.join([path, 'util_stats'])
                desc = df_all.describe()
                export_to_csv(path_file, desc, True)

            # prepare status to index
            sol_id = json_docs[0].get('id_solution')
            sol_name = json_docs[0].get('name_solution')
            payload = {
                'exp_name': result_name,
                'creation_time': ct,
                'sol_id': sol_id,
                'sol_name': sol_name,
                'exp': begin.get('diff_in_mins'),
                'dt_ini': begin.get('begin'),
                'dt_end': begin.get('end'),
                'data_status': exp_stats_error
            }

            takentime = timeit.default_timer() - starttime
            write_to_timelog('diag', takentime)
            
            rs = save_status_to_index(payload)
        else:
            print('Docs not found')

    else:
        print('Begin not found')
    takentime = timeit.default_timer() - starttime
    write_to_timelog('diag', takentime)

    return ndocs, exp_result, payload

def process_save_each_vc(df, path=None):

    results = []
    df_stats = pd.DataFrame()

    # iterate by container name
    cont_names = df['name_container'].unique()
    for con in cont_names:

        df_con = df[df['name_container'] == con]
        df_min, df_max, df_mean, df_mdn, df_std, thresholds = statistics_of_container(df_con)

        df_stt_con = pd.DataFrame()
        df_stt_con = df_stt_con.append(df_min)
        df_stt_con = df_stt_con.append(df_max)
        df_stt_con = df_stt_con.append(df_mean)
        df_stt_con = df_stt_con.append(df_mdn)
        df_stt_con = df_stt_con.append(df_std)
        # append thresholds row
        s = thresholds + ['threshold']
        pds = pd.Series(s, index=df_stt_con.columns, name=con)
        df_stt_con = df_stt_con.append(pds)

        df_stats = df_stats.append(df_stt_con)

        # save each container util dataset
        # if path:
            # path_file = os.sep.join([path, con])
            # results.append(export_to_csv(path_file, df_stt_con))

    # prepare results to save in indexing module
    json_df_stats = df_stats.to_json(orient='split')
    json_df_stats = json.loads(json_df_stats)

    return results, json_df_stats 



@diagnosis_bp.route('/v2/aggregates/<string:sol_id_or_name>/<string:begin_full_date>/<int:window_size>/<int:cores>/<string:result_name>', methods=['GET'])
def aggregates_v2(sol_id_or_name, begin_full_date, window_size, cores, result_name):
    """Calculate utilizations and its aggregates in period start to end
    start is begin_full_date
    end is start + each experiment in window_size
    aggregates are descriptive statistics min,max,mean,median,std
    and also the status threshold (low,medium,high) depending on 
    the median value.
    Results are saved in indexing
    
    Args:
        sol_id_or_name (str): the name or id of the solution
        begin_full_date (str): is the start period separated by mid slash or minimum date when this value is BEGIN. e.g. 2020-3-26-6-14-30
        window_size (int): size of time to get aggregates
        cores (int): number of cores to be considered, 0 for default all cores
        result_name (str): the name to save results in idx

    Returns:
        response: 200 if results saved correctly 400 if not
    """
    starttime = timeit.default_timer()
    ndocs, exps_result, payload = agg_v2_fun(sol_id_or_name, begin_full_date, window_size, cores, result_name)
    takentime = timeit.default_timer() - starttime
    write_to_timelog('diag', takentime)
    if ndocs > 0:
        save_status_to_index(payload)
        # request_make_model(result_name, payload)
        data = {
            'n': ndocs, 'exps_result': exps_result, 'status': payload
        }
        resp = jsonify({'msg':'documents found', 'data': data})
    else:
        resp = jsonify({'msg':'documents not found', 'n':ndocs, 'exps':exps_result}), 400

    return resp

def agg_v2_fun(sol_id_or_name, begin_full_date, window_size, cores, result_name):
    
    ndocs = 0
    exp = []

    # obtain the begin date if not provided
    begin = get_date_by_label(begin_full_date, sol_id_or_name)
    if begin == '':
        print('Not found: invalid date option')
        return ndocs, exp, None
        
    # experiments: expand and calculate times for each experiment
    # calculate times for each experiment
    if begin_full_date == 'BEGIN':
        exp = [window_size, begin, begin + timedelta(minutes=window_size)]
    elif begin_full_date == 'END':
        exp = [window_size, begin - timedelta(minutes=window_size), begin]
    else:
        exp = [window_size, begin, begin + timedelta(seconds=window_size)]

    # create main folder
    ct = parse_RFC3339_datetime_to_str(datetime.today())
    path = os.sep.join([os.getcwd(), DATASETS_FOLDER, sol_id_or_name, ct, str(exp[0])])
    if FLAG_SAVE_DATASETS:
        make_subfolders(path)
            
    # get metric docs in period from index
    ndocs, result = get_period_btwn_begin_end(sol_id_or_name, exp[1], exp[2])
    json_docs = parse_docs(result, ndocs)
    exp_result = []
    stats_error = {}
        
    if ndocs > 0:
        arr_docs, arr_utils, cols = structure_docs(json_docs, cores_considered=cores, path=path)
        df_all = None

        # save raw datasets
        # filename = 'ds_v1_' + str(exp[0]) + 'm_' + str(exp[1]) + 'ch'
        # df_all = pd.DataFrame(arr_docs, columns=cols)
        # path_file = os.sep.join([path, 'raw'])
        # export_to_csv(path_file, df_all, True)
        # path_file = os.sep.join([path, 'raw_stats'])
        # desc = df_all.describe()
        # export_to_csv(path_file, desc, True)

        # reduce columns
        df_all = pd.DataFrame(arr_utils, columns=cols)            
        selected_cols = ['name_solution','name_container','cpu_util','filesystem_util','memory_util','network_util','timestamp']
        df_all = df_all[selected_cols]

        # calculate top network based on max value in period
        max_net = df_all['network_util'].max()
        total_net = top_net_value(max_net)

        # preprocess dataframe and process each container
        df_all['network_util'] = df_all['network_util'].apply(get_utilization, args=[total_net])
        df_all['timestamp'] = df_all['timestamp'].apply(lambda _: parse_RFC3339_str_to_datetime(_))
        exp_result, exp_stats_error = process_save_each_vc(df_all, path)                

    exp.append(exp_result)
    # exp.append(exp_stats_error)

    # save util datasets
    if FLAG_SAVE_DATASETS:
        path_file = os.sep.join([path, 'util'])
        export_to_csv(path_file, df_all, True)
        path_file = os.sep.join([path, 'util_stats'])
        desc = df_all.describe()
        export_to_csv(path_file, desc, True)

    # prepare status to index
    sol_id = json_docs[0].get('id_solution')
    sol_name = json_docs[0].get('name_solution')
    payload = {
        'exp_name': result_name,
        'creation_time': parse_RFC3339_datetime_to_str(datetime.today()),
        'sol_id': sol_id,
        'sol_name': sol_name,
        'exp': exp[0],
        'dt_ini': parse_RFC3339_datetime_to_str(exp[1]),
        'dt_end': parse_RFC3339_datetime_to_str(exp[2]),
        'data_status': exp_stats_error
    }

    return ndocs, exp, payload


def structure_docs(json_docs, cores_considered=0, path=None):
    """allows to frame dataset correctly
    useful when the utilization fields are lists 
    and dataframe doesn makes correcty
    this method iterate over the lists and create 
    one row by each element.
    Supports many containers

    Args:
        json_docs (dict): list of dict elements, where one element is a document

    Returns:
        list,list,list: restructured dataset, colum names of dataset
    """
    unique_containers = {}
    arr_rows_filled = []
    arr_utils = []
    c_names = ['id_solution','name_solution','id_container','name_container','host',
    'cpu_util','memory_util','filesystem_util','network_util','timestamp']
    i = 0

    for jd in json_docs:
        ivalues = []
        for col in c_names:
            ivalues.append(jd.get(col))
            # save representative link, does not need to store data. key is the value
            if col == 'host':
                global_hosts[jd.get(col)] = None
            if col == 'name_container':
                unique_containers[jd.get(col)] = []
        # square data
        for j in range( len(ivalues[-1]) ):
            i += 1
            raw = [ivalues[5][j], ivalues[6][j], ivalues[7][j], ivalues[8][j], ivalues[9][j]]
            cur_row = ivalues[0:5].copy() + raw.copy()
            arr_rows_filled.append(cur_row)
        
    # group data by container
    for rf in arr_rows_filled:
        for uc in unique_containers.keys():
            if rf[3] == uc:
                unique_containers[uc].append(rf)
                break

    for _, dataset in unique_containers.items():
        # calculate utilizations 
        prev_row = []
        i = 0
        for row in dataset:
            if len(prev_row) > 0:
                interval = get_interval(row[-1], prev_row[-1])
                if global_hosts.get(row[4]):
                    host_info = global_hosts.get(row[4])
                else:
                    # get and parse documents
                    result, ndocs = get_host_info(row[4])
                    host_info = {}
                    if ndocs > 0:
                        result = parse_docs(result, ndocs)
                        host_info = result[0]

                    global_hosts[row[4]] = host_info
                    if path and FLAG_SAVE_DATASETS:
                        write_json_to_disk(host_info, path+'/'+str(i))
                # cpu
                u1 = get_cpu_util(interval, row[5], prev_row[5], host_info.get('cpu_frequency_khz'),
                    host_info.get('num_cores'), cores_considered)
                if u1 < 0:
                    u1 = 0
                # memory
                u2 = get_utilization(row[6], host_info.get('memory'))
                # filesystem
                if host_info.get('overlay'):
                    u3 = get_utilization(row[7], host_info.get('overlay'))
                else:
                    u3 = get_utilization(row[7], host_info.get('storage'))
                # network is calculated later
                u4 = get_net(interval, row[8], prev_row[8])
                util_row = row.copy()
                util_row[5] = u1
                util_row[6] = u2
                util_row[7] = u3
                util_row[8] = u4
                arr_utils.append(util_row)
            else:
                prev_row = row.copy()

    return arr_rows_filled,arr_utils,c_names

def parse_docs(result, n):
    """
    parse mongo result to json when containig dates
    """
    docs = []
    if n and n > 0:
        for i in range(n):
            try:
                elem = json.loads( JSONEncoder().encode(result[i]) )
            except:
                # TypeError: Object of type datetime is not JSON serializable
                elem = parse_doc_containing_date_v1_v2(result[i])
            docs.append(elem)
    return docs

def parse_doc_containing_date_v1_v2(doc):
    """
    parse cursor to json when contains datetime fields in
    first level and second level (into an array element)
    """
    new_doc = {}
    for k,v in doc.items():
        if k in ['first','last']:
            # convert datetime.datetime to str
            v = parse_RFC3339_datetime_to_str(v)

        # for samples v1
        if k == 'timestamp':
            if type(v) is list:
                t_stamps = []
                for t in v:
                    # convert datetime.datetime to str
                    t_stamps.append( parse_RFC3339_datetime_to_str(t) )
                v = t_stamps
            else:
                v = parse_RFC3339_datetime_to_str(v)
            
        # for samples v2
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

def get_date_by_label(begin_full_date, id_or_name_sol):
    t_stamp = ''
    if begin_full_date == 'BEGIN':
        result = get_bot_top_dates(CL_RESOURCES[0], id_or_name_sol)
        if len(result) > 0:
            t_stamp = result[0].get('minimumDate')
    
    elif begin_full_date == 'END':
        result = get_bot_top_dates(CL_RESOURCES[0], id_or_name_sol)
        if len(result) > 0:
            t_stamp = result[0].get('maximumDate')
    
    else:
        t_stamp = ''
        begin_full_date = begin_full_date.split('-', 6)
        if len(begin_full_date) == 6:
            d = [int(v) if v else None for v in begin_full_date]
            t_stamp = datetime(year = d[0], month = d[1], day = d[2], hour = d[3], minute = d[4], second = d[5])
    return t_stamp

def statistics_of_container(df_con):

    metric_cols = ['name_container','cpu_util','filesystem_util','memory_util','network_util']
    df_con = df_con[metric_cols]
    gp3 = df_con.groupby('name_container')

    df_min = gp3.min()
    df_max = gp3.max()
    df_mean = gp3.mean()
    df_mdn = gp3.median()
    # stdev of sample
    df_std = gp3.std() # pandas default degrees of freedom is one
    # stdev of population
    # df_std = gp3.std(ddof=0)

    df_min['statistic'] = ['min']
    df_max['statistic'] = ['max']
    df_mean['statistic'] = ['mean']
    df_mdn['statistic'] = ['median']
    df_std['statistic'] = ['std']

    thresholds = []
    for m in df_mdn.iloc[:,0:4]:
        mdn = df_mdn[m][0]
        if THRESHOLDS[0] <= mdn and mdn < THRESHOLDS[1]:
            thresholds.append('low')
        elif THRESHOLDS[1] <= mdn and mdn < THRESHOLDS[2]:
            thresholds.append('medium')
        elif THRESHOLDS[2] <= mdn and mdn <= THRESHOLDS[3]:
            thresholds.append('high')
        else:
            thresholds.append('unknown')
            print(f'mdn: {mdn}')

    return df_min,df_max,df_mean,df_mdn,df_std,thresholds

def top_net_value(max_net):
    global ten_megabyte
    if max_net and max_net > ten_megabyte:
        print(f'total_net overcomed: {max_net}')
        # TODO: handle max net, probably new max net as total net
        # return new_max
    return ten_megabyte  



# @diagnosis_bp.route('/v3/aggregates/<string:sol_id_or_name>/<string:begin_full_date>/<string:window_size>/<int:chunk_size>/<string:result_name>', methods=['GET'])
# def aggregates_v3(sol_id_or_name, begin_full_date, window_size, chunk_size, result_name):
#     """ DEV ONLY
#     Calculate utilizations and its aggregates in period start to end
#     start is begin_full_date
#     end is start + each experiment in window_size
#     aggregates are descriptive statistics min,max,mean,median,std
#     and also the status threshold (low,medium,high) depending on 
#     the median value.
#     Results are saved in indexing

#     Args:
#         sol_id_or_name (str): the name or id of the solution
#         begin_full_date (str): is the start period separated by mid slash or minimum date when this value is BEGIN. e.g. 2020-3-26-6-14-30
#         window_size (str): experiments to get separated by mid slash, e.g. 1-10-100
#         chunk_size (int): is for increasing the begin time as many times as requiered to reach the end time. This means: while (start <= end) do { actual experiment and increase start = start + chunk_size }
#         result_name (str): the name to save results in idx

#     Returns:
#         response: 200 if results saved correctly 400 if not
#     """
#     ndocs,exps_result = agg_v2_fun(sol_id_or_name, begin_full_date, window_size, chunk_size, result_name)

#     if ndocs > 0:
#         resp = jsonify({'msg':'documents found', 'n':ndocs, 'exps':exps_result})
#     else:
#         resp = jsonify({'msg':'documents not found', 'n':ndocs, 'exps':exps_result}), 400

#     return resp

# def agg_v3_fun(sol_id_or_name, begin_full_date, window_size, chunk_size, result_name):
    
#     starttime = timeit.default_timer()
#     ndocs = 0
#     exps = []

#     # obtain the begin date if not provided
#     begin = get_date_by_label(begin_full_date, sol_id_or_name)
#     if begin == '':
#         print('Not found: invalid date option')
#         takentime = timeit.default_timer() - starttime
#         write_to_timelog('diag', takentime)
#         return ndocs, exps
        
#     # experiments: expand and calculate times for each experiment
#     for i,e in enumerate( window_size.split('-') ):
#         # calculate times for each experiment (element 0 in array)
#         if begin_full_date == 'BEGIN':
#             exp = [int(e), chunk_size, begin, begin + timedelta(minutes=int(e))]
#         elif begin_full_date == 'END':
#             exp = [int(e), chunk_size, begin - timedelta(minutes=int(e)), begin]
#         else:
#             exp = [int(e), chunk_size, begin, begin + timedelta(minutes=int(e))]

#         # create main folder
#         ct = parse_RFC3339_datetime_to_str(datetime.today())
#         path = os.sep.join([os.getcwd(), DATASETS_FOLDER, sol_id_or_name, ct, str(exp[0])])
#         make_subfolders(path)
            
#         # get metric docs in period from index
#         ndocs, result = get_period_btwn_begin_end(sol_id_or_name, exp[2], exp[3])
#         json_docs = parse_docs(result,ndocs)
#         if ndocs > 0:
#             arr_docs, arr_utils, cols = structure_docs(json_docs, path)
#             df_all = None

#             # save raw datasets
#             # filename = 'ds_v1_' + str(exp[0]) + 'm_' + str(exp[1]) + 'ch'
#             # df_all = pd.DataFrame(arr_docs, columns=cols)
#             # path_file = os.sep.join([path, 'raw'])
#             # export_to_csv(path_file, df_all, True)
#             # path_file = os.sep.join([path, 'raw_stats'])
#             # desc = df_all.describe()
#             # export_to_csv(path_file, desc, True)

#             # reduce columns
#             df_all = pd.DataFrame(arr_utils, columns=cols)            
#             selected_cols = ['name_solution','name_container','cpu_util','filesystem_util','memory_util','network_util','timestamp']
#             df_all = df_all[selected_cols]

#             # calculate top network based on max value in period
#             # max_net = df_all['network_util'].max()
#             # total_net = top_net_value(max_net)

#             # preprocess dataframe and process each container
#             df_all['network_util'] = df_all['network_util'].apply( get_utilization, args=[total_net] )
#             df_all['timestamp'] = df_all['timestamp'].apply(lambda _: parse_RFC3339_str_to_datetime(_))
#             exp_result, exp_stats_error = process_save_each_vc(df_all, path)                

#             chunks = []
#             stats_error = []
#             for ch in range(1, int(exp[0] / exp[1]) + 1):
#                 chunk = []
#                 # |\|\..., calculate times for each chunk
#                 if ch == 1:
#                     chunk = [exp[2], exp[2] + timedelta(minutes=exp[1])]
#                 else:
#                     chunk = [chunks[ch - 2][1], chunks[ch - 2][1] + timedelta(minutes=exp[1])]

#                 path_ch = os.sep.join([path, 'chunks', str(ch)])
#                 make_subfolders(path_ch)

#                 # filter by date and process chunk
#                 df_date = df_all[(df_all['timestamp'] >= chunk[0]) & (df_all['timestamp'] < chunk[1])]
#                 ch_results, ch_stats_error = process_save_each_vc(df_date, path_ch)
#                 chunk.append(ch_results)
#                 stats_error.append(ch_stats_error)

#                 chunks.append(chunk)

#         exp.append(ndocs)
#         exp.append(exp_result)
#         exp.append(chunks)
#         exps.append(exp)

#         # save util datasets
#         if FLAG_SAVE_DATASETS:
#             path_file = os.sep.join([path, 'util'])
#             export_to_csv(path_file, df_all, True)
#             path_file = os.sep.join([path, 'util_stats'])
#             desc = df_all.describe()
#             export_to_csv(path_file, desc, True)

#     # prepare status to index
#     sol_id = json_docs[0].get('id_solution')
#     sol_name = json_docs[0].get('name_solution')
#     payload = {
#         'exp_name': result_name,
#         'creation_time': parse_RFC3339_datetime_to_str(datetime.today()),
#         'sol_id': sol_id,
#         'sol_name': sol_name,
#         'exp': exp[0],
#         'dt_ini': parse_RFC3339_datetime_to_str(chunk[0]),
#         'dt_end': parse_RFC3339_datetime_to_str(chunk[1]),
#         'data_status': stats_error
#     }

#     takentime = timeit.default_timer() - starttime
#     write_to_timelog('diag', takentime)

#     print(f'payload len: {len(payload)}')
#     rs = save_status_to_index(payload)

#     return ndocs, exps