"""Tests de integración del endpoint GET /propiedades."""

import re

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


def _find_anchor_with_text(html: str, text: str) -> str | None:
	"""
	Retorna el HTML del <a> cuyo <span> contiene exactamente `text`.

	Robusto ante la presencia de un icono (otro <span>) entre <a> y el
	<span> con el texto, ya que el sidebar renderiza icono + texto.
	"""
	pattern = (
		r'<a\b[^>]*>(?:(?!</a>).)*<span[^>]*>\s*'
		+ re.escape(text)
		+ r'\s*</span>(?:(?!</a>).)*</a>'
	)
	match = re.search(pattern, html, re.DOTALL)
	return match.group(0) if match is not None else None


@pytest.mark.asyncio
async def test_propiedades_responde_200(postgres_url: str, async_session: AsyncSession):
	"""Verifica que GET /propiedades retorna 200 con HTML y layout base."""
	_setup(postgres_url)
	_override_session(async_session)

	try:
		transport = ASGITransport(app=app)
		async with AsyncClient(transport=transport, base_url='http://test') as client:
			response = await client.get('/propiedades')

		assert response.status_code == 200
		html = response.text
		assert 'sidebar' in html
		assert 'navbar' in html
		assert 'propiedades-grid' in html
		assert 'propiedades-header' in html
	finally:
		app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_propiedades_cards_seed(postgres_url: str, async_session: AsyncSession):
	"""Verifica que renderiza 10 cards (seed de propiedades)."""
	_setup(postgres_url)
	_override_session(async_session)

	try:
		transport = ASGITransport(app=app)
		async with AsyncClient(transport=transport, base_url='http://test') as client:
			response = await client.get('/propiedades')

		html = response.text
		assert html.count('card-propiedad--grid') == 10
	finally:
		app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_propiedades_estructura_cards(
	postgres_url: str, async_session: AsyncSession
):
	"""Verifica que las cards tienen estructura media/body/footer."""
	_setup(postgres_url)
	_override_session(async_session)

	try:
		transport = ASGITransport(app=app)
		async with AsyncClient(transport=transport, base_url='http://test') as client:
			response = await client.get('/propiedades')

		html = response.text
		assert 'card-propiedad__media' in html
		assert 'card-propiedad__body' in html
		assert 'card-propiedad__footer' in html
		assert 'card-propiedad__titulo' in html
		assert 'card-propiedad__direccion' in html
		assert 'card-propiedad__detalles' in html
		assert 'card-propiedad__detalle' in html
		assert 'card-propiedad__precio' in html
		assert 'badge-estado' in html
		assert 'm²' in html
	finally:
		app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_propiedades_imagenes_explicitas(
	postgres_url: str, async_session: AsyncSession
):
	"""Verifica que las cards tienen <img con src explícito por propiedad."""
	_setup(postgres_url)
	_override_session(async_session)

	try:
		transport = ASGITransport(app=app)
		async with AsyncClient(transport=transport, base_url='http://test') as client:
			response = await client.get('/propiedades')

		html = response.text
		# Cada propiedad del seed debe tener su <img con src no vacío
		img_tags = re.findall(r'<img[^>]*\bsrc="([^"]+)"', html)
		assert len(img_tags) == 10, f'Se esperaban 10 imgs, hay {len(img_tags)}'
		# Las URLs deben ser explícitas (no generadas por hash)
		assert 'picsum.photos' not in html
		assert 'seed/' not in html
		for src in img_tags:
			assert src.startswith('https://'), f'URL no absoluta: {src}'
			assert src != '', 'src vacío detectado'
		assert 'loading="lazy"' in html
		assert 'decoding="async"' in html
	finally:
		app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_propiedades_sin_estilos_inline_en_imagen(
	postgres_url: str, async_session: AsyncSession
):
	"""Verifica que la card no usa estilos inline para imagen/placeholder."""
	_setup(postgres_url)
	_override_session(async_session)

	try:
		transport = ASGITransport(app=app)
		async with AsyncClient(transport=transport, base_url='http://test') as client:
			response = await client.get('/propiedades')

		html = response.text
		# Ningún style="display:none" ni onerror con manipulación de estilo
		assert 'style="display' not in html
		# El onerror solo debe agregar clase, no manipular style
		assert 'this.style.display' not in html
	finally:
		app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_propiedades_estado_vacio(postgres_url: str, async_session: AsyncSession):
	"""Verifica que GET /propiedades muestra estado vacío sin propiedades."""
	setup_db(postgres_url)

	await async_session.execute(sa_text('DELETE FROM propiedades'))
	await async_session.commit()

	_override_session(async_session)

	try:
		transport = ASGITransport(app=app)
		async with AsyncClient(transport=transport, base_url='http://test') as client:
			response = await client.get('/propiedades')

		html = response.text
		assert 'No hay propiedades registradas' in html
		assert 'propiedades--empty' in html
		assert 'propiedades-grid' not in html
	finally:
		app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_propiedades_placeholder_imagen(
	postgres_url: str, async_session: AsyncSession
):
	"""Verifica que una propiedad sin imagen muestra placeholder."""
	setup_db(postgres_url)
	seed_ok(postgres_url)

	await async_session.execute(
		sa_text(
			"UPDATE propiedades SET imagen = '' WHERE titulo = 'Sunny Palms Apartments'"
		)
	)
	await async_session.commit()

	_override_session(async_session)

	try:
		transport = ASGITransport(app=app)
		async with AsyncClient(transport=transport, base_url='http://test') as client:
			response = await client.get('/propiedades')

		html = response.text
		assert 'card-propiedad__imagen-placeholder' in html
		# La card sin imagen debe tener la clase --no-image
		assert 'card-propiedad--no-image' in html
	finally:
		app.dependency_overrides.clear()


# =============================================================
# Sidebar: estado activo, hrefs, Inquilinos/Contratos separados
# =============================================================


@pytest.mark.asyncio
async def test_sidebar_activa_propiedades_en_propiedades(
	postgres_url: str, async_session: AsyncSession
):
	"""En /propiedades el link Propiedades debe estar activo y Dashboard no."""
	_setup(postgres_url)
	_override_session(async_session)

	try:
		transport = ASGITransport(app=app)
		async with AsyncClient(transport=transport, base_url='http://test') as client:
			response = await client.get('/propiedades')

		html = response.text
		# El link a /propiedades contiene la clase activa
		prop_link_match = re.search(r'<a\s+[^>]*href="/propiedades"[^>]*>', html)
		assert prop_link_match is not None, 'Falta el link /propiedades'
		prop_link = prop_link_match.group(0)
		assert 'sidebar__item--active' in prop_link
		assert 'aria-current="page"' in prop_link

		# El link a / (Dashboard) NO debe estar activo
		dash_link_match = re.search(r'<a\s+[^>]*href="/"[^>]*>', html)
		assert dash_link_match is not None, 'Falta el link /'
		dash_link = dash_link_match.group(0)
		assert 'sidebar__item--active' not in dash_link
		assert 'aria-current="page"' not in dash_link
	finally:
		app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_sidebar_activa_dashboard_en_root(
	postgres_url: str, async_session: AsyncSession
):
	"""En / el link Dashboard debe estar activo y Propiedades no."""
	_setup(postgres_url)
	_override_session(async_session)

	try:
		transport = ASGITransport(app=app)
		async with AsyncClient(transport=transport, base_url='http://test') as client:
			response = await client.get('/')

		html = response.text
		dash_link_match = re.search(r'<a\s+[^>]*href="/"[^>]*>', html)
		assert dash_link_match is not None
		dash_link = dash_link_match.group(0)
		assert 'sidebar__item--active' in dash_link
		assert 'aria-current="page"' in dash_link

		prop_link_match = re.search(r'<a\s+[^>]*href="/propiedades"[^>]*>', html)
		assert prop_link_match is not None
		prop_link = prop_link_match.group(0)
		assert 'sidebar__item--active' not in prop_link
		assert 'aria-current="page"' not in prop_link
	finally:
		app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_sidebar_inquilinos_y_contratos_separados(
	postgres_url: str, async_session: AsyncSession
):
	"""Inquilinos y Contratos deben ser anchors separados en el sidebar."""
	_setup(postgres_url)
	_override_session(async_session)

	try:
		transport = ASGITransport(app=app)
		async with AsyncClient(transport=transport, base_url='http://test') as client:
			response = await client.get('/propiedades')

		html = response.text
		# Buscamos el <a> que contiene cada texto como span propio.
		# El HTML entre <a> y <span> incluye el icono (otro <span> con svg).
		inquilinos_link = _find_anchor_with_text(html, 'Inquilinos')
		contratos_link = _find_anchor_with_text(html, 'Contratos')
		assert inquilinos_link is not None, (
			'Inquilinos no aparece como anchor independiente'
		)
		assert contratos_link is not None, (
			'Contratos no aparece como anchor independiente'
		)
		assert inquilinos_link != contratos_link, (
			'Inquilinos y Contratos no deben compartir el mismo <a>'
		)
	finally:
		app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_sidebar_items_completos(postgres_url: str, async_session: AsyncSession):
	"""El sidebar debe contener los 7 items en su propio anchor."""
	_setup(postgres_url)
	_override_session(async_session)

	try:
		transport = ASGITransport(app=app)
		async with AsyncClient(transport=transport, base_url='http://test') as client:
			response = await client.get('/propiedades')

		html = response.text
		items = [
			'Dashboard',
			'Propiedades',
			'Inquilinos',
			'Contratos',
			'Pagos',
			'Mantenimiento',
			'Configuración',
		]
		for item in items:
			anchor = _find_anchor_with_text(html, item)
			assert anchor is not None, f'Item sidebar faltante: {item}'
	finally:
		app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_sidebar_tiene_href_propiedades(
	postgres_url: str, async_session: AsyncSession
):
	"""Verifica que el sidebar contiene href="/propiedades"."""
	_setup(postgres_url)
	_override_session(async_session)

	try:
		transport = ASGITransport(app=app)
		async with AsyncClient(transport=transport, base_url='http://test') as client:
			response = await client.get('/')

		html = response.text
		assert 'href="/propiedades"' in html
	finally:
		app.dependency_overrides.clear()


# =============================================================
# Navbar: breadcrumb dinámico por ruta
# =============================================================


@pytest.mark.asyncio
async def test_navbar_breadcrumb_en_propiedades(
	postgres_url: str, async_session: AsyncSession
):
	"""En /propiedades el breadcrumb debe ser Inicio / Propiedades."""
	_setup(postgres_url)
	_override_session(async_session)

	try:
		transport = ASGITransport(app=app)
		async with AsyncClient(transport=transport, base_url='http://test') as client:
			response = await client.get('/propiedades')

		html = response.text
		# Tomamos el bloque del breadcrumb
		bc_match = re.search(
			r'<div class="navbar__breadcrumbs"[^>]*>(.*?)</div>', html, re.DOTALL
		)
		assert bc_match is not None, 'No se encontró navbar__breadcrumbs'
		bc = bc_match.group(1)
		assert 'Inicio' in bc
		assert 'Propiedades' in bc
		# No debe seguir mostrando Dashboard
		assert 'Dashboard' not in bc
	finally:
		app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_navbar_breadcrumb_en_root(
	postgres_url: str, async_session: AsyncSession
):
	"""En / el breadcrumb debe ser Inicio / Dashboard."""
	_setup(postgres_url)
	_override_session(async_session)

	try:
		transport = ASGITransport(app=app)
		async with AsyncClient(transport=transport, base_url='http://test') as client:
			response = await client.get('/')

		html = response.text
		bc_match = re.search(
			r'<div class="navbar__breadcrumbs"[^>]*>(.*?)</div>', html, re.DOTALL
		)
		assert bc_match is not None
		bc = bc_match.group(1)
		assert 'Inicio' in bc
		assert 'Dashboard' in bc
	finally:
		app.dependency_overrides.clear()
