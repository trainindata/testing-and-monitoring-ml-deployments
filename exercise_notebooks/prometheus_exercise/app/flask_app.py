import prometheus_client
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from app.helpers.middleware import setup_metrics


def index():
    return 'home'


def create_app():
    main_app = Flask(__name__)
    main_app.add_url_rule('/', 'index', index)
    setup_metrics(main_app)

    # Add prometheus wsgi middleware to route /metrics requests
    app = DispatcherMiddleware(main_app.wsgi_app, {
        '/metrics': prometheus_client.make_wsgi_app()
    })

    return app
