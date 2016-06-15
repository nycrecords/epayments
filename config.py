import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = os.environ.get('SQLALCHEMY_COMMIT_ON_TEARDOWN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://brandon:@localhost:5432/epayments'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://brandon:@localhost:5432/epayments'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://brandon:@localhost:5432/epayments'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
