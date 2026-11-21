"""Tests for Celery configuration and smoke-task registration."""

import pytest
from app.core.config import Settings
from app.workers.celery_app import celery_app, create_celery_app
from app.workers.tasks import smoke_check
from pydantic import ValidationError


def test_redis_url_has_a_safe_local_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("KNOWCAST_REDIS_URL", raising=False)
    settings = Settings(_env_file=None)
    assert str(settings.redis_url) == "redis://localhost:6379/0"


def test_redis_url_can_be_overridden(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("KNOWCAST_REDIS_URL", "redis://localhost:6380/4")
    settings = Settings(_env_file=None)
    assert str(settings.redis_url) == "redis://localhost:6380/4"


def test_invalid_redis_url_does_not_echo_password(monkeypatch: pytest.MonkeyPatch) -> None:
    password = "private-redis-password"
    monkeypatch.setenv("KNOWCAST_REDIS_URL", f"redis://:{password}@localhost:bad/0")
    with pytest.raises(ValidationError) as error:
        Settings(_env_file=None)
    assert password not in str(error.value)


def test_celery_uses_redis_and_retries_until_broker_returns() -> None:
    settings = Settings(_env_file=None, redis_url="redis://localhost:6381/3")
    celery_application = create_celery_app(settings)

    assert celery_application.conf.broker_url == "redis://localhost:6381/3"
    assert celery_application.conf.result_backend == "redis://localhost:6381/3"
    assert celery_application.conf.broker_connection_retry_on_startup is True
    assert celery_application.conf.broker_connection_max_retries is None
    assert celery_application.conf.include == ["app.workers.tasks"]


def test_smoke_task_is_registered_and_returns_success() -> None:
    celery_app.loader.import_default_modules()
    registered_task = celery_app.tasks["app.workers.tasks.smoke_check"]

    assert registered_task.name == smoke_check.name
    assert smoke_check.apply().get() == {"status": "ok"}
