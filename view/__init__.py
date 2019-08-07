from ._app import app
from . import views
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

app.config.from_object('view.config')  # 追加

db = SQLAlchemy(app)  # 追加
