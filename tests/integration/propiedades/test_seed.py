"""Pruebas de la carga inicial de propiedades (seed)."""


import pytest

from tests.integration.conftest import REPO_ROOT, _alembic, _seed


class TestSeedPropiedades:
    """Pruebas de integración del script de seed."""

    def test_primera_ejecucion_deja_10_propiedades(
        self, postgres_url: str,
    ) -> None:
        """La primera ejecución debe crear 10 propiedades (FR-010, SC-002)."""
        _alembic(postgres_url, "upgrade", "head")
        resultado = _seed(postgres_url)
        assert resultado.returncode == 0, f"seed falló: {resultado.stderr}"
        assert "10" in resultado.stdout

    def test_segunda_ejecucion_mantiene_cardinalidad(
        self, postgres_url: str,
    ) -> None:
        """Dos ejecuciones deben mantener 10 propiedades (FR-005, SC-003)."""
        _alembic(postgres_url, "upgrade", "head")
        _seed(postgres_url)  # primera
        resultado = _seed(postgres_url)  # segunda
        assert resultado.returncode == 0
        assert "Procesadas 10" in resultado.stdout

    def test_estados_validos(self, postgres_url: str) -> None:
        """El 100% de propiedades debe tener estado del catálogo (SC-004)."""
        _alembic(postgres_url, "upgrade", "head")
        resultado = _seed(postgres_url)
        assert resultado.returncode == 0
        for estado_invalido in ("vendida", "alquilada", "reservada"):
            assert estado_invalido not in resultado.stdout.lower()

    def test_imagen_determinista(self, postgres_url: str) -> None:
        """Dos ejecuciones deben producir mismo resultado (SC-005)."""
        _alembic(postgres_url, "upgrade", "head")
        resultado1 = _seed(postgres_url)
        resultado2 = _seed(postgres_url)
        assert resultado1.returncode == 0
        assert resultado2.returncode == 0
        assert resultado1.stdout == resultado2.stdout

    def test_seed_no_importa_psycopg2(self, postgres_url: str) -> None:
        """El script de seed no debe importar psycopg2 ni psycopg (SC-009)."""
        seed_path = REPO_ROOT / "scripts" / "dev" / "seed_propiedades.py"
        if not seed_path.exists():
            pytest.skip("Script de seed no creado aún")
        content = seed_path.read_text()
        assert "import psycopg2" not in content, "import psycopg2 detectado"
        assert "import psycopg\n" not in content, "import psycopg detectado"

    def test_seed_usa_asyncpg(self, postgres_url: str) -> None:
        """El script debe usar asyncpg y create_async_engine."""
        seed_path = REPO_ROOT / "scripts" / "dev" / "seed_propiedades.py"
        if not seed_path.exists():
            pytest.skip("Script de seed no creado aún")
        content = seed_path.read_text()
        assert "create_async_engine" in content
        assert "asyncpg" in content or "DATABASE_URL" in content
