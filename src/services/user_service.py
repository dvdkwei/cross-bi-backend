from flask import jsonify
from src.models import cb_user

user_table = cb_user

class UserNotFoundException(Exception):
  pass

class UserService:
  def get_all_users(self):
    try:
      users = user_table.query.all()
    except Exception as db_err:
      raise db_err
    
    return jsonify(users)
  
  def get_user_by_id(self, user_id):
    try:
      user = user_table.query.filter_by(id=user_id).first()
    except Exception as db_err:
      raise db_err
    
    if not user:
      raise UserNotFoundException
    
    return jsonify(user)
