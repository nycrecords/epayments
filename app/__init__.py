# from flask import Blueprint
#
# main = Blueprint('main', __name__)
#
# from . import views, errors


from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_apscheduler import APScheduler
from flask.ext.cors import CORS

from config import config

# Flask extensions
bootstrap = Bootstrap()
db = SQLAlchemy()
scheduler = APScheduler()

from app.models import orders, client_info, birth, marriage, death, photo, prop_card


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
    CORS(app)

    # Base template that uses React for frontend
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # API CALL GOES HERE

    return app
