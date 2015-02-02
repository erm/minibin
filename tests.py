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

        # @app.route('/')
        # def index():
        #     return '\n'.join(x.title for x in self.Todo.query.all())

        @app.route('/new', methods=['POST'])
        def create_new_paste():
            form_ = flask.request.form
            paste = self.Paste(form_['title'], form_['content'],
                               from_['password'])
            db.session.add(paste)
            db.session.commit()
            return 'Added new paste'

        db.create_all()

        self.app = app
        self.db = db

    def tearDown(self):
        self.db.drop_all()

    # def test_basic_insert(self):
    #     c = self.app.test_client()
    #     c.post('/add', data=dict(title='First Item', text='The text'))
    #     c.post('/add', data=dict(title='2nd Item', text='The text'))
    #     rv = c.get('/')
    #     self.assertEqual(rv.data, b'First Item\n2nd Item')

if __name__ == '__main__':
    unittest.main()
