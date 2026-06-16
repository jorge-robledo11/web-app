"""
Tests de estructura del dashboard.

Las verificaciones completas de métricas reales, estado vacío,
orden de secciones y accesos rápidos están en:
tests/integration/dashboard/test_dashboard.py

Estos tests requieren PostgreSQL disponible y seed aplicado.
"""

import pytest


@pytest.mark.asyncio
async def test_dashboard_ok(async_client):
	"""
	Verifica que GET / retorna el dashboard con sidebar y métricas reales.
	Requiere BD disponible con seed de propiedades aplicado.
	"""
	response = await async_client.get('/')

	assert response.status_code == 200
	html = response.text

	assert 'sidebar' in html
	assert 'navbar' in html
	assert 'tarjeta-metrica' in html
	assert 'Propiedades disponibles' in html
	assert 'Propiedades rentadas' in html
	assert 'Ingresos' in html
	assert 'Vencidos' in html
	assert 'No disponible' in html
