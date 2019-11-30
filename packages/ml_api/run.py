from api.app import create_app
from config import DevelopmentConfig

_config = DevelopmentConfig()
application = create_app(config_object=_config).app


if __name__ == '__main__':
    application.run(port=_config.SERVER_PORT)
