from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from import_xml import import_xml as import_xml_blueprint
    app.register_blueprint(import_xml_blueprint, url_prefix='/import')

    return app
