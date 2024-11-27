import requests
import json
from .constants import IDX_PAIR, JSON_HEADERS

def get_solution_info_from_index(id):
  url = 'http://' + IDX_PAIR + '/solutions/' + id
  data = {}
  try:
    r = requests.get(url)
  except requests.exceptions.RequestException as e:
    # print(e)
    print('Couldnt get solution')
    r = None
  if r and r.status_code == 200:
    data = r.json()
  return data

def index_td_cards(payload):
  url = 'http://' + IDX_PAIR + '/solutions/td-cards'
  resp = {}
  status = 500
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

def get_status_from_index(id):
  url = 'http://' + IDX_PAIR + '/solutions/status/' + id
  data = {}
  try:
    r = requests.get(url)
  except requests.exceptions.RequestException as e:
    # print(e)
    print('Couldnt get status')
    r = None
  if r and r.status_code == 200:
    data = r.json()
  return data