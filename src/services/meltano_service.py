import os

def run_meltano():
  try:
    os.system('meltano run tap-spreadsheets-anywhere target-postgres')
  except Exception as run_err:
    raise run_err