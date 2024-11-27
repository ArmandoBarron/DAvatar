from flask import Blueprint, jsonify
from flask_api import status

errors_bp = Blueprint("errors", __name__)

@errors_bp.errorhandler(status.HTTP_404_NOT_FOUND)
def client_error(e):
    return jsonify({'msg': 'Not Found'}), status.HTTP_404_NOT_FOUND