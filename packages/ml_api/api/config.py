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
    ENV = os.getenv("FLASK_ENV", "production")
    SERVER_PORT = int(os.getenv("SERVER_PORT", 5000))
    SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", logging.INFO)


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"  # do not use in production!
    LOGGING_LEVEL = logging.DEBUG


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    LOGGING_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    pass


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
