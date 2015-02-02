from flask.ext.restful import Resource
from .models import *


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


class PastesAPI(Resource):

    def get(self):
        pastes = Paste.query.order_by(Paste.date_created).all()
        _pastes = []
        for p in pastes:
            _paste = format_paste(p)
            if _paste:
                _pastes.append(_paste)
        return _pastes


class PasteAPI(Resource):

    def get(self, pid):
        paste = Paste.query.get(pid)
        if not paste:
            abort(404)
        _paste = format_paste(paste)
        if not _paste:
            return "This paste is private."
        return _paste
