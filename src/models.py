from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

db = SQLAlchemy(session_options={'expire_on_commit': False})

class Mixin(object):
  __abstract__ = True
  
  def asdict(self):
    dict_ = {}
    for key in self.__dict__.keys():
      if key != '_sa_instance_state':
        dict_[key] = getattr(self, key)
    return dict_ 

@dataclass
class cb_user(db.Model, Mixin):
    
  id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
  email: str = db.Column(db.String(100), nullable=False)
  username: str = db.Column(db.String(100), nullable=False)
  forename: str = db.Column(db.String(100), nullable=False)
  surname: str = db.Column(db.String(100), nullable=False)
  company: str = db.Column(db.String(100))
  password_id: int = db.Column(db.Integer, db.ForeignKey('cb_password.id'))
  
  def __repr__(self):
    return dict(self)
  
@dataclass
class cb_password(db.Model, Mixin):
  
  id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
  current_value: str = db.Column(db.String(150), nullable=False)
  created: str = db.Column(db.DateTime(timezone=True), default=func.now())
  
  def __repr__(self):
    return f"<Password {self.id}>"
