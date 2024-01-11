from sqlalchemy import select, delete, update
from src.models import cb_workspace
from .abstract_repository import IRepository, db

class WorkspaceNotFoundException(Exception):
  def __init__(self, *args: object, attr: any) -> None:
    super().__init__(*args)
    self.message = 'Workspace ' + str(attr) + ' not found'
  
  def __str__(self) -> str:
    return self.message

class WorkspaceRepository(IRepository):
  def get_all(self):
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
  
  def get_by_id(self, wsp_id):
    try:
      workspace = db.session.execute(db.select(cb_workspace).filter_by(id = wsp_id)).one()
    except Exception:
      db.session.remove()
      raise WorkspaceNotFoundException(attr = wsp_id)
    finally:
      db.session.close()
      
    return workspace
  
  def create(self, new_wsp: cb_workspace):
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
  
  def update(self, wsp_id: str, new_wsp: cb_workspace):
    try:      
      db.session.execute(
        update(cb_workspace)
          .where(cb_workspace.id == wsp_id)
          .values(
            name = new_wsp['name']
          )
      )
      
      db.session.commit()
      
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
      
    return new_wsp
  
  def delete(self, worskpace_id):
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