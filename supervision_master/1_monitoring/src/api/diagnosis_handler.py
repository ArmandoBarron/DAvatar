from .requests_handler import do_get
from .constants import DIAG_PAIR

def do_aggregates_all(sol_name):
  url = 'http://'+DIAG_PAIR+'/v6/aggregates/'+sol_name+'/ALL/status-'+sol_name+'-ALL'
  r = do_get(url)
  status = (r.status_code if r != None and r.status_code else 500)
  if status == 200: # must be 201
    return r.json()
  return None