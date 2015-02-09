from flask import (Blueprint, request, redirect, url_for, render_template,
                   abort, flash, session)
from flask import current_app as app
from urllib.request import urlopen
from urllib.parse import urlencode
import codecs
import json
import string
import random
from minibin.models import *

string_domain = string.ascii_letters + string.digits


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


@frontend.route('/search', defaults={'page': 1}, methods=['POST'])
@frontend.route('/page/<int:page>', methods=['POST', 'GET'])
def search(page):
    if request.method == 'POST':
        terms = request.form.get('terms')
        if not terms:
            flash("No search terms specified.")
        else:
            terms = str(terms)
            pastes = Paste.query.whoosh_search(terms,
                                               app.config['MAX_SEARCH_RESULTS']
                                               ).paginate(page,
                                                          10,
                                                          False).items
            return render_template('view_many_pastes.html',
                                   pastes=pastes,
                                   page=page)
    return redirect(url_for('frontend.index'))


@frontend.route('/recent', defaults={'page': 1})
@frontend.route('/page/<int:page>', methods=['POST', 'GET'])
def recent(page):
    pastes = Paste.query.limit(app.config['MAX_RECENT_RESULTS']
                               ).paginate(page,
                                          10,
                                          False).items
    return render_template('view_many_pastes.html',
                           pastes=pastes,
                           page=page)


@frontend.route('/')
def index():
    return render_template('index.html')


@frontend.route('/new', methods=['POST'])
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
            return redirect(url_for('frontend.index'))
        else:
            if not api_response:
                flash("Invalid captcha!")
                return redirect(url_for('frontend.index'))
            else:  # they passed the recaptcha, we can create the paste now
                content = request.form.get('content')
                if not content:
                    flash("No paste content detected.")
                    return redirect(url_for('frontend.index'))
                url_id = ''.join([random.choice(string_domain)
                                 for i in range(8)])
                paste = Paste(url_id,
                              request.form.get('title', None),
                              content,
                              request.form.get('password', None),
                              True)  # change later (public/prviate)
                db.session.add(paste)
                db.session.commit()
                flash("Successfully created new paste!")
                return redirect(url_for('frontend.view_paste', url_id=url_id))


@frontend.route('/p/<url_id>', methods=['GET'])
def view_paste(url_id):
    session.pop('_flashes', None)
    paste = Paste.query.filter_by(url_id=url_id).first()
    return render_template('view_paste.html', paste=paste)
