from flask import Blueprint, jsonify, request
from src.services.incident_service import IncidentService
from src.models import cb_incident
import json
from src.responses import SuccessResponse, FailResponse
from src.json_encoder import rowToDict, resultToDict

base_url='/crossbi/v1/api/incident'
incident_controller = Blueprint('incident', __name__, url_prefix=base_url)
incident_service = IncidentService()

@incident_controller.route('/', methods=['GET'])
def getAllDashboards() -> json:
  try:
    workspaces = incident_service.get_incidents()
    
    if len(workspaces) > 0:
      workspaces = rowToDict(workspaces)
  except Exception as ex:
    return FailResponse(message=str(ex)).get_json()

  return SuccessResponse(data=workspaces).get_json()