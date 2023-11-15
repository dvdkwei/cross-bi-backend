from src.models import cb_pushsubscription
from src.services.pushsubscription_service import PushSubscriptionService
from flask import current_app, Blueprint, request, jsonify
from src.responses import SuccessResponse, FailResponse
import json

base_url='/crossbi/v1/api/subscription'
pushsubscription_controller = Blueprint('subscription', __name__, url_prefix=base_url)
pushsubscription_service = PushSubscriptionService()

@pushsubscription_controller.route('/notify', methods=['POST'])
def notify():
  if request.method == 'POST':
    try:
      req = request.get_json()
      title = req['title']
      body = req['body']
      
      if not title or not body:
        raise Exception
      
      pushsubscription_service.trigger_notification(title, body)
    except Exception as notif_err:
      raise notif_err
      # return FailResponse(message=notif_err).get_json()
      
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
      pushsubscription_service.add_subscription(sub_to_add)
    except Exception as notif_err:
      return FailResponse(message=str(notif_err)).get_json()
      
  return SuccessResponse().get_json()

@pushsubscription_controller.route('/', methods=['GET'])
def test():
  return SuccessResponse(message='test 123').get_json()