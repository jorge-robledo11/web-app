<!--
Informe de impacto de sincronización
- Cambio de versión: 1.2.0 -> 1.3.0
- Secciones agregadas:
  - IX.5. Organización de tests (nueva subsección con estructura
    obligatoria tests/unit/ y tests/integration/)
- Secciones modificadas:
  - XII. Frontend y sistema visual: subsección «Sistema visual
    canónico» degradada de ## a ### para corregir nivel jerárquico
  - XIII. Estructura obligatoria del repositorio: tests movidos de
    app/modules/<feature>/tests/ a tests/unit/<feature>/ y
    tests/integration/<feature>/ en raíz
- Secciones eliminadas:
  - Ninguna
- Artefactos relacionados revisados:
  - AGENTS.md ✅ ya usa 3.13.13
  - .specify/templates/plan-template.md ✅ sin cambios necesarios
  - .specify/templates/spec-template.md ✅ sin cambios necesarios
  - .specify/templates/tasks-template.md ✅ sin cambios necesarios
  - tests/conftest.py ✅ fixture async_client en raíz
  - tests/integration/conftest.py ✅ Testcontainers PostgreSQL
- Pendientes de seguimiento:
  - Ninguno
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

| Componente       | Herramienta                                                                          |
| ---------------- | ------------------------------------------------------------------------------------ |
| Runtime          | Python 3.13.13, gestionado con `uv`                                                   |
| Empaquetado      | `pyproject.toml` + `uv.lock`                                                         |
| HTTP             | FastAPI                                                                              |
| Vistas           | Jinja2 server-rendered + HTMX                                                        |
| ORM              | SQLAlchemy 2.x async con `Mapped[...]`, `mapped_column`, `select()` y `AsyncSession` |
| Validación       | Pydantic v2 con `model_config = ConfigDict(frozen=True)`                             |
| Base de datos    | PostgreSQL vía asyncpg, local con Docker o Docker Compose                            |
| Migraciones      | Alembic como única herramienta permitida                                             |
| Tests            | pytest + pytest-asyncio + httpx.AsyncClient                                          |
| Integración      | Testcontainers cuando se requiera infraestructura real                               |
| Calidad estática | Ruff + mypy `--strict` mínimo en `app/modules/`                                      |
| Iconografía      | SVG outline de Lucide vendoreados en `app/static/icons/`                             |

## III. Prohibiciones absolutas

Las siguientes herramientas, prácticas y patrones están PROHIBIDOS en todo el
proyecto:

* `pip`, `poetry`, `conda`, `pipenv`, `requirements.txt`, `setup.py`.
* Bootstrap, Tailwind, Bulma, Foundation o cualquier framework CSS.
* Cargar HTMX o cualquier JS de terceros desde CDN en runtime.
* Iconos como webfont, Bootstrap Icons, Font Awesome, Material Icons font,
  emojis o caracteres Unicode como íconos funcionales.
* Estilo legacy de SQLAlchemy: `Column(...)` en clase, `Query` o sesiones
  síncronas.
* Funciones `def` síncronas en `routes.py`, `service.py` o `repository.py`
  cuando realicen I/O.
* Carpetas globales por capa técnica: `controllers/`, `services/`,
  `repositories/`, `handlers/`, `managers/` fuera de un módulo.
* Exponer entidades SQLAlchemy como respuesta HTTP.
* Retornar `dict` libres en errores.
* Strings mágicos para estados de dominio.
* Usar Supabase en producción o desarrollo.
* Usar extensión `.yml` para archivos YAML; usar siempre `.yaml`.
* Separar frontend y backend en aplicaciones o repositorios independientes.
* Crear microservicios sin una enmienda formal a esta constitución.

## IV. Arquitectura: Vertical Slice

El proyecto sigue una arquitectura de Vertical Slice. Cada feature vive en su
propio módulo bajo `app/modules/<feature>/`.

Cada módulo DEBE contener estos artefactos:

* `routes.py` — capa delgada: parsea entrada, llama al servicio y retorna
  respuesta.
* `schemas.py` — DTOs Pydantic v2 con `frozen=True`.
* `models.py` — entidades SQLAlchemy 2.x async con `Mapped[...]` y
  `mapped_column`.
* `repository.py` — solo acceso a datos.
* `service.py` — lógica de negocio del módulo.
* `templates/` — plantillas Jinja2 del módulo.
* `tests/` — pruebas unitarias, integración o endpoint del módulo.

La lógica de negocio reside en `service.py`. `routes.py` y `repository.py` son
capas de entrada e infraestructura sin reglas de negocio. La lógica compartida
solo se extrae cuando exista duplicación real demostrable, nunca por anticipación.

## V. Spec-Driven Development

No se implementa NADA que no esté descrito en un `spec.md` aprobado.

Las specs deben crearse exclusivamente mediante los comandos de Spec Kit. No se
deben crear, mover o duplicar specs manualmente fuera de la ruta que resuelvan
esos comandos.

Cada `spec.md` aprobado es la fuente de verdad funcional de su feature, siempre
que no contradiga esta constitución.

La ruta de specs no es una decisión de arquitectura de aplicación. Si una versión
futura de Spec Kit cambia la ruta generada por sus comandos, deben actualizarse
solo los documentos derivados o el puntero operativo correspondiente, sin
modificar la arquitectura del proyecto.

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

* `specify` crea o actualiza `spec.md`.
* `clarify` resuelve ambigüedades antes del plan.
* `plan` crea `plan.md` con decisiones técnicas y dependencias.
* `analyze` valida consistencia entre spec, plan y restricciones.
* `tasks` crea `tasks.md` con tareas pequeñas, ordenadas y verificables.
* `implement` modifica código real solo después de existir spec, plan y tasks.

Los comandos `speckit.specify` y `speckit.clarify` deben operar en modo
interactivo cuando existan decisiones abiertas. El comando `speckit.plan` puede
operar en modo interactivo solo cuando detecte decisiones estructurales no
resueltas que afecten la implementación o specs futuras.

## VII. Modo interactivo de preguntas

Cuando un comando o prompt opere en modo interactivo, DEBE hacer una sola
pregunta a la vez y esperar respuesta antes de continuar. Está prohibido lanzar
una lista completa de preguntas cuando la decisión requiera interacción guiada.

### 1. Cuándo usar modo interactivo

El modo interactivo debe usarse cuando existan:

- Ambigüedades funcionales en una spec.
- Decisiones técnicas que afecten el plan o la implementación.
- Criterios de aceptación incompletos.
- Gaps que puedan generar retrabajo durante `plan`, `tasks` o `implement`.
- Decisiones con más de una opción razonable y efectos distintos en código,
  pruebas, infraestructura o experiencia de usuario.

### 2. Formato de pregunta con opciones

Cada pregunta con opciones debe usar exactamente este formato:

```text
Pregunta [N de TOTAL] — [tema corto]
─────────────────────────────────────
[Enunciado claro de la pregunta]

Por qué importa: [1 línea explicando el impacto de decidir mal]

A) [opción concreta con valor específico]
B) [opción concreta con valor específico] ← Recomendado
C) [opción concreta con valor específico]
D) Otro — escribe tu respuesta

> Responde con la letra (A, B, C o D) o escribe tu respuesta libre.
```

Reglas de las opciones:

- Cada opción debe ser concreta, verificable y accionable.
- Las opciones deben ser mutuamente excluyentes.
- Cada opción debe llevar a un resultado distinto en spec, plan, tareas,
  implementación, pruebas o configuración.
- La opción marcada con `← Recomendado` debe ser la más alineada con FastAPI,
  PostgreSQL local, SQLAlchemy async, Docker o Docker Compose, `uv`,
  Python 3.13.13 y esta constitución.
- La opción `D) Otro` siempre debe estar presente cuando existan alternativas
  personalizadas razonables.

Ejemplo correcto:

```text
A) Colapsar sidebar por debajo de 768px.
B) Colapsar sidebar por debajo de 1024px. ← Recomendado
C) Colapsar sidebar por debajo de 1280px.
D) Otro — escribe tu respuesta
```

Ejemplo prohibido:

```text
A) Usar un breakpoint pequeño.
B) Usar un breakpoint estándar.
C) Usar un breakpoint grande.
```

### 3. Formato de pregunta Sí/No

Cuando la decisión sea binaria, debe usarse este formato:

```text
Pregunta [N de TOTAL] — [tema corto]
─────────────────────────────────────
[Enunciado de la pregunta]

Por qué importa: [1 línea]

S) Sí ← Recomendado
N) No

> Responde S o N.
```

La opción recomendada puede ser `S` o `N`, según la opción más consistente con
esta constitución y con la spec vigente.

### 4. Reglas de respuesta

Si el usuario responde con una letra (`A`, `B`, `C`, `S` o `N`), el agente debe:

1. Confirmar la elección en una línea con el valor concreto elegido.
2. Registrar la decisión para el resumen final.
3. Pasar inmediatamente a la siguiente pregunta.

Si el usuario responde `D` o escribe texto libre, el agente debe:

1. Aceptar la respuesta.
2. Confirmarla en una línea.
3. Registrar la decisión para el resumen final.
4. Pasar a la siguiente pregunta.

El agente no debe debatir la elección salvo que contradiga la constitución. Si
la respuesta contradice la constitución, debe pausar, explicar el conflicto y
pedir una alternativa válida.

### 5. Cierre del modo interactivo

Después de la última pregunta, el agente debe mostrar un resumen de decisiones
tomadas.

Según el comando en ejecución, debe actualizar el artefacto correspondiente:

- `speckit.specify`: integrar las decisiones en `spec.md`.
- `speckit.clarify`: añadir o actualizar la sección `Clarificaciones` en
  `spec.md`.
- `speckit.plan`: integrar las decisiones en `plan.md`.
- Prompts custom de clarificación: seguir el comportamiento declarado en el
  prompt, siempre que no contradiga esta constitución.

## VIII. Test-Driven Development

El ciclo Red-Green-Refactor es obligatorio:

1. **Red**: escribir primero una prueba que falle por el motivo correcto.
2. **Green**: implementar el código mínimo necesario para que la prueba pase.
3. **Refactor**: mejorar el diseño sin cambiar el comportamiento observable.

Reglas complementarias:

* No se escribe código de producción sin una prueba asociada.
* Toda regla de negocio debe estar cubierta por pruebas.
* Toda corrección de bug comienza con una prueba que reproduzca el fallo.
* Refactorizar solo con la suite de tests en verde.
* No se elimina ni debilita una prueba para hacer pasar la suite.

## IX. Calidad y validación

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

* Las pruebas unitarias usan pytest.
* Las pruebas asíncronas usan pytest-asyncio.
* Las pruebas HTTP usan httpx.AsyncClient.
* Las pruebas de integración que requieran PostgreSQL usan Testcontainers.
* La base de datos de pruebas debe estar aislada.
* Las pruebas deben ser deterministas y enfocadas en comportamiento observable.

### Organización de tests

La estructura de directorios de tests es obligatoria y no negociable:

```text
tests/
├── conftest.py          # Fixtures compartidas (cliente HTTP, etc.)
├── unit/                # Pruebas unitarias puras
│   └── <feature>/       # Sin dependencias externas de ningún tipo
└── integration/         # Pruebas de integración con infraestructura real
    └── <feature>/       # PostgreSQL vía Testcontainers
```

Reglas obligatorias:

* Los tests unitarios viven en `tests/unit/<feature>/`. Está PROHIBIDO que
  dependan de base de datos, red, sistema de archivos o cualquier
  infraestructura externa.
* Los tests de integración viven en `tests/integration/<feature>/`. DEBEN
  usar Testcontainers para PostgreSQL. Está PROHIBIDO conectarse a la base
  de datos de desarrollo.
* El directorio `tests/unit/` y `tests/integration/` son obligatorios en la
  raíz del repositorio. No se aceptan tests dentro de `app/modules/`.
* Las fixtures de infraestructura (conexión a BD, contenedores) solo pueden
  definirse en `tests/integration/conftest.py`. Está PROHIBIDO definirlas en
  `tests/conftest.py` raíz.
* El contenedor PostgreSQL de Testcontainers debe ser `postgres:16-alpine`,
  coherente con la imagen de desarrollo.

## X. Base de datos

* PostgreSQL se ejecuta localmente con Docker o Docker Compose.
* La base de datos de producción no usará Supabase.
* Las migraciones se gestionan exclusivamente con Alembic.
* Las sesiones de base de datos se manejan mediante dependencias controladas con
  inyección de `AsyncSession`.
* `.env` nunca debe versionarse con secretos reales.
* `.env.example` debe existir como plantilla de configuración.
* La infraestructura local debe usar archivos `.yaml`, nunca `.yml`.

## XI. Async-First

Todo I/O del sistema debe ser asíncrono cuando forme parte del flujo web,
persistencia o integración externa.

Esto incluye:

* Base de datos.
* HTTP saliente.
* Colas.
* Storage remoto.
* Servicios externos.
* Operaciones de infraestructura.

Solo se permite `def` síncrono para puro cómputo en memoria, mapeos, cálculos o
validaciones sin I/O.

## XII. Frontend y sistema visual

La interfaz será server-rendered con Jinja2 y mejorada progresivamente con HTMX.
No se debe convertir la aplicación en una SPA.

Reglas obligatorias:

* HTMX vive vendoreado en `app/static/vendor/htmx.min.js`.
* El CSS propio vive en `app/static/css/app.css`.
* Los iconos SVG outline viven en `app/static/icons/`.
* La librería estándar de iconografía es Lucide.
* Las plantillas compartidas viven en `app/templates/`.
* Las plantillas específicas viven dentro del módulo correspondiente.
* Los componentes compartidos viven en `app/templates/components/`.
* Las macros compartidas viven en `app/templates/macros/`.

### Blindaje de tokens visuales canónicos

Los tokens visuales canónicos definidos en
`.opencode/instructions/frontend.instructions.md` y en `app/static/css/app.css`
están protegidos contra modificaciones no autorizadas.

* Cualquier cambio en tokens visuales canónicos (colores, sombras, radios,
  espaciados, tipografía, breakpoints, layout base, componentes compartidos,
  macros de iconos o patrones visuales de estados) requiere autorización
  explícita, justificación y trazabilidad en `tasks.md` con el marcador
  `[visual]`.
* Las extensiones (nuevos tokens que no modifican los existentes) se permiten
  con marcador `[visual][extension]`.
* Las correcciones de bugs visuales se permiten con marcador
  `[visual][bugfix]`.
* Toda modificación de un token existente debe registrarse en
  `Complexity Tracking` de `plan.md` con justificación.
* La fuente operativa de los tokens es
  `.opencode/instructions/frontend.instructions.md`.
* La spec `002-blindar-tokens-visuales` define el proceso completo de
  gobernanza visual.

### Sistema visual canónico

Para todo trabajo frontend, la definición canónica de tokens visuales vive en
`.opencode/instructions/frontend.instructions.md`.

La implementación en `app/static/css/app.css`, templates Jinja, componentes,
macros e iconografía DEBE respetar exactamente esos tokens visuales.

No se aceptan cambios implícitos de color, sombra, radio, espaciado, tipografía,
breakpoints, layout base o patrones visuales compartidos por criterio estético
durante la implementación.

Toda variación de tokens visuales canónicos requiere:

- Spec aprobada.
- Autorización explícita.
- Actualización de las instrucciones frontend, si corresponde.
- Trazabilidad en `tasks.md`.
- Registro en `Complexity Tracking` cuando implique una desviación visual global.

El incumplimiento de esta regla invalida la implementación de la spec en revisión.

## XIII. Estructura obligatoria del repositorio

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
tests/
  conftest.py
  unit/
    <feature>/
      test_*.py
  integration/
    conftest.py
    <feature>/
      test_*.py
pyproject.toml
uv.lock
docker-compose.yaml
.env.example
```

Cualquier desviación debe justificarse en `plan.md`.

## XIV. Contratos de dominio

* Las entidades SQLAlchemy no se exponen como respuesta HTTP.
* Las respuestas HTTP se mapean a DTOs Pydantic.
* Todos los DTOs Pydantic deben usar `model_config = ConfigDict(frozen=True)`.
* Los estados de dominio se modelan con `Enum` o tipos explícitos.
* Los errores usan `HTTPException` o modelos de error tipados.
* Los límites del sistema validan entradas antes de ejecutar lógica de negocio.

## XV. Complexity Tracking

Toda desviación del stack, arquitectura, estructura, flujo obligatorio o reglas
de esta constitución debe registrarse explícitamente en la sección
`Complexity Tracking` de `plan.md`.

Debe incluir:

* Qué regla se desvía.
* Por qué la desviación es necesaria.
* Alternativas consideradas.
* Riesgos introducidos.
* Cómo se mitigarán esos riesgos.
* Cómo se validará que la desviación no rompe el sistema.

En ausencia de justificación, la desviación debe rechazarse.

## XVI. Jerarquía de autoridad

Durante la implementación de una spec, aplica el siguiente orden de prioridad
ante cualquier conflicto:

```text
constitución > spec > AGENTS.md > instructions > comando
```

Si hay conflicto entre capas, se debe pausar, advertir el conflicto
explícitamente y seguir la capa de mayor autoridad.

## XVII. Gobernanza

* Esta constitución es la fuente de verdad suprema del proyecto. Ninguna
  decisión, spec o implementación puede contradecirla.
* Toda modificación a esta constitución requiere una enmienda documentada con
  justificación, impacto evaluado y plan de migración si aplica.
* Las enmiendas se versionan siguiendo el esquema semántico
  `MAJOR.MINOR.PATCH`.
* **MAJOR**: cambios incompatibles en stack, arquitectura, flujo obligatorio o
  principios.
* **MINOR**: nuevas secciones, nuevos principios o ampliaciones materiales.
* **PATCH**: correcciones de redacción, aclaraciones o cambios no semánticos.
* El cumplimiento de esta constitución se verifica en cada code review y en cada
  etapa del flujo Spec-Driven.
* La complejidad introducida debe justificarse explícitamente. Ante la duda,
  elegir la opción más simple.

## XVIII. Historial de versiones

* **v1.0.0** — Versión inicial de la constitución del proyecto Realtor.
* **v1.1.0** — Agregado el protocolo de modo interactivo de preguntas para
  `speckit.specify`, `speckit.clarify`, `speckit.plan` y prompts custom de
  clarificación.
* **v1.2.0** — Agregada la regla de blindaje de tokens visuales canónicos en
  la sección XII, exigiendo autorización explícita, justificación y trazabilidad
  en `tasks.md` con marcador `[visual]`.
* **v1.3.0** — Agregada la subsección «Organización de tests» en la sección IX
  con estructura obligatoria `tests/unit/` y `tests/integration/`, prohibición
  de dependencias externas en tests unitarios, obligatoriedad de Testcontainers
  en tests de integración, y prohibición de tests dentro de `app/modules/`.
  Actualizada la estructura del repositorio en la sección XIII para reflejar
  la nueva ubicación de tests. Corregido el nivel jerárquico de la
  subsección «Sistema visual canónico».

**Versión**: 1.3.0 | **Ratificada**: 2026-06-08 | **Última enmienda**: 2026-06-14
