from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

# Flask extensions
db = SQLAlchemy()

# Import models so they are registered with SQLAlchemy
from . import models

def create_app(config_name):
    """
    Set up the Flask Application context.

    :param config_name: Configuration for specific application context.

    :return: Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    # Base template that uses React for frontend
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # API calls used by React + Flux to manage data
    from .api_1_0 import api_1_0 as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0/')

    return app
