from flask import Blueprint, jsonify, request
from src.services.workspace_service import WorkspaceService
from src.services.user_workspace_service import UserWorkspaceService
from src.models import cb_workspace
import json
from src.responses import SuccessResponse, FailResponse
from src.json_encoder import rowToDict, resultToDict

base_url='/crossbi/v1/api/workspace'
workspace_controller = Blueprint('workspace', __name__, url_prefix=base_url)
workspace_service = WorkspaceService()
user_workspace_service = UserWorkspaceService()

@workspace_controller.route('/', methods=['GET'])
def getAllWorkspaces() -> json:
  try:
    workspaces = workspace_service.get_workspaces()
    
    if len(workspaces) > 0:
      workspaces = rowToDict(workspaces)
  except Exception as ex:
    return FailResponse(str(ex)).get_json()

  return SuccessResponse(data=workspaces).get_json()

@workspace_controller.route('/filter', methods=['GET'])
def getWorkspacesByUserId() -> json:
  try:
    user_id = request.args.get('user_id')
    
    if not user_id:
      return FailResponse('No parameters found').get_json()
    
    mapped_workspaces = user_workspace_service.get_user_workspace_by_user_id(user_id)
    
    if len(mapped_workspaces) == 0:
      return SuccessResponse(data=[]).get_json()
    
    workspace_ids = set(map(lambda workspace: workspace.workspace_id, rowToDict(mapped_workspaces)))
    workspaces = workspace_service.filter_workspaces_by_id(workspace_ids)
    workspaces = rowToDict(workspaces)
  except Exception as ex:
    return FailResponse(str(ex)).get_json()

  return SuccessResponse(data=workspaces).get_json()

@workspace_controller.route('/<id>', methods=['GET'])
def getWorkspace(id):
  try:
    workspace = workspace_service.get_workspace_by_id(int(id))
    workspace = resultToDict(workspace)
  except Exception as ex:
    return FailResponse(str(ex)).get_json()
  
  return SuccessResponse(data=workspace).get_json()
  
@workspace_controller.route('/', methods=['POST'])
def addWorkspace():
  try:
    if request.method == 'POST':
      req = request.get_json(force=True)
      wsp_name = req['name']
      newWorkspace = workspace_service.add_workspace(cb_workspace(name=wsp_name))
  except Exception as workspace_creation_err:
    return FailResponse(status=409, message=str(workspace_creation_err)).get_json()
  
  return SuccessResponse(data=newWorkspace).get_json()

@workspace_controller.route('/<id>', methods=['DELETE'])
def deleteWorkspace(id):
  try:
    if request.method == 'DELETE':
      deleted_workspace_id = workspace_service.delete_workspace(int(id))
  except Exception as workspace_delete_err:
    return FailResponse(status=404, message=str(workspace_delete_err)).get_json()
  
  return SuccessResponse(status=204, data={'id': deleted_workspace_id}).get_json()

@workspace_controller.route('/assign', methods=['POST'])
def assignWorkspace():
  try:
    if request.method == 'POST':
      req = request.get_json(force=True)
      wsp_id = req['workspace_id']
      user_id = req['user_id']
      
      newWorkspace = user_workspace_service.add_user_workspace(user_id, wsp_id)
  except Exception as user_creation_err:
    return FailResponse(status=409, message=str(user_creation_err)).get_json()
  
  return SuccessResponse(data=newWorkspace).get_json()