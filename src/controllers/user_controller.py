from flask import Blueprint, jsonify
from src.services.user_service import UserService

user_controller = Blueprint('user_controller', __name__)
base_url='/crossbi/v1/api/user'
user_service = UserService()

@user_controller.route(base_url + '/')
def getAllUsers():
  return user_service.get_all_users()

@user_controller.route(base_url + '/<id>')
def getUser(id):
  try:
    return user_service.get_user_by_id(id)
  except Exception as ex:
    return jsonify([])