import prometheus_client
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from api.app import create_app
from api.config import DevelopmentConfig, setup_app_logging

import logging
from logging.config import fileConfig


_config = DevelopmentConfig()
setup_app_logging(config=_config)
main_app = create_app(config_object=_config).app


application = DispatcherMiddleware(
        app=main_app.wsgi_app,
        mounts={'/metrics': prometheus_client.make_wsgi_app()}
    )



if __name__ == "__main__":
    main_app.run(port=_config.SERVER_PORT, host=_config.SERVER_HOST)
