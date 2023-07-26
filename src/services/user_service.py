from flask import jsonify
from sqlalchemy import select, delete
from src.models import db, cb_user, cb_password

class UserNotFoundException(Exception):
  def __init__(self, *args: object, attr: any) -> None:
    super().__init__(*args)
    self.message = 'user ' + str(attr) + ' not found'
  
  def __str__(self) -> str:
    return self.message

class AuthenticationException(Exception):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)
    self.message = 'False credentials :('
  
  def __str__(self) -> str:
    return self.message

class UserService:
  def get_all_users(self):
    try:
      users = db.session.execute(select(cb_user).order_by(cb_user.id)).all()
    except Exception as db_err:
      raise db_err
    finally:
      db.session.close()
    
    return users
  
  def get_user_by_id(self, user_id):
    try:
      user = db.session.execute(db.select(cb_user).filter_by(id = user_id)).one()
    except Exception:
      raise UserNotFoundException(attr = user_id)
    finally:
      db.session.close()
    
    return user
  
  def get_user_by_email(self, user_email):
    try:
      user = db.session.execute(db.select(cb_user).filter_by(email = user_email)).one()
    except Exception:
      raise UserNotFoundException(attr = user_email)
    finally:
      db.session.close()
    
    return user
  
  def add_user(self, user: cb_user):
    newUser = None
    try:
      db.session.add(user)
      db.session.flush()
      
      newUser = user
      
      db.session.commit()
    except Exception as db_err:
      raise db_err
    finally:
      db.session.close()
      
    return newUser
  
  def delete_user(self, user_id):
    try:
      affected_rows = db.session.execute(delete(cb_user).where(cb_user.id == user_id)).rowcount
      
      if affected_rows == 0:
        raise UserNotFoundException(attr = user_id)
      
      db.session.commit()
    except Exception as db_err:
      raise db_err
    finally:
      db.session.close()
    
    return user_id
  
  def authenticate_user(self, email, password):
    try:
      user_password = db.session.execute(select(cb_password).join(cb_user, cb_user.password_id == cb_password.id).where(cb_user.email == email)).first()
      
      if not user_password:
        raise UserNotFoundException(attr = email)
      
      user_password = dict(user_password)
      value = user_password['cb_password'].current_value
      
      if value != password:
        raise AuthenticationException()
    except Exception as ex:
      raise ex
    finally:
      db.session.close()
      
      
    
