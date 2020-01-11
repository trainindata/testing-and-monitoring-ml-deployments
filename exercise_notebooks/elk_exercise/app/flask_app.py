import logging

from flask import Flask
from pythonjsonlogger import jsonlogger
from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.handler import LogstashFormatter
import json


_logger = logging.getLogger('logstash')

def index():
    _logger.warning(json.dumps({'home': 'here'}))
    _logger.info('hello')
    return 'home'


def create_app():
    main_app = Flask(__name__)
    main_app.add_url_rule('/', 'index', index)

    return main_app
