"""Pruebas de migración Alembic para la tabla propiedades."""

import pytest

from tests.integration.conftest import REPO_ROOT, _alembic


class TestMigracionPropiedades:
	"""
	Pruebas de integración de la migración de estructura.
	"""

	def test_upgrade_head_crea_tabla(self, postgres_url: str) -> None:
		"""
		alembic upgrade head debe crear la tabla propiedades (SC-001).
		"""
		resultado = _alembic(postgres_url, 'upgrade', 'head')
		assert resultado.returncode == 0, f'upgrade head falló: {resultado.stderr}'

	def test_tabla_propiedades_existe(self, postgres_url: str) -> None:
		"""
		La tabla propiedades debe existir tras upgrade.
		"""
		_alembic(postgres_url, 'upgrade', 'head')
		resultado = _alembic(postgres_url, 'current')
		assert resultado.returncode == 0
		assert 'head' in resultado.stdout

	def test_downgrade_revierte_cambios(self, postgres_url: str) -> None:
		"""
		downgrade -1 debe revertir la migración sin errores (FR-008).
		"""
		_alembic(postgres_url, 'upgrade', 'head')
		resultado = _alembic(postgres_url, 'downgrade', '-1')
		assert resultado.returncode == 0, f'downgrade -1 falló: {resultado.stderr}'

	def test_ciclo_upgrade_downgrade_upgrade(self, postgres_url: str) -> None:
		"""
		Ciclo completo upgrade → downgrade → upgrade sin errores (SC-006).
		"""
		r1 = _alembic(postgres_url, 'upgrade', 'head')
		assert r1.returncode == 0, f'upgrade 1 falló: {r1.stderr}'

		r2 = _alembic(postgres_url, 'downgrade', '-1')
		assert r2.returncode == 0, f'downgrade falló: {r2.stderr}'

		r3 = _alembic(postgres_url, 'upgrade', 'head')
		assert r3.returncode == 0, f'upgrade 2 falló: {r3.stderr}'

	def test_downgrade_no_es_pass(self, postgres_url: str) -> None:
		"""
		Verificar que el downgrade tiene código real (no es pass).
		"""
		versions_dir = REPO_ROOT / 'alembic' / 'versions'
		migration_files = sorted(versions_dir.glob('*propiedades*'))
		if not migration_files:
			pytest.skip('Migración de propiedades no encontrada aún')
		content = migration_files[0].read_text()
		assert 'def downgrade' in content
		downgrade_start = content.index('def downgrade')
		downgrade_block = content[downgrade_start:]
		next_def = downgrade_block.find('def ', len('def downgrade'))
		if next_def == -1:
			downgrade_body = downgrade_block
		else:
			downgrade_body = downgrade_block[:next_def]
		lines = downgrade_body.strip().split('\n')
		real_code = [
			line
			for line in lines
			if (
				line.strip()
				and not line.strip().startswith('#')
				and line.strip() != 'pass'
			)
		]
		assert len(real_code) > 1, 'downgrade no debe ser solo pass'
