"""Tests de humo para GET /health."""

from unittest.mock import AsyncMock

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_session
from app.main import app


@pytest.mark.asyncio
async def test_health_ok(async_client):
    """Verifica que /health retorna 200 cuando la base de datos responde."""
    mock_session = AsyncMock()
    mock_session.execute = AsyncMock()

    async def override_get_session():
        yield mock_session

    app.dependency_overrides[get_session] = override_get_session

    try:
        response = await async_client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok", "database": "ok"}
    finally:
        app.dependency_overrides.pop(get_session, None)


@pytest.mark.asyncio
async def test_health_db_unavailable(async_client):
    """Verifica que /health retorna 503 cuando la base de datos no responde."""
    mock_session = AsyncMock()
    mock_session.execute = AsyncMock(side_effect=SQLAlchemyError())

    async def override_get_session():
        yield mock_session

    app.dependency_overrides[get_session] = override_get_session

    try:
        response = await async_client.get("/health")
        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "error"
        assert data["database"] == "unavailable"
        assert "detail" in data
    finally:
        app.dependency_overrides.pop(get_session, None)
