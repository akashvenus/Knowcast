"""Centralized application settings loaded from environment variables."""

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

# NON-OBVIOUS: repository-root environment file path
# What it does: resolves the repository root from this config module's location.
# Why it is used here: settings find the same root .env file from any working directory.
# Related code: Settings.model_config uses ENV_FILE_PATH to load local settings.
# Simpler alternative: use ".env" directly, but that depends on the command's working directory.
ENV_FILE_PATH = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    """Application settings with safe defaults for local development."""

    app_env: Literal["development", "test", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        env_prefix="KNOWCAST_",
        hide_input_in_errors=True,
    )
