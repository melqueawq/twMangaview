from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
app = Flask(__name__, template_folder='../templates',
            static_folder="../static")

app.config.from_object('view.config')
db = SQLAlchemy(app)
Migrate(app, db)


@app.before_first_request
def create_tables():
    from view.models import Books, Users
    db.create_all()
