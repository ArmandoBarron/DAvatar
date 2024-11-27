from TPS.Builder import Builder #TPS API BUILDER
import sys
import os
import time


metaworkflow=Builder("REDMET_MERRA",TPS_manager_host="http://localhost:54350")

log_path = sys.argv[1] #where the log will be saved

join_time = time.time() ## <--------------- TIME
query = metaworkflow.TPSapi.format_query("group_CO","group_NO",keygroups=["FECHA-FECHA","stations-stations"])
res = metaworkflow.TPSapi.TPS(query,"getdata",label="pollutants")
list_data = ["NO2","NOX","O3","PM10","PM25","PMCO","SO2"]
for pollutant in list_data:
    query = metaworkflow.TPSapi.format_query("pollutants","group_"+pollutant,keygroups=["FECHA-FECHA","stations-stations"])
    res = metaworkflow.TPSapi.TPS(query,"getdata",label="pollutants")
    print(res)
join_time = time.time() - join_time## <--------------- TIME


logfile= open(log_path+"/log_join_RAMA.txt", "a+")
logfile.write("%s\n" %(join_time))
logfile.close()
