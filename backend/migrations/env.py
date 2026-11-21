"""Alembic environment bound to application settings and model metadata."""

from logging.config import fileConfig

from alembic import context
from app import models  # noqa: F401
from app.core.config import Settings
from app.db.base import Base
from sqlalchemy import create_engine, pool

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_database_url() -> str:
    """Read the database URL without putting credentials in Alembic config."""
    database_url = Settings().database_url
    if database_url is None:
        raise RuntimeError("KNOWCAST_DATABASE_URL must be set to run database migrations.")
    return str(database_url)


def run_migrations_offline() -> None:
    """Render migration SQL without opening a database connection."""
    context.configure(
        url=get_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations using a short-lived synchronous engine."""
    connectable = create_engine(get_database_url(), poolclass=pool.NullPool, pool_pre_ping=True)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()
    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
