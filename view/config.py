import os

SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL') or "sqlite:///data.db"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = os.urandom(24)
