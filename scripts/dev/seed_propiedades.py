"""
Carga inicial idempotente de 10 propiedades de Miami.

Ejecutar después de ``alembic upgrade head``::

    uv run python scripts/dev/seed_propiedades.py

Reglas:
- Idempotente por clave de negocio (titulo + direccion + ciudad).
- Timestamps server-side (nunca desde Python).
- Cada propiedad tiene una URL de imagen inmobiliaria explícita, curada
  y estable. No se generan URLs con hash ni se usan servicios de
  imágenes aleatorias.
- Solo asyncpg vía create_async_engine. Prohibido psycopg2.
"""

import asyncio
import sys
import uuid
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
	sys.path.insert(0, str(REPO_ROOT))

from sqlalchemy import text  # noqa: E402
from sqlalchemy.ext.asyncio import create_async_engine  # noqa: E402

from app.config import get_settings  # noqa: E402

PROPIEDADES_MIAMI = [
	{
		'titulo': 'Sunny Palms Apartments',
		'direccion': '123 Ocean Drive',
		'ciudad': 'Miami',
		'precio_mensual': 2500.00,
		'habitaciones': 2,
		'banos': 1,
		'area': 850,
		'estado': 'disponible',
		'imagen': 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800&h=500&fit=crop',
	},
	{
		'titulo': 'Bayfront Lofts',
		'direccion': '456 Biscayne Blvd',
		'ciudad': 'Miami',
		'precio_mensual': 3200.00,
		'habitaciones': 3,
		'banos': 2,
		'area': 1200,
		'estado': 'disponible',
		'imagen': 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=500&fit=crop',
	},
	{
		'titulo': 'Coconut Grove Studio',
		'direccion': '789 Main Highway',
		'ciudad': 'Miami',
		'precio_mensual': 1800.00,
		'habitaciones': 1,
		'banos': 1,
		'area': 550,
		'estado': 'disponible',
		'imagen': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&h=500&fit=crop',
	},
	{
		'titulo': 'Brickell Heights',
		'direccion': '1000 Brickell Ave',
		'ciudad': 'Miami',
		'precio_mensual': 4200.00,
		'habitaciones': 3,
		'banos': 2,
		'area': 1500,
		'estado': 'disponible',
		'imagen': 'https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800&h=500&fit=crop',
	},
	{
		'titulo': 'Little Havana Casa',
		'direccion': '234 Calle Ocho',
		'ciudad': 'Miami',
		'precio_mensual': 1500.00,
		'habitaciones': 2,
		'banos': 1,
		'area': 700,
		'estado': 'rentada',
		'imagen': 'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800&h=500&fit=crop',
	},
	{
		'titulo': 'Design District Loft',
		'direccion': '567 NE 2nd Ave',
		'ciudad': 'Miami',
		'precio_mensual': 3800.00,
		'habitaciones': 2,
		'banos': 2,
		'area': 1100,
		'estado': 'rentada',
		'imagen': 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&h=500&fit=crop',
	},
	{
		'titulo': 'Wynwood Arts Residence',
		'direccion': '890 NW 3rd Ave',
		'ciudad': 'Miami',
		'precio_mensual': 2900.00,
		'habitaciones': 2,
		'banos': 1,
		'area': 950,
		'estado': 'rentada',
		'imagen': 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=500&fit=crop',
	},
	{
		'titulo': 'Coral Gables Manor',
		'direccion': '345 Miracle Mile',
		'ciudad': 'Miami',
		'precio_mensual': 5500.00,
		'habitaciones': 4,
		'banos': 3,
		'area': 2200,
		'estado': 'mantenimiento',
		'imagen': 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=500&fit=crop',
	},
	{
		'titulo': 'Key Biscayne Villa',
		'direccion': '678 Crandon Blvd',
		'ciudad': 'Miami',
		'precio_mensual': 6500.00,
		'habitaciones': 4,
		'banos': 3,
		'area': 2800,
		'estado': 'mantenimiento',
		'imagen': 'https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800&h=500&fit=crop',
	},
	{
		'titulo': 'South Beach Retreat',
		'direccion': '901 Collins Ave',
		'ciudad': 'Miami',
		'precio_mensual': 2000.00,
		'habitaciones': 1,
		'banos': 1,
		'area': 600,
		'estado': 'inactiva',
		'imagen': 'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=800&h=500&fit=crop',
	},
]

UPSERT_SQL = """
    INSERT INTO propiedades (
        id, titulo, direccion, ciudad, precio_mensual,
        habitaciones, banos, area, estado, imagen
    ) VALUES (
        CAST(:id AS uuid), :titulo, :direccion, :ciudad, :precio_mensual,
        :habitaciones, :banos, :area, CAST(:estado AS estado_propiedad), :imagen
    )
    ON CONFLICT (titulo, direccion, ciudad) DO UPDATE SET
        precio_mensual = EXCLUDED.precio_mensual,
        habitaciones = EXCLUDED.habitaciones,
        banos = EXCLUDED.banos,
        area = EXCLUDED.area,
        estado = EXCLUDED.estado,
        imagen = EXCLUDED.imagen,
        updated_at = now()
"""


def _uuid_negocio(titulo: str, direccion: str, ciudad: str) -> uuid.UUID:
	"""
	UUID v5 determinista a partir de clave de negocio.
	"""
	namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
	return uuid.uuid5(namespace, f'{titulo}|{direccion}|{ciudad}')


async def _cargar() -> int:
	"""
	Ejecuta carga inicial. Retorna cantidad de propiedades.
	"""
	database_url = get_settings().database_url
	if not database_url:
		print('[seed] ERROR: DATABASE_URL no configurada', file=sys.stderr)
		sys.exit(1)

	engine = create_async_engine(database_url, echo=False)

	async with engine.begin() as conn:
		for prop in PROPIEDADES_MIAMI:
			prop_id = _uuid_negocio(prop['titulo'], prop['direccion'], prop['ciudad'])
			imagen = prop['imagen']

			await conn.execute(
				text(UPSERT_SQL),
				{
					'id': prop_id,
					'titulo': prop['titulo'],
					'direccion': prop['direccion'],
					'ciudad': prop['ciudad'],
					'precio_mensual': prop['precio_mensual'],
					'habitaciones': prop['habitaciones'],
					'banos': prop['banos'],
					'area': prop['area'],
					'estado': prop['estado'],
					'imagen': imagen,
				},
			)

		result = await conn.execute(
			text('SELECT count(*) FROM propiedades'),
		)
		total = result.scalar_one()

	await engine.dispose()

	print(f'[seed] Procesadas {total} propiedades en Miami')
	print('[seed] Carga idempotente completada')
	return int(total)


def main() -> None:
	"""
	Punto de entrada.
	"""
	total = asyncio.run(_cargar())
	assert total == 10, f'Se esperaban 10 propiedades, se encontraron {total}'


if __name__ == '__main__':
	main()
