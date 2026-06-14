# Quickstart: Propiedades base

**Feature**: 004-propiedades-base
**Phase**: 1 — Design
**Date**: 2026-06-14

## Requisitos previos

- Docker y Docker Compose instalados
- `uv` instalado
- Repositorio clonado y dependencias instaladas (`uv sync`)

## Pasos para validar la feature

### 1. Levantar PostgreSQL

```bash
docker compose up -d
```

### 2. Aplicar migración de estructura

```bash
uv run alembic upgrade head
```

Esto ejecuta la migración `002_create_propiedades.py` que crea:
- Tipo enum `estado_propiedad` (implícito por DDL de tabla)
- Tabla `propiedades` con todas las columnas, constraints e índices

### 3. Ejecutar carga inicial de propiedades

```bash
uv run python scripts/seed_propiedades.py
```

Salida esperada:
```
[seed] Insertadas 10 propiedades en Miami
[seed] 0 duplicadas, 10 nuevas
```

### 4. Verificar idempotencia

```bash
uv run python scripts/seed_propiedades.py
```

Salida esperada:
```
[seed] 10 propiedades ya existentes, 0 nuevas
[seed] Actualizadas 0 (sin cambios)
```

### 5. Verificar reversibilidad

```bash
uv run alembic downgrade -1
uv run alembic upgrade head
```

Ambos comandos deben finalizar sin errores.

### 6. Ejecutar pruebas

```bash
uv run pytest app/modules/propiedades/tests -q
```

### 7. Ejecutar validaciones de calidad

```bash
uv run ruff check app/modules/propiedades/
uv run mypy --strict app/modules/propiedades/
```

Ambos deben finalizar sin hallazgos.

### 8. Reset completo para entorno limpio

```bash
docker compose exec db psql -U postgres -d realtor -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
uv run alembic upgrade head
uv run python scripts/seed_propiedades.py
```

## Verificaciones rápidas

```bash
# Contar propiedades
docker compose exec db psql -U postgres -d realtor -c "SELECT count(*) FROM propiedades;"
# Esperado: 10

# Verificar estados
docker compose exec db psql -U postgres -d realtor -c "SELECT estado, count(*) FROM propiedades GROUP BY estado;"
# Esperado: disponible=4, rentada=3, mantenimiento=2, inactiva=1

# Verificar que no hay timestamps enviados desde Python (todos tienen valor)
docker compose exec db psql -U postgres -d realtor -c "SELECT count(*) FROM propiedades WHERE created_at IS NULL;"
# Esperado: 0

# Verificar idempotencia: re-ejecutar seed y contar
uv run python scripts/seed_propiedades.py
docker compose exec db psql -U postgres -d realtor -c "SELECT count(*) FROM propiedades;"
# Esperado: 10
```
