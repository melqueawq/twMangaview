import flask
from ._app import app


@app.route('/')
def show_entries():
    return 'Hello, World!'
