from flask import Flask, jsonify, Blueprint, request
import logging
import logging.handlers
import os
from flask_cors import CORS
from src.auth import Auth
from src.controllers.meltano_ops import meltano_ops
from src.controllers.user_controller import user_controller


handler = logging.handlers.SysLogHandler(address = '/dev/log')
handler.setFormatter(logging.Formatter('flask [%(levelname)s] %(message)s'))

app = Flask(__name__)
app.logger.addHandler(handler)
app.config.from_object('config.Config')
app.register_blueprint(meltano_ops)
app.register_blueprint(user_controller)
CORS(app)


base_url = '/crossbi/v1/api'

@app.route(base_url + '/')
@Auth.validate_request
def hello():
  return {"Hello": os.environ.get('FLASK_ENV'), "ti": "titit"} 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001, debug=True)