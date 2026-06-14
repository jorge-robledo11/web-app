"""Pruebas del repositorio de propiedades."""

from decimal import Decimal

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.propiedades.models import EstadoPropiedad
from app.modules.propiedades.repository import (
    crear,
    eliminar,
    listar,
    obtener_por_id,
)
from app.modules.propiedades.schemas import PropiedadIn


class TestRepositorioPropiedades:
    """Pruebas de acceso a datos para Propiedad."""

    @pytest_asyncio.fixture
    async def propiedad_in(self) -> PropiedadIn:
        """Fixture con datos válidos de entrada."""
        return PropiedadIn(
            titulo="Casa Repo Test",
            direccion="Av. Repositorio 456",
            ciudad="Miami",
            precio_mensual=Decimal("1800.00"),
            habitaciones=2,
            banos=1,
            area=700,
            estado=EstadoPropiedad.DISPONIBLE,
            imagen="https://example.com/repo.jpg",
        )

    @pytest.mark.asyncio
    async def test_crear_retorna_propiedad(
        self, async_session: AsyncSession, propiedad_in: PropiedadIn,
    ) -> None:
        """crear debe persistir y retornar una Propiedad con id."""
        prop = await crear(async_session, propiedad_in)
        assert prop.id is not None
        assert prop.titulo == "Casa Repo Test"
        assert prop.estado == EstadoPropiedad.DISPONIBLE

    @pytest.mark.asyncio
    async def test_obtener_por_id_existente(
        self, async_session: AsyncSession, propiedad_in: PropiedadIn,
    ) -> None:
        """obtener_por_id debe encontrar una propiedad recién creada."""
        creada = await crear(async_session, propiedad_in)
        encontrada = await obtener_por_id(async_session, creada.id)
        assert encontrada is not None
        assert encontrada.id == creada.id

    @pytest.mark.asyncio
    async def test_obtener_por_id_inexistente(
        self, async_session: AsyncSession,
    ) -> None:
        """obtener_por_id debe retornar None para id inexistente."""
        import uuid
        inexistente = await obtener_por_id(async_session, uuid.uuid4())
        assert inexistente is None

    @pytest.mark.asyncio
    async def test_listar_devuelve_propiedades(
        self, async_session: AsyncSession, propiedad_in: PropiedadIn,
    ) -> None:
        """listar debe devolver al menos las propiedades creadas."""
        await crear(async_session, propiedad_in)
        todas = await listar(async_session)
        assert len(todas) >= 1
        titulos = {p.titulo for p in todas}
        assert "Casa Repo Test" in titulos

    @pytest.mark.asyncio
    async def test_eliminar_remueve_propiedad(
        self, async_session: AsyncSession, propiedad_in: PropiedadIn,
    ) -> None:
        """eliminar debe remover la propiedad y retornar True."""
        creada = await crear(async_session, propiedad_in)
        resultado = await eliminar(async_session, creada.id)
        assert resultado is True
        assert await obtener_por_id(async_session, creada.id) is None
