"""Tests de humo para GET / dashboard."""

import pytest


@pytest.mark.asyncio
async def test_dashboard_ok(async_client):
    """Verifica que GET / retorna el dashboard con sidebar y 3 tarjetas."""
    response = await async_client.get("/")

    assert response.status_code == 200
    html = response.text

    assert 'class="sidebar"' in html or "sidebar" in html
    assert 'class="navbar"' in html or "navbar" in html
    assert html.count("tarjeta-metrica") >= 3
    assert "Propiedades activas" in html
    assert "124" in html
