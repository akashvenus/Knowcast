"""Disposable PostgreSQL migration lifecycle verification."""

import os
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from app.db.base import Base
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import IntegrityError

pytestmark = pytest.mark.integration


def _verify_database_constraints(engine) -> None:
    """Exercise uniqueness and owned-row cascades against PostgreSQL."""
    user_id = uuid4()
    with engine.begin() as connection:
        connection.execute(
            text("INSERT INTO users (id, email) VALUES (:id, :email)"),
            {"id": user_id, "email": "migration-test@example.invalid"},
        )

    with pytest.raises(IntegrityError):
        with engine.begin() as connection:
            connection.execute(
                text("INSERT INTO users (id, email) VALUES (:id, :email)"),
                {"id": uuid4(), "email": "migration-test@example.invalid"},
            )

    source_id = uuid4()
    newsletter_id = uuid4()
    with engine.begin() as connection:
        connection.execute(
            text(
                "INSERT INTO sources (id, user_id, provider, name, ingestion_type) "
                "VALUES (:id, :user_id, 'test', 'test', 'url')"
            ),
            {"id": source_id, "user_id": user_id},
        )
        connection.execute(
            text(
                "INSERT INTO newsletters (id, source_id, title, original_url) "
                "VALUES (:id, :source_id, 'test', 'https://example.invalid/test')"
            ),
            {"id": newsletter_id, "source_id": source_id},
        )
        connection.execute(text("DELETE FROM users WHERE id = :id"), {"id": user_id})
        assert (
            connection.scalar(
                text("SELECT count(*) FROM sources WHERE id = :id"), {"id": source_id}
            )
            == 0
        )
        assert (
            connection.scalar(
                text("SELECT count(*) FROM newsletters WHERE id = :id"),
                {"id": newsletter_id},
            )
            == 0
        )


def test_migration_upgrade_downgrade_and_reupgrade() -> None:
    database_url = os.getenv("KNOWCAST_TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("Set KNOWCAST_TEST_DATABASE_URL to a disposable knowcast_test database.")

    parsed_url = make_url(database_url)
    assert parsed_url.database == "knowcast_test", "Refusing to migrate a non-test database."
    assert parsed_url.host in {"localhost", "127.0.0.1"}, "Test database must be local."

    os.environ["KNOWCAST_DATABASE_URL"] = database_url
    config = Config("backend/alembic.ini")
    config.set_main_option("script_location", "backend/migrations")
    engine = create_engine(database_url)
    expected_tables = set(Base.metadata.tables)

    try:
        command.upgrade(config, "head")
        assert expected_tables <= set(inspect(engine).get_table_names())
        _verify_database_constraints(engine)

        command.upgrade(config, "head")
        assert expected_tables <= set(inspect(engine).get_table_names())

        command.downgrade(config, "base")
        assert not expected_tables.intersection(inspect(engine).get_table_names())

        command.upgrade(config, "head")
        assert expected_tables <= set(inspect(engine).get_table_names())
    finally:
        engine.dispose()
        os.environ.pop("KNOWCAST_DATABASE_URL", None)
