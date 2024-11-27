#!/usr/bin/python3
from flask import Flask, jsonify
from api.metrics import fill_active_hosts_list

app = Flask(__name__)
app.config.from_object('config')

@app.before_first_request
def before_first_req_fun():
    fill_active_hosts_list()

@app.route('/', methods=['GET'])
def home():
  return jsonify({'msg': 'Monitoring module'})

from api.errors import errors_bp
from api.metrics import metrics_bp
from api.monitor import monitor_bp
from api.time_measurement import time_bp

app.register_blueprint(errors_bp)
app.register_blueprint(metrics_bp)
app.register_blueprint(monitor_bp)
app.register_blueprint(time_bp)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
