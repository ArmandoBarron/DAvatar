#!/usr/bin/python3
from flask import Flask
# from api.settings import init_db

app = Flask(__name__)
app.config.from_object('config')

@app.before_first_request
def before_fr():
  # init_db()
  pass

@app.route('/', methods=['GET'])
def index():
  return 'Diagnosis module'

# from api.errors import errors_bp
from api.diagnosis import diagnosis_bp
from api.time_measurement import time_bp

app.register_blueprint(diagnosis_bp)
app.register_blueprint(time_bp)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000)
