from flask import Flask, jsonify, Blueprint, request
from flask_sqlalchemy import SQLAlchemy
import logging
import logging.handlers
from os import environ
from flask_cors import CORS
from src.controllers.meltano_controller import meltano_controller
from src.controllers.user_controller import user_controller

handler = logging.handlers.SysLogHandler(address = '/dev/log')
handler.setFormatter(logging.Formatter('flask [%(levelname)s] %(message)s'))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def create_app():
  CORS(app)
  db.init_app(app)
  app.logger.addHandler(handler)
  app.config.from_object('config.Config')
  
  with app.app_context():
    app.register_blueprint(meltano_controller)
    app.register_blueprint(user_controller)
  
  return app