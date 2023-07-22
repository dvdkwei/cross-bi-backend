from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

db = SQLAlchemy()

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
  password_id: int = db.Column(db.Integer, db.ForeignKey('password.id'))
  
  # relationship
  # password = relationship('Password', uselist=False, backref='cb_user')
  
  def __repr__(self):
    return dict(self)
  
@dataclass
class Password(db.Model, Mixin):
  
  id: int = db.Column(db.Integer, primary_key=True)
  current_value: str = db.Column(db.String(150), nullable=False)
  created_at: str = db.Column(db.DateTime(timezone=True), default=func.now())
  
  def __repr__(self):
    return f"<Password {self.id}>"
