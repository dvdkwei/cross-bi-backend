from flask import jsonify, make_response
import json

class Response(object):
  resp_data = None
  resp_status = 0
  resp_message = None
  
  def __init__(self, status: int,  message: str = None, data: any = None) -> None:
    self.resp_status = status
    self.resp_data = data
    self.resp_message = message
  
  def get_json(self) -> json:
    return make_response(jsonify(data=self.resp_data, message=self.resp_message), self.resp_status)
  
class SuccessResponse(Response):
  def __init__(self, status=200, data: any = None, message: str = None) -> None:
    super().__init__(status, message, data)
    
class FailResponse(Response):
  def __init__(self, status=500, message: str = None) -> None:
    super().__init__(status, message)
  