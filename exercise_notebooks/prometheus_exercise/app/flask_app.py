import prometheus_client
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware


def index():
    return 'home'


def create_app():
    main_app = Flask(__name__)
    main_app.add_url_rule('/', 'index', index)

    # Add prometheus wsgi middleware to route /metrics requests
    app = DispatcherMiddleware(main_app.wsgi_app, {
        '/metrics': prometheus_client.make_wsgi_app()
    })

    return app
