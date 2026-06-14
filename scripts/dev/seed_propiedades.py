"""Carga inicial idempotente de 10 propiedades de Miami.

Ejecutar después de ``alembic upgrade head``::

    uv run python scripts/dev/seed_propiedades.py

Reglas:
- Idempotente por clave de negocio (titulo + direccion + ciudad).
- Timestamps server-side (nunca desde Python).
- Imagen determinista por UUID v5.
- Solo asyncpg vía create_async_engine. Prohibido psycopg2.
"""

import asyncio
import hashlib
import sys
import uuid
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from sqlalchemy import text  # noqa: E402
from sqlalchemy.ext.asyncio import create_async_engine  # noqa: E402

from app.config import settings  # noqa: E402

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


def _imagen_determinista(prop_id: uuid.UUID, seed: int) -> str:
    """URL de imagen estable a partir de UUID y semilla."""
    hash_val = hashlib.md5(f'{prop_id}-{seed}'.encode()).hexdigest()[:8]
    return f'https://images.unsplash.com/photo-{hash_val}?w=800'


def _uuid_negocio(titulo: str, direccion: str, ciudad: str) -> uuid.UUID:
    """UUID v5 determinista a partir de clave de negocio."""
    namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
    return uuid.uuid5(namespace, f'{titulo}|{direccion}|{ciudad}')


async def _cargar() -> int:
    """Ejecuta carga inicial. Retorna cantidad de propiedades."""
    if not settings.DATABASE_URL:
        print('[seed] ERROR: DATABASE_URL no configurada', file=sys.stderr)
        sys.exit(1)

    engine = create_async_engine(settings.DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        for i, prop in enumerate(PROPIEDADES_MIAMI, start=1):
            prop_id = _uuid_negocio(prop['titulo'], prop['direccion'], prop['ciudad'])
            imagen = _imagen_determinista(prop_id, seed=i)

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
    """Punto de entrada."""
    total = asyncio.run(_cargar())
    assert total == 10, f'Se esperaban 10 propiedades, se encontraron {total}'


if __name__ == '__main__':
    main()
