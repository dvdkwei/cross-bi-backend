from flask import Blueprint, jsonify, request
from src.services.user_service import UserService
from src.models import cb_user
import json
from src.responses import SuccessResponse, FailResponse
from src.json_encoder import rowToDict, resultToDict

base_url='/crossbi/v1/api/user'
user_controller = Blueprint('user_controller', __name__, url_prefix=base_url)
user_service = UserService()

@user_controller.route('/', methods=['GET'])
def getAllUsers() -> json:
  try:
    users = user_service.get_all_users()
  except Exception as ex:
    return FailResponse(str(ex)).get_json()
  
  users = rowToDict(users)
  return SuccessResponse(data=users).get_json()

@user_controller.route('/<id>', methods=['GET'])
def getUser(id):
  try:
    user = user_service.get_user_by_id(int(id))
    user = resultToDict(user)
  except Exception as ex:
    return FailResponse(str(ex)).get_json()
  
  return SuccessResponse(data=user).get_json()
  
@user_controller.route('/', methods=['POST'])
def registerUser():
  try:
    if request.method == 'POST':
      req = request.get_json(force=True)
      user = cb_user(
        email = req['email'],
        username = req['username'],
        forename = req['forename'],
        surname = req['surname'],
        company = req['company'],
        password_id = req['password_id']
      )
      
      newUser = user_service.add_user(user)
  except Exception as user_creation_err:
    raise FailResponse(status=404, message=str(user_creation_err)).get_json()
  
  return SuccessResponse(data=newUser).get_json()

@user_controller.route('/<id>', methods=['DELETE'])
def deleteUser(id):
  try:
    if request.method == 'DELETE':
      deleted_user_id = user_service.delete_user(int(id))
  except Exception as user_delete_err:
    return FailResponse(status=404, message=str(user_delete_err)).get_json()
  
  return SuccessResponse(status=204, data={'id': deleted_user_id}).get_json()