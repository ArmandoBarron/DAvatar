#!/usr/bin/python3
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

@app.route('/', methods=['GET'])
def index():
    return 'Representation module'

from api.errors import errors_bp
from api.representation import rep_bp
from api.time_measurement import time_bp

app.register_blueprint(errors_bp)
app.register_blueprint(rep_bp)
app.register_blueprint(time_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
