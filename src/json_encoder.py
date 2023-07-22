from datetime import datetime
import dataclasses
import json
from flask import jsonify

class CustomJSONEncoder(json.JSONEncoder):  # <<-- Add this custom encoder
  """Custom JSON encoder for the DB class."""

  def default(self, o):
    # this serializes anything dataclass can handle
    if dataclasses.is_dataclass(o):
      return dataclasses.asdict(o)
    if isinstance(o, datetime):  # this adds support for datetime
      return o.isoformat()
    return super().default(o)
  
def rowToDict(row):
  d = [dict(col) for col in row]
  key = list(d[0].keys())[0]

  d = list(map(lambda x: x[key], d))

  return d

def resultToDict(result):
  d = dict(result)
  key = list(d.keys())[0]
  
  return d[key]
