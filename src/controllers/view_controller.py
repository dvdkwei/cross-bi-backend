from flask import Blueprint, jsonify, request
from src.services.view_service import ViewService
from src.models import cb_view
import json
from src.responses import SuccessResponse, FailResponse
from src.json_encoder import rowToDict, resultToDict, rawResultsToDict
from functools import reduce

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

@view_controller.route('/filter', methods=['GET'])
def filterViews() -> json:
  try:
    workspace_id = request.args.get('workspace_id')
    dashboard_id = request.args.get('dashboard_id')
    view_name = request.args.get('view_name')
    
    if workspace_id and dashboard_id:
      views = view_service.get_views_of_workspace(workspace_id, dashboard_id)
      
      if len(views) > 0:
        views = rowToDict(views)
      else:
        views = []
    
    if view_name:
      views = view_service.get_view_by_name(view_name)

      if views:
        views = resultToDict(views)
        
  except Exception as ex:
    return FailResponse(message=str(ex)).get_json()

  return SuccessResponse(data=views).get_json()

@view_controller.route('/<id>', methods=['GET'])
def getViewById(id) -> json:
  try:
    view = view_service.get_view_by_id(id)
    
    if view:
      view = resultToDict(view)
  except Exception as ex:
    return FailResponse(message=str(ex), status=404).get_json()

  return SuccessResponse(data=view).get_json()

@view_controller.route('/columns', methods=['GET'])
def getColumnsOfAView() -> json:
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

@view_controller.route('/filter', methods=['GET'])
def getViewByName() -> json:
  try:
    view_name = request.args.get('view_name')
    view = view_service.get_view_by_name(view_name)
    
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
        name= req['name'],
        dashboard_id= req['dashboard_id'],
        workspace_id= req['workspace_id'],
        
      )
      
      new_view = view_service.add_view(view)
      new_view = resultToDict(new_view)
  except Exception as ex:
    return FailResponse(message=str(ex)).get_json()

  return SuccessResponse(data=new_view).get_json()

@view_controller.route('/<id>', methods=['PUT'])
def updateView(id) -> json:
  try:
    if request.method == 'PUT':
      req = request.get_json(force=True)
      
      row = view_service.update_view(id, req)
      
      if row:
        row = resultToDict(row)
  except Exception as ex:
    return FailResponse(message=str(ex)).get_json()

  return SuccessResponse(data=row).get_json()

@view_controller.route('/<id>', methods=['DELETE'])
def deleteView(id) -> json:
  try:
    if request.method == 'DELETE':
      deleted_view_id = view_service.delete_view(id)
  except Exception as ex:
    return FailResponse(message=str(ex)).get_json()

  return SuccessResponse(data=deleted_view_id).get_json()

@view_controller.route('/inspect/<id>', methods=['GET'])
def inspectView(id: str):
  try:
    should_categorize = request.args.get('categorize')
    view = view_service.get_view_by_id(id)
    view_details = view_service.inspect_view(id)
    
    if view:
      view = resultToDict(view)
    
    if len(view_details) > 0:
      view_details = rawResultsToDict(view_details)
      
    if should_categorize == 'false':
      data = list(
        map(lambda col: {
            'descriptionTitle': view.x_axis,
            'descriptionValue': col[view.x_axis],
            'valueTitle': view.y_axis,
            'value': col[view.y_axis]
          }, 
          view_details
        )
      )
    else:
      data = {
        'xAxisTitle': view.x_axis,
        'xAxisValue': list(map(lambda detail: detail[view.x_axis], view_details))
      }
      
      filtered_view_details = []
      
      for detail in view_details:
        detail.pop(view.x_axis)
        to_be_appended = []
        keys = detail.keys()
        for key in keys:
          try:
            to_be_appended.append({
              'yAxisTitle': key,
              'yAxisValue': float(detail[key])
            })
          except Exception as ex:
            continue
        filtered_view_details.append(to_be_appended)
      
      data.update({'yAxisData': filtered_view_details})
      
  except Exception as ex:
    return FailResponse(message=str(ex)).get_json()
  
  return SuccessResponse(data=data).get_json()

@view_controller.route('/aggregate/<id>', methods=['GET'])
def aggregateView(id):
  try:
    view = view_service.get_view_by_id(id)
    view_details = view_service.inspect_view(id)
    
    if not view or len(view_details) == 0:
      raise Exception('Data not sufficient for view with id=' + id)
      
    view = resultToDict(view)
    view_details = rawResultsToDict(view_details)
    
    method = view.aggregate
    x_axis = view.x_axis
    y_axis = view.y_axis
    
    if not x_axis or not y_axis:
      raise Exception('False aggregate method for id=' + id)
    
    val_array = list(map(lambda elem: elem[y_axis], view_details))
    if method == 'sum':
      value = reduce(lambda a,b: a+b, val_array)
    elif method == 'count':
      value = len(val_array)
    else:
      value = val_array
    
    if method: 
      data = {
        'valueTitle': method + '_of_' + view.y_axis,
        'value': value
      }
    else:
      data = {
        'valueTitle': view.y_axis,
        'value': value
      }
  except Exception as ex:
    # return FailResponse(message=str(ex)).get_json()
    raise ex
  
  return SuccessResponse(data=data).get_json()