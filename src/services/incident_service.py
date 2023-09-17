from sqlalchemy import select, delete, update
from src.models import cb_incident
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy(session_options={'expire_on_commit': False})

class IncidentNotFoundException(Exception):
  def __init__(self, *args: object, attr: any) -> None:
    super().__init__(*args)
    self.message = 'Incident ' + str(attr) + ' not found'
  
  def __str__(self) -> str:
    return self.message

class IncidentService:
  def get_incidents(self):
    try:
      incidents = db.session.execute(
        select(cb_incident).order_by(cb_incident.id)
      ).all()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
    
    return incidents
  
  def get_incident_by_id(self, incident_id):
    try:
      incident = db.session.execute(
        db.select(cb_incident)
            .filter_by(id = incident_id)
      ).one()
      
    except Exception:
      db.session.remove()
      raise IncidentNotFoundException(attr = incident_id)
    finally:
      db.session.close()
      
    return incident
  
  def add_incident(self, new_incident: cb_incident):
    incident = None
    try:
      db.session.add(new_incident)
      db.session.flush()
      
      incident = new_incident.asdict()
      
      db.session.commit()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
    
    return incident
  
  def update_incident(self, incident_id: str, incident_obj: json):
    try:      
      db.session.execute(
        update(cb_incident)
          .where(cb_incident.id == incident_id)
          .values(
            title = incident_obj['title'],
            timestamp = incident_obj['timestamp'],
            description = incident_obj['description'],
            department = incident_obj['department'],
            status = incident_obj['status']
          )
      )
      
      db.session.commit()
      
      updated_incident = self.get_incident_by_id(incident_id)
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
      
    return updated_incident