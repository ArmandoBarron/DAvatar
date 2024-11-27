from .requests_handler import do_get, do_post
from .constants import T_OUT_LOW

def get_host_metrics_raw(url):
  r = do_get(url, timeout=T_OUT_LOW) # , auth=(USER, PASS)
  if r != None and r.status_code == 200:
    status = 200
    data = r.json()
  else:
    print('Couldnt get host metrics')
    status = (r.status_code if r != None and r.status_code else 500)
    data = {'msg': 'not found'}
  return data, status

def get_containers(url):
  payload = {
    'num_stats':1,
    'num_samples':0
  }
  r = do_post(url, payload)
  status = (r.status_code if r != None and r.status_code else 500)
  if status == 200:
    return r
  return None

def get_container_metrics_raw(url, n):
  # url = hosts_list[host_id]['location']+'/'+endpoints_list[2]['endpoint']+'/'+container_id
  # Request 60s of container history and no samples.
  payload = {
    'num_stats': n, # cAdvisor default: 60
    'num_samples': 0
  }
  status = 500
  r = do_post(url, payload)
  print(f'respuesta de cadvisor {r.text} al {url}')
  if r != None and r.status_code == 200:
    data = r.json()
    status = 200
  else:
    data = None
    status = (r.status_code if r != None and r.status_code else 500)
  return data, status