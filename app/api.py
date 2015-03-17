from flask.ext.restful import Resource
from .models import *


def format_paste(paste):
    """
    Format a paste for the RESTful API
    """
    if not paste.public:
        return None  # disallow api access to private pastes
    _paste = {
        'content': paste.content,
        'created_on': str(paste.created_on),
        'url_id': paste.url_id,
        'id': paste.id
    }
    if paste.title:  # title is optional
        _paste['title'] = paste.title
    return _paste


# class PastesAPI(Resource): # implementing this when i add pagination

#     def get(self):
#         pastes = Paste.query.order_by(Paste.date_created).all()
#         _pastes = []
#         for p in pastes:
#             _paste = format_paste(p)
#             if _paste:
#                 _pastes.append(_paste)
#         return _pastes


class PasteAPI(Resource):

    def get(self, url_id):
        paste = Paste.query.filter_by(url_id=url_id).first()
        if not paste:
            abort(404)
        _paste = format_paste(paste)
        if not _paste:
            return "This paste is private."
        return _paste
