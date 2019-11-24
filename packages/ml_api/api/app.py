import connexion


app = connexion.FlaskApp(__name__, specification_dir='openapi/')
app.add_api('my_api.yaml')


from flask import Flask

from api.config import get_logger


_logger = get_logger(logger_name=__name__)


def create_app(*, config_object) -> Flask:
    """Create a flask app instance."""

    flask_app = Flask('ml_api')
    flask_app.config.from_object(config_object)
    app = connexion.FlaskApp('ml_api', specification_dir='openapi/')
    app.add_api('api.yaml')

    # import blueprints
    from api.controller import prediction_app
    flask_app.register_blueprint(prediction_app)
    _logger.debug('Application instance created')

    return app