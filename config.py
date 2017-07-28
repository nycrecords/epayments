import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

dotenv_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path)


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://developer@127.0.0.1:5432/epayments'
    REMOTE_FILE_PATH = os.environ.get('REMOTE_FILE_PATH')
    LOCAL_FILE_PATH = (os.environ.get('LOCAL_FILE_PATH') or
                       os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/'))

    USE_SFTP = os.environ.get('USE_SFTP') == 'True'
    SFTP_HOSTNAME = os.environ.get('SFTP_HOSTNAME')
    SFTP_PORT = os.environ.get('SFTP_PORT')
    SFTP_USERNAME = os.environ.get('SFTP_USERNAME')
    SFTP_RSA_KEY_FILE = os.environ.get('SFTP_RSA_KEY_FILE')
    SFTP_UPLOAD_DIRECTORY = os.environ.get('SFTP_UPLOAD_DIRECTORY')

    @staticmethod
    def init_app(app):
        pass


# localhost Config Vars
class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (os.environ.get('TEST_DATABASE_URL') or 'postgresql://developer@127.0.0.1:5432/epayments_test')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://developer:@localhost:5432/epayments'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
