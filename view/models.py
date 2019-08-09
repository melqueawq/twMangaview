from ._app import db
from flask_sqlalchemy import SQLAlchemy


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    author = db.Column(db.Text)
    url = db.Column(db.Text)
    jsonfile = db.Column(db.Text)

    def __repr__(self):
        return f'<Books id={self.id} author={self.author} url={self.url} jsonfile={self.jsonfile}>'


def init():
    db.create_all()
