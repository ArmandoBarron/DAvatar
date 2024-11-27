import os

JSON_HEADERS = {'Content-Type': 'application/json'}
LOG_FILE = 'logs/mylog.csv'
DATASETS_FOLDER = 'datasets'
FLAG_CALCULATE_TIMES = int(os.getenv('FLAG_CALCULATE_TIMES', False))
FLAG_SAVE_DATASETS = int(os.getenv('FLAG_SAVE_DATASETS', False))

DB_PAIR = os.getenv('DB_HOST', 'datacube') + ':' + os.getenv('DB_PORT', '27019')
IDX_PAIR = os.getenv('INDEXING_HOST', 'indexing') + ':' + os.getenv('INDEXING_PORT', '5000')
REP_PAIR = os.getenv('REPRESENTATION_HOST', 'representation') + ':' + os.getenv('REPRESENTATION_PORT', '5000')

DB_DATACUBE = 'datacube'
CL_RESOURCES = ['AggDocPerSecond_v1', 'hosts', 'duration']
THRESHOLDS = (0, 0.33, 0.66, 1)