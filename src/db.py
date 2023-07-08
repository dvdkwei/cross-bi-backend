import psycopg2
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Database:
  host = 'pg_container'
  database = 'postgres'
  port = '5432'
  user = ''
  password = ''
  
  def __init__(self):
    if environ.get('FLASK_ENV') == 'prod':
      self.user = ''
    else:
      self.user = environ.get('DEV_DB_USERNAME')
      self.password = environ.get('DEV_DB_PASSWORD')
      
  def connect_to_db(self):
    # conn = None
    try:
      conn = psycopg2.connect(
        host = self.host,
        database = self.database,
        port = self.port,
        user = self.user,
        password = self.password
      )
    except Exception as error:
      print(error) 
      
    return conn

  def close_connection(self, conn, cursor):
    cursor.close()
    conn.close()
    
  
  def execute_command(self, command:str):
    conn = self.connect_to_db()
    cursor = conn.cursor()
    
    try:
      cursor.execute(command)
    except Exception as db_execute_error:
      raise db_execute_error
    
    conn.commit()
    self.close_connection(conn, cursor)
  
  def fetch_table(self, command:str):
    conn = self.connect_to_db()
    cursor = conn.cursor()
    
    try:
      cursor.execute(command)
    except Exception as db_execute_error:
      raise db_execute_error
    
    result = cursor.fetchall()
    self.close_connection(conn, cursor)
    return result