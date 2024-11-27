import os

LOG_FILE = 'logs/mylog.csv'
ALL_LOG_FILE = 'logs-services.csv'
YML_FOLDER = 'files'
FLAG_CALCULATE_TIMES = int(os.environ['FLAG_CALCULATE_TIMES'])

IDX_PAIR = os.environ['INDEXING_HOST'] + ':' + os.environ['INDEXING_PORT']
MTR_PAIR = os.environ['MONITORING_HOST'] + ':' + os.environ['MONITORING_PORT']
RPR_PAIR = os.environ['REPRESENTATION_HOST'] + ':' + os.environ['REPRESENTATION_PORT']
DGS_PAIR = os.environ['DIAGNOSIS_HOST'] + ':' + os.environ['DIAGNOSIS_PORT']

JSON_HEADERS = {"Content-Type": "application/json"}