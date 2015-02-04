#  minibin

A minimal pastebin created using Python 3.4 and the Flask micro-framework.

# Todo

- Tests.
- Have recaptcha appear only on suspicious activity
- Style templates
- Add paste browsing
- Add private pastes and deletion passwords
- Add pagination for restful API pastes
- Replace current search with better fulltext search

# Requirements

- Python 3.4
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- Recaptcha API keys

For full-text search, we also require Flask-WhooshAlchemy. However, the current release of the Flask-WhooshAlchemy extension does not support Python 3. To install a temporary compatability solution, use the following steps (within your virtual environment):

    git clone https://github.com/tonet666p/Flask-WhooshAlchemy.git
    cd Flask-WhooshAlchemy
    git checkout python-3-compatibility
    python setup.py install