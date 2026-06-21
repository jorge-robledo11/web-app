"""Tests unitarios del DTO de entrada de formulario PropiedadFormIn."""


import pytest
from pydantic import ValidationError

from app.modules.propiedades.schemas import PropiedadFormIn


class TestPropiedadFormIn:
	"""
	Pruebas del DTO de entrada del formulario de creación.
	"""

	def test_acepta_datos_validos_completos(self) -> None:
		"""
		Debe aceptar todos los campos con valores válidos.
		"""
		form = PropiedadFormIn(
			titulo='Casa Test',
			direccion='Calle 123',
			precio_mensual='1500.00',
			habitaciones=2,
			banos=1,
			area=80,
		)
		assert form.titulo == 'Casa Test'
		assert form.direccion == 'Calle 123'
		assert str(form.precio_mensual) == '1500.00'
		assert form.habitaciones == 2
		assert form.banos == 1
		assert form.area == 80

	def test_titulo_vacio_despues_de_strip_falla(self) -> None:
		"""
		titulo='' debe fallar con min_length=1.
		"""
		with pytest.raises(ValidationError):
			PropiedadFormIn(
				titulo='',
				direccion='Calle 123',
				precio_mensual='1500.00',
				habitaciones=2,
				banos=1,
			)

	def test_direccion_solo_espacios_falla(self) -> None:
		"""
		direccion con solo espacios debe tratarse como vacía.
		"""
		with pytest.raises(ValidationError):
			PropiedadFormIn(
				titulo='Casa Test',
				direccion='   ',
				precio_mensual='1500.00',
				habitaciones=2,
				banos=1,
			)

	def test_titulo_256_caracteres_falla(self) -> None:
		"""
		titulo con 256 chars debe fallar (max_length=255).
		"""
		with pytest.raises(ValidationError):
			PropiedadFormIn(
				titulo='A' * 256,
				direccion='Calle 123',
				precio_mensual='1500.00',
				habitaciones=2,
				banos=1,
			)

	def test_direccion_256_caracteres_falla(self) -> None:
		"""
		direccion con 256 chars debe fallar (max_length=255).
		"""
		with pytest.raises(ValidationError):
			PropiedadFormIn(
				titulo='Casa Test',
				direccion='A' * 256,
				precio_mensual='1500.00',
				habitaciones=2,
				banos=1,
			)

	def test_precio_mensual_menor_o_igual_cero_falla(self) -> None:
		"""
		precio_mensual <= 0 debe fallar con gt=0.
		"""
		for precio in ('0', '-1'):
			with pytest.raises(ValidationError):
				PropiedadFormIn(
					titulo='Casa Test',
					direccion='Calle 123',
					precio_mensual=precio,
					habitaciones=2,
					banos=1,
				)

	def test_precio_mensual_sin_decimales_aceptado(self) -> None:
		"""
		precio_mensual='1500' (sin .00) debe ser aceptado (sin decimal_places).
		"""
		form = PropiedadFormIn(
			titulo='Casa Test',
			direccion='Calle 123',
			precio_mensual='1500',
			habitaciones=2,
			banos=1,
		)
		assert str(form.precio_mensual) == '1500'

	def test_habitaciones_mayor_20_falla(self) -> None:
		"""
		habitaciones > 20 debe fallar con le=20.
		"""
		with pytest.raises(ValidationError):
			PropiedadFormIn(
				titulo='Casa Test',
				direccion='Calle 123',
				precio_mensual='1500.00',
				habitaciones=21,
				banos=1,
			)

	def test_banos_mayor_10_falla(self) -> None:
		"""
		banos > 10 debe fallar con le=10.
		"""
		with pytest.raises(ValidationError):
			PropiedadFormIn(
				titulo='Casa Test',
				direccion='Calle 123',
				precio_mensual='1500.00',
				habitaciones=2,
				banos=11,
			)

	def test_area_opcional_default_cero(self) -> None:
		"""
		area es opcional y debe usar default 0 cuando se omite.
		"""
		form = PropiedadFormIn(
			titulo='Casa Test',
			direccion='Calle 123',
			precio_mensual='1500.00',
			habitaciones=2,
			banos=1,
		)
		assert form.area == 0

	def test_area_negativa_falla(self) -> None:
		"""
		area < 0 debe fallar con ge=0.
		"""
		with pytest.raises(ValidationError):
			PropiedadFormIn(
				titulo='Casa Test',
				direccion='Calle 123',
				precio_mensual='1500.00',
				habitaciones=2,
				banos=1,
				area=-1,
			)

	def test_es_frozen(self) -> None:
		"""
		El DTO debe ser inmutable (frozen=True).
		"""
		form = PropiedadFormIn(
			titulo='Casa Test',
			direccion='Calle 123',
			precio_mensual='1500.00',
			habitaciones=2,
			banos=1,
		)
		with pytest.raises(ValidationError):
			form.titulo = 'otro'  # type: ignore[misc]
