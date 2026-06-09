# Modelo de Datos: Bootstrap del Proyecto Realtor

**Feature**: `001-bootstrap-proyecto` | **Date**: 2026-06-08

## Resumen

Esta spec fundacional no define entidades de dominio. El modelo de datos se
limita a:

1. **Configuración** — parámetros de entorno validados por Pydantic.
2. **Migración baseline** — instalación de `pgcrypto`.
3. **Dashboard Demo** — datos presentacionales hardcodeados (sin persistencia).

## 1. Configuración (Pydantic Settings)

### Settings

| Campo | Tipo | Default | Descripción |
|---|---|---|---|
| `DATABASE_URL` | `str` | `postgresql+asyncpg://realtor_dev:realtor_dev@localhost:5432/realtor_dev` | URL async a PostgreSQL |
| `APP_ENV` | `str` | `"development"` | Entorno: `development`, `staging`, `production` |
| `LOG_LEVEL` | `str` | `"INFO"` | Nivel: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |

Configuración: `model_config = SettingsConfigDict(env_file=".env", frozen=True)`.

### Definición Pydantic

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        frozen=True,
    )
    DATABASE_URL: str = (
        "postgresql+asyncpg://realtor_dev:realtor_dev@localhost:5432/realtor_dev"
    )
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
```

## 2. Migración Baseline

Archivo: `alembic/versions/001_bootstrap_extensions.py`

```python
"""bootstrap: instala extensión pgcrypto

Revision ID: 001
Revises: None
Create Date: 2026-06-08
"""
from typing import Sequence, Union
from alembic import op

revision: str = "001_bootstrap"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS pgcrypto")
```

### Tabla `alembic_version`

Creada automáticamente por Alembic al ejecutar `alembic upgrade head`.

| Columna | Tipo | Descripción |
|---|---|---|
| `version_num` | `VARCHAR(32)` | ID de la revisión aplicada (PK) |

## 3. Dashboard Demo

Datos hardcodeados en el handler de `GET /`. Sin entidad de base de datos.

### Tarjetas de métrica

| Label | Valor | Icono |
|---|---|---|
| Propiedades activas | 124 | `building-2` |
| Inquilinos al día | 87 | `users` |
| Contratos vigentes | 53 | `file-text` |

### Contexto Jinja2

```python
context = {
    "request": request,
    "metricas": [
        {"label": "Propiedades activas", "valor": 124, "icono": "building-2"},
        {"label": "Inquilinos al día", "valor": 87, "icono": "users"},
        {"label": "Contratos vigentes", "valor": 53, "icono": "file-text"},
    ],
}
```

## 4. Diagrama de dependencias

```
.env ──► Settings(config.py)
              │
              ├──► database.py (AsyncEngine + AsyncSession)
              │         │
              │         └──► alembic/env.py (migraciones)
              │
              └──► main.py (lifespan, GET /health, GET /)
                        │
                        ├──► templates/base.html
                        ├──► templates/dashboard.html
                        ├──► templates/components/*
                        └──► templates/macros/icons.html
```

## 5. Notas para specs futuras

- Entidades de dominio heredarán de `Base` (`app/database.py`).
- PKs usarán `UUID` con `default=uuid.uuid4` o `server_default=func.gen_random_uuid()`.
- Schemas Pydantic usarán `model_config = ConfigDict(frozen=True)`.
- Migraciones se crearán con `alembic revision --autogenerate -m "descripción en español"`.
- Tablas en plural snake_case: `propiedades`, `inquilinos`, `contratos_renta`.
