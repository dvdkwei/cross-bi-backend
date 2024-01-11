from flask import Blueprint, jsonify, request
from src.repositories.user_repository import UserRepository
from src.repositories.password_repository import PasswordRepository
from src.repositories.user_workspace_repository import UserWorkspaceRepository
from src.models import cb_user
import json
from src.responses import SuccessResponse, FailResponse
from src.json_encoder import rowToDict, resultToDict

base_url='/crossbi/v1/api/users'
user_controller = Blueprint('user_controller', __name__, url_prefix=base_url)
user_repository = UserRepository()
password_repository = PasswordRepository()
user_workspace_repository = UserWorkspaceRepository()

@user_controller.route('/', methods=['GET'])
def getAllUsers() -> json:
  try:
    users = user_repository.get_all()
    
    if len(users):
      users = rowToDict(users)
  except Exception as ex:
    return FailResponse(message=str(ex)).get_json()

  return SuccessResponse(data=users).get_json()

@user_controller.route('/<id>', methods=['GET'])
def getUser(id):
  try:
    user = user_repository.get_by_id(int(id))
    user = resultToDict(user)
  except Exception as ex:
    return FailResponse(message=str(ex)).get_json()
  
  return SuccessResponse(data=user).get_json()

@user_controller.route('/login', methods=['POST'])
def login():
  try:
    if request.method == 'POST':
      req = request.get_json(force=True)
      email = req['email']
      password = req['password']
      
      user = user_repository.get_by_email(email)    
      password_instance = password_repository.get_by_id(user.cb_user.password_id)
      
      if not password_repository.is_password_valid(password_instance.cb_password.current_value, password):
        raise Exception
      
      user = resultToDict(user)
  except Exception as user_auth_err:
    return FailResponse(status=401, message=str(user_auth_err)).get_json()
  
  return SuccessResponse(data=user).get_json()
  
@user_controller.route('/', methods=['POST'])
async def registerUser():
  try:
    if request.method == 'POST':
      req = request.get_json(force=True)
      
      if user_repository.get_by_email(req['email']):
        raise Exception
      
      pass_id = await password_repository.create(req['password'])
      
      if not pass_id:
        raise Exception
      
      user = cb_user(
        email = req['email'],
        username = req['username'],
        forename = req['forename'],
        surname = req['surname'],
        company = req['company'],
        password_id = pass_id
      )
      
      newUser = user_repository.create(user)
  except Exception as user_creation_err:
    return FailResponse(status=409, message=str(user_creation_err)).get_json()
  
  return SuccessResponse(data=newUser).get_json()

@user_controller.route('/<id>', methods=['DELETE'])
def deleteUser(id):
  try:
    if request.method == 'DELETE':
      deleted_user_id = user_repository.delete(int(id))
  except Exception as user_delete_err:
    return FailResponse(status=404, message=str(user_delete_err)).get_json()
  
  return SuccessResponse(status=204, data={'id': deleted_user_id}).get_json()