from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from minibin import create_app
from config import DevelopmentConfig
from minibin.models import *
import sqlalchemy


app = create_app(config=DevelopmentConfig)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    engine = sqlalchemy.create_engine(app.config['POSTGRESQL_INFO'])
    conn = engine.connect()
    conn.execute("commit")
    conn.execute("create database %s" % app.config['DATABASE_NAME'])
    print("Creating database...")
    db.create_all()
    print("Success!")


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
