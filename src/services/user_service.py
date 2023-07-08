from src.db import Database
from flask import jsonify
from dataclasses import dataclass, asdict
from json import dumps

db = Database()

@dataclass
class User:
  user_id: str
  email: str
  forename: str
  surname: str
  company: str
  password_id: str
  
  @property
  def __dict__(self):
    return asdict(self)

class UserService:
  def get_all_users(self):
    users: list[User] = []
    try:
      data = db.fetch_table('select * from cb_user')
    except Exception as db_err:
      raise db_err
    
    for user in data:
      obj = User(
        user_id = user[0],
        email = user[1],
        forename = user[2],
        surname = user[3],
        company = user[4],
        password_id = user[5]
      )
      
      users.append(obj.__dict__)
    
    return jsonify({ 'data': users })
  
  def get_user(self, id:int):
    try:
      data = db.fetch_table('select * from cb_user where user_id = ' + id)
      if not data:
        return jsonify({ 'data': None })
      data = data[0]
      user = User(data[0], data[1], data[2], data[3], data[4], data[5])
    except Exception as db_err:
      raise db_err
    
    return jsonify({'data': user.__dict__})