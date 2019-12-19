import os

import mock
import pytest
from sqlalchemy_utils import create_database, database_exists

from api.app import create_app
from api.config import TestingConfig
from api.persistence import core


@pytest.fixture
def _db():
    db_url = TestingConfig.SQLALCHEMY_DATABASE_URI
    if not database_exists(db_url):
        create_database(db_url)
    # alembic can be configured through the configuration file. For testing
    # purposes 'env.py' also checks the 'ALEMBIC_DB_URI' variable first.
    engine = core.create_db_engine_from_config(config=TestingConfig())
    evars = {'ALEMBIC_DB_URI': db_url}
    with mock.patch.dict(os.environ, evars):
        core.run_migrations()

    yield engine


@pytest.fixture
def _db_session(_db):
    """ Create DB session for testing.
    """
    session = core.create_db_session(engine=_db)
    yield session


@pytest.fixture
def app(_db_session):
    app = create_app(
        config_object=TestingConfig(), db_session=_db_session).app
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client  # Has to be yielded to access session cookies
