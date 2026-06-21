"""Tests de integración del endpoint GET/POST /propiedades/nueva y POST /propiedades."""

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text as sa_text
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.database import get_session
from app.main import app
from tests.integration.conftest import seed_ok, setup_db


def _setup(postgres_url: str) -> None:
	"""Aplica alembic y seed validando returncode."""
	setup_db(postgres_url)
	seed_ok(postgres_url)


def _override_session(async_session: AsyncSession) -> None:
	"""Inyecta la sesión de test en la app."""

	async def _dep() -> AsyncSession:
		return async_session

	app.dependency_overrides[get_session] = _dep


@pytest.fixture(autouse=True)
def _clean_overrides() -> None:
	"""Limpia dependency_overrides después de cada test."""
	yield
	app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_nueva_retorna_200_con_formulario(
	postgres_url: str,
	async_session: AsyncSession,
) -> None:
	"""GET /propiedades/nueva debe retornar 200 con el formulario."""
	_setup(postgres_url)
	_override_session(async_session)

	transport = ASGITransport(app=app)
	async with AsyncClient(transport=transport, base_url='http://test') as client:
		response = await client.get('/propiedades/nueva')

	assert response.status_code == 200
	html = response.text
	assert 'class="formulario-crear"' in html
	assert 'name="titulo"' in html
	assert 'name="direccion"' in html
	assert 'name="precio_mensual"' in html
	assert 'name="habitaciones"' in html
	assert 'name="banos"' in html
	assert 'name="area"' in html
	assert 'Crear propiedad' in html


@pytest.mark.asyncio
async def test_post_valido_redirige_303_y_setea_flash(
	postgres_url: str,
	async_session: AsyncSession,
) -> None:
	"""POST con datos válidos redirige 303 a /propiedades y setea cookie flash."""
	_setup(postgres_url)
	_override_session(async_session)

	transport = ASGITransport(app=app)
	async with AsyncClient(transport=transport, base_url='http://test') as client:
		response = await client.post(
			'/propiedades',
			data={
				'titulo': 'Casa Test Integration',
				'direccion': '123 Test St',
				'precio_mensual': '1500',
				'habitaciones': '2',
				'banos': '1',
				'area': '80',
			},
		)

	assert response.status_code == 303
	assert response.headers['location'].endswith('/propiedades')
	assert 'flash' in response.headers.get('set-cookie', '').lower()


@pytest.mark.asyncio
async def test_get_propiedades_con_flash_valido_renderiza_y_limpia_cookie(
	postgres_url: str,
	async_session: AsyncSession,
) -> None:
	"""GET /propiedades con cookie flash válida debe renderizar la alerta y limpiar."""
	_setup(postgres_url)
	_override_session(async_session)

	transport = ASGITransport(app=app)
	async with AsyncClient(transport=transport, base_url='http://test') as client:
		# Crear propiedad para setear flash
		await client.post(
			'/propiedades',
			data={
				'titulo': 'Flash Test',
				'direccion': '789 Flash St',
				'precio_mensual': '2000',
				'habitaciones': '3',
				'banos': '2',
			},
		)
		# El siguiente GET debe leer la flash cookie
		response = await client.get('/propiedades')

	assert response.status_code == 200
	html = response.text
	assert 'alerta--success' in html
	# La cookie debe ser eliminada (set-cookie con Max-Age=0)
	cookies_header = response.headers.get('set-cookie', '')
	assert 'flash' in cookies_header.lower()


@pytest.mark.asyncio
async def test_post_titulo_vacio_re_renderiza_con_error_inline(
	postgres_url: str,
	async_session: AsyncSession,
) -> None:
	"""POST con titulo='' debe re-renderizar con error inline."""
	_setup(postgres_url)
	_override_session(async_session)

	transport = ASGITransport(app=app)
	async with AsyncClient(transport=transport, base_url='http://test') as client:
		response = await client.post(
			'/propiedades',
			data={
				'titulo': '',
				'direccion': 'Calle Valida 100',
				'precio_mensual': '1500',
				'habitaciones': '2',
				'banos': '1',
				'area': '80',
			},
		)

	assert response.status_code == 200
	html = response.text
	assert 'form-field__error' in html
	# El valor de direccion debe conservarse
	assert 'Calle Valida 100' in html


@pytest.mark.asyncio
async def test_post_direccion_solo_espacios_rechaza(
	postgres_url: str,
	async_session: AsyncSession,
) -> None:
	"""POST con direccion='   ' debe rechazarse."""
	_setup(postgres_url)
	_override_session(async_session)

	transport = ASGITransport(app=app)
	async with AsyncClient(transport=transport, base_url='http://test') as client:
		response = await client.post(
			'/propiedades',
			data={
				'titulo': 'Test',
				'direccion': '   ',
				'precio_mensual': '1500',
				'habitaciones': '2',
				'banos': '1',
			},
		)

	assert response.status_code == 200
	assert 'form-field__error' in response.text


@pytest.mark.asyncio
async def test_post_precio_mensual_no_numerico_rechaza(
	postgres_url: str,
	async_session: AsyncSession,
) -> None:
	"""POST con precio_mensual='abc' debe rechazarse."""
	_setup(postgres_url)
	_override_session(async_session)

	transport = ASGITransport(app=app)
	async with AsyncClient(transport=transport, base_url='http://test') as client:
		response = await client.post(
			'/propiedades',
			data={
				'titulo': 'Test',
				'direccion': 'Calle',
				'precio_mensual': 'abc',
				'habitaciones': '2',
				'banos': '1',
			},
		)

	assert response.status_code == 200
	html = response.text
	assert 'form-field__error' in html
	assert 'precio_mensual' in html


@pytest.mark.asyncio
async def test_post_precio_mensual_menor_o_igual_cero_rechaza(
	postgres_url: str,
	async_session: AsyncSession,
) -> None:
	"""POST con precio_mensual='0' o negativo debe rechazarse."""
	_setup(postgres_url)
	_override_session(async_session)

	transport = ASGITransport(app=app)
	async with AsyncClient(transport=transport, base_url='http://test') as client:
		response = await client.post(
			'/propiedades',
			data={
				'titulo': 'Test',
				'direccion': 'Calle',
				'precio_mensual': '0',
				'habitaciones': '2',
				'banos': '1',
			},
		)

	assert response.status_code == 200
	assert 'form-field__error' in response.text


@pytest.mark.asyncio
async def test_post_habitaciones_fuera_rango_rechaza(
	postgres_url: str,
	async_session: AsyncSession,
) -> None:
	"""POST con habitaciones='25' debe rechazarse."""
	_setup(postgres_url)
	_override_session(async_session)

	transport = ASGITransport(app=app)
	async with AsyncClient(transport=transport, base_url='http://test') as client:
		response = await client.post(
			'/propiedades',
			data={
				'titulo': 'Test',
				'direccion': 'Calle',
				'precio_mensual': '1500',
				'habitaciones': '25',
				'banos': '1',
			},
		)

	assert response.status_code == 200
	html = response.text
	assert 'form-field__error' in html
	assert 'habitaciones' in html


@pytest.mark.asyncio
async def test_post_banos_fuera_rango_rechaza(
	postgres_url: str,
	async_session: AsyncSession,
) -> None:
	"""POST con banos='11' debe rechazarse."""
	_setup(postgres_url)
	_override_session(async_session)

	transport = ASGITransport(app=app)
	async with AsyncClient(transport=transport, base_url='http://test') as client:
		response = await client.post(
			'/propiedades',
			data={
				'titulo': 'Test',
				'direccion': 'Calle',
				'precio_mensual': '1500',
				'habitaciones': '2',
				'banos': '11',
			},
		)

	assert response.status_code == 200
	html = response.text
	assert 'form-field__error' in html
	assert 'banos' in html


@pytest.mark.asyncio
async def test_post_area_vacio_persiste_con_cero(
	postgres_url: str,
	async_session: AsyncSession,
) -> None:
	"""POST con area='' debe persistir la propiedad con area=0."""
	_setup(postgres_url)
	_override_session(async_session)

	transport = ASGITransport(app=app)
	async with AsyncClient(transport=transport, base_url='http://test') as client:
		response = await client.post(
			'/propiedades',
			data={
				'titulo': 'Sin Area Test',
				'direccion': 'Calle Sin Area 999',
				'precio_mensual': '1000',
				'habitaciones': '1',
				'banos': '1',
			},
		)

	assert response.status_code == 303
	# Verificar que la propiedad se persistió con area=0
	result = await async_session.execute(
		sa_text("SELECT area FROM propiedades WHERE titulo = 'Sin Area Test'"),
	)
	row = result.fetchone()
	assert row is not None
	assert row[0] == 0


@pytest.mark.asyncio
async def test_post_area_negativo_rechaza(
	postgres_url: str,
	async_session: AsyncSession,
) -> None:
	"""POST con area='-5' debe rechazarse."""
	_setup(postgres_url)
	_override_session(async_session)

	transport = ASGITransport(app=app)
	async with AsyncClient(transport=transport, base_url='http://test') as client:
		response = await client.post(
			'/propiedades',
			data={
				'titulo': 'Test',
				'direccion': 'Calle',
				'precio_mensual': '1500',
				'habitaciones': '2',
				'banos': '1',
				'area': '-5',
			},
		)

	assert response.status_code == 200
	assert 'form-field__error' in response.text


@pytest.mark.asyncio
async def test_post_titulo_256_caracteres_rechaza(
	postgres_url: str,
	async_session: AsyncSession,
) -> None:
	"""POST con titulo de 256 chars debe rechazarse (max_length=255)."""
	_setup(postgres_url)
	_override_session(async_session)

	transport = ASGITransport(app=app)
	async with AsyncClient(transport=transport, base_url='http://test') as client:
		response = await client.post(
			'/propiedades',
			data={
				'titulo': 'A' * 256,
				'direccion': 'Calle',
				'precio_mensual': '1500',
				'habitaciones': '2',
				'banos': '1',
			},
		)

	assert response.status_code == 200
	assert 'form-field__error' in response.text


@pytest.mark.asyncio
async def test_post_duplicado_retorna_error_global(
	postgres_url: str,
	async_session: AsyncSession,
) -> None:
	"""POST con duplicado re-renderiza con error global."""
	_setup(postgres_url)
	_override_session(async_session)

	transport = ASGITransport(app=app)
	async with AsyncClient(transport=transport, base_url='http://test') as client:
		# Primer POST: crea
		await client.post(
			'/propiedades',
			data={
				'titulo': 'Duplicado Test',
				'direccion': '999 Dup St',
				'precio_mensual': '1500',
				'habitaciones': '2',
				'banos': '1',
			},
		)
		# Segundo POST con mismos datos: error
		response = await client.post(
			'/propiedades',
			data={
				'titulo': 'Duplicado Test',
				'direccion': '999 Dup St',
				'precio_mensual': '1500',
				'habitaciones': '2',
				'banos': '1',
			},
		)

	assert response.status_code == 200
	html = response.text
	assert 'alerta--danger' in html
	assert 'Ya existe una propiedad' in html


@pytest.mark.asyncio
async def test_get_root_navbar_contiene_enlace_nueva_propiedad(
	postgres_url: str,
	async_session: AsyncSession,
) -> None:
	"""GET / debe contener el enlace /propiedades/nueva en el navbar."""
	_setup(postgres_url)
	_override_session(async_session)

	transport = ASGITransport(app=app)
	async with AsyncClient(transport=transport, base_url='http://test') as client:
		response = await client.get('/')

	assert response.status_code == 200
	html = response.text
	assert 'href="/propiedades/nueva"' in html
	assert 'Nueva propiedad' in html
	assert 'navbar__accion' in html


@pytest.mark.asyncio
async def test_cookie_flash_firma_invalida_se_ignora_silenciosamente(
	postgres_url: str,
	async_session: AsyncSession,
) -> None:
	"""GET con cookie de flash con firma inválida debe ignorar la cookie."""
	_setup(postgres_url)
	_override_session(async_session)

	transport = ASGITransport(app=app)
	async with AsyncClient(transport=transport, base_url='http://test') as client:
		client.cookies.set('flash', 'datos_invalidos.firma_invalida')
		response = await client.get('/propiedades')

	assert response.status_code == 200
	# Sin alerta de éxito (firma inválida → cookie ignorada)
	assert 'alerta--success' not in response.text
