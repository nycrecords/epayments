import os
from app import create_app, db
from app.models import Orders
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
# from flask.ext.sqlalchemy import SQLAlchemy


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    """Create the shell context for the Flask application."""
    return dict(app=app, db=db, Order=Order)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def import_xml():
    """Import XML files"""
    from app.utils import import_xml_folder
    import_xml_folder()

@manager.command
def reset_db():
    """Empties the database and generates it again with db_setup"""
    db.drop_all()
    db.create_all()


if __name__ == '__main__':
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)
    manager.run()
