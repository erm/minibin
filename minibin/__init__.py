from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.whooshalchemy as whooshalchemy
from flask.ext.restful import Api as API
from .models import Paste
from .api import PasteAPI  # , PastesAPI


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    setup_api(app)
    setup_database(app)
    from minibin.views.frontend import frontend
    app.register_blueprint(frontend)
    return app


def setup_database(app):
    db = SQLAlchemy(app)
    whooshalchemy.whoosh_index(app, Paste)


def setup_api(app):
    api = API(app)
    api.add_resource(PasteAPI, '/api/paste/<int:id>')
