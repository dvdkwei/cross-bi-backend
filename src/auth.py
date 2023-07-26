from flask import request
from os import environ

class Auth:
  @staticmethod
  def validate_request():
    """Validates every coming in request, proving
        the availability of the X-API-KEY header
    
    """
    api_key = request.headers.get('x-api-key')
    return api_key == environ.get('API_KEY')