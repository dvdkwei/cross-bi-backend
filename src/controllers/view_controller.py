from flask import Blueprint, request
from src.repositories.view_repository import ViewRepository
from src.services.view_service import ViewService
from src.models import cb_view
import json
from src.responses import SuccessResponse, FailResponse
from src.json_encoder import rowToDict, resultToDict, rawResultsToDict
from functools import reduce

base_url='/crossbi/v1/api/views'
view_controller = Blueprint('views', __name__, url_prefix=base_url)
view_repository = ViewRepository()
view_service = ViewService()

@view_controller.route('/', methods=['GET'])
def getAllViewsFromDB() -> json:
  try:
    views = view_repository.get_all()
    
    if len(views) > 0:
      views = rowToDict(views)
  except Exception as ex:
    return FailResponse(message=str(ex)).get_json()

  return SuccessResponse(data=views).get_json()

@view_controller.route('/filter', methods=['GET'])
def filterViews() -> json:
  try:
    workspace_id = request.args.get('workspace_id')
    dashboard_id = request.args.get('dashboard_id')
    view_name = request.args.get('view_name')
    
    if workspace_id and dashboard_id:
      views = view_repository.get_views_of_workspace(workspace_id, dashboard_id)
      
      if len(views) > 0:
        views = rowToDict(views)
      else:
        views = []
    
    if view_name:
      views = view_repository.get_view_by_name(view_name)

      if views:
        views = resultToDict(views)
        
  except Exception as ex:
    return FailResponse(message=str(ex)).get_json()

  return SuccessResponse(data=views).get_json()

@view_controller.route('/<id>', methods=['GET'])
def getViewById(id) -> json:
  try:
    view = view_repository.get_by_id(id)
    
    if view:
      view = resultToDict(view)
  except Exception as ex:
    return FailResponse(message=str(ex), status=404).get_json()

  return SuccessResponse(data=view).get_json()

@view_controller.route('/columns', methods=['GET'])
def getColumnsOfAView() -> json:
  try:
    view_name = request.args.get('view_name')
    columns = view_repository.get_columns_of_a_view(view_name)
    
    if len(columns) > 0:
      columns = rowToDict(columns)
  except Exception as ex:
    if 'psycopg2.errors.UndefinedTable' in str(ex):
      return FailResponse(message='View Not Found', status=404).get_json()
    return FailResponse(message=str(ex)).get_json()

  return SuccessResponse(data=columns).get_json()

@view_controller.route('/filter', methods=['GET'])
def getViewByName() -> json:
  try:
    view_name = request.args.get('view_name')
    view = view_repository.get_view_by_name(view_name)
    
    if view:
      view = resultToDict(view)
  except Exception as ex:
    if 'psycopg2.errors.UndefinedTable' in str(ex):
      return FailResponse(message='View Not Found', status=404).get_json()
    return FailResponse(message=str(ex)).get_json()

  return SuccessResponse(data=view).get_json()

@view_controller.route('/', methods=['POST'])
def postView() -> json:
  try:
    if request.method == 'POST':
      req = request.get_json(force=True)
      
      view = cb_view(
        name = req['name'],
        dashboard_id = req['dashboard_id'],
        workspace_id = req['workspace_id'],
        x_axis = req['x_axis'],
        y_axis = req['y_axis'],
        aggregate = req['aggregate'],
        categories = req['categories'],
        title = req['title'],
        updated_at = req['updated_at'],
        date_column = req['date_column']
      )
      
      new_view = view_repository.create(view)
      new_view = resultToDict(new_view)
  except Exception as ex:
    return FailResponse(message=str(ex)).get_json()

  return SuccessResponse(data=new_view).get_json()

@view_controller.route('/<id>', methods=['PUT'])
def updateView(id) -> json:
  try:
    if request.method == 'PUT':
      req = request.get_json(force=True)
      
      row = view_repository.update(id, req)
      
      if row:
        row = resultToDict(row)
  except Exception as ex:
    return FailResponse(message=str(ex)).get_json()

  return SuccessResponse(data=row).get_json()

@view_controller.route('/<id>', methods=['DELETE'])
def deleteView(id) -> json:
  try:
    if request.method == 'DELETE':
      deleted_view_id = view_repository.delete(id)
  except Exception as ex:
    return FailResponse(message=str(ex)).get_json()

  return SuccessResponse(data=deleted_view_id).get_json()

@view_controller.route('/inspect/<id>', methods=['GET'])
def inspectView(id: str):
  try:
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    data = view_service.inspect(id, from_date, to_date)
      
  except Exception as ex:
    return FailResponse(message=str(ex)).get_json()
  
  return SuccessResponse(data=data).get_json()

@view_controller.route('/aggregate/<id>', methods=['GET'])
def aggregateView(id):
  try:
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    data = view_service.aggregate(id, from_date, to_date)
  except Exception as ex:
    return FailResponse(message=str(ex)).get_json()
  
  return SuccessResponse(data=data).get_json()