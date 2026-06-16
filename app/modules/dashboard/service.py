"""Lógica de negocio del dashboard."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.dashboard.repository import obtener_metricas


def _construir_metricas(
	disponibles: int,
	rentadas: int,
) -> list[dict[str, object]]:
	"""
	Construye la lista de métricas en orden fijo.

	Las métricas reales omiten tendencia por no tener datos históricos.
	Las métricas no operativas incluyen marcador "No disponible".
	"""
	return [
		{
			'label': 'Propiedades disponibles',
			'valor': disponibles,
			'icono': 'building-2',
			'estado': 'datos',
		},
		{
			'label': 'Propiedades rentadas',
			'valor': rentadas,
			'icono': 'check-circle-2',
			'estado': 'datos',
		},
		{
			'label': 'Ingresos',
			'valor': 0,
			'icono': 'wallet',
			'marcador': 'No disponible',
			'estado': 'datos',
		},
		{
			'label': 'Vencidos',
			'valor': 0,
			'icono': 'clock',
			'marcador': 'No disponible',
			'estado': 'datos',
		},
	]


def _accesos() -> list[dict[str, str]]:
	"""
	Accesos rápidos hardcodeados del dashboard demo.
	"""
	return [
		{'icono': 'building-2', 'label': 'Propiedades', 'url': '#'},
		{'icono': 'users', 'label': 'Inquilinos', 'url': '#'},
		{'icono': 'file-text', 'label': 'Contratos', 'url': '#'},
		{'icono': 'wallet', 'label': 'Pagos', 'url': '#'},
	]


def _actividad() -> list[dict[str, str]]:
	"""
	Actividad reciente hardcodeada de demo.
	"""
	return [
		{
			'tipo': 'propiedad',
			'descripcion': 'Nueva propiedad registrada: Av. Reforma 245, Col. Centro',
			'fecha': 'Hace 2 horas',
			'badge_variante': 'accent',
			'estado': 'datos',
		},
		{
			'tipo': 'contrato',
			'descripcion': 'Contrato por vencer: Depto. Condesa — vence en 3 días',
			'fecha': 'Hace 5 horas',
			'badge_variante': 'warning',
			'estado': 'datos',
		},
		{
			'tipo': 'pago',
			'descripcion': 'Pago recibido: $15,000 — Renta Depto. Polanco',
			'fecha': 'Ayer',
			'badge_variante': 'success',
			'estado': 'datos',
		},
	]


async def construir_contexto(session: AsyncSession) -> dict[str, object]:
	"""
	Orquesta el repositorio de dashboard y construye el contexto
	para el template dashboard.html.
	"""
	metricas_raw = await obtener_metricas(session)
	disponibles = metricas_raw['disponibles']
	rentadas = metricas_raw['rentadas']
	total = metricas_raw['total']

	return {
		'metricas': _construir_metricas(disponibles, rentadas),
		'accesos': _accesos(),
		'actividad': _actividad(),
		'actividad_estado': 'datos',
		'vacio': total == 0,
	}