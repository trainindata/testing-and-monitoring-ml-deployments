from api.app import create_app


class ProductionConfig:
    DEBUG = True


application = create_app(
    config_object=ProductionConfig)


if __name__ == '__main__':
    application.run()