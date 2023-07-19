from flask import Flask, jsonify, Blueprint, request
import os
from src.auth import Auth
from context import create_app

app = create_app()

base_url = '/crossbi/v1/api'

@app.before_request
def is_authenticated():
  if not Auth.validate_request():
    return jsonify(status='401', message='Invalid API Key')

@app.route(base_url + '/')
def hello():
  return {"Hello": os.environ.get('FLASK_ENV'), "ti": "titit"} 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001, debug=True)