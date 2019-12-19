import os

from alembic import context
from sqlalchemy import engine_from_config, pool

# Import the models so the changes in them are automatically reflected in the
# generated migrations.
from api.persistence import models  # noqa
from api.config import DevelopmentConfig as user_config
from api.persistence.core import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
database_url = os.environ.get("ALEMBIC_DB_URI", user_config.SQLALCHEMY_DATABASE_URI)
config.set_main_option("sqlalchemy.url", database_url)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not a user_ratings, though a user_ratings is acceptable
    here as well.  By skipping the user_ratings creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create a user_ratings
    and associate a connection with the context.
    """
    alembic_config = config.get_section(config.config_ini_section)
    connectable = engine_from_config(
        alembic_config, prefix="sqlalchemy.", poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
