# Quickstart: Dashboard con datos reales

**Feature**: 005-dashboard-datos-reales
**Phase**: 1 — Design
**Date**: 2026-06-15

## Requisitos previos

- Docker y Docker Compose instalados y ejecutándose (`docker compose up -d`)
- `uv` instalado y dependencias sincronizadas (`uv sync`)
- Migraciones aplicadas (`uv run alembic upgrade head`)
- Seed de propiedades ejecutado (`uv run python scripts/dev/seed_propiedades.py`)

## Pasos para validar la feature

### 1. Verificar métricas reales con seed aplicado

```bash
# Iniciar servidor
uv run fastapi dev app/main.py

# Solicitar dashboard
curl -s http://localhost:8000/ | grep -o 'Propiedades disponibles\|Propiedades rentadas\|Ingresos\|Vencidos'
```

Salida esperada:
```
Propiedades disponibles
Propiedades rentadas
Ingresos
Vencidos
```

Verificar valores reales (4 disponibles, 3 rentadas):
```bash
curl -s http://localhost:8000/ | grep -oP 'tarjeta-metrica__valor">\K[0-9,]+'
```

Salida esperada (primeros dos valores):
```
4
3
0
0
```

### 2. Verificar métricas no operativas

```bash
curl -s http://localhost:8000/ | grep -c "No disponible"
```

Salida esperada: `2` (una por ingresos, una por vencidos)

### 3. Verificar estado vacío (sin propiedades)

```bash
# Limpiar la base de datos
docker compose exec db psql -U realtor_dev -d realtor_dev -c "DELETE FROM propiedades;"

# Solicitar dashboard
curl -s http://localhost:8000/ | grep -i "no hay datos\|sin datos\|vacío\|vacio"
```

Debe retornar el mensaje de estado vacío.

### 4. Restaurar seed después de la prueba

```bash
uv run python scripts/dev/seed_propiedades.py
```

### 5. Verificar orden de secciones

```bash
curl -s http://localhost:8000/ > /tmp/dashboard.html
python3 -c "
html = open('/tmp/dashboard.html').read()
pos_m = html.find('class=\"metricas\"')
pos_a = html.find('class=\"accesos-rapidos\"')
pos_ac = html.find('class=\"actividad\"')
assert pos_m < pos_a < pos_ac, f'Orden roto: {pos_m} {pos_a} {pos_ac}'
print('Orden correcto: métricas → accesos → actividad')
"
```

### 6. Verificar accesos rápidos sin cambios

```bash
curl -s http://localhost:8000/ | grep -c "acceso-rapido"
```

Salida esperada: `4`

### 7. Ejecutar pruebas

```bash
# Pruebas unitarias del servicio
uv run pytest tests/unit/dashboard/ -q

# Pruebas de integración (requiere PostgreSQL + seed)
uv run pytest tests/integration/dashboard/ -q

# Pruebas existentes actualizadas
uv run pytest tests/unit/test_dashboard.py -q
```

### 8. Validaciones de calidad

```bash
uv run ruff check app/modules/dashboard/
uv run mypy --strict app/modules/dashboard/
uv run ruff check app/modules/propiedades/repository.py
```

## Reset completo para entorno limpio

```bash
docker compose exec db psql -U realtor_dev -d realtor_dev -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
uv run alembic upgrade head
uv run python scripts/dev/seed_propiedades.py
```
