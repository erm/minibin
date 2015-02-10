from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from app import create_app
from config import DevelopmentConfig
from app.models import *
import sqlalchemy


app = create_app(config=DevelopmentConfig)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    if app.config['TESTING']:
        print("You are not using the correct config for database creation...")
    else:
        try:
            engine = sqlalchemy.create_engine(app.config['POSTGRESQL_INFO'])
            conn = engine.connect()
            conn.execute("commit")
            conn.execute("create database %s" % app.config['DATABASE_NAME'])
            print("Creating database...")
            db.create_all()
            print("Success!")
        except:
            print("There was an error creating the database...")


@manager.command
def purge_db():
    try:
        num_rows_deleted = db.query(Paste).delete()
        db.commit()
        print("Purging %d rows from Paste table!" % num_rows_deleted)
    except:
        db.rollback()
        print("Purge failed, rolling back changes...")


@manager.command
def runserver():
    print("Running server...")
    app.run(threaded=True)


if __name__ == "__main__":
    manager.run()
