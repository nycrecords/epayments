import os

import pytz
from datetime import date, timedelta
from elasticsearch import Elasticsearch
from flask import Flask, session, g
from flask_session import Session
from flask_apscheduler import APScheduler
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import config, Config
from app.lib.nycholidays import NYCHolidays

# Flask extensions
bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
scheduler = APScheduler()
sess = Session()
login_manager = LoginManager()

PYTZ_TIMEZONE = pytz.timezone(Config.TIME_ZONE)

# ElasticSearch Extension
es = Elasticsearch(Config.ELASTICSEARCH_URL)

nyc_holidays = NYCHolidays(years=[year for year in range(date.today().year, date.today().year + 1)])


def create_app(config_name):
    """
    Set up the Flask Application context

    :param config_name: Configuration for specfic application context

    :return: Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # config[config_name].init_app(app)
    scheduler.init_app(app)

    bootstrap.init_app(app)
    sess.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    app.elasticsearch = Elasticsearch(Config.ELASTICSEARCH_URL)

    # Base template that uses React for frontend
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # API CALL GOES HERE
    from .api.v1 import api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    from .auth import auth
    app.register_blueprint(auth, url_prefix="/auth")

    from .admin import admin
    app.register_blueprint(admin, url_prefix="/admin")

    @app.before_request
    def before_request():
        session.permanent = True
        session_lifetime = int(os.environ.get("PERMANENT_SESSION_LIFETIME", 35))
        app.permanent_session_lifetime = timedelta(minutes=session_lifetime)
        session.modified = True
        g.user = current_user

    return app
