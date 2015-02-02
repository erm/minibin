from flask.ext.script import Manager
from minibin import create_app
from config import DevelopmentConfig
from minibin.models import *


app = create_app(config=DevelopmentConfig)
manager = Manager(app)


@manager.command
def create_db():
    print("Creating database...")
    db.create_all()
    print("Success!")


if __name__ == "__main__":
    manager.run()
