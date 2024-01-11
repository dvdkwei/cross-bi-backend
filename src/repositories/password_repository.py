from src.models import cb_password
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import select, delete, update
from.abstract_repository import IRepository, db

class PasswordRepository(IRepository):
  def get_all(self):
    try:
      passwords = db.session.execute(
        select(cb_password).order_by(cb_password.id)
      ).all()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
    
    return passwords
  
  def get_by_id(self, pass_id):
    try:
      password = db.session.execute(select(cb_password).filter_by(id = pass_id)).one()
    except Exception as pass_not_found:
      db.session.remove()
      raise pass_not_found
    finally:
      db.session.close()

    return password
  
  async def create(self, password: str):
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
  
  def update(self, pass_id: str, new_password: cb_password):
    try:      
      db.session.execute(
        update(cb_password)
          .where(cb_password.id == pass_id)
          .values(
            current_value = new_password['current_value'],
            created = new_password['created'],
          )
      )
      
      db.session.commit()
      
      updated_password = self.get_by_id(pass_id)
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
      
    return updated_password
  
  async def delete(self, pass_id: int):
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