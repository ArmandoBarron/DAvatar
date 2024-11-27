import requests
import json

from .constants import IDX_PAIR, JSON_HEADERS

def save_status_to_index(payload):
    url = 'http://'+IDX_PAIR+'/solutions/status'
    resp = {}
    status = 500
    r = None
    try:
        r = requests.post(url, data=json.dumps(payload), headers=JSON_HEADERS)
    except requests.exceptions.RequestException as e:
        # print(e)
        status = 500
    if r and r.status_code == 201 :
        resp = r.json() 
        status = 201
    else:
        status = (r.status_code if r != None and r.status_code else 500)
    return resp, status