from src.models import cb_pushsubscription
from src.repositories.pushsubscription_repository import PushSubscriptionRepository
from flask import current_app, Blueprint, request, jsonify
from src.responses import SuccessResponse, FailResponse
import json

base_url='/crossbi/v1/api/subscriptions'
pushsubscription_controller = Blueprint('subscriptions', __name__, url_prefix=base_url)
pushsubscription_repository = PushSubscriptionRepository()

@pushsubscription_controller.route('/notify', methods=['POST'])
def notify():
  if request.method == 'POST':
    try:
      req = request.get_json()
      title = req['title']
      body = req['body']
      
      if not title or not body:
        raise Exception
      
      pushsubscription_repository.trigger_notification(title, body)
    except Exception as notif_err:
      return FailResponse(message=str(notif_err)).get_json()
      
  return SuccessResponse().get_json()

@pushsubscription_controller.route('/', methods=['POST'])
def addSubscription():
  if request.method == 'POST':
    try:
      req = request.get_json(force=True)
      sub_json = req['subscription_json']
      
      if not sub_json:
        raise Exception
      
      sub_to_add = cb_pushsubscription(subscription_json = json.dumps(sub_json))
      pushsubscription_repository.create(sub_to_add)
    except Exception as notif_err:
      return FailResponse(message=str(notif_err)).get_json()
      
  return SuccessResponse().get_json()