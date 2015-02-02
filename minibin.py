from flask import Flask, request, redirect, url_for, render_template, \
    abort, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext import restful
from datetime import datetime
from urllib.request import urlopen
from urllib.parse import urlencode
import os
import codecs
import json


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)
api = restful.Api(app)


class Paste(db.Model):

    __tablename__ = 'pastes'

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


def format_paste(paste):  # format our pastes for the restful api
    if paste.password:
        _paste = None  # do not allow api access to private pastes
    else:
        _paste = {'content': paste.content,
                  'date_created': str(paste.date_created),
                  'id': paste.id}
        if paste.title:  # title is optional
            _paste['title'] = paste.title
    return _paste


class PastesAPI(restful.Resource):

    def get(self):
        pastes = Paste.query.order_by(Paste.date_created).all()
        _pastes = []
        for p in pastes:
            _paste = format_paste(p)
            if _paste:
                _pastes.append(_paste)
        return _pastes


class PasteAPI(restful.Resource):

    def get(self, pid):
        paste = Paste.query.get(pid)
        if not paste:
            abort(404)
        _paste = format_paste(paste)
        if not _paste:
            return "This paste is private."
        return _paste

api.add_resource(PasteAPI, '/api/paste/<int:pid>')
api.add_resource(PastesAPI, '/api/pastes/')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new', methods=['POST'])
def create_paste():
    if request.method == 'POST':
        #  verify the recaptcha response
        api_request_data = urlencode({
            'secret': app.config['RECAPTCHA_PRIVATE_KEY'],
            'response': request.form.get('g-recaptcha-response')})
        api_request = urlopen(app.config['RECAPTCHA_VERIFY_URL'],
                              data=api_request_data.encode('utf-8'))
        reader = codecs.getreader('utf-8')
        #  check the api response for success (True) or failure (False)
        try:
            api_response = json.load(reader(api_request)).get('success')
        except URLError:  # i probably want to handle this differently later
            flash("There was an error with the captcha, try again later.")
            return redirect(url_for('index'))
        else:
            if not api_response:
                flash("Invalid captcha!")
                return redirect(url_for('index'))
            else:  # they passed the recaptcha, we can create the paste now
                paste = Paste(request.form.get('title', None),
                              request.form.get('content'),
                              request.form.get('password', None))
                db.session.add(paste)
                db.session.commit()
                pid = paste.id
                flash("Successfully created new paste!")
                return redirect(url_for('view_paste', pid=pid))


@app.route('/p/<pid>', methods=['POST', 'GET'])
def view_paste(pid):
    try:
        int(pid)  # paste ids are always an integer
    except ValueError:
        abort(404)
    else:
        paste = Paste.query.get_or_404(pid)
        paste_enum = enumerate(paste.content.split('\n'))  # for line numbers
        return render_template('view_paste.html', paste=paste,
                               paste_enum=paste_enum)


if __name__ == '__main__':
    app.run()
