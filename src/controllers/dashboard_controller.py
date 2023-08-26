from flask import Blueprint, jsonify, request
from src.services.workspace_service import WorkspaceService
from src.services.dashboard_service import DashboardService
from src.services.meltano_service import MeltanoService
from src.models import cb_dashboard
import json
from src.responses import SuccessResponse, FailResponse
from src.json_encoder import rowToDict, resultToDict

base_url='/crossbi/v1/api/dashboard'
dashboard_controller = Blueprint('dashboard', __name__, url_prefix=base_url)
workspace_service = WorkspaceService()
dashboard_service = DashboardService()
meltano_service = MeltanoService()

@dashboard_controller.route('/', methods=['GET'])
def getAllDashboards() -> json:
  try:
    workspaces = dashboard_service.get_dashboards()
    
    if len(workspaces) > 0:
      workspaces = rowToDict(workspaces)
  except Exception as ex:
    return FailResponse(message=str(ex)).get_json()

  return SuccessResponse(data=workspaces).get_json()

@dashboard_controller.route('/filter', methods=['GET'])
def getDashboardsByWorkspaceId() -> json:
  try:
    workspace_id = request.args.get('workspace_id')
    
    if not workspace_id:
      return FailResponse('No parameters found').get_json()
    
    dashboards = dashboard_service.filter_dashboards_by_workspace_id(workspace_id)
    
    if len(dashboards) == 0:
      return SuccessResponse(data=[]).get_json()
    
    dashboards = rowToDict(dashboards)
  except Exception as ex:
    return FailResponse(message=str(ex)).get_json()

  return SuccessResponse(data=dashboards).get_json()

@dashboard_controller.route('/', methods=['POST'])
def addDashboard():
  try:
    if request.method == 'POST':
      req = request.get_json(force=True)
      req_name = req['name']
      req_workspace_id = req['workspace_id']
      
      new_dashboard = dashboard_service.add_dashboard(
        cb_dashboard(
          name=req_name, 
          workspace_id=req_workspace_id
        )
      )
      
  except Exception as dashboard_creation_err:
    return FailResponse(status=409, message=str(dashboard_creation_err)).get_json()
  
  return SuccessResponse(data=new_dashboard).get_json()

@dashboard_controller.route('/<id>', methods=['DELETE'])
def deleteDashboard(id):
  try:
    if request.method == 'DELETE':
      deleted_dashboard_id = dashboard_service.delete_dashboard(int(id))
  except Exception as dashboard_delete_err:
    return FailResponse(status=404, message=str(dashboard_delete_err)).get_json()
  
  return SuccessResponse(status=204, data={'id': deleted_dashboard_id}).get_json()

