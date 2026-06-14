# Guía de Validación Rápida: Bootstrap del Proyecto Realtor

**Feature**: `001-bootstrap-proyecto` | **Date**: 2026-06-08

## Prerrequisitos

- Python 3.13.13 (o `uv` capaz de descargarlo automáticamente)
- Docker y Docker Compose
- `uv` instalado (https://docs.astral.sh/uv/)

## Setup inicial

```bash
# 1. Instalar dependencias
uv sync

# 2. Copiar variables de entorno
cp .env.example .env

# 3. Levantar PostgreSQL local
docker compose up -d

# 4. Esperar a que PostgreSQL esté listo
docker compose exec db pg_isready -U realtor_dev

# 5. Aplicar migración baseline
uv run alembic upgrade head
```

## Validación de endpoints

```bash
# Arrancar servidor en background
uv run fastapi dev app/main.py &
sleep 2

# GET /health — éxito
curl -s http://localhost:8000/health | python3 -m json.tool
# Esperado: {"status": "ok", "database": "ok"}, HTTP 200

# GET /health — fallo (simulado)
docker compose stop db
curl -s -w "\nHTTP %{http_code}\n" http://localhost:8000/health
# Esperado: HTTP 503, {"status":"error","database":"unavailable","detail":"timeout after 2s"}
docker compose up -d

# GET / — dashboard
curl -s http://localhost:8000/
# Esperado: HTML con class="sidebar", class="navbar", 3× class="tarjeta-metrica"
```

## Validación visual (navegador)

1. Abrir `http://localhost:8000/`
2. Verificar sidebar visible con iconos de navegación
3. Verificar 3 tarjetas de métrica: "Propiedades activas (124)", "Inquilinos al día (87)", "Contratos vigentes (53)"
4. Reducir viewport < 1024px: sidebar colapsa a overlay, botón hamburguesa visible
5. Reducir viewport < 768px: sidebar oculta, toggle hamburguesa la revela

## Validación de calidad estática

```bash
uv run ruff check .              # Esperado: código de salida 0, sin warnings
uv run ruff format --check .     # Esperado: código de salida 0
uv run mypy --strict app/modules/  # Esperado: Success: no issues found
```

## Validación de tests

```bash
uv run pytest -v
# Esperado:
#   tests/test_health.py::test_health_ok PASSED
#   tests/test_health.py::test_health_db_unavailable PASSED
#   tests/test_dashboard.py::test_dashboard_ok PASSED
```

## Limpieza

```bash
docker compose down        # Detener PostgreSQL (datos persisten)
docker compose down -v     # Destruir volumen de datos
```
