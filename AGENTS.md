<!-- SPECKIT START -->
Para obtener contexto adicional sobre tecnologías, estructura del proyecto,
comandos de shell y otra información importante, lee el plan vigente.
<!-- SPECKIT END -->

# Instrucciones — Proyecto Realtor

Este archivo resume las reglas obligatorias del proyecto. La fuente de verdad
completa es `.specify/memory/constitution.md`. Ante cualquier conflicto, la
constitución prevalece.

Cada `spec.md` aprobado bajo `.specify/specs/` es la fuente de verdad funcional
de su feature, siempre que no contradiga la constitución.

## Idioma

Todo el contenido `.md`, los comentarios, los docstrings y los mensajes de
commit DEBEN estar en español. NUNCA mezclar idiomas dentro de un mismo archivo.

## Stack obligatorio inmutable

- Python 3.13+, gestionado con `uv` (`pyproject.toml` + `uv.lock`).
- FastAPI para HTTP.
- Jinja2 server-rendered + HTMX para vistas.
- SQLAlchemy 2.x async con `Mapped[...]`, `mapped_column`, `select()` y
  `AsyncSession`.
- Pydantic v2 con `model_config = ConfigDict(frozen=True)` en todos los DTOs.
- PostgreSQL vía asyncpg ejecutado localmente con Docker o Docker Compose.
- Alembic como única herramienta de migraciones.
- pytest + pytest-asyncio + httpx.AsyncClient para tests.
- Testcontainers para pruebas de integración con infraestructura real.
- Ruff + mypy `--strict` mínimo en `app/modules/`.
- Iconografía SVG outline de Lucide vendoreada en `app/static/icons/`.

## Prohibiciones absolutas

- `pip`, `poetry`, `conda`, `pipenv`, `requirements.txt`, `setup.py`.
- Bootstrap, Tailwind, Bulma, Foundation o cualquier framework CSS.
- Cargar HTMX o cualquier JS de terceros desde CDN en runtime.
- Iconos como webfont, Bootstrap Icons, Font Awesome, Material Icons font,
  emojis o caracteres Unicode como íconos funcionales.
- Estilo legacy de SQLAlchemy: `Column(...)` en clase, `Query` o sesiones
  síncronas.
- Funciones `def` síncronas en `routes.py`, `service.py` o `repository.py`
  cuando hagan I/O.
- Carpetas globales por capa técnica: `controllers/`, `services/`,
  `repositories/`, `handlers/`, `managers/` fuera de un módulo.
- Exponer entidades SQLAlchemy como respuesta HTTP.
- Retornar `dict` libres en errores.
- Strings mágicos para estados de dominio.
- Usar Supabase en producción o desarrollo.
- Usar extensión `.yml`; usar siempre `.yaml`.
- Separar frontend y backend en aplicaciones o repositorios independientes.
- Crear microservicios sin enmienda formal a la constitución.

## Arquitectura: Vertical Slice

Cada feature vive en `app/modules/<feature>/` con estos artefactos:

- `routes.py`
- `schemas.py`
- `models.py`
- `repository.py`
- `service.py`
- `templates/`
- `tests/`

La lógica de negocio vive SIEMPRE en `service.py`. `routes.py` es delgado:
parsea entrada, llama al servicio y retorna respuesta. `repository.py` solo hace
acceso a datos.

La lógica compartida solo se extrae cuando exista duplicación real demostrable,
nunca por anticipación.

## Spec-Driven Development

NO implementar nada que no esté descrito en un `spec.md` aprobado bajo
`.specify/specs/`.

Cada spec debe vivir en:

```text
.specify/specs/<numero>-<nombre>/
```

y contener, como mínimo:

```text
spec.md
plan.md
tasks.md
```

El orden de implementación lo define el prefijo numérico de cada spec. Toda tarea
debe rastrear a `tasks.md`.

## Flujo Spec Kit obligatorio

Toda feature debe seguir este flujo:

```text
/speckit.specify
/speckit.clarify
/speckit.plan
/speckit.analyze
/speckit.tasks
/speckit.implement
```

Ninguna fase puede saltarse.

## Test-Driven Development

Ciclo Red-Green-Refactor obligatorio:

1. Red: escribir primero una prueba que falle por el motivo correcto.
2. Green: implementar el código mínimo necesario para que la prueba pase.
3. Refactor: mejorar el diseño sin cambiar el comportamiento observable.

No se escribe código de producción sin una prueba asociada. Toda regla de negocio
debe estar cubierta por pruebas. Toda corrección de bug comienza con una prueba
que reproduzca el fallo. Refactorizar solo con la suite en verde.

## Calidad y validación

Antes de cerrar una implementación, ejecutar como mínimo:

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy --strict app/modules/
```

Las pruebas unitarias usan pytest. Las pruebas asíncronas usan pytest-asyncio.
Las pruebas HTTP usan httpx.AsyncClient. Las pruebas de integración que requieran
PostgreSQL usan Testcontainers.

## Base de datos

- PostgreSQL se ejecuta localmente con Docker o Docker Compose.
- La base de datos de producción no usará Supabase.
- Las migraciones se gestionan exclusivamente con Alembic.
- Las sesiones de base de datos se manejan mediante dependencias controladas con
  inyección de `AsyncSession`.
- `.env` nunca debe versionarse con secretos reales.
- `.env.example` debe existir como plantilla.
- La infraestructura local debe usar `.yaml`, nunca `.yml`.

## Frontend y sistema visual

- HTMX vive en `app/static/vendor/htmx.min.js`.
- El CSS propio vive en `app/static/css/app.css`.
- Los iconos SVG outline viven en `app/static/icons/`.
- La librería estándar de iconografía es Lucide.
- Las plantillas compartidas viven en `app/templates/`.
- Las plantillas específicas viven dentro del módulo correspondiente.
- Los componentes compartidos viven en `app/templates/components/`.
- Las macros compartidas viven en `app/templates/macros/`.

## Estructura obligatoria del repositorio

```text
app/
  __init__.py
  main.py
  config.py
  database.py
  modules/
    <feature>/
      routes.py
      schemas.py
      models.py
      repository.py
      service.py
      templates/
      tests/
  static/
    css/
      app.css
    vendor/
      htmx.min.js
    icons/
  templates/
    base.html
    components/
    macros/
alembic/
  env.py
  versions/
pyproject.toml
uv.lock
docker-compose.yaml
.env.example
```

## Complexity Tracking

Toda desviación del stack, arquitectura, estructura, flujo obligatorio o reglas
de la constitución debe registrarse en la sección `Complexity Tracking` de
`plan.md`.

## Conflicto entre capas

Durante la implementación de una spec, aplica este orden:

```text
constitución > spec > AGENTS.md > instructions > comando
```

Si hay conflicto entre capas, se debe pausar, advertir el conflicto y seguir la
capa de mayor autoridad.