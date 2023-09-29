import multiprocessing
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '../.env'))

# gunicorn
workers = multiprocessing.cpu_count() + 1
bind = "0.0.0.0:3001"
raw_env = [
  "FLASK_APP=" + environ.get('FLASK_APP'),
  'FLASK_ENV=' + environ.get('FLASK_ENV'),
  "API_KEY=" + environ.get('API_KEY'),
  "DEV_DB_USERNAME=" + environ.get('DEV_DB_USERNAME'),
  "DEV_DB_PASSWORD=" + environ.get('DEV_DB_PASSWORD'),
  "SQLALCHEMY_DATABASE_URI=" + environ.get('SQLALCHEMY_DATABASE_URI'),
  "DBT_POSTGRES_HOST=" + environ.get('DBT_POSTGRES_HOST'),
  "DBT_POSTGRES_USER =" + environ.get('DBT_POSTGRES_USER'),
  "DBT_POSTGRES_PASSWORD =" + environ.get('DBT_POSTGRES_PASSWORD'),
  "DBT_POSTGRES_PORT =" + environ.get('DBT_POSTGRES_PORT'),
  "DBT_POSTGRES_DBNAME =" + environ.get('DBT_POSTGRES_DBNAME'),
  "DBT_POSTGRES_SCHEMA =" + environ.get('DBT_POSTGRES_SCHEMA')
]