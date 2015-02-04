from flask import Blueprint, request, redirect, url_for, render_template, \
    abort, flash, current_app, session
from minibin.models import *
from urllib.request import urlopen
from urllib.parse import urlencode
import os
import codecs
import json


frontend = Blueprint('frontend', __name__)


@frontend.app_errorhandler(404)
def handle_404(err):
    return render_template('404.html'), 404


@frontend.app_errorhandler(413)
def handle_413(err):
    return render_template('413.html'), 413


@frontend.app_errorhandler(500)
def handle_500(err):
    return render_template('500.html'), 500


@frontend.route('/github')
def github():
    return redirect('https://github.com/erm/minibin', code=302)


@frontend.route('/api')
def api():
    return render_template('api.html')


@frontend.route('/search')
def search():
    paste = Paste.query.whoosh_search('second OR last').all()
    return paste


@frontend.route('/')
def index():
    return render_template('index.html')


@frontend.route('/new', methods=['POST'])
def create_paste():
    if request.method == 'POST':
        #  verify the recaptcha response
        api_request_data = urlencode({
            'secret': current_app.config['RECAPTCHA_PRIVATE_KEY'],
            'response': request.form.get('g-recaptcha-response')})
        api_request = urlopen(current_app.config['RECAPTCHA_VERIFY_URL'],
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
                return redirect(url_for('frontend.index'))
            else:  # they passed the recaptcha, we can create the paste now
                paste = Paste(request.form.get('title', None),
                              request.form.get('content'),
                              request.form.get('password', None))
                db.session.add(paste)
                db.session.commit()
                pid = paste.id
                flash("Successfully created new paste!")
                return redirect(url_for('frontend.view_paste', pid=pid))


@frontend.route('/p/<id>', methods=['POST', 'GET'])
def view_paste(pid):
    session.pop('_flashes', None)
    try:
        int(id)  # paste ids are always an integer
    except ValueError:
        abort(404)
    else:
        paste = Paste.query.get_or_404(id)
        return render_template('view_paste.html', paste=paste)
