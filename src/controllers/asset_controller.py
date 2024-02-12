from flask import Blueprint, request
import json, os
from src.responses import SuccessResponse, FailResponse
from src.json_encoder import rowToDict, resultToDict
from werkzeug.utils import secure_filename
from flask import current_app
from flask_cors import cross_origin

base_url='/crossbi/v1/api/assets'
asset_controller = Blueprint('assets', __name__, url_prefix=base_url)

@asset_controller.route('/upload', methods=['POST'])
@cross_origin(origins='*', methods=['POST'])
def upload_asset() -> json:
  if request.method == 'POST':
    try:
      assets_path = current_app.config['ASSETS_PATH']
      file = request.files['file']
      workspace_id = json.loads(request.form['body'])['workspace_id']
      
      if not file:
        return FailResponse(message=str(request), status=415).get_json()
      
      filename = secure_filename(file.filename)
      
      if filename == '':
        return FailResponse(message='Empty filename', status=415).get_json()
      
      destination_path = os.path.join(
        current_app.root_path, 
        assets_path, 
        workspace_id
      )
      
      if not os.path.exists(destination_path):
        os.mkdir(destination_path)
      
      new_file_path = os.path.join(
        current_app.root_path, 
        assets_path, 
        workspace_id, 
        filename
      )
      
      if os.path.exists(new_file_path):
        return FailResponse(
          message='File already exists, nothing uploaded', 
          status=409
        ).get_json()
      
      file.save(new_file_path)
    except Exception as ex:
      return FailResponse(message=str(ex), status=400).get_json()
      
    return SuccessResponse().get_json()
    
    
@asset_controller.route('/update', methods=['POST'])
def update_asset():
  if request.method == 'POST':
    assets_path = current_app.config['ASSETS_PATH']
    file = request.files['file']
    dashboard_id = json.loads(request.form['body'])['dashboard_id']
    
    if not file:
      return FailResponse(message='No file sent', status=415).get_json()
    
    filename = secure_filename(file.filename)
    
    if filename == '':
      return FailResponse(message='Empty filename', status=415).get_json()
    
    file_path = os.path.join(
      current_app.root_path, 
      assets_path, 
      dashboard_id, 
      filename
    )
    
    if not os.path.exists(file_path):
      return FailResponse(
        message='File not found.', 
        status=404
      ).get_json()
    
    os.remove(file_path)
    file.save(file_path)
    
    return SuccessResponse().get_json()
    
    