from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api as API
from .api import PasteAPI, PastesAPI


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


def setup_api(app):
    api = API(app)
    api.add_resource(PasteAPI, '/api/paste/<int:pid>')
    api.add_resource(PastesAPI, '/api/pastes/')
