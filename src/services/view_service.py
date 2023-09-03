from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from src.models import cb_view, cb_dashboard
from sqlalchemy import select, delete, update
import os, json

db = SQLAlchemy(session_options={'expire_on_commit': False})

class ViewNotFoundException(Exception):
  def __init__(self, *args: object, attr: any) -> None:
    super().__init__(*args)
    self.message = 'user ' + str(attr) + ' not found'
  
  def __str__(self) -> str:
    return self.message

class ViewService():
  def get_all_views(self):
    try:
      views = db.session.execute(
        "SELECT table_name FROM INFORMATION_SCHEMA.views "
        "WHERE table_schema = ANY (current_schemas(false)) "
        "AND table_name not like 'stg_%' "
        "AND table_name not like 'int_%'"
      ).all()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
    
    return views
  
  def get_views_of_workspace(self, workspace_id: str, dashboard_id: str):
    try:
      # views_sqls = os.listdir(os.path.join(
      #   current_app.root_path, 
      #   'transform/models',
      #   workspace_id,
      #   'marts'
      # ))
      
      # views_sqls = list(map(lambda x: x.removesuffix('.sql'), views_sqls))
      
      views = db.session.execute(
        select(cb_view)
          .filter(cb_view.workspace_id == workspace_id)
          .filter(cb_view.dashboard_id == dashboard_id)
      ).all()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
    
    return views
  
  def get_columns_of_a_view(self, view_name):
    try:
      columns = db.session.execute(
        "SELECT attname AS columns "
        "FROM pg_attribute " 
        "WHERE  attrelid = '"+ view_name + 
        "'::regclass "
        "ORDER BY attnum"
      ).all()
    except Exception as file_err:
      raise file_err
    
    return columns
  
  def get_view_by_id(self, id: int):
    try:
      view = db.session.execute(
        select(cb_view).filter(cb_view.id == id)
      ).one()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
    
    return view
  
  def get_view_by_name(self, view_name: str):
    try:
      view = db.session.execute(
        select(cb_view).filter(cb_view.name == view_name)
      ).one()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
    
    return view
  
  def add_view(self, view: cb_view):
    try:
      db.session.add(view)
      db.session.flush()
      new_view = cb_view
      db.session.commit()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
    
    return new_view
  
  def delete_view(self, view_id: str):
    try:
      affected_rows = db.session.execute(
        delete(cb_view).where(cb_view.id == view_id)
      ).rowcount
      
      if affected_rows == 0:
        raise ViewNotFoundException(attr = view_id)
      
      db.session.commit()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
    
    return view_id
  
  def inspect_view(self, id: str):
    try:
      view_name = self.get_view_by_id(id)._asdict()['cb_view'].name
      
      rows = db.session.execute(
        'select * from ' + view_name
      ).all()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
    
    return rows
  
  def update_view(self, view_id: str, view_obj: json):
    try:      
      db.session.execute(
        update(cb_view)
          .where(cb_view.id == view_id)
          .values(
            name = view_obj['name'],
            updated_at = view_obj['updated_at'],
            dashboard_id= view_obj['dashboard_id'],
            workspace_id= view_obj['workspace_id'],
            diagramm_type= view_obj['diagramm_type'],
            x_axis = view_obj['x_axis'],
            y_axis = view_obj['y_axis'],
            aggregate = view_obj['aggregate']
          )
      )
      
      db.session.commit()
      
      row = self.get_view_by_id(view_id)
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
      
    return row