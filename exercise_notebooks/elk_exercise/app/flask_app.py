import logging

from flask import Flask

gunicorn_error_logger = logging.getLogger('gunicorn.error')
gunicorn_error_logger.setLevel(logging.DEBUG)


def index():
    gunicorn_error_logger.info('hello')
    return 'home'


def create_app():
    main_app = Flask(__name__)
    main_app.add_url_rule('/', 'index', index)

    return main_app
