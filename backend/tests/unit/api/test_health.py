"""Tests for the API application and its liveness route."""

import pytest
from app.main import app, create_app
from fastapi.testclient import TestClient
from pydantic import ValidationError


def test_health_endpoint_returns_minimal_success_response() -> None:
    """The liveness route returns only a simple successful status."""
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_endpoint_does_not_connect_to_configured_database(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An unreachable database does not affect application liveness."""
    monkeypatch.setenv(
        "KNOWCAST_DATABASE_URL",
        "postgresql+psycopg://user:password@127.0.0.1:1/knowcast_test",
    )
    with TestClient(create_app()) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_endpoint_does_not_connect_to_redis(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Redis availability is not part of the infrastructure liveness check."""
    monkeypatch.setenv("KNOWCAST_REDIS_URL", "redis://127.0.0.1:1/0")
    with TestClient(create_app()) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_invalid_settings_prevent_app_creation_without_echoing_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Invalid configuration fails app creation without exposing its value."""
    invalid_value = "do-not-expose-this-value"
    monkeypatch.setenv("KNOWCAST_LOG_LEVEL", invalid_value)

    with pytest.raises(ValidationError) as error:
        create_app()

    error_message = str(error.value)
    assert "log_level" in error_message
    assert invalid_value not in error_message
