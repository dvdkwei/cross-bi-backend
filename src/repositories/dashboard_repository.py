from sqlalchemy import select, delete
from src.models import cb_dashboard
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={'expire_on_commit': False})

class DashboardNotFoundException(Exception):
  def __init__(self, *args: object, attr: any) -> None:
    super().__init__(*args)
    self.message = 'Dashboard ' + str(attr) + ' not found'
  
  def __str__(self) -> str:
    return self.message

class DashboardRepository:
  def get_dashboards(self):
    try:
      dashboards = db.session.execute(
        select(cb_dashboard).order_by(cb_dashboard.id)
      ).all()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
    
    return dashboards
  
  def filter_dashboards_by_workspace_id(self, id: set):
    try:
      dashboards = db.session.execute(
        select(cb_dashboard)
          .filter(cb_dashboard.workspace_id == id)
      ).all()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
      
    return dashboards
  
  def get_dashboard_by_id(self, dashboard_id):
    try:
      dashboard = db.session.execute(db.select(cb_dashboard).filter_by(id = dashboard_id)).one()
    except Exception:
      db.session.remove()
      raise DashboardNotFoundException(attr = dashboard_id)
    finally:
      db.session.close()
      
    return dashboard
  
  def add_dashboard(self, new_dashboard: cb_dashboard):
    newDashboard = None
    try:
      db.session.add(new_dashboard)
      db.session.flush()
      
      newDashboard = new_dashboard.asdict()
      
      db.session.commit()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
    
    return newDashboard
  
  def delete_dashboard(self, dashboard_id):
    try:
      affected_rows = db.session.execute(
        delete(cb_dashboard)
          .where(cb_dashboard.id == dashboard_id)
      ).rowcount
      
      if affected_rows == 0:
        raise DashboardNotFoundException(attr = dashboard_id)
      
      db.session.commit()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
    
    return dashboard_id