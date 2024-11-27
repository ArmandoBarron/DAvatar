#!/usr/bin/python3
# Execution command: python3 studycase-step-2.py -l .

# to see resultant data
# http://localhost:54350/{METAWORKFLOW}/stadistics_all_data/
# http://localhost:54350/{METAWORKFLOW}/{label}/

import os
import argparse
import timeit
from TPS.Builder import Builder # TPS API BUILDER
from base64 import b64decode,b64encode


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
    logfile = open(log_path+"/log2-join.txt", "a+")
    logfile.write("%s\n" %(times))
    logfile.close()

def parseArguments():
    """
    define and parse arguments passed to the program
    """
    parser = argparse.ArgumentParser(description='Description of your program')
    # parser.add_argument('-w','--workflow', help='Desc', required=True)
    # parser.add_argument('-p','--pollutant', help='Desc', required=True)
    # parser.add_argument('-f','--folder', help='Desc', required=True)
    parser.add_argument('-l','--logpath', help='Desc', required=True)
    return parser.parse_args()

if __name__ == '__main__':
    args = parseArguments()

    metaworkflow=Builder("STUDY-CASE-TEST",TPS_manager_host="http://localhost:54350")

    log_path = args.logpath


    # init_time = timeit.default_timer() ## <--------------- TIME
    # query = metaworkflow.TPSapi.format_query("group_CO","group_NO",keygroups=["FECHA-FECHA","stations-stations"])
    # res = metaworkflow.TPSapi.TPS(query,"getdata",label="pollutants")
    # list_data = ["NO2","NOX","O3","PM10","PM25","PMCO","SO2"]
    # for pollutant in list_data:
    #     query = metaworkflow.TPSapi.format_query("pollutants","group_"+pollutant,keygroups=["FECHA-FECHA","stations-stations"])
    #     res = metaworkflow.TPSapi.TPS(query,"getdata",label="pollutants")
    #     print(res)
    # end_time = timeit.default_timer() - init_time ## <--------------- TIME

    # save_times_to_file(log_path,end_time)

    # al final este script agrupa todas las columnas de los contaminantes en una sola tabla llamada pollutants
    # tambien se pueden aplicar las funciones dell script “DataAnalysis_Pollutants”



    # to verify if was saved
    # query data without label to get them and print in console
    query = metaworkflow.TPSapi.format_single_query("pollutants")
    res = metaworkflow.TPSapi.TPS(query,"getdata")
    print('verify if data was saved')
    if res:
        print(f'res: {type(res)}')
        print(f'res: {len(res)}')



    #statistics of each column
    query = metaworkflow.TPSapi.format_single_query("pollutants") #query to a single task
    result_desc = metaworkflow.TPSapi.TPS(query,"describe",options={'columns':'all'},label="stadistics_pollutants")
    print(result_desc)



    list_pollutants =['CO','NO','NO2','NOX','O3','PM10','PM25',"SO2"]

    folder1 = 'Pollutants-plots/'
    folder2 = 'Pollutants-clust/'
    create_subfolders_777(folder1)
    create_subfolders_777(folder2)

    # Create a histogram of each pollutant
    for poll in list_pollutants:
            query = metaworkflow.TPSapi.format_single_query("pollutants") # query to a single task
            res= metaworkflow.TPSapi.TPS(query,"graphics",options={"kind":"hist","variables":[poll],"alpha":.25,"bins":20 })
            with open(folder1+poll+"_"+res['filename'],"wb") as file:
                    file.write(res['result'])
    


    # get some clusters ange make a graphic
    # we use a clustering alghoritm to see the behavior of this difference
    for poll in list_pollutants:
        query = metaworkflow.TPSapi.format_single_query("pollutants") # query to a single task
        res = metaworkflow.TPSapi.TPS(query,"clustering",options={"k":3,"alghoritm":"kmeans","variables":poll},label="clust_"+poll)
        print(res)
        

        query = metaworkflow.TPSapi.format_single_query("pollutants",filter1={'sample':{'n':5000,'replace':False}}) # query to a single task
        res = metaworkflow.TPSapi.TPS(query,"clustering",options={"alghoritm":"silhouette","variables":poll})
        print('end silhouette')
        with open(folder2+res['result']['filename'],"wb") as file:
                file.write(b64decode(res['result']['image'].encode()))

