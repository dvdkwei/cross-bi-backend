from flask import Blueprint, jsonify
from src.db import Database
from src.services.user_service import UserService
import os

user_controller = Blueprint('user_controller', __name__)
db = Database()
base_url='/crossbi/v1/api/user'
user_service = UserService()


@user_controller.route(base_url + '/')
def getAllUsers():
  return user_service.get_all_users()

@user_controller.route(base_url + '/<id>')
def getUser(id):
  return user_service.get_user(id)