from flask_sqlalchemy import SQLAlchemy
from flask import current_app
import os

db = SQLAlchemy(session_options={'expire_on_commit': False})

class ViewService():
  def get_all_views(self):
    try:
      views = db.session.execute(
        "select table_name from INFORMATION_SCHEMA.views "
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
  
  def get_views_of_workspace(self, workspace_id: str):
    try:
      views = os.listdir(os.path.join(
        current_app.root_path, 
        'transform/models',
        workspace_id,
        'marts'
      ))
      
      views = list(map(lambda x: x.removesuffix('.sql'), views))
    except Exception as file_err:
      raise file_err
    
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