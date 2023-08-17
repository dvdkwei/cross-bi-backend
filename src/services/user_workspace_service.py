from sqlalchemy import select, delete
from flask_sqlalchemy import SQLAlchemy
from src.models import cb_user_workspace

db = SQLAlchemy(session_options={'expire_on_commit': False})

class UserWorkspaceNotFoundException(Exception):
  def __init__(self, *args: object, attr: any) -> None:
    super().__init__(*args)
    self.message = 'User workspace relation with ' + str(attr) + ' not found'

class UserWorkspaceService:
  def get_all_user_workspaces():
    try:
      user_workspaces = db.session.execute(select(cb_user_workspace)).all()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
      
    return user_workspaces
  
  def get_user_workspace_by_user_id(self, uid: int):
    try:
      user_workspace = db.session.execute(
        db.select(cb_user_workspace)
          .filter_by(user_id = uid)
      ).all()
    except Exception:
      db.session.remove()
      raise UserWorkspaceNotFoundException(attr = 'user_id=' + str(uid))
    finally:
      db.session.close()
    
    return user_workspace
  
  def get_user_workspace_by_workspace_id(self, wid: int):
    try:
      user_workspace = db.session.execute(
        db.select(cb_user_workspace)
          .filter_by(workspace_id = wid)
      ).all()
    except Exception:
      db.session.remove()
      raise UserWorkspaceNotFoundException(attr = 'user_id=' + str(wid))
    finally:
      db.session.close()
    
    return user_workspace
  
  def add_user_workspace(self, uid: int, wspid: int):
    try:
      newUserWorkspace = cb_user_workspace(
        workspace_id=wspid, 
        user_id=uid
      )
      db.session.add(newUserWorkspace)
      db.session.commit()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
      
    return newUserWorkspace
  
  def delete_user_workspace(self, user_workspace_id):
    try:
      affected_rows = db.session.execute(
        delete(cb_user_workspace)
          .where(cb_user_workspace.id == user_workspace_id)
      ).rowcount
      
      if affected_rows == 0:
        raise UserWorkspaceNotFoundException(attr = user_workspace_id)
      
      db.session.commit()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
    
    return user_workspace_id