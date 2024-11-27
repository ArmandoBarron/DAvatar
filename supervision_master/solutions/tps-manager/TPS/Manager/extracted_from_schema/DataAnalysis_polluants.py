from TPS.Builder import Builder #TPS API BUILDER
import sys
import os
import time
import pandas as pd



metaworkflow=Builder("REDMET_MERRA",TPS_manager_host="http://localhost:54350")

metaworkflow.TPSapi.PutData('DataAnalysis_polluants.py',"poll")


#query = metaworkflow.TPSapi.format_query("clust_DIFF","pollutants",keygroups=["FECHA-FECHA","stations-stations"] })

query = metaworkflow.TPSapi.format_single_query("poll")
res = metaworkflow.TPSapi.TPS(query,"getdata",label="all_data")
print(res)

"""

#mix REDMET and REDMA
query = metaworkflow.TPSapi.format_query("clust_DIFF","pollutants",keygroups=["FECHA-FECHA","stations-stations"] })
res = metaworkflow.TPSapi.TPS(query,"getdata",label="all_data")
print(res)

query = metaworkflow.TPSapi.format_single_query("all_data",filter1={"rename":[{"class":"class_tmp"}] })
res = metaworkflow.TPSapi.TPS(query,"getdata",label="all_data")
print(res)




#cleaning. droping records with na values

query = metaworkflow.TPSapi.format_single_query("all_data") #query
res = metaworkflow.TPSapi.TPS(query,"cleaningtools",options={"columns":"all","ReplaceWithNa":['None',-99,-99.0,'NaN','nan'],"DropNa":{"thresh":25}},label="clean_all_data")
print(res)

#statistics of each column
query = metaworkflow.TPSapi.format_single_query("clean_all_data") #query to a single task
result_desc = metaworkflow.TPSapi.TPS(query,"describe",options={'columns':'all'},label="stadistics_all_data")
print(result_desc)


query = metaworkflow.TPSapi.format_single_query("clean_all_data") #query to a single task
res= metaworkflow.TPSapi.TPS(query,"graphics",options={"kind":"hist","variables":['CO','NO','NO2','NOX','O3','PM10','PM25',"SO2"],"alpha":.25,"bins":20 })
with open("polluants_"+res['filename'],"wb") as file:
        file.write(res['result'])


list_pollutants =['CO','NO','NO2','NOX','O3','PM10','PM25',"SO2"]
# Create a histogram of each pollutant
for poll in list_pollutants:
        query = metaworkflow.TPSapi.format_single_query("clean_all_data") #query to a single task
        res= metaworkflow.TPSapi.TPS(query,"graphics",options={"kind":"hist","variables":[poll],"alpha":.25,"bins":20 })
        with open("polluants_"+poll+"_"+res['filename'],"wb") as file:
                file.write(res['result'])


#get correlation with kendall coeficient

list_variables = "CO,NO,NO2,NOX,O3,PM10,PM25,SO2,TMP,T2MMEAN,DIFF"
query = metaworkflow.TPSapi.format_single_query("clean_all_data") #query to a single task
result_desc = metaworkflow.TPSapi.TPS(query,"ANOVA",options={"variables":list_variables,"method":"kendall"},label="kendall_all_data")
print(result_desc)
#get correlation with kendall coeficient

list_variables = "CO,NO,NO2,NOX,O3,PM10,PM25,SO2,TMP,T2MMEAN,DIFF"
query = metaworkflow.TPSapi.format_single_query("clean_all_data") #query to a single task
result_desc = metaworkflow.TPSapi.TPS(query,"ANOVA",options={"variables":list_variables,"method":"spearman"},label="spearman_all_data")
print(result_desc)


#get some clusters ange make a graphic
#we use a clustering alghoritm to see the behavior of this difference
query = metaworkflow.TPSapi.format_single_query("clean_MERRA_REDMET") #query to a single task
res= metaworkflow.TPSapi.TPS(query,"clustering",options={"k":3,"alghoritm":"kmeans","variables":"DIFF"},label="clust_DIFF")
print(res)



query = metaworkflow.TPSapi.format_single_query("clean_all_data")
res = metaworkflow.TPSapi.TPS(query,"getdata")
pd.DataFrame.from_records(data=res['result']).to_csv('dict_file.csv',index=False)

pd.DataFrame.from_records(data=res['result']).to_csv('dict_file.csv',index=False)
"""