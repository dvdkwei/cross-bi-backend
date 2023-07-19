from flask import Flask, jsonify, Blueprint, request
from flask_sqlalchemy import SQLAlchemy
import logging
import logging.handlers
from flask_cors import CORS
from src.controllers.meltano_ops import meltano_ops
from src.controllers.user_controller import user_controller

handler = logging.handlers.SysLogHandler(address = '/dev/log')
handler.setFormatter(logging.Formatter('flask [%(levelname)s] %(message)s'))

app = Flask(__name__)
db = SQLAlchemy(app)

def create_app():
  CORS(app)
  db.init_app(app)
  app.logger.addHandler(handler)
  app.config.from_object('config.Config')
  app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://root:root@pg_container:5432/postgres'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  
  with app.app_context():
    app.register_blueprint(meltano_ops)
    app.register_blueprint(user_controller)
  
  return app