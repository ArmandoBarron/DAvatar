from .requests_handler import do_post
from .constants import REP_PAIR

def request_make_model(status_name, payload):
  url = 'http://' + REP_PAIR + '/model/wot-td/' + status_name
  r = do_post(url, payload)
  status = (r.status_code if r != None and r.status_code else 500)
  if status == 201:
    return r.json()
  return None