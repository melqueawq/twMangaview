from flask_sqlalchemy import SQLAlchemy
from flask import Flask
app = Flask(__name__, template_folder='../templates')

db = SQLAlchemy(app)
