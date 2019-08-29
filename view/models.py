from ._app import db
from flask_sqlalchemy import SQLAlchemy


class Books(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    author = db.Column(db.Text)
    url = db.Column(db.Text)
    thumbnail = db.Column(db.Text)
    jsonfile = db.Column(db.Text)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Books id={self.id} jsonfile={self.jsonfile}>'


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    screen_name = db.Column(db.Text)
    jsonfile = db.Column(db.Text)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Books id={self.id} jsonfile={self.jsonfile}>'


def init():
    db.create_all()
