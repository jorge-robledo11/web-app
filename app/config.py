"""Configuración central de la aplicación Realtor."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Parámetros de entorno validados con pydantic-settings."""

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        frozen=True,
    )

    DATABASE_URL: str = (
        'postgresql+asyncpg://realtor_dev:realtor_dev@localhost:5432/realtor_dev'
    )
    APP_ENV: str = 'development'
    LOG_LEVEL: str = 'INFO'


settings = Settings()
