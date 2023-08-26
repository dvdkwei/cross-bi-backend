from flask import Blueprint, jsonify, request
from src.services.workspace_service import WorkspaceService
from src.services.user_workspace_service import UserWorkspaceService
from src.models import cb_workspace
import json, os
from src.responses import SuccessResponse, FailResponse
from src.json_encoder import rowToDict, resultToDict
from werkzeug.utils import secure_filename
from flask import current_app

asset_path = 'src/assets'
base_url='/crossbi/v1/api/asset'
asset_controller = Blueprint('asset', __name__, url_prefix=base_url)

@asset_controller.route('/upload', methods=['POST'])
def upload_asset():
  if request.method == 'POST':
    file = request.files['file']
    dashboard_id = json.loads(request.form['body'])['dashboard_id']
    
    if not file:
      return FailResponse(message='No file sent', status=415).get_json()
    
    filename = secure_filename(file.filename)
    
    if filename == '':
      return FailResponse(message='Empty filename', status=415).get_json()
    
    destination_path = os.path.join(
      current_app.root_path, 
      asset_path, 
      dashboard_id
    )
    
    if not os.path.exists(destination_path):
      os.mkdir(destination_path)
    
    new_file_path = os.path.join(
      current_app.root_path, 
      asset_path, 
      dashboard_id, 
      filename
    )
    
    if os.path.exists(new_file_path):
      return FailResponse(
        message='File already exists. Try another endpoint to replace the file.', 
        status=409
      ).get_json()
    
    file.save(new_file_path)
    
    return SuccessResponse().get_json()
    
@asset_controller.route('/update', methods=['POST'])
def update_asset():
  if request.method == 'POST':
    file = request.files['file']
    dashboard_id = json.loads(request.form['body'])['dashboard_id']
    
    if not file:
      return FailResponse(message='No file sent', status=415).get_json()
    
    filename = secure_filename(file.filename)
    
    if filename == '':
      return FailResponse(message='Empty filename', status=415).get_json()
    
    file_path = os.path.join(
      current_app.root_path, 
      asset_path, 
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
    
    