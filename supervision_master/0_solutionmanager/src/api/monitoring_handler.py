from .requests_handler import do_get
from .constants import MTR_PAIR

def monitor_start_monitoring(monitor_flag, key, aggregates_flag):
    # global aggregates_flag
    url = 'http://'+MTR_PAIR+'/api/v1/monitor/start/'+str(monitor_flag)+'/'+key+'/'+str(aggregates_flag)
    ret = None
    r = do_get(url)
    status = (r.status_code if r != None and r.status_code else 500)
    if status == 200:
        ret = r.json()
    return ret