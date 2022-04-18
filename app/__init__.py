import pytz
from datetime import date
from elasticsearch import Elasticsearch
from flask import Flask
from flask_apscheduler import APScheduler
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from config import config, Config
from app.lib.nycholidays import NYCHolidays

# Flask extensions
bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
scheduler = APScheduler()

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
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    app.elasticsearch = Elasticsearch(Config.ELASTICSEARCH_URL)

    # Base template that uses React for frontend
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # API CALL GOES HERE
    from .api.v1 import api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    return app
