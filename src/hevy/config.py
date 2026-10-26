"""Pydantic settings loaded from environment/`.env`."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="HEVY_", extra="ignore")

    api_key: str | None = None
    base_url: str = "https://api.hevyapp.com"


settings = Settings()