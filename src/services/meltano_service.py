import os
import yaml
import json
import datetime
from flask import current_app

class MeltanoService:
  async def run_extract_load():
    try:
      await os.system('meltano run tap-spreadsheets-anywhere target-postgres')
    except Exception as run_err:
      raise run_err
  
  async def update_tables_config(
    self,
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
      config_path = os.path.join(
        current_app.root_path,
        'config.json'
      )
      
      config_file = open(config_path, 'r')
      
      config_json = json.load(config_file)
      tables: [object] = config_json['tables']
      new_table = {
        "path": new_file_path,
        "name": dashboard_id + '_' + table_name,
        "pattern": new_file_name,
        "start_date": datetime.datetime.now(),
        "key_properties": key_properties,
        "format": file_format,
        "delimiter": delimiter,
        "quotechar": quote_char
      }
      
      tables.append(new_table)
      config_file.close()
    except Exception as update_err:
      raise update_err
    
    return tables
  
  async def transform():
    try:
      await os.system('meltano invoke dbt-postgres run')
    except Exception as run_err:
      raise run_err