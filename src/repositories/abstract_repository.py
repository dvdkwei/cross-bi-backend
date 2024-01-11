from flask_sqlalchemy import SQLAlchemy
from abc import ABC, abstractmethod

db = SQLAlchemy(session_options={'expire_on_commit': False})

class IRepository(ABC):
  @abstractmethod
  def get_all(self):
    raise NotImplementedError
  
  @abstractmethod
  def get_by_id(self, id):
    raise NotImplementedError
  
  @abstractmethod
  def create(self, object):
    raise NotImplementedError
  
  @abstractmethod
  def update(self, id, new_object):
    raise NotImplementedError
  
  @abstractmethod
  def delete(self, id):
    raise NotImplementedError