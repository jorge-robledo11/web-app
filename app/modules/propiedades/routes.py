"""
Rutas HTTP del módulo de propiedades.

GET /propiedades renderiza la página de propiedades con grid de cards.
GET /propiedades/nueva renderiza el formulario de creación.
POST /propiedades procesa el formulario y crea la propiedad.
"""

import base64
import hashlib
import hmac
import json
import logging
from decimal import Decimal
from pathlib import Path
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_paths, get_settings
from app.infra.database import get_session
from app.modules.propiedades import service
from app.modules.propiedades.schemas import PropiedadFormIn

SessionDep = Annotated[AsyncSession, Depends(get_session)]

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent

paths = get_paths()
settings = get_settings()

templates = Jinja2Templates(
	directory=[
		paths.templates_dir,
		paths.static_dir,
		BASE_DIR / 'templates',
	]
)

router = APIRouter(prefix='/propiedades', tags=['propiedades'])

FLASH_COOKIE_NAME = 'flash'
FLASH_MAX_AGE = 60
FLASH_MENSAJE_EXITO = 'Propiedad creada exitosamente.'
FLASH_MENSAJE_DUPLICADO = 'Ya existe una propiedad con ese título y dirección en Miami.'


def _firmar_flash(payload: dict[str, str], secret: str) -> str:
	"""
	Serializa y firma un payload de flash con HMAC-SHA256.

	Retorna un string con formato ``{base64(json)}.{hmac_hex}``.
	"""
	payload_json = json.dumps(payload, separators=(',', ':'), sort_keys=True)
	payload_b64 = base64.urlsafe_b64encode(payload_json.encode('utf-8')).decode(
		'ascii',
	)
	sig = hmac.new(
		secret.encode('utf-8'),
		payload_b64.encode('ascii'),
		hashlib.sha256,
	).hexdigest()
	return f'{payload_b64}.{sig}'


def _verificar_flash(cookie: str, secret: str) -> dict[str, str] | None:
	"""
	Verifica la firma HMAC de una cookie de flash y retorna el payload.

	Retorna ``None`` si la firma no coincide, el formato es inválido o
	el JSON no parsea. El uso de ``hmac.compare_digest`` evita timing
	side-channels.
	"""
	partes = cookie.rsplit('.', 1)
	if len(partes) != 2:
		return None
	payload_b64, sig_recibida = partes
	sig_esperada = hmac.new(
		secret.encode('utf-8'),
		payload_b64.encode('ascii'),
		hashlib.sha256,
	).hexdigest()
	if not hmac.compare_digest(sig_recibida, sig_esperada):
		return None
	try:
		payload_json = base64.urlsafe_b64decode(payload_b64.encode('ascii'))
		return dict(json.loads(payload_json))
	except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
		return None


def _leer_y_limpiar_flash(
	request: Request,
	secret: str,
) -> dict[str, str] | None:
	"""
	Lee la cookie de flash firmada y la elimina de la request actual.

	Retorna el payload del flash o ``None`` si no hay cookie válida.
	El caller debe llamar a ``response.delete_cookie(FLASH_COOKIE_NAME)``
	en la respuesta para que la cookie no se mantenga en siguientes
	requests.
	"""
	cookie = request.cookies.get(FLASH_COOKIE_NAME)
	if not cookie:
		return None
	return _verificar_flash(cookie, secret)


def _convertir_form_numericos(
	titulo: str,
	direccion: str,
	precio_mensual_str: str,
	habitaciones_str: str,
	banos_str: str,
	area_str: str,
) -> dict[str, object]:
	"""
	Construye ``PropiedadFormIn`` desde strings del form.

	Distigue entre campos requeridos (``precio_mensual``, ``habitaciones``,
	``banos``) y el opcional ``area``. Para los requeridos, si la
	conversión falla se mantiene string vacío para que Pydantic genere
	el error específico del campo. Para el opcional ``area``, string
	vacío se trata como ``0`` (default aplicado); si no es parseable
	como int, se mantiene string vacío para que Pydantic genere el
	error. No se usa ``None`` porque Pydantic v2 lo rechaza en campos
	tipados como ``int`` aunque tengan default.
	"""
	datos: dict[str, object] = {
		'titulo': titulo,
		'direccion': direccion,
	}

	# precio_mensual: Decimal requerido
	try:
		datos['precio_mensual'] = Decimal(precio_mensual_str)
	except (ValueError, TypeError, ArithmeticError):
		datos['precio_mensual'] = precio_mensual_str

	# habitaciones: int requerido
	try:
		datos['habitaciones'] = int(habitaciones_str)
	except (ValueError, TypeError):
		datos['habitaciones'] = habitaciones_str

	# banos: int requerido
	try:
		datos['banos'] = int(banos_str)
	except (ValueError, TypeError):
		datos['banos'] = banos_str

	# area: int opcional (string vacío se trata como 0)
	if area_str == '':
		datos['area'] = 0
	else:
		try:
			datos['area'] = int(area_str)
		except (ValueError, TypeError):
			datos['area'] = area_str

	return datos


def _errores_desde_validation_error(exc: ValidationError) -> dict[str, str]:
	"""
	Convierte errores de ``Pydantic.ValidationError`` a un dict plano.

	Para errores anidados (``loc`` con tuplas), toma el último segmento
	como nombre de campo.
	"""
	errores: dict[str, str] = {}
	for err in exc.errors():
		loc = err.get('loc', ())
		campo = str(loc[-1]) if loc else '__all__'
		errores[campo] = err.get('msg', 'valor inválido')
	return errores


@router.get('', response_class=HTMLResponse)
async def propiedades(
	request: Request,
	session: SessionDep,
) -> HTMLResponse:
	"""
	Renderiza la página de propiedades con grid de cards.

	Si la request trae una cookie de flash firmada válida, la incluye
	en el contexto para que se renderice como alerta y la elimina de
	la respuesta (one-shot).
	"""
	logger.info('propiedades.listar.inicio')
	flash = _leer_y_limpiar_flash(request, settings.session_secret)
	lista = await service.listar_propiedades(session)
	ctx: dict[str, Any] = {
		'request': request,
		'propiedades': lista,
		'vacio': len(lista) == 0,
	}
	if flash is not None:
		ctx['flash'] = flash
	tmpl = templates.get_template('propiedades.html')
	logger.info(
		'propiedades.listar.fin',
		extra={'total': len(lista), 'vacio': ctx['vacio']},
	)
	response = HTMLResponse(tmpl.render(ctx))
	if flash is not None:
		response.delete_cookie(FLASH_COOKIE_NAME, path='/')
	return response


@router.get('/nueva', response_class=HTMLResponse)
async def crear_propiedad_form(request: Request) -> HTMLResponse:
	"""
	Renderiza el formulario de creación vacío.
	"""
	logger.info('propiedad.formulario.render')
	ctx: dict[str, Any] = {
		'request': request,
		'form': {},
		'errores': {},
	}
	tmpl = templates.get_template('crear_propiedad.html')
	return HTMLResponse(tmpl.render(ctx))


@router.post('', response_model=None)
async def crear_propiedad(
	request: Request,
	session: SessionDep,
	titulo: Annotated[str, Form()] = '',
	direccion: Annotated[str, Form()] = '',
	precio_mensual: Annotated[str, Form()] = '',
	habitaciones: Annotated[str, Form()] = '',
	banos: Annotated[str, Form()] = '',
	area: Annotated[str, Form()] = '',
) -> HTMLResponse | RedirectResponse:
	"""
	Procesa el formulario de creación.

	Valida con ``PropiedadFormIn``, llama al servicio y redirige a
	``/propiedades`` con mensaje flash firmado. En validación fallida o
	duplicado, re-renderiza el formulario con errores inline y conserva
	los valores ingresados.
	"""
	logger.info('propiedad.crear_formulario.inicio')
	datos = _convertir_form_numericos(
		titulo=titulo,
		direccion=direccion,
		precio_mensual_str=precio_mensual,
		habitaciones_str=habitaciones,
		banos_str=banos,
		area_str=area,
	)

	try:
		form = PropiedadFormIn(**datos)  # type: ignore[arg-type]
	except ValidationError as exc:
		errores = _errores_desde_validation_error(exc)
		logger.info(
			'propiedad.crear_formulario.validacion_error',
			extra={'campos': list(errores.keys())},
		)
		ctx: dict[str, Any] = {
			'request': request,
			'form': {
				'titulo': titulo,
				'direccion': direccion,
				'precio_mensual': precio_mensual,
				'habitaciones': habitaciones,
				'banos': banos,
				'area': area,
			},
			'errores': errores,
		}
		tmpl = templates.get_template('crear_propiedad.html')
		return HTMLResponse(tmpl.render(ctx), status_code=status.HTTP_200_OK)

	resultado = await service.crear_propiedad_desde_formulario(session, form)

	if resultado is None:
		# Duplicado por constraint único
		logger.info('propiedad.crear_formulario.duplicado')
		ctx = {
			'request': request,
			'form': {
				'titulo': titulo,
				'direccion': direccion,
				'precio_mensual': precio_mensual,
				'habitaciones': habitaciones,
				'banos': banos,
				'area': area,
			},
			'errores': {'__all__': FLASH_MENSAJE_DUPLICADO},
		}
		tmpl = templates.get_template('crear_propiedad.html')
		return HTMLResponse(tmpl.render(ctx), status_code=status.HTTP_200_OK)

	# Éxito: redirigir a /propiedades con flash firmado
	logger.info(
		'propiedad.crear_formulario.ok',
		extra={'propiedad_id': str(resultado.id)},
	)
	payload = {'tipo': 'success', 'mensaje': FLASH_MENSAJE_EXITO}
	cookie_value = _firmar_flash(payload, settings.session_secret)
	response = RedirectResponse(
		url='/propiedades',
		status_code=status.HTTP_303_SEE_OTHER,
	)
	response.set_cookie(
		key=FLASH_COOKIE_NAME,
		value=cookie_value,
		max_age=FLASH_MAX_AGE,
		path='/',
		httponly=True,
		samesite='lax',
	)
	return response
