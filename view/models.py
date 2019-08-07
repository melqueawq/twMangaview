from view import db
from flask_sqlalchemy import SQLAlchemy


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    jsonfile = db.Column(db.Text)

    def __repr__(self):
        return "<Entry id={} jsonfile={!r}>".format(self.id, self.jsonfile)


def init():
    db.create_all()
