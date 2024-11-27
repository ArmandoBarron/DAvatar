import requests
import json
from .constants import JSON_HEADERS

def do_get(url, timeout=0):
  if url == '':
    return None
  try:
    if timeout > 0:
      r = requests.get(url, timeout=timeout)
    else:
      r = requests.get(url)
    if r != None and r.json():
      return r
  except requests.exceptions.RequestException as e:
    print(e)
  return None

def do_post(url, payload, headers=JSON_HEADERS, timeout=0):
  if url == '':
    return None
  try:
    if timeout > 0:
      r = requests.post(url, data=json.dumps(payload), headers=headers, timeout=timeout)
    else:
      r = requests.post(url, data=json.dumps(payload), headers=headers)
    if r != None and r.json():
      return r
  except requests.exceptions.RequestException as e:
    print(e)
  return None

def do_put(url, payload, headers=JSON_HEADERS, timeout=0):
  if url == '':
    return None
  try:
    if timeout > 0:
      r = requests.put(url, data=json.dumps(payload), headers=headers, timeout=timeout)
    else:
      r = requests.put(url, data=json.dumps(payload), headers=headers)
    if r != None and r.json():
      return r
  except requests.exceptions.RequestException as e:
    print(e)
  return None

def do_delete(url, timeout=0):
  if url == '':
    return None
  try:
    if timeout > 0:
      r = requests.delete(url, timeout=timeout)
    else:
      r = requests.delete(url)
    if r != None and r.json():
      return r
  except requests.exceptions.RequestException as e:
    print(e)
  return None