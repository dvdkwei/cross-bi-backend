from flask import jsonify, make_response
import json

class Response(object):
  resp_data = None
  resp_status = 0
  
  def __init__(self, status: int, data: any = None) -> None:
    self.resp_status = status
    if data:
      self.resp_data = data
  
  def get_json(self) -> json:
    return make_response(jsonify(data=self.resp_data), self.resp_status)
  
class SuccessResponse(Response):
  def __init__(self, status=200, data: any = None) -> None:
    super().__init__(status, data)
    
class FailResponse(Response):
  message = ''
  
  def __init__(self, message: str = None, status=500) -> None:
    super().__init__(status)
    if message:
      self.message = message
      
  def get_json(self) -> json:
    return make_response(jsonify(message=self.message), self.resp_status)
  