#!/usr/bin/python3
from flask import Flask, request, jsonify, render_template, redirect
from flask.helpers import send_file
from flask.json import dumps
import requests
# import simplejson as json
# import os
# import sys
# import time
# import datetime
# from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config.from_object('config')
endpoints = {
  "monitor": {
    "name": "http://monitoring:5000",
    "endpoint": "/hosts"
  },
  "index": {
    "name": "http://indexing:5000",
    "endpoint": "/solutions"
  }
}



### routes for web page ###

@app.route('/')
def home():
  return render_template('index.html')

# @app.route('/infrastructure')
# def infrastructure():
#     return render_template('infrastructure.html')

@app.route('/solutions')
def solutions():
  return render_template('solutions.html')

@app.route('/load')
def load():
  return render_template('new-solution.html')

@app.route('/status/<string:solution>')
def status(solution):
  return render_template('status.html', solution=solution)



### routes for backend ###

@app.route('/getsolutions', methods=['GET'])
def getSolutions():
  try:
    url = endpoints['index']['name'] + endpoints['index']['endpoint']
    res = requests.get(url, timeout=10)
  except requests.exceptions.RequestException as e:
    print(e)
    res = None
  status = (res.status_code if res != None and res.status_code else 500)
  if status == 200:
    rj = res.json()
    return jsonify(rj)
  else:
    return jsonify({'error': 'Sorry, solutions aren\'t available at this time.'})

@app.route('/upload-file', methods=['POST'])
def upload_image():
  flag = 0
  if request.method == 'POST':
    # print(request.json)
    # print(request.form)
    if 'ymlFile' in request.files:
      print('there are files')
      flag = 1
      # send file to manager 
      url = 'http://solution_mgr:5000/api/v2/solutions'
      f = request.files['ymlFile']
      f.seek(0)
      # r = requests.post(url, data={"mysubmit":"Go"}, files={"file": file})
      params = {'monitor_interval': request.form.get('monitor_interval'), 'aggregates_interval': request.form.get('aggregates_interval')}
      send_file = {"file": (f.filename, f.stream, f.mimetype)}
      r = requests.post(url, data=params, files=send_file)
      print('r: ', r)
  return jsonify({'msg': flag})

@app.route('/getstructure/<string:solution>', methods=['GET'])
def getStructure(solution):
  url = 'http://representation:5000/model/structure/' + solution
  try:
    r = requests.get(url)
  except requests.exceptions.RequestException as e:
    print(e)
    r = None
  status = (r.status_code if r != None and r.status_code else 500)
  if status == 200:
    rj = r.json()
    return jsonify(rj)
  return jsonify({'msj': 'Error'}), status

@app.route('/solutions/<string:solution>/status/<string:interval>/<string:cores>', methods=['GET'])
def getStatus(solution, interval, cores):
  endpoint = 'v2/aggregates/' + solution + '/END/' + interval + '/' + cores + '/status-1m-' + solution
  url = 'http://diagnosis:5000/' + endpoint
  try:
    r = requests.get(url)
  except requests.exceptions.RequestException as e:
    print(e)
    r = None
  status = (r.status_code if r != None and r.status_code else 500)
  if status == 200:
    rj = r.json()
    return jsonify(rj)
  return jsonify({'msj': 'Error'}), status

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
