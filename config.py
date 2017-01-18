import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DATABASE_URL = os.environ.get('DATABASE_URL')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') # Uncomment for Heroku

    @staticmethod
    def init_app(app):
        pass


# Heroku Config Vars
# class DevelopmentConfig(Config):
#     DEBUG = True
#
#
# class TestingConfig(Config):
#     TESTING = True
#
#
# class ProductionConfig(Config):
#     pass


# localhost Config Vars
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://btang:@localhost:5432/epayments'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://btang:@localhost:5432/epayments'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://btang:@localhost:5432/epayments'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
