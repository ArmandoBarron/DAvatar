from TPS.Builder import Builder #TPS API BUILDER
import sys
import os
import time


metaworkflow=Builder("REDMET_MERRA",TPS_manager_host="http://localhost:54350")

workflow_name= "REDMET-wf"
pollutant = "CO" #pollutant


metaworkflow.TPSapi.PutData("./CO",pollutant)

extraction_time = time.time() ## <--------------- TIME
metaworkflow.init_tps() # all the extractor defined are executed
extraction_time = time.time() - extraction_time## <--------------- TIME

#first cleaning
fc_time = time.time()## <--------------- TIME
query = metaworkflow.TPSapi.format_single_query(pollutant) #query
res = metaworkflow.TPSapi.TPS(query,"cleaningtools",options={"columns":"all","ReplaceWithNa":['None',-99,-99.0,'NaN','nan'],"DropNa":None,\
                        "NaReaplace":"interpolate"},label="clean_"+pollutant)
fc_time = time.time() - fc_time## <--------------- TIME

print(res)

#transform columns to records with the label stations
tr_time = time.time() # <--------------- TIME
query = metaworkflow.TPSapi.format_single_query("clean_"+pollutant) #query to a single task
res= metaworkflow.TPSapi.TPS(query,"transform",options={"process":"melt","id_vars":['FECHA','HORA'],"var_name":"stations","value_name":pollutant },label="T_"+pollutant)
tr_time = time.time() - tr_time## <--------------- TIME
print(res)

#group all the records which has the same FECHA and station values. this help us to reduce data. data producen in a single day by the same station is grouped by mean.
gr_time = time.time()## <--------------- TIME
query = metaworkflow.TPSapi.format_single_query("T_"+pollutant) #query to a single task
res= metaworkflow.TPSapi.TPS(query,"transform",options={"process":"group","group":['FECHA','stations'],"variable":pollutant,"group_by":"mean" },label="group_"+pollutant)
gr_time = time.time() - gr_time## <--------------- TIME
print(res)

#logfile= open(log_path+"/log_"+pollutant+".txt", "a+")
#logfile.write("%s,%s,%s,%s \n" %( extraction_time,fc_time,tr_time,gr_time))
#logfile.close()
