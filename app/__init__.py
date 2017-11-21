import pytz
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_apscheduler import APScheduler
from flask_login import LoginManager

from config import config, Config

# Flask extensions
bootstrap = Bootstrap()
db = SQLAlchemy()
scheduler = APScheduler()

login_manager = LoginManager()

PYTZ_TIMEZONE = pytz.timezone(Config.TIME_ZONE)


def create_app(config_name):
    """
    Set up the Flask Application context

    :param config_name: Configuration for specfic application context

    :return: Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    scheduler.init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # Base template that uses React for frontend
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # API CALL GOES HERE
    from .api_1_0 import api_1_0 as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
