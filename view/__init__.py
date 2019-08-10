from ._app import app
from . import views

app.config.from_object('view.config')
