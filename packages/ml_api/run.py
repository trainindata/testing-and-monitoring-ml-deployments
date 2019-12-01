from api.app import create_app
from api.config import DevelopmentConfig, setup_app_logging


_config = DevelopmentConfig()

# setup logging as early as possible
setup_app_logging(config=_config)
application = create_app(config_object=_config).app


if __name__ == "__main__":
    application.run(port=_config.SERVER_PORT, host=_config.SERVER_HOST)
