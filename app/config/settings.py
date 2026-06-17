"""
Settings runtime de la aplicación.

Prioridad de configuración:

1. Valores pasados directamente a Settings(...)
2. Variables de entorno reales del sistema
3. Archivo YAML config/app.yaml
4. Secrets de archivo, si se configuran
"""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from pydantic_settings import (
	BaseSettings,
	PydanticBaseSettingsSource,
	SettingsConfigDict,
	YamlConfigSettingsSource,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_FILE = PROJECT_ROOT / 'config' / 'app.yaml'


class PathSettings(BaseModel):
	"""
	Rutas declarativas usadas por la aplicación.
	"""

	model_config = ConfigDict(frozen=True)

	templates_dir: Path
	static_dir: Path


class Settings(BaseSettings):
	"""
	Configuración runtime cargada desde YAML y variables de entorno reales.
	"""

	model_config = SettingsConfigDict(
		env_nested_delimiter='__',
		case_sensitive=False,
		extra='ignore',
		frozen=True,
		yaml_file=CONFIG_FILE,
	)

	app_name: str = Field(
		validation_alias=AliasChoices('app_name', 'APP_NAME'),
	)
	environment: Literal['development', 'test', 'production'] = Field(
		validation_alias=AliasChoices('environment', 'ENVIRONMENT', 'APP_ENV'),
	)
	debug: bool = Field(
		validation_alias=AliasChoices('debug', 'DEBUG'),
	)
	log_level: str = Field(
		validation_alias=AliasChoices('log_level', 'LOG_LEVEL'),
	)
	database_url: str = Field(
		validation_alias=AliasChoices('database_url', 'DATABASE_URL'),
	)
	static_url: str = Field(
		validation_alias=AliasChoices('static_url', 'STATIC_URL'),
	)
	paths: PathSettings

	@classmethod
	def settings_customise_sources(
		cls,
		settings_cls: type[BaseSettings],
		init_settings: PydanticBaseSettingsSource,
		env_settings: PydanticBaseSettingsSource,
		dotenv_settings: PydanticBaseSettingsSource,
		file_secret_settings: PydanticBaseSettingsSource,
	) -> tuple[PydanticBaseSettingsSource, ...]:
		"""
		Define fuentes de configuración y su prioridad.

		No se usa archivo .env. Solo se aceptan variables de entorno reales
		del sistema y el archivo YAML declarativo config/app.yaml.
		"""
		del dotenv_settings

		sources: list[PydanticBaseSettingsSource] = [
			init_settings,
			env_settings,
		]

		if CONFIG_FILE.exists():
			sources.append(YamlConfigSettingsSource(settings_cls))

		return tuple(sources) + (file_secret_settings,)


@lru_cache
def get_settings() -> Settings:
	"""
	Devuelve Settings cacheado.
	"""
	return Settings()