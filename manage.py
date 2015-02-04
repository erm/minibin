from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from minibin import create_app
from config import DevelopmentConfig
from minibin.models import *


app = create_app(config=DevelopmentConfig)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    print("Creating database...")
    db.create_all()
    print("Success!")


@manager.command
def runserver():
    print("Running server...")
    app.run(threaded=True)


if __name__ == "__main__":
    manager.run()
