from sqlalchemy import select, delete
from src.models import cb_workspace
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={'expire_on_commit': False})

class WorkspaceNotFoundException(Exception):
  def __init__(self, *args: object, attr: any) -> None:
    super().__init__(*args)
    self.message = 'Workspace ' + str(attr) + ' not found'
  
  def __str__(self) -> str:
    return self.message

class WorkspaceService:
  def get_workspaces(self):
    try:
      workspaces = db.session.execute(select(cb_workspace).order_by(cb_workspace.id)).all()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
      
    return workspaces
  
  def filter_workspaces_by_id(self, id: set):
    try:
      workspaces = db.session.execute(select(cb_workspace).filter(cb_workspace.id.in_(id))).all()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
      
    return workspaces
  
  def get_workspace_by_id(self, wsp_id):
    try:
      workspace = db.session.execute(db.select(cb_workspace).filter_by(id = wsp_id)).one()
    except Exception:
      db.session.remove()
      raise WorkspaceNotFoundException(attr = wsp_id)
    finally:
      db.session.close()
      
    return workspace
  
  def add_workspace(self, new_wsp: cb_workspace):
    newWorkspace = None
    try:
      db.session.add(new_wsp)
      db.session.flush()
      
      newWorkspace = new_wsp
      
      db.session.commit()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
      
    return newWorkspace
  
  def delete_workspace(self, worskpace_id):
    try:
      affected_rows = db.session.execute(
        delete(cb_workspace)
          .where(cb_workspace.id == worskpace_id)
      ).rowcount
      
      if affected_rows == 0:
        raise WorkspaceNotFoundException(attr = worskpace_id)
      
      db.session.commit()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
    
    return worskpace_id