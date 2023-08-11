import os
from getpass import getpass

from flask_migrate import Migrate

from app import create_app, db
from app.models import (Orders, Suborders, Customers, BirthSearch, MarriageSearch, DeathSearch, BirthCertificate,
                        MarriageCertificate, DeathCertificate, PropertyCard, TaxPhoto, PhotoGallery, Events, Users)
from app.search.utils import recreate

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage

    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


def make_shell_context():
    """Create the shell context for the Flask application."""
    return dict(app=app, db=db, Orders=Orders, Suborders=Suborders, Events=Events,
                Customers=Customers, BirthSearch=BirthSearch, MarriageSearch=MarriageSearch,
                DeathSearch=DeathSearch, BirthCertificate=BirthCertificate,
                MarriageCertificate=MarriageCertificate, DeathCertificate=DeathCertificate,
                PropertyCard=PropertyCard, TaxPhoto=TaxPhoto, PhotoGallery=PhotoGallery, Users=Users)


@app.cli.command()
def daily_import():
    """Import XML files"""
    from datetime import date, datetime, timedelta
    from app.import_utils import import_from_api

    # Set variables for import method
    today = date.today()
    yesterday = date.today() - timedelta(days=1)
    start_date = datetime.combine(yesterday, datetime.min.time()).isoformat()
    end_date = datetime.combine(today, datetime.min.time()).isoformat()

    import_from_api(start_date, end_date)


@app.cli.command()
def reset_db():
    """Empties the database and generates it again with db_setup"""
    from flask_migrate import upgrade
    db.drop_all()
    db.create_all()
    upgrade()
    create_test_user()
    recreate()


@app.cli.command()
def create_test_user():
    user = Users('test@email.com', '1234', is_active=True)
    db.session.add(user)
    db.session.commit()


@app.cli.command()
def create_user():
    """
    Command line tool to create a user in the database.
    :return: message indicating either error or success
    """
    email = input("Enter your email: ")
    password = getpass("Enter your desired password: ")
    confirm_password = getpass("Re-enter your password: ")
    if password != confirm_password:
        return print("Passwords are not the same. Please try again.")

    user = Users(email=email, password=password, is_active=True)
    db.session.add(user)
    db.session.commit()

    return print("Successfully created user, " + email)


@app.cli.command()
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/indexJS.html' % covdir)
        COV.erase()


@app.cli.command()
def es_recreate():
    """Recreates the index and docs"""
    recreate()
