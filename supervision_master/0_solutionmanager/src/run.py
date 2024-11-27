#!/usr/bin/python3
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')


@app.route('/', methods=['GET'])
def root():
    return 'Solution manager module'

from api.errors import errors_bp
from api.time_measurement import time_bp
from api.manager import mgr_bp
from api.managerv2 import mgrv2_bp

app.register_blueprint(errors_bp)
app.register_blueprint(time_bp)
app.register_blueprint(mgr_bp)
app.register_blueprint(mgrv2_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
