"""
Rutas internas calculadas del proyecto.
"""

from pathlib import Path

from pydantic import BaseModel, ConfigDict

from app.config.settings import PROJECT_ROOT, Settings, get_settings


class ProjectPaths(BaseModel):
	"""
	Rutas internas usadas por la aplicación.

	Estas rutas no representan configuración externa de negocio. Son rutas
	derivadas del layout del repo, con soporte para overrides declarativos
	desde Settings cuando haga falta.
	"""

	model_config = ConfigDict(frozen=True)

	project_root: Path
	app_dir: Path
	templates_dir: Path
	static_dir: Path

	@classmethod
	def from_settings(cls, settings: Settings | None = None) -> 'ProjectPaths':
		"""
		Construye rutas internas a partir de Settings.
		"""
		resolved_settings = settings or get_settings()

		project_root = PROJECT_ROOT
		app_dir = project_root / 'app'

		return cls(
			project_root=project_root,
			app_dir=app_dir,
			templates_dir=_resolve_path(
				project_root,
				resolved_settings.paths.templates_dir,
				app_dir / 'templates',
			),
			static_dir=_resolve_path(
				project_root,
				resolved_settings.paths.static_dir,
				app_dir / 'static',
			),
		)


def _resolve_path(root_dir: Path, configured: Path | None, default: Path) -> Path:
	"""
	Resuelve una ruta configurada o devuelve el default.

	Las rutas relativas se interpretan desde la raíz del repo.
	"""
	if configured is None:
		return default

	if configured.is_absolute():
		return configured

	return root_dir / configured


def get_paths(settings: Settings | None = None) -> ProjectPaths:
	"""
	Devuelve rutas internas del proyecto.
	"""
	return ProjectPaths.from_settings(settings)
