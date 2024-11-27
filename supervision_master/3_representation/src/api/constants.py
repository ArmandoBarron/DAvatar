from os import getenv

IDX_PAIR = getenv('INDEXING_HOST', 'indexing') + ':' + getenv('INDEXING_PORT', '5000')

JSON_HEADERS = {"Content-Type": "application/json"}
OUT_FOLDER = 'sink'
LOG_FILE = 'logs/mylog.csv'
FLAG_CALCULATE_TIMES = int(getenv('FLAG_CALCULATE_TIMES', False))
FLAG_SAVE_DATASETS = int(getenv('FLAG_SAVE_DATASETS', False))