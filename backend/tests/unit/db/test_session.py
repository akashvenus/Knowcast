"""Tests for optional database configuration and request sessions."""

from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from app.core.config import Settings
from app.db.session import create_session_factory, get_db_session
from fastapi import HTTPException
from pydantic import ValidationError


def test_database_url_is_optional_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("KNOWCAST_DATABASE_URL", raising=False)
    assert Settings(_env_file=None).database_url is None


def test_valid_database_url_can_be_loaded(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(
        "KNOWCAST_DATABASE_URL",
        "postgresql+psycopg://user:password@localhost:5432/knowcast_test",
    )
    settings = Settings(_env_file=None)
    assert settings.database_url is not None
    assert "knowcast_test" in str(settings.database_url)


def test_invalid_database_url_hides_input(monkeypatch: pytest.MonkeyPatch) -> None:
    secret = "postgresql+psycopg://alice:secret-value@localhost:bad/db"
    monkeypatch.setenv("KNOWCAST_DATABASE_URL", secret)
    with pytest.raises(ValidationError) as error:
        Settings(_env_file=None)
    assert "secret-value" not in str(error.value)


def test_engine_is_created_without_connecting() -> None:
    factory = create_session_factory(
        Settings(
            _env_file=None,
            database_url="postgresql+psycopg://user:pass@127.0.0.1:1/db",
        ).database_url
    )
    assert factory is not None
    assert factory.kw["bind"].engine.url.database == "db"
    factory.kw["bind"].engine.dispose()


def test_missing_database_returns_generic_service_error() -> None:
    request = SimpleNamespace(
        app=SimpleNamespace(state=SimpleNamespace(database_session_factory=None))
    )
    with pytest.raises(HTTPException) as error:
        next(get_db_session(request))
    assert error.value.status_code == 503
    assert error.value.detail == "Database is not configured."


def test_request_session_closes_after_use() -> None:
    session = Mock()
    request = SimpleNamespace(
        app=SimpleNamespace(
            state=SimpleNamespace(database_session_factory=Mock(return_value=session))
        )
    )
    generator = get_db_session(request)
    assert next(generator) is session
    with pytest.raises(StopIteration):
        next(generator)
    session.close.assert_called_once()
