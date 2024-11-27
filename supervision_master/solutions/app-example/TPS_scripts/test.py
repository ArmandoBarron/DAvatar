from TPS.Builder import Builder #TPS API BUILDER
import sys
import os
import time


metaworkflow=Builder("REDMET_MERRA",TPS_manager_host="http://localhost:54350")

workflow_name= "RAMA-wf"
pollutant = "CO" #pollutant


metaworkflow.TPS_data_extraction("Org",path="/categories/" + pollutant,workflow=workflow_name,monitor="dagon",label=pollutant)

extraction_time = time.time() ## <--------------- TIME
metaworkflow.init_tps() # all the extractor defined are executed
extraction_time = time.time() - extraction_time## <--------------- TIME

