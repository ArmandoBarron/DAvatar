from flask import Blueprint, jsonify
from flask_api import status

errors_bp = Blueprint("errors", __name__)

@errors_bp.errorhandler(status.HTTP_404_NOT_FOUND)
def client_error(e):
  return jsonify({'msg': 'Not Found'}), status.HTTP_404_NOT_FOUND

@errors_bp.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def server_error(e):
  print('An error occurred during a request. ', e)
  return jsonify({'msg': 'An internal error occured'}), status.HTTP_500_INTERNAL_SERVER_ERROR