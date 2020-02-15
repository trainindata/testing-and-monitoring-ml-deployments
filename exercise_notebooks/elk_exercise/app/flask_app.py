import logging

from flask import Flask, current_app


def index():
    current_app.logger.info('home')
    return 'home'


def create_app():
    main_app = Flask(__name__)
    main_app.add_url_rule('/', 'index', index)
    gunicorn_error_logger = logging.getLogger('gunicorn.error')
    main_app.logger.addHandler(gunicorn_error_logger)
    main_app.logger.setLevel(logging.DEBUG)

    return main_app
