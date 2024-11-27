from TPS.Builder import Builder #TPS API BUILDER
import sys
import os
import time
from base64 import b64decode,b64encode


metaworkflow=Builder("REDMET_MERRA",TPS_manager_host="http://localhost:54350")
"""
#mix merra with REDMET
query = metaworkflow.TPSapi.format_query("MERRA","temperatures",keygroups=["FECHA-FECHA","Station_code-stations"])
res = metaworkflow.TPSapi.TPS(query,"getdata",label="MERRA_REDMET")
print(res)

#lets start with some basic stadistics
query = metaworkflow.TPSapi.format_single_query("MERRA_REDMET") #query to a single task
result_desc = metaworkflow.TPSapi.TPS(query,"describe",options={'columns':'all'},label="stadistics_ME-RE")
print(result_desc)



#cleaning. since the mix in REDMET created null values (because there are)
# its nos possible now to interpolate the data, so we decide to drop the columns

query = metaworkflow.TPSapi.format_single_query("MERRA_REDMET") #query
res = metaworkflow.TPSapi.TPS(query,"cleaningtools",options={"columns":"all","ReplaceWithNa":['None',-99,-99.0,'NaN','nan'],"DropNa":{"thresh":14}},label="clean_MERRA_REDMET")
print(res)


#get difference and get more stadistics
query = metaworkflow.TPSapi.format_single_query("clean_MERRA_REDMET",filter1={"eval":["DIFF = T2MMEAN - TMP"]}) #modify
res = metaworkflow.TPSapi.TPS(query,"getdata",label = "clean_MERRA_REDMET")
print(res)

query = metaworkflow.TPSapi.format_single_query("clean_MERRA_REDMET") #query to a single task
result_desc = metaworkflow.TPSapi.TPS(query,"describe",options={'columns':'all'},label="stadistics_ME-RE")
print(result_desc)

"""

#get some clusters ange make a graphic
#we use a clustering alghoritm to see the behavior of this difference
#make some test..... n =  50
for test in range(1,51):
        query = metaworkflow.TPSapi.format_single_query("clean_MERRA_REDMET",filter1={'sample':{'n':5000,'replace':False}}) #query to a single task
        res= metaworkflow.TPSapi.TPS(query,"clustering",options={"alghoritm":"silhouette","variables":"DIFF"})
        #print(res)
        with open("50_test/test_"+str(test)+"_"+res['result']['filename'],"wb") as file:
                file.write(b64decode(res['result']['image'].encode()))

        cluster_data = res['result']['data'] #data to send 
        # Create a scatter graph of results

        query = metaworkflow.TPSapi.format_single_query("clust_DIFF") #query to a single task
        res= metaworkflow.TPSapi.TPS(query,"graphics",workload=cluster_data,options={"kind":"scatter","variables":['TMP','T2MMEAN','DIFF'],"labels":"class"})
        with open("50_test/test_"+str(test)+"_"+res['filename'],"wb") as file:
                file.write(res['result'])
"""
query = metaworkflow.TPSapi.format_single_query("clust_DIFF") #query to a single task
res= metaworkflow.TPSapi.TPS(query,"graphics",options={"kind":"hist","variables":['TMP','T2MMEAN'],"alpha":.25,"bins":20 })
with open(res['filename'],"wb") as file:
        file.write(res['result'])
        """
