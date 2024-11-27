#!/usr/bin/python3
# Execution command: python3 studycase-step-1.py -f Pollutants-data/19RAMA/ -l .

# to see resultant data
# http://localhost:54350/{METAWORKFLOW}/stadistics_all_data/
# http://localhost:54350/{METAWORKFLOW}/{label}/

import os
import argparse
import timeit
from TPS.Builder import Builder # TPS API BUILDER


def save_times_to_file(log_path,times):
    logfile = open(log_path+"/log1-load.txt", "a+")
    for plltt,extraction_time,fc_time,tr_time,gr_time in times:
        logfile.write( "%s,%s,%s,%s,%s\r\n" %(plltt,extraction_time,fc_time,tr_time,gr_time) )
    logfile.close()

def parseArguments():
    """
    define and parse arguments passed to the program
    """
    parser = argparse.ArgumentParser(description='Description of your program')
    # parser.add_argument('-w','--workflow', help='Desc', required=True)
    # parser.add_argument('-p','--pollutant', help='Desc', required=True)
    parser.add_argument('-f','--folder', help='Desc', required=True)
    parser.add_argument('-l','--logpath', help='Desc', required=True)
    return parser.parse_args()

if __name__ == '__main__':
    args = parseArguments()

    metaworkflow=Builder("STUDY-CASE-TEST",TPS_manager_host="http://localhost:54350")

    # pollutant = args.pollutant # "RAMA-CO"
    folder = args.folder # 'Pollutants/data-small/'
    log_path = args.logpath

    pollutants = []
    times = []

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

            # transform columns to records with the label stations
            tr_time = timeit.default_timer() ## <--------------- TIME
            query = metaworkflow.TPSapi.format_single_query("clean_"+plltt) # query to a single task
            res= metaworkflow.TPSapi.TPS(query,"transform",options={"process":"melt","id_vars":['FECHA','HORA'],"var_name":"stations","value_name":plltt },label="T_"+plltt)
            tr_time = timeit.default_timer() - tr_time ## <--------------- TIME
            print(res)

            # group all the records which has the same FECHA and station values. 
            # This help us to reduce data. data producen in a single day by the same station is grouped by mean.
            gr_time = timeit.default_timer() ## <--------------- TIME
            query = metaworkflow.TPSapi.format_single_query("T_"+plltt) # query to a single task
            res= metaworkflow.TPSapi.TPS(query,"transform",options={"process":"group","group":['FECHA','stations'],"variable":plltt,"group_by":"mean" },label="group_"+plltt)
            gr_time = timeit.default_timer() - gr_time ## <--------------- TIME
            print(res)

            times.append((plltt,extraction_time,fc_time,tr_time,gr_time))


    save_times_to_file(log_path,times)