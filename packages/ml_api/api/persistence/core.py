import logging

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from api.config import Config

_logger = logging.getLogger(__name__)

# Base class for SQLAlchemy models
Base = declarative_base()


def create_db_engine_from_config(*, config: Config) -> Engine:
    """The Engine is the starting point for any SQLAlchemy application.

    It’s “home base” for the actual database and its DBAPI, delivered to the SQLAlchemy
    application through a connection pool and a Dialect, which describes how to talk to
    a specific kind of database / DBAPI combination.
    """

    engine = create_engine(config.SQLALCHEMY_DATABASE_URI,)

    _logger.info(f"creating DB conn with URI: {config.SQLALCHEMY_DATABASE_URI}")
    return engine


def create_db_session(*, engine: Engine) -> scoped_session:
    """Broadly speaking, the Session establishes all conversations with the database.

     It represents a “holding zone” for all the objects which you’ve loaded or
     associated with it during its lifespan.
     """
    return scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine,),
    )


def init_database(app: Flask, config: Config, db_session=None) -> None:
    """Connect to the database and attach DB session to the app."""

    if not db_session:
        engine = create_db_engine_from_config(config=config)
        db_session = create_db_session(engine=engine)

    app.db_session = db_session

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
