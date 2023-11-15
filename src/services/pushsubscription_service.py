from src.models import cb_pushsubscription
from pywebpush import webpush, WebPushException
from sqlalchemy import select, delete
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
import json

db = SQLAlchemy(session_options={'expire_on_commit': False})

class PushSubscriptionService():
  def get_all_subscriptions(self):
    try:
      subs = db.session.execute(select(cb_pushsubscription)).all()
    except Exception as db_err:
      db.session.remove()
      raise db_err
    finally:
      db.session.close()
    
    return subs
  
  def get_subcription_by_json(self, sub_json):
    try:
      subscription = db.session.execute(select(cb_pushsubscription).filter_by(subscription_json = sub_json)).one()
    except Exception:
      db.session.remove()
      return None
    finally:
      db.session.close()
      
    return subscription
  
  def add_subscription(self, sub: cb_pushsubscription):
    try:
      is_sub_available = self.get_subcription_by_json(sub.subscription_json)
      
      if not is_sub_available:
        db.session.add(sub)
        db.session.flush()
        
        id = sub.id
        
        db.session.commit()
    except Exception as add_subscription_error:
      db.session.remove()
      raise add_subscription_error
    finally:
      db.session.close()
    
    return id
  
  def notify(self, sub: cb_pushsubscription, title, body):
    try: 
      webpush(
          subscription_info=json.loads(sub['cb_pushsubscription'].subscription_json),
          data=json.dumps({"title": title, "body": body}),
          vapid_private_key=current_app.config["VAPID_PRIVATE_KEY"],
          vapid_claims={
              "sub": "mailto:{}".format(
                current_app.config["VAPID_MAILTO"]
              )
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
    subscriptions = self.get_all_subscriptions()
    return [self.notify(sub, title, body) for sub in subscriptions]
  
  def delete_subscription(self, user_id):
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
  