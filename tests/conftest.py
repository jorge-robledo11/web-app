"""Fixtures compartidos para tests de endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def async_client():
    """Cliente HTTP asíncrono para tests de endpoints FastAPI."""
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")
