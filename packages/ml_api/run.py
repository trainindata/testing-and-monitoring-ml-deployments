from api.app import create_app
from api.config import DevelopmentConfig, setup_app_logging, LOGGING_FILE_PATH


# setup logging as early as possible
setup_app_logging(logging_config_file=LOGGING_FILE_PATH)
_config = DevelopmentConfig()
application = create_app(config_object=_config).app


if __name__ == '__main__':
    application.run(port=_config.SERVER_PORT)
