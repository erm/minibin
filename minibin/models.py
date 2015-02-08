from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.whooshalchemy
from datetime import datetime


db = SQLAlchemy()


class Paste(db.Model):

    __tablename__ = 'paste'
    __searchable__ = ['title', 'content']

    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.String(255))
    public = db.Column(db.Boolean(), default=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, url_id, title, content, password, truncated, public):
        self.url_id = url_id
        self.title = title
        self.content = content
        self.password = password
        self.created_on = datetime.utcnow().replace(microsecond=0)

    def __repr__(self):
        return '<Paste %s [%s] %s>' % (self.id, self.url, self.date_created)

    def __str__(self):
        return self.id
