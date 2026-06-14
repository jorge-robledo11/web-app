"""Pruebas de schemas Pydantic v2 para propiedades."""

import pytest
from pydantic import ValidationError

from app.modules.propiedades.schemas import PropiedadIn, PropiedadOut


class TestPropiedadIn:
    """Pruebas del DTO de entrada PropiedadIn."""

    def test_es_frozen(self) -> None:
        """El DTO debe ser inmutable (frozen=True)."""
        datos = {
            'titulo': 'Casa Test',
            'direccion': 'Calle 123',
            'ciudad': 'Miami',
            'precio_mensual': 2500.00,
            'habitaciones': 2,
            'banos': 1,
            'area': 850,
            'estado': 'disponible',
            'imagen': 'https://example.com/img.jpg',
        }
        prop = PropiedadIn(**datos)  # type: ignore[arg-type]
        with pytest.raises(ValidationError):
            prop.titulo = 'otro'  # type: ignore[misc]

    def test_estado_invalido_rechazado(self) -> None:
        """Debe rechazar un estado fuera del catálogo (FR-003)."""
        datos = {
            'titulo': 'Casa Test',
            'direccion': 'Calle 123',
            'ciudad': 'Miami',
            'precio_mensual': 2500.00,
            'habitaciones': 2,
            'banos': 1,
            'area': 850,
            'estado': 'vendida',
            'imagen': 'https://example.com/img.jpg',
        }
        with pytest.raises(ValidationError):
            PropiedadIn(**datos)  # type: ignore[arg-type]

    def test_estados_validos_aceptados(self) -> None:
        """Debe aceptar los 4 estados del catálogo."""
        for estado in ('disponible', 'rentada', 'mantenimiento', 'inactiva'):
            datos = {
                'titulo': 'Casa Test',
                'direccion': 'Calle 123',
                'ciudad': 'Miami',
                'precio_mensual': 2500.00,
                'habitaciones': 2,
                'banos': 1,
                'area': 850,
                'estado': estado,
                'imagen': 'https://example.com/img.jpg',
            }
            prop = PropiedadIn(**datos)  # type: ignore[arg-type]
            assert prop.estado == estado

    def test_precio_mensual_debe_ser_positivo(self) -> None:
        """El precio mensual debe ser mayor a 0."""
        datos = {
            'titulo': 'Casa Test',
            'direccion': 'Calle 123',
            'ciudad': 'Miami',
            'precio_mensual': -100.00,
            'habitaciones': 2,
            'banos': 1,
            'area': 850,
            'estado': 'disponible',
            'imagen': 'https://example.com/img.jpg',
        }
        with pytest.raises(ValidationError):
            PropiedadIn(**datos)  # type: ignore[arg-type]

    def test_campos_obligatorios(self) -> None:
        """Todos los campos deben ser obligatorios."""
        with pytest.raises(ValidationError):
            PropiedadIn(titulo='Solo título')  # type: ignore[call-arg]

    def test_sin_id_ni_timestamps(self) -> None:
        """PropiedadIn no debe aceptar id, created_at ni updated_at."""
        datos = {
            'id': '00000000-0000-0000-0000-000000000001',
            'titulo': 'Casa Test',
            'direccion': 'Calle 123',
            'ciudad': 'Miami',
            'precio_mensual': 2500.00,
            'habitaciones': 2,
            'banos': 1,
            'area': 850,
            'estado': 'disponible',
            'imagen': 'https://example.com/img.jpg',
        }
        with pytest.raises(ValidationError):
            PropiedadIn(**datos)  # type: ignore[arg-type]


class TestPropiedadOut:
    """Pruebas del DTO de salida PropiedadOut."""

    def test_incluye_id_y_timestamps(self) -> None:
        """PropiedadOut debe incluir id, created_at y updated_at."""
        datos = {
            'id': '00000000-0000-0000-0000-000000000001',
            'titulo': 'Casa Test',
            'direccion': 'Calle 123',
            'ciudad': 'Miami',
            'precio_mensual': 2500.00,
            'habitaciones': 2,
            'banos': 1,
            'area': 850,
            'estado': 'disponible',
            'imagen': 'https://example.com/img.jpg',
            'created_at': '2026-01-01T00:00:00Z',
            'updated_at': '2026-01-01T00:00:00Z',
        }
        prop = PropiedadOut(**datos)  # type: ignore[arg-type]
        assert prop.id is not None
        assert prop.created_at is not None
        assert prop.updated_at is not None

    def test_es_frozen(self) -> None:
        """El DTO debe ser inmutable."""
        datos = {
            'id': '00000000-0000-0000-0000-000000000001',
            'titulo': 'Casa Test',
            'direccion': 'Calle 123',
            'ciudad': 'Miami',
            'precio_mensual': 2500.00,
            'habitaciones': 2,
            'banos': 1,
            'area': 850,
            'estado': 'disponible',
            'imagen': 'https://example.com/img.jpg',
            'created_at': '2026-01-01T00:00:00Z',
            'updated_at': '2026-01-01T00:00:00Z',
        }
        prop = PropiedadOut(**datos)  # type: ignore[arg-type]
        with pytest.raises(ValidationError):
            prop.titulo = 'otro'  # type: ignore[misc]
