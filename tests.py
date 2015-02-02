import unittest
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


def make_paste_model(db):
    class Paste(db.Model):

        __tablename__ = 'pastes'

        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(255))
        content = db.Column(db.Text, nullable=False)
        date_created = db.Column(db.DateTime, nullable=False)
        password = db.Column(db.String(255))

        def __init__(self, title, content, password, ip_address):
            self.title = title
            self.content = content
            self.password = password
            _date = datetime.utcnow()
            _date = _date.replace(microsecond=0)
            self.date_created = _date

        def __repr__(self):
            return '<Paste %s %s>'.format(self.id, self.date_created)

        def __str__(self):
            return self.id
    return Paste


class MinibinTestCase(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)
        app.config.from_object('config.TestingConfig')
        db = SQLAlchemy(app)
        self.Paste = make_paste_model(db)

        db.create_all()

        self.app = app
        self.db = db

    def tearDown(self):
        self.db.drop_all()

if __name__ == '__main__':
    unittest.main()
