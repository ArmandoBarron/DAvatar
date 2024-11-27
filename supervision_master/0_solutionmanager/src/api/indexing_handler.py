from .requests_handler import do_post, do_put, do_delete
from .constants import IDX_PAIR

def index_add_solution(payload):
  url = 'http://'+IDX_PAIR+'/solutions'
  info = {}
  status = 500
  r = do_post(url, payload)
  status = (r.status_code if r != None and r.status_code else 500)
  if status == 201:
      info = r.json()
  return info, status

def index_remove_solution(id_or_name, del_metrics):
  url = 'http://'+IDX_PAIR+'/solutions/'+id_or_name+'/metrics/'+str(del_metrics)
  info = {}
  status = 500
  r = do_delete(url)
  status = (r.status_code if r != None and r.status_code else 500)
  if status == 200:
      info = r.json()
  return info, status

def index_update_containerids(sol_id, sol_conts):
  url = 'http://'+IDX_PAIR+'/solutions/'+sol_id+'/container_ids'
  info = {}
  status = 500
  r = do_put(url, sol_conts)
  status = (r.status_code if r != None and r.status_code else 500)
  if status == 200:
      info = r.json()
  return info, status