from sqlalchemy import select, delete, update
from src.models import cb_user, cb_password
from .abstract_repository import IRepository, db

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

class UserRepository(IRepository):
  def get_all(self):
    try:
      users = db.session.execute(select(cb_user).order_by(cb_user.id)).all()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
    
    return users
  
  def get_by_id(self, user_id):
    try:
      user = db.session.execute(db.select(cb_user).filter_by(id = user_id)).one()
    except Exception:
      raise UserNotFoundException(attr = user_id)
    finally:
      db.session.remove()
      db.session.close()
    
    return user
  
  def get_by_email(self, user_email):
    try:
      user = db.session.execute(db.select(cb_user).filter_by(email = user_email)).one()
    except Exception:
      return None
    finally:
      db.session.remove()
      db.session.close()
    
    return user
  
  def create(self, user: cb_user):
    newUser = None
    try:
      db.session.add(user)
      db.session.flush()
      
      newUser = user
      
      db.session.commit()
    except Exception as db_err:
      raise db_err
    finally:
      db.session.remove()
      db.session.close()
      
    return newUser
  
  def update(self, user_id: str, updated_user: cb_user):
    try:      
      db.session.execute(
        update(cb_user)
          .where(cb_user.id == user_id)
          .values(
            current_value = updated_user['current_value'],
            created = updated_user['created'],
          )
      )
      
      db.session.commit()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
      
    return updated_user
  
  def delete(self, user_id):
    try:
      affected_rows = db.session.execute(
        delete(cb_user).where(cb_user.id == user_id)
      ).rowcount
      
      if affected_rows == 0:
        raise UserNotFoundException(attr = user_id)
      
      db.session.commit()
    except Exception as db_err:
      db.session.remove()
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
      db.session.remove()
      raise ex
    finally:
      db.session.close()