from flask import Blueprint
from src.repositories.incident_repository import IncidentRepository
import json
from src.responses import SuccessResponse, FailResponse
from src.json_encoder import rowToDict, resultToDict

base_url='/crossbi/v1/api/incidents'
incident_controller = Blueprint('incidents', __name__, url_prefix=base_url)
incident_repository = IncidentRepository()

@incident_controller.route('/', methods=['GET'])
def getAllIncidents() -> json:
  try:
    incidents = incident_repository.get_all()
    
    if len(incidents) > 0:
      incidents = rowToDict(incidents)
  except Exception as ex:
    return FailResponse(message=str(ex)).get_json()

  return SuccessResponse(data=incidents).get_json()