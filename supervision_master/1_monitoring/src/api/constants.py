import os

# IDX_HOST = os.environ['INDEXING_HOST']
# IDX_PORT = os.environ['INDEXING_PORT']
# MONITOR_HOST = os.environ['MONITORING_HOST']
# MONITOR_PORT = os.environ['MONITORING_PORT']
# SOL_MGR_HOST = os.environ['SOLUTION_MGR_HOST']
# SOL_MGR_PORT = os.environ['SOLUTION_MGR_PORT']
# DIAG_HOST = os.environ['DIAGNOSIS_HOST']
# DIAG_PORT = os.environ['DIAGNOSIS_PORT']
# LH_IP = os.environ['LOCALHOST_IP']
# LH_PORT = os.environ['LOCALHOST_PORT']
LH_ID = int(os.environ['LOCALHOST_ID'])

USER = 'root' # USER = os.environ['ADMIN_USER']
PASS = 'jupiter' # PASS = os.environ['ADMIN_PASSWORD']

T_OUT_HIGH = 10
T_OUT_LOW = 3
JSON_HEADERS = {'Content-Type': 'application/json'}

LOG_FILE = 'logs/mylog.csv'
FLAG_CALCULATE_TIMES = int(os.environ['FLAG_CALCULATE_TIMES'])

IDX_PAIR = os.environ['INDEXING_HOST'] + ':' + os.environ['INDEXING_PORT']
MTR_PAIR = os.environ['MONITORING_HOST'] + ':' + os.environ['MONITORING_PORT']
SMGR_PAIR = os.environ['SOLUTION_MGR_HOST'] + ':' + os.environ['SOLUTION_MGR_PORT']
DIAG_PAIR = os.environ['DIAGNOSIS_HOST'] + ':' + os.environ['DIAGNOSIS_PORT']
LH_PAIR = os.environ['LOCALHOST_IP'] + ':' + os.environ['LOCALHOST_PORT']