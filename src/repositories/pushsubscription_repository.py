from src.models import cb_pushsubscription
from pywebpush import webpush, WebPushException
from sqlalchemy import select, delete
from flask import current_app
import json
from .abstract_repository import IRepository, db

class PushSubscriptionNotFoundException(Exception):
  def __init__(self, *args: object, attr: any) -> None:
    super().__init__(*args)
    self.message = 'user ' + str(attr) + ' not found'
  
  def __str__(self) -> str:
    return self.message

class PushSubscriptionRepository(IRepository):
  def get_all(self):
    try:
      subs = db.session.execute(select(cb_pushsubscription)).all()
    except Exception:
      db.session.remove()
      raise PushSubscriptionNotFoundException
    finally:
      db.session.close()
    
    return subs
  
  def get_by_id(self, pushsub_id:str):
    try:
      push_subscription = db.session.execute(select(cb_pushsubscription).filter_by(id = pushsub_id)).one()
    except Exception:
      db.session.remove()
      raise PushSubscriptionNotFoundException
    finally:
      db.session.close()
    
    return push_subscription
  
  def get_subcription_by_json(self, sub_json):
    try:
      subscription = db.session.execute(select(cb_pushsubscription).filter_by(subscription_json = sub_json)).one()
    except Exception:
      db.session.remove()
      return None
    finally:
      db.session.close()
      
    return subscription
  
  def create(self, sub: cb_pushsubscription):
    try:
      is_sub_available = self.get_subcription_by_json(sub.subscription_json)
      
      if not is_sub_available:
        db.session.add(sub)
        db.session.flush()
        
        id = sub.id
        
        db.session.commit()
        
        return id
    except Exception as add_subscription_error:
      db.session.remove()
      raise add_subscription_error
    finally:
      db.session.close()
  
  def notify(self, sub: cb_pushsubscription, title, body):
    private_key = current_app.config["VAPID_PRIVATE_KEY"]
    mail_to = current_app.config["VAPID_MAILTO"]
    
    try: 
      webpush(
          subscription_info=json.loads(sub['cb_pushsubscription'].subscription_json),
          data=json.dumps({"title": title, "body": body}),
          vapid_private_key=private_key,
          vapid_claims={
              "sub": "mailto:{}".format(mail_to)
          }
      )
    except WebPushException as ex:
      if ex.response and ex.response.json():
          extra = ex.response.json()
          print("Remote service replied with a {}:{}, {}",
                extra.code,
                extra.errno,
                extra.message
                )
          raise ex
    
  def trigger_notification(self, title, body):
    subscriptions = self.get_all()
    return [self.notify(sub, title, body) for sub in subscriptions]
  
  def update(self, id, new_object):
    raise Exception(message='No direct update on push subscription object')
  
  def delete(self, user_id):
    try:
      affected_rows = db.session.execute(
        delete(cb_pushsubscription).where(cb_pushsubscription.id == user_id)
      ).rowcount
      
      if affected_rows == 0:
        raise Exception
      
      db.session.commit()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
    
    return user_id
  