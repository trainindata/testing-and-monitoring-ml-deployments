import logging
import os
import pathlib
import sys
from logging.config import fileConfig

import api

# logging format
FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s —" "%(funcName)s:%(lineno)d — %(message)s"
)

# Project Directories
ROOT = pathlib.Path(api.__file__).resolve().parent.parent

APP_NAME = 'ml_api'


class Config:
    DEBUG = False
    TESTING = False
    ENV = os.getenv("FLASK_ENV", "production")
    SERVER_PORT = int(os.getenv("SERVER_PORT", 5000))
    SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", logging.INFO)
    SHADOW_MODE_ACTIVE = os.getenv('SHADOW_MODE_ACTIVE', True)
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )
    # DB config matches docker container
    DB_USER = os.getenv("DB_USER", "user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_PORT = os.getenv("DB_PORT", 6609)
    DB_HOST = os.getenv("DB_HOST", "0.0.0.0")
    DB_NAME = os.getenv("DB_NAME", "ml_api_dev")


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"  # do not use in production!
    LOGGING_LEVEL = logging.DEBUG


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    LOGGING_LEVEL = logging.DEBUG

    # DB config matches test docker container
    DB_USER = os.getenv("DB_USER", "test_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_PORT = os.getenv("DB_PORT", 6608)
    DB_HOST = os.getenv("DB_HOST", "0.0.0.0")
    DB_NAME = "ml_api_test"
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:"
        f"{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class ProductionConfig(Config):
    DB_USER = os.getenv("DB_USER", "user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_PORT = os.getenv("DB_PORT", 6609)
    DB_HOST = os.getenv("DB_HOST", "database")
    DB_NAME = os.getenv("DB_NAME", "ml_api")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:"
        f"{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


def get_console_handler():
    """Setup console logging handler."""
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def setup_app_logging(config: Config) -> None:
    """Prepare custom logging for our application."""
    _disable_irrelevant_loggers()
    fileConfig(ROOT / 'gunicorn_logging.conf')
    logger = logging.getLogger('mlapi')
    logger.setLevel(config.LOGGING_LEVEL)


def _disable_irrelevant_loggers() -> None:
    """Disable loggers created by packages which create a lot of noise."""
    for logger_name in (
        "connexion.apis.flask_api",
        "connexion.apis.abstract",
        "connexion.decorators",
        "connexion.operation",
        "connexion.operations",
        "connexion.app",
        "openapi_spec_validator",
    ):
        logging.getLogger(logger_name).level = logging.WARNING
