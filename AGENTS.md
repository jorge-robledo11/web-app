# Instrucciones para GitHub Copilot — Proyecto Realtor

Este archivo resume las reglas obligatorias del proyecto. La fuente de verdad
completa es `.specify/memory/constitution.md`. Ante cualquier conflicto, la
constitution prevalece.

## Idioma

Todo el contenido `.md`, los comentarios, los docstrings y los mensajes de
commit DEBEN estar en español. NUNCA mezclar idiomas dentro de un mismo
archivo.

## Stack obligatorio (inmutable)

- Python 3.13+, gestionado con `uv` (`pyproject.toml` + `uv.lock`).
- FastAPI para HTTP, Jinja2 server-rendered + HTMX para vistas.
- SQLAlchemy 2.x async (estilo `Mapped[...]` + `mapped_column` + `select()` +
  `AsyncSession`). PROHIBIDO el estilo legacy (`Column(...)` en clase,
  `Query`, sesiones síncronas).
- Pydantic v2 con `model_config = ConfigDict(frozen=True)` en todos los DTOs.
- PostgreSQL vía asyncpg ejecutado localmente con Docker o Docker Compose.
- Alembic única herramienta de migraciones.
- pytest + pytest-asyncio + httpx.AsyncClient para tests.
- Ruff + mypy `--strict` mínimo en `app/modules/`.
- Iconografía: SVG outline de Lucide vendoreados en `app/static/icons/`.

## Prohibiciones absolutas

- `pip`, `poetry`, `conda`, `pipenv`, `requirements.txt`, `setup.py`.
- Bootstrap, Tailwind, Bulma, Foundation o cualquier framework CSS.
- Cargar HTMX o cualquier JS de terceros desde CDN en runtime. HTMX vive
  en `app/static/vendor/htmx.min.js`.
- Iconos como webfont (Bootstrap Icons, Font Awesome, Material Icons font),
  emojis o caracteres Unicode como íconos funcionales.
- Funciones `def` síncronas en `routes.py`, `service.py` o `repository.py`
  cuando hagan I/O. Solo `def` sync para puro cómputo en memoria.
- Carpetas globales por capa técnica: `controllers/`, `services/`,
  `repositories/`, `handlers/`, `managers/` fuera de un módulo.
- Exponer entidades SQLAlchemy como respuesta HTTP. Siempre mapear a
  Pydantic.
- Retornar `dict` libres en errores. Usar `HTTPException` o modelo de error
  tipado.
- Strings mágicos para estados de dominio. Usar `Enum` o tipos explícitos.

## Arquitectura: Vertical Slice

Cada feature vive en `app/modules/<feature>/` con exactamente estos archivos:
`routes.py`, `schemas.py`, `models.py`, `repository.py`, `service.py`,
`templates/`, `tests/`.

La lógica de negocio vive SIEMPRE en `service.py`. `routes.py` es delgado:
parsea entrada, llama al servicio, retorna respuesta. `repository.py` solo
hace acceso a datos.

## Spec-Driven Development

NO implementar nada que no esté descrito en un `spec.md` aprobado bajo
`.specify/specs/`. El orden de implementación lo define el prefijo numérico
de cada spec. Toda tarea debe rastrear a `tasks.md`.

## Test-Driven Development

Ciclo Red-Green-Refactor obligatorio:

1. Red: escribir primero una prueba que falle por el motivo correcto.
2. Green: implementar el código mínimo necesario para que la prueba pase.
3. Refactor: mejorar el diseño sin cambiar el comportamiento observable.

No se escribe código de producción sin una prueba asociada. Toda regla de
negocio debe estar cubierta por pruebas. Toda corrección de bug comienza con
una prueba que reproduzca el fallo. Refactorizar solo con la suite en verde.

## Base de datos (PostgreSQL local)

- PostgreSQL se ejecuta localmente con Docker o Docker Compose.
- La base de datos de producción no usará Supabase.
- Las migraciones se gestionan con Alembic.
- Las sesiones de base de datos se manejan mediante dependencias controladas.
- `.env` nunca debe versionarse con secretos reales.