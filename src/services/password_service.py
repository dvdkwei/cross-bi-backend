from src.models import db, cb_password
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import select, delete
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={'expire_on_commit': False})

class PasswordService():
  def get_password(self, pass_id):
    try:
      password = db.session.execute(select(cb_password).filter_by(id = pass_id)).one()
    except Exception as pass_not_found:
      db.session.remove()
      raise pass_not_found
    finally:
      db.session.close()

    return password
  
  async def add_password(self, password: str):
    id = 0
    try:
      if type(password) is not str:
        password = str(password)
        
      pass_instance = cb_password(current_value = generate_password_hash(password, method='sha256'))
      db.session.add(pass_instance)
      db.session.flush()
      
      id = pass_instance.id
      
      db.session.commit()
    except Exception as create_pass_err:
      db.session.remove()
      raise create_pass_err
    finally:
      db.session.close()
    
    return id
  
  def is_password_valid(self, hashed, raw_password):
    return check_password_hash(hashed, raw_password)
  
  async def delete_password(self, pass_id: int):
    try:
      affected_rows = db.session.execute(delete(cb_password).filter_by(id = pass_id)).rowcount
      
      if affected_rows == 0:
        raise Exception
      
      db.session.commit()
    except Exception as delete_pass_err:
      db.session.remove()
      raise delete_pass_err
    finally:
      db.session.close()
      
    return pass_id