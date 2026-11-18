"""Tests for centralized application settings."""

from pathlib import Path

import pytest
from app.core.config import ENV_FILE_PATH, Settings
from pydantic import ValidationError


def test_settings_use_safe_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    """Settings use safe local values when environment values are absent."""
    monkeypatch.delenv("KNOWCAST_APP_ENV", raising=False)
    monkeypatch.delenv("KNOWCAST_LOG_LEVEL", raising=False)

    settings = Settings(_env_file=None)

    assert settings.app_env == "development"
    assert settings.log_level == "INFO"


def test_settings_read_environment_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    """Environment variables override the safe defaults."""
    monkeypatch.setenv("KNOWCAST_APP_ENV", "test")
    monkeypatch.setenv("KNOWCAST_LOG_LEVEL", "DEBUG")

    settings = Settings(_env_file=None)

    assert settings.app_env == "test"
    assert settings.log_level == "DEBUG"


def test_settings_read_values_from_env_file(tmp_path: Path) -> None:
    """Pydantic settings can read the local environment-file format."""
    env_file = tmp_path / ".env"
    env_file.write_text(
        "KNOWCAST_APP_ENV=test\nKNOWCAST_LOG_LEVEL=WARNING\n",
        encoding="utf-8",
    )

    settings = Settings(_env_file=env_file)

    assert settings.app_env == "test"
    assert settings.log_level == "WARNING"


def test_env_file_path_points_to_repository_root() -> None:
    """The configured environment file location does not depend on the working directory."""
    repository_root = Path(__file__).resolve().parents[4]

    assert ENV_FILE_PATH == repository_root / ".env"


def test_invalid_settings_hide_input_values(monkeypatch: pytest.MonkeyPatch) -> None:
    """Validation errors identify invalid settings without echoing their input value."""
    secret_like_value = "do-not-show-this-value"
    monkeypatch.delenv("KNOWCAST_APP_ENV", raising=False)
    monkeypatch.setenv("KNOWCAST_LOG_LEVEL", secret_like_value)

    with pytest.raises(ValidationError) as error:
        Settings(_env_file=None)

    error_message = str(error.value)
    assert "log_level" in error_message
    assert secret_like_value not in error_message
