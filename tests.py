import unittest
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from minibin.models import Paste
from datetime import datetime


def make_paste_model(db):

    class Paste(db.Model):

        __tablename__ = 'pastes'
        __searchable__ = ['title', 'content']

        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(255))
        content = db.Column(db.Text, nullable=False)
        date_created = db.Column(db.DateTime, nullable=False)
        password = db.Column(db.String(255))

        def __init__(self, title, content, password):
            self.title = title
            self.content = content
            self.password = password
            _date = datetime.utcnow()
            _date = _date.replace(microsecond=0)
            self.date_created = _date

        def __repr__(self):
            return '<Paste %s %s>' % (self.id, self.date_created)

        def __str__(self):
            return self.id
    return Paste


class MinibinTestCase(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)
        app.config.from_object('config.TestingConfig')
        db = SQLAlchemy(app)
        self.paste = make_paste_model(db)

        # @app.route('/new', methods=['POST'])
        # def create_new_paste():
        #     form_ = flask.request.form
        #     paste = self.Paste(form_['title'], form_['content'],
        #                        from_['password'])
        #     db.session.add(paste)
        #     db.session.commit()
        #     return 'Added new paste'

        db.create_all()

        self.app = app
        self.db = db

    def test_whoosh_search(self):
        paste = self.paste('my title lol', 'my content lol', None)
        self.db.session.add(paste)
        self.db.session.commit()
        pastes = self.paste.query.whoosh_search('my content').all()
        self.assertIsNotNone(pastes)

    def tearDown(self):
        self.db.drop_all()


if __name__ == '__main__':
    unittest.main()
