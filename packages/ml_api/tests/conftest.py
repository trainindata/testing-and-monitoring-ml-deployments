import mock
import os
import pytest

from sqlalchemy_utils import drop_database

from api.config import TestingConfig
from api.app import create_app
from api.persistence import core


@pytest.fixture
def _db_session(postgresql_proc):
    """ Create an in-memory DB session for testing.
    """
    # alembic can be configured through the configuration file. For testing
    # purposes 'env.py' also checks the 'ALEMBIC_DB_URI' variable first.
    db_url = TestingConfig.SQLALCHEMY_DATABASE_URI
    engine = core.create_db_engine_from_config(config=TestingConfig)
    evars = {'ALEMBIC_DB_URI': db_url}
    with mock.patch.dict(os.environ, evars):  # type: ignore
        core.run_migrations()

    session = core.create_db_session(engine)
    yield session

    # clean up
    drop_database(db_url)


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
