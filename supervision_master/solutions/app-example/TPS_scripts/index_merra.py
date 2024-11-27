from TPS.Builder import Builder #TPS API BUILDER
import sys
import os
import time


metaworkflow=Builder("REDMET_MERRA",TPS_manager_host="http://localhost:54350")

metaworkflow.TPSapi.PutData("/home/robot/Escritorio/Projects/Workflows/MERRA-sinaica/datos_merra_sinaica/with_date","MERRA")

query = metaworkflow.TPSapi.format_single_query("MERRA",filter1={"eval":["T2MMAX = T2MMAX - 273.15"
                                                                        ,"T2MMEAN = T2MMEAN - 273.15"
                                                                        ,"T2MMIN = T2MMIN - 273.15"
                                                                        ], "columns":['FECHA','HOURNORAIN','Station_code',
                                                                        'T2MMAX','T2MMEAN','T2MMIN','TPRECMAX','latitud','longitud'] }) #modify
res = metaworkflow.TPSapi.TPS(query,"getdata",label = "MERRA")
print(res)