"""
Estructuras tipadas del contexto del dashboard.

Estos TypedDict describen el contrato interno entre el servicio y
los templates Jinja2. No son DTOs HTTP; por eso se usa TypedDict
de stdlib en lugar de Pydantic.
"""

from typing import NotRequired, TypedDict


class MetricaDashboard(TypedDict):
	"""
	Métrica renderizada en una tarjeta de KPI.
	"""

	label: str
	valor: int
	icono: str
	estado: str
	marcador: NotRequired[str]
	tendencia: NotRequired[dict[str, str]]


class AccesoDashboard(TypedDict):
	"""
	Acceso rápido renderizado en la home.
	"""

	icono: str
	label: str
	url: str


class ActividadDashboard(TypedDict):
	"""
	Ítem de actividad reciente.
	"""

	tipo: str
	descripcion: str
	fecha: str
	badge_variante: str
	estado: str


class MetricasPropiedades(TypedDict):
	"""
	Conteos de propiedades usados por el dashboard.
	"""

	disponibles: int
	rentadas: int
	total: int


class ContextoDashboard(TypedDict):
	"""
	Contexto completo esperado por dashboard.html.
	"""

	metricas: list[MetricaDashboard]
	accesos: list[AccesoDashboard]
	actividad: list[ActividadDashboard]
	actividad_estado: str
	vacio: bool
