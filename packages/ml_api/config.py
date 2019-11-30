import os


class Config:
    DEBUG = False
    TESTING = False
    ENV = os.environ.get('FLASK_ENV', 'production')
    SERVER_PORT = os.environ.get('SERVER_PORT', 5000)


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'  # do not use in production!


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    pass
