import os
import logging.config
import pathlib

import api


# Project Directories
ROOT = pathlib.Path(api.__file__).resolve().parent.parent
LOGGING_FILE_PATH = ROOT / "logging.cfg"


def setup_app_logging(*, logging_config_file: pathlib.Path) -> None:
    logging.config.fileConfig(logging_config_file)


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
