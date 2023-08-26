import os
import yaml
import json
import datetime
from flask import current_app
from src.responses import FailResponse, SuccessResponse

class MeltanoService:
  async def run_extract_load():
    try:
      await os.system('meltano run tap-spreadsheets-anywhere target-postgres')
    except Exception as run_err:
      return FailResponse(message=run_err.message).get_json()
    
    return SuccessResponse().get_json

  async def update_extractor_tables(
    dashboard_id: str,
    new_file_path: str,
    table_name: str,
    new_file_name: str,
    key_properties: [str],
    file_format: str,
    delimiter: str = ';',
    quote_char: str = "\""
  ):
    try:
      meltano_yaml_path = os.path.join(
        current_app.root_path,
        'meltano.yml'
      )
      
      meltano_file = open(meltano_yaml_path, 'w')
      
      meltano_json = json.loads(json.dumps(yaml.safe_load(meltano_file)))
      tables: [object] = meltano_json['plugins']['extractors'][0]['config']['tables']    
      new_table = json.dumps({
        "path": new_file_path,
        "name": dashboard_id + '_' + table_name,
        "pattern": new_file_name,
        "start_date": datetime.datetime.now(),
        "key_properties": key_properties,
        "format": file_format,
        "delimiter": delimiter,
        "quotechar": quote_char
      })
      
      tables.append(new_table)
      
      yaml.dump(meltano_json, meltano_yaml_path)
      meltano_file.close()
    except Exception as update_err:
      return FailResponse(message=update_err.message).get_json()
    
    return SuccessResponse().get_json()