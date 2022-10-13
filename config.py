import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

dotenv_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path)


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    REMOTE_FILE_PATH = os.environ.get('REMOTE_FILE_PATH')
    LOCAL_FILE_PATH = (os.environ.get('LOCAL_FILE_PATH') or
                       os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/'))
    TAR_DATA_PATH = os.environ.get('TAR_DATA_PATH', 'data/files/DOR/')
    PRINT_FILE_PATH = os.environ.get('PRINT_FILE_PATH',
                                     os.path.join(os.path.abspath(os.path.dirname(__file__)),'data/files/'))
    NO_AMENDS_FILE_PATH = os.environ.get('NO_AMENDS_FILE_PATH',
                                         os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/no_amends/'))

    MAIL_SERVER = os.environ.get("MAIL_SERVER") or "localhost"
    MAIL_PORT = os.environ.get("MAIL_PORT") or 2525
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") or False
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME") or None
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD") or None
    MAIL_SENDER = os.environ.get("MAIL_SENDER") or "donotreply@records.nyc.gov"
    IMPORT_MAIL_TO = os.environ.get("IMPORT_MAIL_TO")

    USE_SFTP = os.environ.get('USE_SFTP') == 'True'
    SFTP_HOSTNAME = os.environ.get('SFTP_HOSTNAME')
    SFTP_PORT = os.environ.get('SFTP_PORT')
    SFTP_USERNAME = os.environ.get('SFTP_USERNAME')
    SFTP_RSA_KEY_FILE = os.environ.get('SFTP_RSA_KEY_FILE')
    SFTP_UPLOAD_DIRECTORY = os.environ.get('SFTP_UPLOAD_DIRECTORY')
    TIME_ZONE = os.environ.get('TIME_ZONE') or 'US/Eastern'

    # Elastic Search Configurations
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or 'https://localhost:9200'
    ELASTICSEARCH_ENABLED = os.environ.get("ELASTICSEARCH_ENABLED") or 'True'
    ELASTICSEARCH_INDEX = os.environ.get("ELASTICSEARCH_INDEX") or 'suborders'

    # Import API Configurations
    IMPORT_URL = os.environ.get("IMPORT_URL")
    IMPORT_API_KEY = os.environ.get("IMPORT_API_KEY")

    @staticmethod
    def init_app(app):
        pass


# localhost Config Vars
class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://developer:@localhost:5432/epayments_test'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://epayments_v2:@localhost:5432/epayments'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
