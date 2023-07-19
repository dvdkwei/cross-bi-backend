from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from dataclasses import dataclass

Base = declarative_base()

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://root:root@pg_container:5432/postgres'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()

@dataclass
class cb_user(db.Model):
  # __tablename__ = 'cb_user'
  id: int
  email: str
  username: str
  forename: str
  surname: str
  forename: str
  company: str
  password_id: int
    
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(100), nullable=False)
  username = db.Column(db.String(100), nullable=False)
  forename = db.Column(db.String(100), nullable=False)
  surname = db.Column(db.String(100), nullable=False)
  company = db.Column(db.String(100))
  password_id = db.Column(db.Integer, db.ForeignKey('password.id'))
  
  # relationship
  # password = relationship('Password', uselist=False, backref='cb_user')
  
  def __repr__(self):
    return f"<User {self.email}>"
  
@dataclass
class Password(db.Model):
  # __tablename__ = 'cb_password'
  id: int
  current_value: str
  created_at: str
  
  id = db.Column(db.Integer, primary_key=True)
  current_value = db.Column(db.String(150), nullable=False)
  created_at = db.Column(db.DateTime(timezone=True), default=func.now())
  
  def __repr__(self):
    return f"<Password {self.id}>"
