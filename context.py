from flask import Flask, jsonify, Blueprint, request
from flask_sqlalchemy import SQLAlchemy
import logging
import logging.handlers
from os import environ
from flask_cors import CORS
from src.controllers.user_controller import user_controller
from src.controllers.workspace_controller import workspace_controller
from src.controllers.asset_controller import asset_controller
from src.controllers.dashboard_controller import dashboard_controller

handler = logging.handlers.SysLogHandler(address = '/dev/log')
handler.setFormatter(logging.Formatter('flask [%(levelname)s] %(message)s'))

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def create_app():
  db.init_app(app)
  app.logger.addHandler(handler)
  app.config.from_object('config.Config')
  
  with app.app_context():
    app.register_blueprint(user_controller)
    app.register_blueprint(workspace_controller)
    app.register_blueprint(asset_controller)
    app.register_blueprint(dashboard_controller)
  
  return app