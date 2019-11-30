import logging

import connexion

_logger = logging.getLogger(__name__)


def create_app(*, config_object) -> connexion.App:
    """Create a flask app instance."""

    connexion_app = connexion.App(
        __name__,
        debug=config_object.DEBUG,
        specification_dir='spec/')
    flask_app = connexion_app.app
    flask_app.config.from_object(config_object)
    connexion_app.add_api('api.yaml')

    _logger.debug('Application instance created')

    return connexion_app
