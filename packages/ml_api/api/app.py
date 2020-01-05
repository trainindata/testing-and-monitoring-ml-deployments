import logging

import connexion
from sqlalchemy.orm import scoped_session

from api.config import Config
from api.monitoring.middleware import setup_metrics
from api.persistence.core import init_database

_logger = logging.getLogger(__name__)


def create_app(
    *, config_object: Config, db_session: scoped_session = None
) -> connexion.App:
    """Create app instance."""

    connexion_app = connexion.App(
        __name__, debug=config_object.DEBUG, specification_dir="spec/"
    )
    flask_app = connexion_app.app
    flask_app.config.from_object(config_object)

    # Setup database
    init_database(flask_app, config=config_object, db_session=db_session)

    # Setup prometheus monitoring
    setup_metrics(flask_app)

    connexion_app.add_api("api.yaml")
    _logger.info("Application instance created")

    return connexion_app
