# Plan de implementación: Crear propiedad

**Feature**: 007-crear-propiedad
**Spec**: [spec.md](./spec.md)
**Clarificaciones**: sección `## Clarificaciones` en spec.md (8 decisiones integradas)
**Created**: 2026-06-20

## Constitution Check

Verificación de reglas constitucionales obligatorias antes de implementar.

| Regla | Estado | Evidencia |
|-------|--------|-----------|
| Vertical slice (IV) | ✅ | Extiende `app/modules/propiedades/`; no crea módulo nuevo |
| Stack obligatorio (II) | ✅ | FastAPI + Jinja2 + SQLAlchemy async + Pydantic v2 |
| Async-first (XI) | ✅ | `routes.py`, `service.py`, `repository.py` async; formato y firma de cookie síncronos |
| Prohibiciones (III) | ✅ | Sin frameworks CSS, sin CDN, sin `pip`, sin legacy SQLAlchemy. Flash con cookie HMAC firmada usando solo stdlib (`hmac`, `hashlib`, `base64`, `json`); sin `itsdangerous` ni `SessionMiddleware` |
| Spec-driven (V) | ✅ | `spec.md` aprobado, `clarify` completado (8/8) |
| TDD (VIII) | ✅ | Fases 7-8 escriben tests antes de código de producción |
| Separación de capas (IV) | ✅ | `routes.py` delgado, `service.py` lógica, `repository.py` datos |
| Gobernanza visual (XII) | ✅ | VTG-001 a VTG-007 declarados; extensiones con `[visual][extension]`; sin modificar tokens canónicos |
| Contratos de dominio (XIV) | ✅ | DTOs Pydantic v2 con `frozen=True`; errores vía mensajes flash estructurados |
| Frontend y sistema visual (XII) | ✅ | HTMX vendoreado; CSS propio con tokens; iconografía Lucide; templates en vertical slice |

## Decisiones técnicas clave

### Decisión 1 — DTO de entrada de formulario (`PropiedadFormIn`)

Se crea un DTO `PropiedadFormIn` en `app/modules/propiedades/schemas.py` con solo
los campos que el usuario completa en el formulario: `titulo`, `direccion`,
`precio_mensual`, `habitaciones`, `banos`, `area` (opcional con default 0).

Razones:

- `PropiedadIn` exige `estado` e `imagen` que el formulario NO solicita; el
  servicio los rellena con defaults (ver Decisión 3).
- `PropiedadFormIn` valida formato y rango con Pydantic v2 (consistente con la
  constitución XIV): `precio_mensual > 0`, `1 <= habitaciones <= 20`,
  `1 <= banos <= 10`, stripping de whitespace en strings.
- `area` es opcional con default 0 según clarificación 1.
- `PropiedadIn.area` se modifica de `Field(gt=0)` a `Field(ge=0, default=0)`
  para que el servicio pueda construir el DTO canónico con `area=0` cuando el
  formulario no la proporciona (ver Complexity Tracking).

### Decisión 2 — Parseo de formulario en `routes.py`

`POST /propiedades` recibe cada campo como parámetro `Form(...)` de FastAPI
(`python-multipart` ya está en `pyproject.toml`). `routes.py` construye
`PropiedadFormIn` manualmente dentro de un `try/except ValidationError`. Los
errores de validación se traducen a un dict `errores: dict[str, str]` que el
template renderiza inline junto a cada campo.

Razones:

- FastAPI no soporta binding directo de un BaseModel a `Form(...)` sin
  workaround; los parámetros `Form(...)` por campo son el patrón idiomático.
- Mantener `PropiedadFormIn` como contrato de validación centralizado (no
  disperso en annotations de FastAPI).
- `routes.py` permanece delgado: parsea, valida, llama al servicio, retorna
  respuesta.

### Decisión 3 — Función de servicio `crear_propiedad_desde_formulario()`

Se agrega una nueva función `async def crear_propiedad_desde_formulario(session,
form: PropiedadFormIn) -> PropiedadOut | None` en
`app/modules/propiedades/service.py`. No se modifica la función existente
`crear_propiedad()` (preservada para los tests de integración existentes en
`tests/integration/propiedades/test_service.py`).

Flujo:

1. Genera URL de imagen vía helper síncrono `_generar_url_imagen()`.
2. Aplica defaults que el formulario no solicita:
   - `ciudad = "Miami"` (clarificación 2).
   - `estado = EstadoPropiedad.DISPONIBLE` (clarificación; FR-006).
   - `area = form.area` (default 0, clarificación 1).
   - `imagen = _generar_url_imagen()`.
3. Construye `PropiedadIn` con los defaults aplicados.
4. Llama al `crear_propiedad()` existente (`repo_crear` → flush).
5. Captura `IntegrityError` por duplicado
   (`uq_propiedades_identidad_negocio`), llama `await session.rollback()` y
   retorna `None` (clarificación 7).
6. En éxito retorna `PropiedadOut`.

### Decisión 4 — Generación de imagen con fallback

Función `def _generar_url_imagen(ancho: int = 800, alto: int = 600) -> str`
(retorna string, síncrona porque es puro formato). Construye
`f"https://picsum.photos/{ancho}/{alto}"`. En caso de error de formato retorna
`""` para activar el placeholder visual del listado (FR-009, clarificación 4).

Nota: el "fallback" es defensivo. La URL se construye siempre correctamente
(formato determinista). La falla real del servicio `picsum.photos` ocurre
client-side al cargar la imagen; el componente `_card_propiedad.html` ya
maneja este caso con `onerror` que activa el placeholder (spec 006).

### Decisión 5 — Mecanismo de flash post-creación (sin middleware)

POST tradicional con redirect 303 a `/propiedades` (FR-011, clarificación 3 y 8).
Para pasar el mensaje flash entre el POST y el GET siguiente se usa una
**cookie firmada con HMAC-SHA256** usando solo stdlib de Python (`hmac`,
`hashlib`, `base64`, `json`). No se agrega `SessionMiddleware` ni la dependencia
`itsdangerous` (no está disponible en el entorno y la constitución prohíbe
nuevas dependencias explícitas; ver Complexity Tracking).

**Patrón canónico de flash** (referencia para futuras features): ver
`frontend.instructions.md` §7 y §10, que define flash con HTMX OOB swap
(`hx-swap-oob="true"`) al `<div id="flash-zone">` de `base.html`. Esta feature
se desvía de ese patrón porque usa POST tradicional con redirect 303 (no
HTMX). Si una futura feature usa HTMX para el submit del formulario, debe
volver al patrón canónico.

Implementación en `app/modules/propiedades/routes.py`:

- Helper `_firmar_flash(payload: dict, secret: str) -> str`: serializa el dict
  con `json`, lo codifica en `base64.urlsafe_b64encode`, calcula HMAC-SHA256
  con el secret, retorna `f"{payload_b64}.{hex_digest}"`.
- Helper `_verificar_flash(cookie: str, secret: str) -> dict | None`: split por
  último `.`, recalcula HMAC, compara con `hmac.compare_digest` (timing-safe),
  decodifica y retorna dict o `None` si la firma no coincide.
- `POST /propiedades` (éxito): setea `Set-Cookie: flash=<firmado>` con
  `httponly=True`, `samesite='lax'`, `max_age=60`, retorna `RedirectResponse`
  con `status_code=303` y `Location: /propiedades`.
- `POST /propiedades` (validación o duplicado): re-renderiza `crear_propiedad.html`
  con los valores previos y los errores; no setea flash.
- `GET /propiedades`: lee `request.cookies.get('flash')`, verifica firma, pasa
  `flash` al contexto si es válido, llama `response.delete_cookie('flash')`
  para que solo se muestre una vez.

Secret: `settings.session_secret` (nuevo campo en `Settings`; ver
Complexity Tracking).

### Decisión 6 — Ubicación del flash en `propiedades.html`

El flash se renderiza dentro de `{% block content %}` al inicio de
`app/modules/propiedades/templates/propiedades.html`, no en el
`<div id="flash-zone">` de `base.html`. Justificación: VTG-005 prohíbe
modificar `base.html`. La desviación se documenta en Complexity Tracking.

### Decisión 7 — Icono "plus" para el botón

Se vendorea `app/static/icons/plus.svg` desde Lucide (ISC). Contenido
canónico:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-plus" aria-hidden="true"><path d="M5 12h14"></path><path d="M12 5v14"></path></svg>
```

Marca `[visual][extension]` por ser un nuevo vendoring (no modifica los 15
iconos existentes).

### Decisión 8 — Estilo del botón "Nueva propiedad"

Botón secundario en `_navbar.html` con:

- Icono `plus` (size 18) + texto "Nueva propiedad".
- `href="/propiedades/nueva"`.
- `class="navbar__accion navbar__accion--primary"` (nueva clase, extensión
  permitida con `[visual][extension]`).
- Visibilidad coherente con tokens existentes; no se modifica el navbar base.

## Estructura del proyecto

### Archivos a modificar

| Archivo | Cambio |
|---------|--------|
| `app/modules/propiedades/routes.py` | Agregar `GET /propiedades/nueva` y `POST /propiedades`. Helpers `_firmar_flash`, `_verificar_flash`, `_leer_y_limpiar_flash`. Modificar `GET /propiedades` para inyectar flash en el contexto. |
| `app/modules/propiedades/service.py` | Agregar `crear_propiedad_desde_formulario(session, form)`, helper `_generar_url_imagen()`. Capturar `IntegrityError`. |
| `app/modules/propiedades/schemas.py` | Agregar `PropiedadFormIn`. Modificar `PropiedadIn.area` a `Field(ge=0, default=0)`. |
| `app/modules/propiedades/templates/propiedades.html` | Renderizar flash dentro de `{% block content %}` antes del header. |
| `app/templates/components/_navbar.html` | Agregar botón "Nueva propiedad" con icono `plus` antes de `.navbar__user`. |
| `app/static/css/app.css` | Clases `.formulario-crear`, `.formulario-crear__grupo`, `.formulario-crear__acciones`, `.formulario-crear__submit`, `.formulario-crear__cancelar`, `.navbar__accion`, `.navbar__accion--primary`. |
| `app/config/settings.py` | Agregar campo `session_secret: str` con `validation_alias=AliasChoices('session_secret', 'SESSION_SECRET')`. |
| `config/app.example.yaml` | Agregar `session_secret: <placeholder-32-bytes-base64>` como plantilla. |

### Archivos a crear

| Archivo | Propósito |
|---------|-----------|
| `app/static/icons/plus.svg` | Icono `plus` de Lucide vendoreado (24×24, trazo 2px). |
| `app/modules/propiedades/templates/crear_propiedad.html` | Template del formulario. Extiende `base.html`. |
| `tests/unit/propiedades/test_schemas_form.py` | Tests de `PropiedadFormIn` (validación, stripping, rangos). |
| `tests/unit/propiedades/test_service_crear_formulario.py` | Tests de `crear_propiedad_desde_formulario()` con mocks. |
| `tests/integration/propiedades/test_routes_crear.py` | Tests de los endpoints GET/POST con Testcontainers + TestClient. |

### Archivos no modificados

- `app/main.py` — router ya registrado; flash no requiere middleware (cookie
  firmada con HMAC stdlib).
- `app/templates/base.html` — VTG-005 prohíbe modificarlo; flash se renderiza
  dentro de `{% block content %}` (ver Complexity Tracking).
- `app/templates/components/_sidebar.html` — VTG-005.
- `app/modules/propiedades/models.py` — modelo completo y suficiente.
- `app/modules/propiedades/repository.py` — `crear()` existente es suficiente.
- `app/static/icons/` (los 15 existentes) — sin cambios.
- `app/static/vendor/htmx.min.js` — sin cambios.
- `app/static/css/app.css` (secciones existentes) — solo se agregan clases
  nuevas, no se modifican tokens.

## Fases de implementación

### Fase 0: Lectura de contexto

- T0.1: Leer `spec.md`, `plan.md`, sección `## Clarificaciones` y checklist
  `checklists/requirements.md` para entender alcance completo.
- T0.2: Leer instrucciones vigentes: `backend.instructions.md`,
  `frontend.instructions.md`, `database.instructions.md`,
  `tests.instructions.md`, `conventions.instructions.md`.

### Fase 1: DTOs y validación [TDD Red-Green-Refactor]

- T1.1 [RED]: Escribir `tests/unit/propiedades/test_schemas_form.py` con casos:
  - `PropiedadFormIn` acepta datos válidos completos.
  - `titulo` vacío después de strip falla con error en `titulo`.
  - `direccion` con solo espacios falla.
  - `titulo` con 256 caracteres falla con error en `titulo` (`max_length=255`).
  - `direccion` con 256 caracteres falla con error en `direccion`
    (`max_length=255`).
  - `precio_mensual <= 0` falla.
  - `precio_mensual` igual a `"1500"` (sin decimales) es aceptado (sin
    `decimal_places`).
  - `habitaciones > 20` falla.
  - `banos > 10` falla.
  - `area` es opcional y default 0.
  - `area` negativa falla (`ge=0`).
  - `PropiedadFormIn` es `frozen=True`.
- T1.2 [GREEN]: Crear `PropiedadFormIn` en `app/modules/propiedades/schemas.py`
  con `model_config = ConfigDict(frozen=True, extra='forbid')`, validadores
  `mode='before'` para `titulo` y `direccion` que aplican `.strip()`,
  `Field(min_length=1, max_length=255)` para `titulo` y `direccion`
  (post-strip; alineado con `String(255)` del modelo), `Field(gt=0)` para
  `precio_mensual` (la restricción de 2 decimales aplica solo al formato de
  salida, no a la entrada del form), `Field(ge=1, le=20)` para `habitaciones`,
  `Field(ge=1, le=10)` para `banos`, `int = 0` para `area` con
  `Field(ge=0, default=0)`.
- T1.3 [REFACTOR]: Validar que los tests pasan con `uv run pytest tests/unit/propiedades/test_schemas_form.py -q`.
- T1.4 [RED]: Agregar a `tests/unit/propiedades/test_schemas.py` (clase
  `TestPropiedadIn`) dos tests nuevos: `test_area_acepta_cero` y
  `test_area_default_cero`. El primero verifica que
  `PropiedadIn(..., area=0)` es válido. El segundo verifica que
  `PropiedadIn(titulo='X', direccion='Y', precio_mensual=1, habitaciones=1,
  banos=1, estado='disponible', imagen='https://x')` sin `area` usa el
  default 0.
- T1.5 [GREEN]: Modificar `PropiedadIn.area` de `Field(gt=0)` a
  `Field(ge=0, default=0)`.

### Fase 2: Servicio - generación de imagen y creación desde formulario [TDD]

- T2.1 [RED]: Escribir `tests/unit/propiedades/test_service_crear_formulario.py`:
  - `_generar_url_imagen()` retorna URL con formato `https://picsum.photos/800/600`.
  - `_generar_url_imagen()` retorna `""` cuando se mockea excepción.
  - `crear_propiedad_desde_formulario()` aplica defaults:
    `ciudad='Miami'`, `estado='disponible'`, `imagen` no vacía.
  - `crear_propiedad_desde_formulario()` con `form.area=0` propaga `area=0` a
    `PropiedadIn`.
  - `crear_propiedad_desde_formulario()` retorna `None` cuando el repo lanza
    `IntegrityError` y hace rollback.
  - `crear_propiedad_desde_formulario()` retorna `PropiedadOut` con id y
    estado en éxito.
- T2.2 [GREEN]: Implementar `_generar_url_imagen()` (síncrono, retorna string).
- T2.3 [GREEN]: Implementar `crear_propiedad_desde_formulario()`:
  - Recibe `session: AsyncSession` y `form: PropiedadFormIn`.
  - Llama `_generar_url_imagen()`.
  - Construye `PropiedadIn` con defaults `ciudad='Miami'`, `estado=DISPONIBLE`.
  - `try` envolviendo `crear_propiedad()` existente.
  - `except IntegrityError`: `await session.rollback()`, log warning, return
    `None`.
  - En éxito: log info, return `PropiedadOut.model_validate(entidad)`.
- T2.4 [REFACTOR]: Validar `uv run pytest tests/unit/propiedades/test_service_crear_formulario.py -q` verde.

### Fase 3: Configuración - `session_secret` en Settings

- T3.1: Agregar a `app/config/settings.py`:
  ```python
  session_secret: str = Field(
      validation_alias=AliasChoices('session_secret', 'SESSION_SECRET'),
  )
  ```
- T3.2: Agregar a `config/app.example.yaml`:
  ```yaml
  session_secret: <placeholder-de-32-bytes-base64>
  ```
  Con comentario `# Generar valor único con: python -c "import secrets; print(secrets.token_urlsafe(32))"`.
- T3.3: Validar con `uv run python -c "from app.config import get_settings; print(bool(get_settings().session_secret))"` (requiere `config/app.yaml` real; documentar en commit que este paso se valida en entorno local).

### Fase 4: Icono vendoreado

- T4.1 [visual][extension]: Crear `app/static/icons/plus.svg` con el contenido
  XML del icono `plus` de Lucide (especificado en Decisión 7). 24×24, trazo
  2px, `stroke="currentColor"`, clase `lucide lucide-plus`.

### Fase 5: Templates

- T5.1 [visual][extension]: Crear `app/modules/propiedades/templates/crear_propiedad.html`:
  - Extiende `base.html`.
  - Importa macro `icon` desde `macros/icons.html`.
  - Bloque `content` con:
    - Header `<h1 class="formulario-crear__titulo">Nueva propiedad</h1>`.
    - Si `errores.__all__`: bloque de error global con icono `alert-circle` y
      clase `alerta alerta--danger` (estilo de `_alerta.html`).
    - `<form method="post" action="/propiedades" class="formulario-crear">`.
    - Campos con `{% include "components/_form_field.html" %}`:
      - `titulo` (text, required)
      - `direccion` (text, required)
      - `precio_mensual` (number, step="0.01", required)
      - `habitaciones` (number, min=1, max=20, required)
      - `banos` (number, min=1, max=10, required)
      - `area` (number, min=0, helper="Opcional. Si se omite, se usará 0 m².")
    - Grupo `.formulario-crear__acciones`:
      - `<button type="submit" class="formulario-crear__submit">Crear propiedad</button>`
      - `<a href="/propiedades" class="formulario-crear__cancelar">Cancelar</a>`
- T5.2 [visual][extension]: Modificar `app/modules/propiedades/templates/propiedades.html`
  para renderizar el flash al inicio del bloque `content`:
  ```jinja
  {% if flash %}
    {% with tipo=flash.tipo, mensaje=flash.mensaje %}
      {% include "components/_alerta.html" %}
    {% endwith %}
  {% endif %}
  ```
  Con comentario que documenta la desviación: "Renderizado dentro de block
  content porque VTG-005 prohíbe modificar base.html".
- T5.3 [visual][extension]: Modificar `app/templates/components/_navbar.html`:
  - En `.navbar__actions`, antes de `.navbar__user`, agregar:
    ```jinja
    <a href="/propiedades/nueva" class="navbar__accion navbar__accion--primary">
      {{ icon("plus", size=18) }}
      <span>Nueva propiedad</span>
    </a>
    ```

### Fase 6: CSS [visual][extension]

- T6.1: Agregar al final de la sección `5. Componentes` de `app/static/css/app.css`:
  ```css
  /* --- Formulario de creación de propiedad --- */
  .formulario-crear { ... }
  .formulario-crear__titulo { ... }
  .formulario-crear__grupo { ... }
  .formulario-crear__acciones { ... }
  .formulario-crear__submit { ... }
  .formulario-crear__cancelar { ... }

  /* --- Botón de acción en navbar --- */
  .navbar__accion { ... }
  .navbar__accion--primary { ... }
  ```
  Todas las clases usan tokens canónicos (`--color-accent`, `--space-*`,
  `--radius-md`, `--font-*`). Sin modificar tokens existentes.

### Fase 7: Routes - endpoints GET/POST y helpers de flash [TDD]

- T7.1 [RED]: Escribir `tests/integration/propiedades/test_routes_crear.py`:
  - `GET /propiedades/nueva` retorna 200 con HTML que contiene:
    - `class="formulario-crear"`
    - Campos `name="titulo"`, `name="direccion"`, `name="precio_mensual"`,
      `name="habitaciones"`, `name="banos"`, `name="area"`.
    - Botón submit con texto "Crear propiedad".
  - `POST /propiedades` con datos válidos (form-encoded):
    - Retorna 303 con `Location: /propiedades`.
    - Setea cookie `flash` firmada.
  - `GET /propiedades` con cookie `flash` válida renderiza la alerta dentro
    del bloque content y elimina la cookie en la respuesta.
  - `POST /propiedades` con `titulo=""` retorna 200 re-renderizando el
    formulario con error inline en `titulo` y conserva el valor previo en
    `direccion`.
  - `POST /propiedades` con `precio_mensual="abc"` retorna 200 con error
    inline en `precio_mensual`.
  - `POST /propiedades` con `habitaciones="25"` retorna 200 con error inline
    en `habitaciones`.
  - `POST /propiedades` con `area=""` (string vacío del form) retorna 200
    con `area=0` aplicado y propiedad persistida (sin 422 de FastAPI).
  - `POST /propiedades` con `area="-5"` retorna 200 con error inline en
    `area` (`ge=0`).
  - `POST /propiedades` con `titulo` de 256 caracteres retorna 200 con
    error inline en `titulo` (`max_length=255`).
  - `POST /propiedades` con datos válidos duplicados (segunda inserción del
    mismo titulo+direccion+ciudad) retorna 200 con error global
    `__all__` "Ya existe una propiedad con ese título y dirección en Miami".
  - `GET /` contiene `<a href="/propiedades/nueva"` en el navbar.
  - Cookie `flash` con firma inválida se ignora silenciosamente (no rompe el
    render de `/propiedades`).
- T7.2 [GREEN]: Agregar endpoints en `app/modules/propiedades/routes.py`:
  - `GET /propiedades/nueva`: renderiza `crear_propiedad.html` con contexto
    `{'request': request, 'form': {}, 'errores': {}}`.
  - `POST /propiedades`: recibe Form() params. Los campos numéricos
    (`precio_mensual`, `habitaciones`, `banos`) y el opcional `area` se
    reciben como `str` con default `""` (no como `int`/`Decimal`) para
    tolerar campos vacíos o malformados sin generar 422 de FastAPI antes de
    la validación Pydantic. La ruta aplica reglas de conversión distintas:
    - Campos requeridos (`precio_mensual`, `habitaciones`, `banos`): si la
      conversión con `Decimal()` / `int()` falla, mantiene el string vacío
      para que Pydantic genere el error específico del campo.
    - Campo opcional (`area`): si el string está vacío `""`, lo convierte
      a `None` para que Pydantic aplique el default 0 (alineado con FR-020
      y clarificación 1). Si el string es no vacío pero no parseable como
      `int`, mantiene el string vacío para que Pydantic genere el error.
    Intenta construir `PropiedadFormIn`, captura `ValidationError` →
    re-renderiza con `errores` parseados; llama
    `crear_propiedad_desde_formulario()`; si retorna `None` → re-renderiza
    con `errores['__all__']` con el mensaje específico de duplicado; si
    retorna `PropiedadOut` → setea cookie firmada + `RedirectResponse` 303.
  - Modificar `GET /propiedades`: lee cookie `flash`, si válida la agrega
    al contexto como `flash: {tipo, mensaje}`, llama
    `response.delete_cookie('flash')` en la respuesta.
- T7.3 [REFACTOR]: Helpers privados:
  - `_firmar_flash(payload, secret) -> str`
  - `_verificar_flash(cookie, secret) -> dict | None`
  - `_leer_y_limpiar_flash(request, response, secret) -> dict | None` que
    encapsula la lectura + borrado.
  Constantes: `FLASH_COOKIE_NAME = "flash"`, `FLASH_MAX_AGE = 60`.

### Fase 8: Calidad

- T8.1: Ejecutar `uv run ruff check .` y `uv run ruff format --check .`.
  Cero hallazgos.
- T8.2: Ejecutar `uv run mypy --strict app/modules/propiedades/`. Cero
  errores.
- T8.3: Ejecutar `uv run pytest tests/unit/propiedades tests/integration/propiedades -q`.
  Todos verdes.
- T8.4: Ejecutar `uv run pytest --cov=app/modules/propiedades --cov-fail-under=80`.
  Cobertura ≥ 80%.
- T8.5: Ejecutar `make visual-check` (auditoría de trazabilidad visual).

## Contrato de contexto del template `crear_propiedad.html`

```yaml
contexto:
  request:
    type: Request
    source: fastapi
  form:
    type: dict[str, str]
    description: |
      Valores previos del usuario para re-popular campos tras error de
      validación. Vacío en GET inicial. Cada valor es string crudo (no
      procesado); el template lo pasa tal cual al input `value`.
    keys: [titulo, direccion, precio_mensual, habitaciones, banos, area]
    default: {}
  errores:
    type: dict[str, str]
    description: |
      Mensajes de error por campo. Si un campo no tiene error, su clave
      está ausente. La clave especial '__all__' contiene errores globales
      (ej. duplicado por constraint único).
    keys: [titulo, direccion, precio_mensual, habitaciones, banos, area, __all__]
    default: {}
```

## Contrato de contexto del template `propiedades.html` (modificado)

Extiende el contrato existente con un campo opcional:

```yaml
contexto:
  request:
    type: Request
  propiedades:
    type: list[dict]
    required: true
  vacio:
    type: bool
    required: true
  flash:
    type: dict | None
    description: |
      Opcional. Si está presente, contiene {tipo: str, mensaje: str} para
      renderizar `_alerta.html` dentro del bloque content (no en #flash-zone
      por VTG-005).
    default: None
```

## Gobernanza visual

| Marcador | Archivo | Justificación |
|----------|---------|---------------|
| `[visual][extension]` | `app/static/icons/plus.svg` | Nuevo icono Lucide vendoreado; no modifica los 15 existentes |
| `[visual][extension]` | `app/templates/components/_navbar.html` | Botón "Nueva propiedad" con clases nuevas; sin modificar tokens ni estructura |
| `[visual][extension]` | `app/modules/propiedades/templates/crear_propiedad.html` | Template nuevo que extiende base sin modificarlo |
| `[visual][extension]` | `app/modules/propiedades/templates/propiedades.html` | Render de flash al inicio del content block sin modificar tokens |
| `[visual][extension]` | `app/static/css/app.css` | Clases nuevas `.formulario-crear*` y `.navbar__accion*` usando solo tokens existentes |

Sin modificación de tokens visuales canónicos. Sin cambios en `base.html`,
`_sidebar.html` ni en iconografía existente.

## Complexity Tracking

| Regla desviada | Por qué | Alternativas consideradas | Riesgos introducidos | Mitigación | Validación prevista |
|----------------|---------|---------------------------|----------------------|------------|---------------------|
| Modificar `app/config/settings.py` y `config/app.example.yaml` (cross-cutting) | Necesidad de `session_secret` para firmar cookie flash con HMAC | (1) Cookie sin firma (riesgo de tampering de UX); (2) Agregar `itsdangerous` (viola NFR-ARCH-005, no disponible en env); (3) Query param `?flash=success` (visible en URL, no idiomático) | Bajo: el flash solo contiene un mensaje UI sin datos sensibles | HMAC-SHA256 con secret ≥ 32 bytes en `config/app.yaml`; documento de placeholder en `app.example.yaml` con instrucción para generar valor único | Test verifica que cookie con firma inválida se ignora; test verifica que cookie válida se renderiza una sola vez y se elimina |
| Renderizar flash dentro de `{% block content %}` en vez de `#flash-zone` | VTG-005 prohíbe modificar `base.html`; sin bloque `{% block flash %}` no hay forma de inyectar desde templates hijas sin modificar `base.html` | (1) Modificar `base.html` con `[visual][extension]` (prohibido por VTG-005); (2) HTMX OOB swap (no aplica a POST + redirect); (3) Re-render del POST sin redirect (rompe FR-011) | UX: flash aparece dentro del content area (no en zona superior dedicada); comportamiento funcional idéntico | Comentario en `propiedades.html` documenta la desviación; la alerta usa `_alerta.html` con estilos y tokens existentes | Test verifica que el HTML contiene `class="alerta alerta--success"` con el mensaje esperado |
| Modificar `PropiedadIn.area` de `Field(gt=0)` a `Field(ge=0, default=0)` | Clarificación 1 exige default 0 aplicado en service.py, lo que requiere que `PropiedadIn` acepte `area=0` | (1) Bypass `PropiedadIn` y construir `Propiedad` directamente en service (rompe contrato canónico); (2) Default no-cero (mala UX, miente sobre el valor) | Bajo: cambia semántica de "obligatorio > 0" a "opcional >= 0"; los tests existentes en `test_schemas.py` usan `area=850` (siguen pasando) | Changelog y commit message documentan el cambio; `test_schemas_form.py` cubre explícitamente `area=0` y ausencia de area | Tests verifican que `PropiedadIn(area=0)` es válido y que `PropiedadIn` sin `area` usa default 0 |
| Agregar helper de cookie firmada en `routes.py` (no hay abstracción compartida) | YAGNI: solo este módulo usa flash; no anticipar abstracción compartida | (1) Crear `app/core/flash.py` con abstracción genérica (anticipación, no hay duplicación); (2) Usar `SessionMiddleware` de Starlette (requiere `itsdangerous`, no disponible) | Bajo: si futuras features necesitan flash, se duplica código y luego se extrae (patrón recomendado por constitución) | Documentar en el helper que es candidato a extracción tras 2+ consumidores | Tests unitarios e integrales del helper verifican firma, verificación y timing-safe comparison |

## Resumen de cambios

- **5 archivos a crear**: `plus.svg`, `crear_propiedad.html`, 3 archivos de test.
- **8 archivos a modificar**: 4 del vertical slice de propiedades, navbar, CSS, settings, config example.
- **5 archivos explícitamente NO modificados**: `main.py`, `base.html`, `_sidebar.html`, `models.py`, `repository.py`.
- **4 desviaciones documentadas** en Complexity Tracking.
- **5 marcadores `[visual][extension]`** (todos extensions, ningún `[visual]` puro).
- **0 dependencias nuevas** de paquetes Python.
- **0 tokens visuales canónicos modificados**.
