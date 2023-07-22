from flask import jsonify
from sqlalchemy import select, delete
from src.models import db, cb_user

class UserNotFoundException(Exception):
  def __init__(self, *args: object, id: int) -> None:
    super().__init__(*args)
    self.message = 'user with id: ' + str(id) + ' is not found'
  
  def __str__(self) -> str:
    return self.message
  pass

class UserService:
  def get_all_users(self):
    try:
      users = db.session.execute(select(cb_user).order_by(cb_user.id)).all()
    except Exception as db_err:
      raise db_err
    
    return users
  
  def get_user_by_id(self, user_id):
    try:
      user = db.session.execute(db.select(cb_user).filter_by(id = user_id)).one()
    except Exception:
      raise UserNotFoundException(id = user_id)
    
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
    
    return newUser
  
  def delete_user(self, user_id):
    try:
      affected_rows = db.session.execute(delete(cb_user).where(cb_user.id == user_id)).rowcount
      
      if affected_rows == 0:
        raise UserNotFoundException(id = user_id)
      
      db.session.commit()
    except Exception as db_err:
      raise db_err
    
    return user_id
      
      
    
