from flask import Blueprint, jsonify, request
from src.services.view_service import ViewService
from src.models import cb_dashboard
import json
from src.responses import SuccessResponse, FailResponse
from src.json_encoder import rowToDict, resultToDict

base_url='/crossbi/v1/api/view'
view_controller = Blueprint('view', __name__, url_prefix=base_url)
view_service = ViewService()

@view_controller.route('/', methods=['GET'])
def getAllViewsFromDB() -> json:
  try:
    views = view_service.get_all_views()
    
    if len(views) > 0:
      views = rowToDict(views)
  except Exception as ex:
    return FailResponse(message=str(ex)).get_json()

  return SuccessResponse(data=views).get_json()

@view_controller.route('/<workspace_id>', methods=['GET'])
def getAllViewsOfWorkspace(workspace_id) -> json:
  try:
    views = view_service.get_views_of_workspace(workspace_id)
  except Exception as ex:
    return FailResponse(message=str(ex)).get_json()

  return SuccessResponse(data=views).get_json()

@view_controller.route('/columns', methods=['GET'])
def getColumnsOfAWorkspace() -> json:
  try:
    view_name = request.args.get('view_name')
    columns = view_service.get_columns_of_a_view(view_name)
    
    if len(columns) > 0:
      columns = rowToDict(columns)
  except Exception as ex:
    if 'psycopg2.errors.UndefinedTable' in str(ex):
      return FailResponse(message='View Not Found', status=404).get_json()
    return FailResponse(message=str(ex)).get_json()

  return SuccessResponse(data=columns).get_json()