import os
from app import create_app, db
from app.models import Orders, StatusTracker, Customer, BirthSearch, \
    MarriageSearch, DeathSearch, BirthCertificate, MarriageCertificate, \
    DeathCertificate, PropertyCard, PhotoTax, PhotoGallery
from flask_script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    """Create the shell context for the Flask application."""
    return dict(app=app, db=db, Order=Orders, StatusTracker=StatusTracker,
                Customer=Customer, BirthSearch=BirthSearch, MarriageSearch=MarriageSearch,
                DeathSearch=DeathSearch, BirthCertificate=BirthCertificate,
                MarriageCertificate=MarriageCertificate, DeathCertificate=DeathCertificate,
                PropertyCard=PropertyCard, PhotoTax=PhotoTax, PhotoGallery=PhotoGallery)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

# @manager.command
# def import_xml():
#     """Import XML files"""
#     from app.utils import import_xml_folder
#     import_xml_folder()


@manager.command
def reset_db():
    """Empties the database and generates it again with db_setup"""
    db.drop_all()
    db.create_all()


if __name__ == '__main__':
    manager.run()
