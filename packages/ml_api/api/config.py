import logging
import os
import pathlib
import sys

import api


# logging format
FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s —" "%(funcName)s:%(lineno)d — %(message)s"
)

# Project Directories
ROOT = pathlib.Path(api.__file__).resolve().parent.parent


class Config:
    DEBUG = False
    TESTING = False
    ENV = os.environ.get("FLASK_ENV", "production")
    SERVER_PORT = os.environ.get("SERVER_PORT", 5000)
    SERVER_HOST = os.environ.get("SERVER_HOST", "0.0.0.0")
    LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", logging.INFO)

    # DB config matches docker container
    DB_USER = os.environ.get('DB_USER', 'user')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
    DB_PORT = os.environ.get('DB_PORT', 6609)
    DB_HOST = os.environ.get('DB_HOST', '0.0.0.0')
    DB_NAME = os.environ.get('DB_NAME', 'ml_api_dev')
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:"
        f"{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"  # do not use in production!
    LOGGING_LEVEL = logging.DEBUG


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    LOGGING_LEVEL = logging.DEBUG

    # DB config matches test docker container
    DB_USER = os.environ.get('DB_USER', 'test_user')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
    DB_PORT = os.environ.get('DB_PORT', 6608)
    DB_HOST = os.environ.get('DB_HOST', '0.0.0.0')
    DB_NAME = 'ml_api_test'
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:"
        f"{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class ProductionConfig(Config):
    DB_USER = os.environ.get('DB_USER', 'user')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
    DB_PORT = os.environ.get('DB_PORT', 6609)
    DB_HOST = os.environ.get('DB_HOST', 'database')
    DB_NAME = os.environ.get('DB_NAME', 'ml_api')
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
    root = logging.getLogger()
    root.setLevel(config.LOGGING_LEVEL)
    root.addHandler(get_console_handler())
    root.propagate = False


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
