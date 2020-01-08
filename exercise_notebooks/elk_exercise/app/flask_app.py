import logging

from flask import Flask

logging.basicConfig(filename="logFile.txt",
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

_logger = logging.getLogger(__name__)


def index():
    _logger.warning('index')
    return 'home'


def create_app():
    main_app = Flask(__name__)
    main_app.add_url_rule('/', 'index', index)

    return main_app
