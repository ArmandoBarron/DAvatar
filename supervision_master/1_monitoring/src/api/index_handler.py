from .requests_handler import do_get, do_post
from .constants import IDX_PAIR

def index_host_list(payload):
  url = 'http://'+IDX_PAIR+'/hosts'
  r = do_post(url, payload)
  if r and r.status_code == 200:
    ret = 200, r.json()
  else:
    status = (r.status_code if r != None and r.status_code else 500)
    ret = status, None
  return ret

def index_metrics_of_solution(url, payload):
  """
  save the metrics of the solution container
  """
  r = do_post(url, payload)
  if r and r.status_code == 200:
    ret = 200, r.json()
  else:
    status = (r.status_code if r != None and r.status_code else 500)
    ret = status, None
  return ret

def get_solution_info(url):
  """
  get the solution saved in the indexing
  """
  r = do_get(url)
  if r != None and r.status_code == 200:
    data = r.json()
    solution = data.get('data')
  else:
    print('Couldnt get solution')
    solution = {}
  return solution