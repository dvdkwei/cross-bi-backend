from flask import request, jsonify
from functools import wraps
from os import environ

class Auth:
  # def validate_request(func):
  #   '''
    
  #   '''
  #   @wraps(func)
  #   def inner(*args, **kwargs):
  #     api_key = request.headers.get('x-api-key')
  #     if not api_key or api_key != environ.get('API_KEY'):
  #       return jsonify(status='401', message='Invalid API Key')
  #     func()
  #     return func(*args, **kwargs)
  #   return inner
  
  @staticmethod
  def validate_request():
    api_key = request.headers.get('x-api-key')
    return api_key == environ.get('API_KEY')