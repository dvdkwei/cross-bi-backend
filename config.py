"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Base config."""
    ENVIRONMENT = environ.get("FLASK_ENV")
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_DEBUG = environ.get("FLASK_DEBUG")
    VAPID_PUBLIC_KEY = environ.get("VAPID_PUBLIC_KEY")
    VAPID_PRIVATE_KEY = environ.get("VAPID_PRIVATE_KEY")
    VAPID_MAILTO = environ.get("VAPID_MAILTO")
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'