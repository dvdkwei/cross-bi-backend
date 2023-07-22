from flask import Blueprint, jsonify
import os

base_url='/crossbi/v1/api/meltano'
meltano_controller = Blueprint(
    'meltano_ops', 
    __name__, url_prefix=base_url
  )

@meltano_controller.route(base_url + '/run')
def run_meltano():
  try:
    os.system('meltano run tap-spreadsheets-anywhere target-postgres')
  except Exception as run_err:
    raise run_err
  
  return jsonify(status=200, message='successfully ran extraction and load')