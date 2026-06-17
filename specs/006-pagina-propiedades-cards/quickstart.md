# Quickstart: Página de propiedades con cards

**Feature**: 006-pagina-propiedades-cards
**Phase**: 1 — Design
**Date**: 2026-06-16

## Requisitos previos

- Docker y Docker Compose instalados y ejecutándose (`docker compose up -d`)
- `uv` instalado y dependencias sincronizadas (`uv sync`)
- Migraciones aplicadas (`uv run alembic upgrade head`)
- Seed de propiedades ejecutado (`uv run python scripts/dev/seed_propiedades.py`)

## Pasos para validar la feature

### 1. Verificar que el endpoint responde

```bash
# Iniciar servidor
uv run fastapi dev app/main.py

# Solicitar página de propiedades
curl -s http://localhost:8000/propiedades | head -c 500
```

Salida esperada: HTML con `<html lang="es">`, sidebar y contenido.

### 2. Verificar cards con datos reales (10 propiedades del seed)

```bash
curl -s http://localhost:8000/propiedades | grep -c "card-propiedad"
```

Salida esperada: `10` (una card por propiedad del seed)

### 3. Verificar campos visibles en las cards

```bash
curl -s http://localhost:8000/propiedades > /tmp/propiedades.html
python3 -c "
html = open('/tmp/propiedades.html').read()
checks = ['card-propiedad__imagen', 'habitaciones', 'baños', 'm²', '\$', 'badge-estado']
for c in checks:
    assert c in html, f'Falta campo: {c}'
print('Todos los campos presentes')
"
```

### 4. Verificar formato de precio y área

```bash
curl -s http://localhost:8000/propiedades | grep -oP '\$\d{1,3}(,\d{3})*\.\d{2}' | head -5
curl -s http://localhost:8000/propiedades | grep -oP '\d{1,3}(,\d{3})*\sm²' | head -5
```

### 5. Verificar estado vacío (sin propiedades)

```bash
# Limpiar la base de datos
docker compose exec db psql -U realtor_dev -d realtor_dev -c "DELETE FROM propiedades;"

# Solicitar página
curl -s http://localhost:8000/propiedades | grep -i "no hay propiedades"
```

Debe retornar el mensaje de estado vacío.

### 6. Verificar navegación desde sidebar

```bash
curl -s http://localhost:8000/ | grep -o 'href="/propiedades"'
```

Salida esperada: `href="/propiedades"` (el enlace del sidebar apunta a la nueva página)

### 7. Verificar placeholder de imagen

```bash
# Crear propiedad sin imagen
docker compose exec db psql -U realtor_dev -d realtor_dev -c "
INSERT INTO propiedades (titulo, direccion, ciudad, precio_mensual, habitaciones, banos, area, estado, imagen)
VALUES ('Sin Foto Test', 'Calle Placeholder 1', 'Miami', 1000, 1, 1, 500, 'disponible', '');
"

curl -s http://localhost:8000/propiedades | grep -c "card-propiedad__imagen-placeholder"
```

Salida esperada: `>= 1` (al menos una card con placeholder)

### 8. Verificar responsive (CSS)

```bash
curl -s http://localhost:8000/propiedades | grep -c "propiedades-grid"
```

El CSS debe incluir media queries para 3/2/1 columnas en `app.css`.

### 9. Ejecutar pruebas

```bash
# Pruebas unitarias del servicio
uv run pytest tests/unit/propiedades/ -q

# Pruebas de integración (requiere PostgreSQL + seed)
uv run pytest tests/integration/propiedades/ -q

# Cobertura
uv run pytest --cov=app/modules/propiedades --cov-fail-under=80 tests/unit/propiedades tests/integration/propiedades -q
```

### 10. Validaciones de calidad

```bash
uv run ruff check app/modules/propiedades/
uv run mypy --strict app/modules/propiedades/
uv run ruff check app/static/css/app.css
```

## Reset completo para entorno limpio

```bash
docker compose exec db psql -U realtor_dev -d realtor_dev -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
uv run alembic upgrade head
uv run python scripts/dev/seed_propiedades.py
```
