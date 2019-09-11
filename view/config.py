import os
from os.path import join, dirname
from dotenv import load_dotenv

SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL') or "sqlite:///data.db"
SQLALCHEMY_TRACK_MODIFICATIONS = True

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
SECRET_KEY = os.environ.get("SECRET_KEY")
