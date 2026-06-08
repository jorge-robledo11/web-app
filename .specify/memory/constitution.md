<!--
Informe de impacto de sincronización
- Cambio de versión: plantilla inicial -> 1.0.0
- Secciones agregadas:
  - I. Idioma
  - II. Stack obligatorio inmutable
  - III. Prohibiciones absolutas
  - IV. Arquitectura: Vertical Slice
  - V. Spec-Driven Development
  - VI. Flujo Spec Kit obligatorio
  - VII. Test-Driven Development
  - VIII. Calidad y validación
  - IX. Base de datos
  - X. Async-First
  - XI. Frontend y sistema visual
  - XII. Estructura obligatoria del repositorio
  - XIII. Contratos de dominio
  - XIV. Complexity Tracking
  - XV. Jerarquía de autoridad
  - XVI. Gobernanza
- Secciones modificadas:
  - Ninguna
- Secciones eliminadas:
  - Ninguna
- Artefactos relacionados a revisar:
  - AGENTS.md
  - .opencode/instructions/*.md
  - .opencode/commands/*.md
  - .specify/templates/*.md
- Pendientes de seguimiento:
  - Generar o actualizar AGENTS.md desde esta constitución.
  - Verificar que las instrucciones por área no contradigan esta constitución.
  - Verificar que los comandos de Spec Kit respeten el flujo obligatorio.
-->

# Constitución del Proyecto Realtor

Esta constitución es la fuente de verdad superior del proyecto. Toda decisión
técnica, arquitectónica o de proceso debe ser consistente con los principios aquí
declarados. Ante cualquier conflicto entre documentos, esta constitución
prevalece.

## I. Idioma

Todo el contenido `.md`, los comentarios, los docstrings y los mensajes de
commit DEBEN estar en español. NUNCA mezclar idiomas dentro de un mismo archivo.

## II. Stack obligatorio inmutable

El proyecto es un monolito Python con los siguientes componentes fijos. Ningún
componente del stack puede ser reemplazado sin una enmienda formal a esta
constitución.

| Componente | Herramienta |
|---|---|
| Runtime | Python 3.13+, gestionado con `uv` |
| Empaquetado | `pyproject.toml` + `uv.lock` |
| HTTP | FastAPI |
| Vistas | Jinja2 server-rendered + HTMX |
| ORM | SQLAlchemy 2.x async con `Mapped[...]`, `mapped_column`, `select()` y `AsyncSession` |
| Validación | Pydantic v2 con `model_config = ConfigDict(frozen=True)` |
| Base de datos | PostgreSQL vía asyncpg, local con Docker o Docker Compose |
| Migraciones | Alembic como única herramienta permitida |
| Tests | pytest + pytest-asyncio + httpx.AsyncClient |
| Integración | Testcontainers cuando se requiera infraestructura real |
| Calidad estática | Ruff + mypy `--strict` mínimo en `app/modules/` |
| Iconografía | SVG outline de Lucide vendoreados en `app/static/icons/` |

## III. Prohibiciones absolutas

Las siguientes herramientas, prácticas y patrones están PROHIBIDOS en todo el
proyecto:

- `pip`, `poetry`, `conda`, `pipenv`, `requirements.txt`, `setup.py`.
- Bootstrap, Tailwind, Bulma, Foundation o cualquier framework CSS.
- Cargar HTMX o cualquier JS de terceros desde CDN en runtime.
- Iconos como webfont, Bootstrap Icons, Font Awesome, Material Icons font,
  emojis o caracteres Unicode como íconos funcionales.
- Estilo legacy de SQLAlchemy: `Column(...)` en clase, `Query` o sesiones
  síncronas.
- Funciones `def` síncronas en `routes.py`, `service.py` o `repository.py`
  cuando realicen I/O.
- Carpetas globales por capa técnica: `controllers/`, `services/`,
  `repositories/`, `handlers/`, `managers/` fuera de un módulo.
- Exponer entidades SQLAlchemy como respuesta HTTP.
- Retornar `dict` libres en errores.
- Strings mágicos para estados de dominio.
- Usar Supabase en producción o desarrollo.
- Usar extensión `.yml` para archivos YAML; usar siempre `.yaml`.
- Separar frontend y backend en aplicaciones o repositorios independientes.
- Crear microservicios sin una enmienda formal a esta constitución.

## IV. Arquitectura: Vertical Slice

El proyecto sigue una arquitectura de Vertical Slice. Cada feature vive en su
propio módulo bajo `app/modules/<feature>/`.

Cada módulo DEBE contener estos artefactos:

- `routes.py` — capa delgada: parsea entrada, llama al servicio y retorna
  respuesta.
- `schemas.py` — DTOs Pydantic v2 con `frozen=True`.
- `models.py` — entidades SQLAlchemy 2.x async con `Mapped[...]` y
  `mapped_column`.
- `repository.py` — solo acceso a datos.
- `service.py` — lógica de negocio del módulo.
- `templates/` — plantillas Jinja2 del módulo.
- `tests/` — pruebas unitarias, integración o endpoint del módulo.

La lógica de negocio reside en `service.py`. `routes.py` y `repository.py` son
capas de entrada e infraestructura sin reglas de negocio. La lógica compartida
solo se extrae cuando exista duplicación real demostrable, nunca por anticipación.

## V. Spec-Driven Development

No se implementa NADA que no esté descrito en un `spec.md` aprobado bajo
`.specify/specs/`.

Cada `spec.md` aprobado es la fuente de verdad funcional de su feature, siempre
que no contradiga esta constitución.

Cada spec debe vivir en una carpeta secuencial plana:

```text
.specify/specs/<numero>-<nombre>/
```

Cada spec debe contener, como mínimo:

```text
spec.md
plan.md
tasks.md
```

El orden de implementación lo define el prefijo numérico de cada spec. Toda tarea
de implementación debe rastrear a un `tasks.md` generado desde la spec.

## VI. Flujo Spec Kit obligatorio

Toda feature debe seguir este flujo obligatorio:

```text
/speckit.specify
/speckit.clarify
/speckit.plan
/speckit.analyze
/speckit.tasks
/speckit.implement
```

Ninguna fase puede saltarse. Cada fase depende de los artefactos generados por la
fase anterior.

Reglas del flujo:

- `specify` crea o actualiza `spec.md`.
- `clarify` resuelve ambigüedades antes del plan.
- `plan` crea `plan.md` con decisiones técnicas y dependencias.
- `analyze` valida consistencia entre spec, plan y restricciones.
- `tasks` crea `tasks.md` con tareas pequeñas, ordenadas y verificables.
- `implement` modifica código real solo después de existir spec, plan y tasks.

## VII. Test-Driven Development

El ciclo Red-Green-Refactor es obligatorio:

1. **Red**: escribir primero una prueba que falle por el motivo correcto.
2. **Green**: implementar el código mínimo necesario para que la prueba pase.
3. **Refactor**: mejorar el diseño sin cambiar el comportamiento observable.

Reglas complementarias:

- No se escribe código de producción sin una prueba asociada.
- Toda regla de negocio debe estar cubierta por pruebas.
- Toda corrección de bug comienza con una prueba que reproduzca el fallo.
- Refactorizar solo con la suite de tests en verde.
- No se elimina ni debilita una prueba para hacer pasar la suite.

## VIII. Calidad y validación

Toda implementación debe poder validarse localmente con comandos reproducibles.

Comandos mínimos esperados:

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy --strict app/modules/
```

Reglas de testing:

- Las pruebas unitarias usan pytest.
- Las pruebas asíncronas usan pytest-asyncio.
- Las pruebas HTTP usan httpx.AsyncClient.
- Las pruebas de integración que requieran PostgreSQL usan Testcontainers.
- La base de datos de pruebas debe estar aislada.
- Las pruebas deben ser deterministas y enfocadas en comportamiento observable.

## IX. Base de datos

- PostgreSQL se ejecuta localmente con Docker o Docker Compose.
- La base de datos de producción no usará Supabase.
- Las migraciones se gestionan exclusivamente con Alembic.
- Las sesiones de base de datos se manejan mediante dependencias controladas con
  inyección de `AsyncSession`.
- `.env` nunca debe versionarse con secretos reales.
- `.env.example` debe existir como plantilla de configuración.
- La infraestructura local debe usar archivos `.yaml`, nunca `.yml`.

## X. Async-First

Todo I/O del sistema debe ser asíncrono cuando forme parte del flujo web,
persistencia o integración externa.

Esto incluye:

- Base de datos.
- HTTP saliente.
- Colas.
- Storage remoto.
- Servicios externos.
- Operaciones de infraestructura.

Solo se permite `def` síncrono para puro cómputo en memoria, mapeos, cálculos o
validaciones sin I/O.

## XI. Frontend y sistema visual

La interfaz será server-rendered con Jinja2 y mejorada progresivamente con HTMX.
No se debe convertir la aplicación en una SPA.

Reglas obligatorias:

- HTMX vive vendoreado en `app/static/vendor/htmx.min.js`.
- El CSS propio vive en `app/static/css/app.css`.
- Los iconos SVG outline viven en `app/static/icons/`.
- La librería estándar de iconografía es Lucide.
- Las plantillas compartidas viven en `app/templates/`.
- Las plantillas específicas viven dentro del módulo correspondiente.
- Los componentes compartidos viven en `app/templates/components/`.
- Las macros compartidas viven en `app/templates/macros/`.

## XII. Estructura obligatoria del repositorio

La estructura base del proyecto debe respetar esta organización:

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
        *.html
      tests/
        test_*.py
  static/
    css/
      app.css
    vendor/
      htmx.min.js
    icons/
      *.svg
  templates/
    base.html
    components/
      _*.html
    macros/
      *.html
alembic/
  env.py
  versions/
pyproject.toml
uv.lock
docker-compose.yaml
.env.example
```

Cualquier desviación debe justificarse en `plan.md`.

## XIII. Contratos de dominio

- Las entidades SQLAlchemy no se exponen como respuesta HTTP.
- Las respuestas HTTP se mapean a DTOs Pydantic.
- Todos los DTOs Pydantic deben usar `model_config = ConfigDict(frozen=True)`.
- Los estados de dominio se modelan con `Enum` o tipos explícitos.
- Los errores usan `HTTPException` o modelos de error tipados.
- Los límites del sistema validan entradas antes de ejecutar lógica de negocio.

## XIV. Complexity Tracking

Toda desviación del stack, arquitectura, estructura, flujo obligatorio o reglas
de esta constitución debe registrarse explícitamente en la sección
`Complexity Tracking` de `plan.md`.

Debe incluir:

- Qué regla se desvía.
- Por qué la desviación es necesaria.
- Alternativas consideradas.
- Riesgos introducidos.
- Cómo se mitigarán esos riesgos.
- Cómo se validará que la desviación no rompe el sistema.

En ausencia de justificación, la desviación debe rechazarse.

## XV. Jerarquía de autoridad

Durante la implementación de una spec, aplica el siguiente orden de prioridad
ante cualquier conflicto:

```text
constitución > spec > AGENTS.md > instructions > comando
```

Si hay conflicto entre capas, se debe pausar, advertir el conflicto
explícitamente y seguir la capa de mayor autoridad.

## XVI. Gobernanza

- Esta constitución es la fuente de verdad suprema del proyecto. Ninguna
  decisión, spec o implementación puede contradecirla.
- Toda modificación a esta constitución requiere una enmienda documentada con
  justificación, impacto evaluado y plan de migración si aplica.
- Las enmiendas se versionan siguiendo el esquema semántico
  `MAJOR.MINOR.PATCH`.
- **MAJOR**: cambios incompatibles en stack, arquitectura, flujo obligatorio o
  principios.
- **MINOR**: nuevas secciones, nuevos principios o ampliaciones materiales.
- **PATCH**: correcciones de redacción, aclaraciones o cambios no semánticos.
- El cumplimiento de esta constitución se verifica en cada code review y en cada
  etapa del flujo Spec-Driven.
- La complejidad introducida debe justificarse explícitamente. Ante la duda,
  elegir la opción más simple.

**Versión**: 1.0.0 | **Ratificada**: 2026-06-08 | **Última enmienda**: 2026-06-08