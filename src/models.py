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
  
@dataclass
class cb_workspace(db.Model, Mixin):
  
  id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name: str = db.Column(db.String(75))
  
  def __repr__(self):
    return f"<Workspace {self.id}>"
  
@dataclass
class cb_user_workspace(db.Model, Mixin):
  
  workspace_id: int = db.Column(db.Integer, db.ForeignKey('cb_workspace.id'), primary_key=True)
  user_id: int = db.Column(db.Integer, db.ForeignKey('cb_user.id'), primary_key=True)
  
  def __repr__(self):
    return f"<UserWorkspace {self.id}>"

@dataclass
class cb_dashboard(db.Model, Mixin):
  
  id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name: str = db.Column(db.String(150), nullable=False)
  updated_at: str = db.Column(db.DateTime(timezone=True), default=func.now())
  workspace_id: int = db.Column(db.Integer, db.ForeignKey('cb_workspace.id'))
  
  def __repr__(self):
    return f"<Dashboard {self.id}>"
  
@dataclass
class cb_view(db.Model, Mixin):
  
  id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name: str = db.Column(db.String(200), nullable=False)
  updated_at: str = db.Column(db.DateTime(timezone=True), default=func.now())
  dashboard_id: int = db.Column(db.Integer, db.ForeignKey('cb_dashboard.id'))
  workspace_id: int = db.Column(db.Integer, db.ForeignKey('cb_workspace.id'))
  diagramm_type: int = db.Column(db.Integer, db.ForeignKey('cb_diagramm_type.id'))
  x_axis: str = db.Column(db.String)
  y_axis: str = db.Column(db.String)
  aggregate: str = db.Column(db.String)
  
  def __repr__(self):
    return f"<View {self.id}>"
  
@dataclass
class cb_diagramm_type(db.Model, Mixin):
  
  id: int = db.Column(db.Integer, primary_key=True)
  name: str = db.Column(db.String(200), nullable=True)
  
  def __repr__(self):
    return f"<Diagramm Type {self.id}>"