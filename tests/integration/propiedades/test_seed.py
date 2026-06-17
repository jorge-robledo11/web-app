"""Pruebas de la carga inicial de propiedades (seed)."""

import pytest

from tests.integration.conftest import REPO_ROOT, _alembic, _seed


class TestSeedPropiedades:
	"""
	Pruebas de integración del script de seed.
	"""

	def test_primera_ejecucion_deja_10_propiedades(
		self,
		postgres_url: str,
	) -> None:
		"""
		La primera ejecución debe crear 10 propiedades (FR-010, SC-002).
		"""
		_alembic(postgres_url, 'upgrade', 'head')
		resultado = _seed(postgres_url)
		assert resultado.returncode == 0, f'seed falló: {resultado.stderr}'
		assert '10' in resultado.stdout

	def test_segunda_ejecucion_mantiene_cardinalidad(
		self,
		postgres_url: str,
	) -> None:
		"""
		Dos ejecuciones deben mantener 10 propiedades (FR-005, SC-003).
		"""
		_alembic(postgres_url, 'upgrade', 'head')
		_seed(postgres_url)  # primera
		resultado = _seed(postgres_url)  # segunda
		assert resultado.returncode == 0
		assert 'Procesadas 10' in resultado.stdout

	def test_estados_validos(self, postgres_url: str) -> None:
		"""
		El 100% de propiedades debe tener estado del catálogo (SC-004).
		"""
		_alembic(postgres_url, 'upgrade', 'head')
		resultado = _seed(postgres_url)
		assert resultado.returncode == 0
		for estado_invalido in ('vendida', 'alquilada', 'reservada'):
			assert estado_invalido not in resultado.stdout.lower()

	def test_dos_ejecuciones_producen_mismo_resultado(
		self,
		postgres_url: str,
	) -> None:
		"""
		Dos ejecuciones deben producir el mismo resultado (SC-005).

		Las imágenes son URLs explícitas y estables, por lo que la
		salida del script no debe variar entre ejecuciones.
		"""
		_alembic(postgres_url, 'upgrade', 'head')
		resultado1 = _seed(postgres_url)
		resultado2 = _seed(postgres_url)
		assert resultado1.returncode == 0
		assert resultado2.returncode == 0
		assert resultado1.stdout == resultado2.stdout

	def test_seed_no_importa_psycopg2(self, postgres_url: str) -> None:
		"""
		El script de seed no debe importar psycopg2 ni psycopg (SC-009).
		"""
		seed_path = REPO_ROOT / 'scripts' / 'dev' / 'seed_propiedades.py'
		if not seed_path.exists():
			pytest.skip('Script de seed no creado aún')
		content = seed_path.read_text()
		assert 'import psycopg2' not in content, 'import psycopg2 detectado'
		assert 'import psycopg\n' not in content, 'import psycopg detectado'

	def test_seed_usa_asyncpg(self, postgres_url: str) -> None:
		"""
		El script debe usar asyncpg y create_async_engine.
		"""
		seed_path = REPO_ROOT / 'scripts' / 'dev' / 'seed_propiedades.py'
		if not seed_path.exists():
			pytest.skip('Script de seed no creado aún')
		content = seed_path.read_text()
		assert 'create_async_engine' in content
		assert 'asyncpg' in content or 'DATABASE_URL' in content

	# =============================================================
	# Imágenes explícitas y curadas (bugfix visual)
	# =============================================================

	def test_seed_no_usa_hashlib_para_imagenes(
		self,
		postgres_url: str,
	) -> None:
		"""
		El script de seed no debe generar imágenes con hash inventado.

		El bugfix elimina el sistema de imágenes deterministas por hash
		en favor de URLs explícitas y curadas.
		"""
		seed_path = REPO_ROOT / 'scripts' / 'dev' / 'seed_propiedades.py'
		if not seed_path.exists():
			pytest.skip('Script de seed no creado aún')
		content = seed_path.read_text()
		assert 'import hashlib' not in content, (
			'hashlib no debe importarse para imágenes'
		)
		assert 'picsum.photos' not in content, (
			'picsum.photos no debe usarse como fuente de imágenes'
		)
		# No debe existir _imagen_determinista
		assert '_imagen_determinista' not in content, (
			'La función _imagen_determinista fue eliminada en el bugfix'
		)

	def test_seed_propiedades_tienen_imagen_explicita(
		self,
		postgres_url: str,
	) -> None:
		"""
		Cada propiedad del seed debe tener una imagen explícita y curada.
		"""
		seed_path = REPO_ROOT / 'scripts' / 'dev' / 'seed_propiedades.py'
		if not seed_path.exists():
			pytest.skip('Script de seed no creado aún')
		content = seed_path.read_text()
		# Cada dict de propiedad debe contener 'imagen' con URL literal
		# Buscamos los diccionarios dentro de PROPIEDADES_MIAMI
		import re

		bloques = re.findall(r"\{[^{}]*'titulo'[^{}]*\}", content, re.DOTALL)
		# Filtrar solo bloques con URL literal (no referencias a variables)
		bloques_con_url = [
			b for b in bloques if re.search(r"'imagen'\s*:\s*'[^']+'", b)
		]
		assert len(bloques_con_url) >= 10, (
			f'Se esperaban al menos 10 propiedades con URL explícita, '
			f'hay {len(bloques_con_url)}'
		)
		for bloque in bloques_con_url:
			assert "'imagen'" in bloque, (
				f'Propiedad sin campo imagen explícito: {bloque[:80]}'
			)
			match_url = re.search(r"'imagen'\s*:\s*'([^']+)'", bloque)
			assert match_url is not None
			url = match_url.group(1)
			assert url.startswith('https://'), f'URL no absoluta: {url}'
			assert 'picsum.photos' not in url
			assert '/seed/' not in url

	def test_seed_upsert_actualiza_imagen(
		self,
		postgres_url: str,
	) -> None:
		"""
		El ON CONFLICT del UPSERT debe seguir actualizando la columna imagen.
		"""
		seed_path = REPO_ROOT / 'scripts' / 'dev' / 'seed_propiedades.py'
		if not seed_path.exists():
			pytest.skip('Script de seed no creado aún')
		content = seed_path.read_text()
		assert 'ON CONFLICT' in content
		# El bloque ON CONFLICT debe incluir SET imagen = EXCLUDED.imagen
		assert 'imagen = EXCLUDED.imagen' in content, (
			'La migración de imagen en ON CONFLICT debe estar presente'
		)

	def test_seed_persiste_imagenes_en_bd(
		self,
		postgres_url: str,
	) -> None:
		"""
		Tras ejecutar el seed, la BD debe contener imágenes explícitas
		para todas las propiedades.
		"""
		_alembic(postgres_url, 'upgrade', 'head')
		resultado = _seed(postgres_url)
		assert resultado.returncode == 0, resultado.stderr

		import asyncio

		import asyncpg

		# asyncpg no acepta el esquema de SQLAlchemy; usar postgresql://
		raw_url = postgres_url.replace('postgresql+asyncpg://', 'postgresql://', 1)

		async def _check() -> list[tuple[str, str]]:
			conn = await asyncpg.connect(raw_url)
			try:
				rows = await conn.fetch('SELECT titulo, imagen FROM propiedades')
			finally:
				await conn.close()
			return [(r['titulo'], r['imagen']) for r in rows]

		rows = asyncio.run(_check())
		assert len(rows) == 10
		for titulo, imagen in rows:
			assert imagen != '', f'Imagen vacía para {titulo}'
			assert imagen.startswith('https://'), (
				f'Imagen no absoluta para {titulo}: {imagen}'
			)
			assert 'picsum.photos' not in imagen
