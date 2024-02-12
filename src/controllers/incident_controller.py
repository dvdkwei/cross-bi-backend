from flask import Blueprint, request
from src.repositories.incident_repository import IncidentRepository
from src.repositories.pushsubscription_repository import PushSubscriptionRepository
import json
from src.responses import SuccessResponse, FailResponse
from src.json_encoder import rowToDict, resultToDict
from src.models import cb_incident

base_url='/crossbi/v1/api/incidents'
incident_controller = Blueprint('incidents', __name__, url_prefix=base_url)
incident_repository = IncidentRepository()
push_repository = PushSubscriptionRepository()

@incident_controller.route('/', methods=['GET'])
def getAllIncidents() -> json:
  try:
    incidents = incident_repository.get_all()
    
    if len(incidents) > 0:
      incidents = rowToDict(incidents)
  except Exception as ex:
    return FailResponse(message=str(ex)).get_json()

  return SuccessResponse(data=incidents).get_json()

@incident_controller.route('/', methods=['POST'])
def addIncident() -> json:
  try:
    if request.method == 'POST':
      req = request.get_json(force=True)
      
      new_incident = incident_repository.create(cb_incident(
        title = req['title'],
        description = req['description'],
        department = req['department'],
        status = req['status']
      ))
      
      if req['status'] == 0:
        push_repository.trigger_notification(
          title='New Incident ⚡️', 
          body=req['description']
        )
      
  except Exception as ex:
    return FailResponse(message=str(ex)).get_json()

  return SuccessResponse(data=new_incident).get_json()