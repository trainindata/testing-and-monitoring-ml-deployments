import os

from unittest import mock
import pytest
from gradient_boosting_model.processing.data_management import load_dataset
from sqlalchemy_utils import create_database, database_exists

from api.app import create_app
from api.config import TestingConfig
from api.persistence import core


@pytest.fixture(scope='session')
def _db():
    db_url = TestingConfig.SQLALCHEMY_DATABASE_URI
    if not database_exists(db_url):
        create_database(db_url)
    # alembic can be configured through the configuration file. For testing
    # purposes 'env.py' also checks the 'ALEMBIC_DB_URI' variable first.
    engine = core.create_db_engine_from_config(config=TestingConfig())
    evars = {"ALEMBIC_DB_URI": db_url}
    with mock.patch.dict(os.environ, evars):
        core.run_migrations()

    yield engine


@pytest.fixture(scope='session')
def _db_session(_db):
    """ Create DB session for testing.
    """
    session = core.create_db_session(engine=_db)
    yield session


@pytest.fixture(scope='session')
def app(_db_session):
    app = create_app(config_object=TestingConfig(), db_session=_db_session).app
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client  # Has to be yielded to access session cookies


@pytest.fixture
def test_inputs_df():
    # Load the gradient boosting test dataset which
    # is included in the model package
    test_inputs_df = load_dataset(file_name="test.csv")
    return test_inputs_df.copy(deep=True)
