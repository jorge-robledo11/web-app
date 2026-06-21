# Tasks: Crear propiedad

**Feature**: 007-crear-propiedad
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md) | **Report**: [report.md](./report.md)
**Created**: 2026-06-20

## Fase 0: Contexto

- [ ] **T0.1**: Leer `spec.md`, `plan.md`, `report.md` y checklist
  `checklists/requirements.md` para entender alcance completo, decisiones de
  clarificación y contrato de contexto.
- [ ] **T0.2**: Leer instrucciones vigentes: `backend.instructions.md`,
  `frontend.instructions.md`, `database.instructions.md`,
  `tests.instructions.md`, `conventions.instructions.md`.

## Fase 1: DTOs y validación [TDD Red-Green-Refactor]

- [ ] **T1.1** [RED]: Escribir `tests/unit/propiedades/test_schemas_form.py`
  con 12 tests que cubran: datos válidos completos; `titulo=""` falla;
  `direccion="   "` falla; `titulo` 256 chars falla (`max_length=255`);
  `direccion` 256 chars falla; `precio_mensual <= 0` falla; `precio_mensual="1500"`
  (sin decimales) aceptado; `habitaciones > 20` falla; `banos > 10` falla;
  `area` opcional con default 0; `area < 0` falla; `PropiedadFormIn` es
  `frozen=True`. Traza a FR-004, FR-005, FR-014, FR-015, FR-016, FR-020.
- [ ] **T1.2** [GREEN]: Crear `PropiedadFormIn` en
  `app/modules/propiedades/schemas.py` con `ConfigDict(frozen=True,
  extra='forbid')`, validadores `mode='before'` para `titulo` y `direccion`
  que aplican `.strip()`, `Field(min_length=1, max_length=255)` para strings
  (post-strip), `Field(gt=0)` para `precio_mensual` (formato libre), 
  `Field(ge=1, le=20)` para `habitaciones`, `Field(ge=1, le=10)` para
  `banos`, `Field(ge=0, default=0)` para `area`. Traza a FR-004, FR-005,
  FR-014, FR-015, FR-016, FR-020.
- [ ] **T1.3** [REFACTOR]: Validar que `uv run pytest
  tests/unit/propiedades/test_schemas_form.py -q` pasa todos los tests
  verdes.
- [ ] **T1.4** [RED]: Agregar a `tests/unit/propiedades/test_schemas.py` (clase
  `TestPropiedadIn`) los tests `test_area_acepta_cero` y
  `test_area_default_cero` que verifican que `PropiedadIn(area=0)` es válido
  y que `PropiedadIn` sin `area` usa default 0.
- [ ] **T1.5** [GREEN]: Modificar `PropiedadIn.area` de `Field(gt=0)` a
  `Field(ge=0, default=0)`. Validar que los tests existentes en
  `test_schemas.py` (que usan `area=850`) siguen pasando.

## Fase 2: Servicio - generación de imagen y creación desde formulario [TDD]

- [ ] **T2.1** [RED]: Escribir
  `tests/unit/propiedades/test_service_crear_formulario.py` con 6 tests:
  `_generar_url_imagen()` retorna `https://picsum.photos/800/600`; retorna
  `""` cuando se mockea excepción; `crear_propiedad_desde_formulario()`
  aplica defaults `ciudad='Miami'`, `estado='disponible'`, `imagen` no vacía;
  propaga `area=0` a `PropiedadIn` cuando `form.area=0`; retorna `None` y
  hace rollback cuando el repo lanza `IntegrityError`; retorna `PropiedadOut`
  con id y estado en éxito. Traza a FR-006, FR-007, FR-008, FR-009, SC-009.
- [ ] **T2.2** [GREEN]: Implementar `_generar_url_imagen(ancho: int = 800,
  alto: int = 600) -> str` síncrono en `app/modules/propiedades/service.py`.
  Retorna `f"https://picsum.photos/{ancho}/{alto}"` o `""` en excepción.
  Traza a FR-008, FR-009.
- [ ] **T2.3** [GREEN]: Implementar
  `crear_propiedad_desde_formulario(session: AsyncSession, form:
  PropiedadFormIn) -> PropiedadOut | None` async en
  `app/modules/propiedades/service.py`. Llama `_generar_url_imagen()`,
  construye `PropiedadIn` con defaults `ciudad='Miami'`,
  `estado=EstadoPropiedad.DISPONIBLE`, envuelve llamada a `crear_propiedad()`
  existente en `try/except IntegrityError` (con `await session.rollback()`,
  `logger.warning(...)` y `return None`), retorna `PropiedadOut` en éxito.
  Traza a FR-006, FR-007, FR-008, FR-009, FR-017, SC-003, SC-009.
- [ ] **T2.4** [REFACTOR]: Validar `uv run pytest
  tests/unit/propiedades/test_service_crear_formulario.py -q` todos verdes.

## Fase 3: Configuración - `session_secret` en Settings

- [ ] **T3.1**: Agregar a `app/config/settings.py` el campo
  `session_secret: str = Field(validation_alias=AliasChoices('session_secret',
  'SESSION_SECRET'))`.
- [ ] **T3.2**: Agregar a `config/app.example.yaml` la línea
  `session_secret: <placeholder-32-bytes-base64>` con comentario
  `# Generar valor único con: python -c "import secrets; print(secrets.token_urlsafe(32))"`.
- [ ] **T3.3**: Verificar que `config/app.yaml` (gitignored) local contiene
  un valor real para `session_secret`. Documentar en commit message que
  este campo es requerido y debe ser único por entorno. Traza a W5 del
  report.

## Fase 4: Icono vendoreado

- [ ] **T4.1** [visual][extension]: Crear `app/static/icons/plus.svg` con
  el contenido XML del icono `plus` de Lucide (24×24, trazo 2px,
  `stroke="currentColor"`, clase `lucide lucide-plus`). Traza a FR-003,
  VTG-003.

## Fase 5: Templates

- [ ] **T5.1** [visual][extension]: Crear
  `app/modules/propiedades/templates/crear_propiedad.html`:
  - Extiende `base.html`; importa macro `icon` desde `macros/icons.html`.
  - Bloque `content` con `<h1 class="formulario-crear__titulo">Nueva
    propiedad</h1>`.
  - Si `errores.__all__`: bloque con clase `alerta alerta--danger` e icono
    `alert-circle`.
  - `<form method="post" action="/propiedades" class="formulario-crear">`.
  - 6 campos via `{% include "components/_form_field.html" %}`:
    - `titulo` (text, required, value=`form.titulo`, error=`errores.titulo`).
    - `direccion` (text, required, value=`form.direccion`,
      error=`errores.direccion`).
    - `precio_mensual` (number, step="0.01", required, value=`form.precio_mensual`,
      error=`errores.precio_mensual`).
    - `habitaciones` (number, min=1, max=20, required, value=`form.habitaciones`,
      error=`errores.habitaciones`).
    - `banos` (number, min=1, max=10, required, value=`form.banos`,
      error=`errores.banos`).
    - `area` (number, min=0, value=`form.area`, error=`errores.area`,
      helper="Opcional. Si se omite, se usará 0 m².").
  - Grupo `.formulario-crear__acciones` con `<button type="submit"
    class="formulario-crear__submit">Crear propiedad</button>` y `<a
    href="/propiedades" class="formulario-crear__cancelar">Cancelar</a>`.
  - Traza a FR-001, FR-018, FR-019, VTG-002.
- [ ] **T5.2** [visual][extension]: Modificar
  `app/modules/propiedades/templates/propiedades.html` para renderizar
  flash al inicio del bloque `content` (antes del header):
  ```jinja
  {# Flash: renderizado dentro de block content porque VTG-005
     prohíbe modificar base.html. #}
  {% if flash %}
    {% with tipo=flash.tipo, mensaje=flash.mensaje %}
      {% include "components/_alerta.html" %}
    {% endwith %}
  {% endif %}
  ```
  Traza a FR-011, SC-004.
- [ ] **T5.3** [visual][extension]: Modificar
  `app/templates/components/_navbar.html` para agregar en `.navbar__actions`,
  antes de `.navbar__user`, el bloque:
  ```jinja
  <a href="/propiedades/nueva" class="navbar__accion navbar__accion--primary">
    {{ icon("plus", size=18) }}
    <span>Nueva propiedad</span>
  </a>
  ```
  Traza a FR-003, VTG-004.

## Fase 6: CSS [visual][extension]

- [ ] **T6.1**: Agregar al final de la sección 5 (Componentes) de
  `app/static/css/app.css` las clases nuevas:
  - `.formulario-crear` (container con max-width, padding, gap).
  - `.formulario-crear__titulo` (tamaño y peso consistente con header).
  - `.formulario-crear__grupo` (agrupador de campos relacionados).
  - `.formulario-crear__acciones` (flex row con gap, alineación).
  - `.formulario-crear__submit` (botón primario con `--color-accent`,
    `--radius-md`, padding, hover con `--color-accent-hover`).
  - `.formulario-crear__cancelar` (link secundario con color muted).
  - `.navbar__accion` (display inline-flex, gap, padding, border-radius,
    transition, hover).
  - `.navbar__accion--primary` (fondo `--color-accent`, color `#ffffff`,
    hover con `--color-accent-hover`).
  - Todas las clases usan tokens canónicos existentes
    (`--color-*`, `--space-*`, `--radius-md`, `--font-*`).
  - Sin modificar tokens. Traza a VTG-002.

## Fase 7: Routes - endpoints y helpers de flash [TDD]

- [ ] **T7.1** [RED]: Escribir
  `tests/integration/propiedades/test_routes_crear.py` con 15 tests
  siguiendo el patrón de `test_routes.py` existente
  (`_setup(postgres_url)` + `_override_session(async_session)` +
  `app.dependency_overrides.clear()`):
  - `test_get_nueva_retorna_200_con_formulario`: GET `/propiedades/nueva`
    contiene `class="formulario-crear"`, los 6 inputs por name, botón
    submit con texto "Crear propiedad".
  - `test_post_valido_redirige_303_y_setea_flash`: POST form-encoded con
    datos válidos retorna 303 con `Location: /propiedades` y cookie
    `flash` firmada.
  - `test_get_propiedades_con_flash_valido_renderiza_y_limpia_cookie`: GET
    `/propiedades` con cookie `flash` válida renderiza la alerta y elimina
    la cookie en la respuesta.
  - `test_post_titulo_vacio_re_renderiza_con_error_inline`: titulo="",
    otros campos válidos → 200 con error en `titulo`, valor de `direccion`
    conservado.
  - `test_post_direccion_solo_espacios_rechaza`.
  - `test_post_precio_mensual_no_numerico_rechaza`: `precio_mensual="abc"`.
  - `test_post_precio_mensual_menor_o_igual_cero_rechaza`: `precio_mensual="0"`.
  - `test_post_habitaciones_fuera_rango_rechaza`: `habitaciones="25"`.
  - `test_post_banos_fuera_rango_rechaza`: `banos="11"`.
  - `test_post_area_vacio_persiste_con_cero`: `area=""` → 200 con `area=0`
    y propiedad persistida (no 422).
  - `test_post_area_negativo_rechaza`: `area="-5"`.
  - `test_post_titulo_256_caracteres_rechaza`.
  - `test_post_duplicado_retorna_error_global`: segunda inserción del mismo
    `titulo+direccion+ciudad` → 200 con error en `__all__` "Ya existe una
    propiedad con ese título y dirección en Miami".
  - `test_get_root_navbar_contiene_enlace_nueva_propiedad`: GET `/`
    contiene `<a href="/propiedades/nueva"`.
  - `test_cookie_flash_firma_invalida_se_ignora_silenciosamente`: cookie
    con firma alterada no rompe el render de `/propiedades`.
  Traza a SC-001, SC-002, SC-003, SC-004, SC-005, SC-006, SC-007, SC-008,
  SC-009, SC-010, SC-011.
- [ ] **T7.2** [GREEN]: Implementar en
  `app/modules/propiedades/routes.py`:
  - `GET /propiedades/nueva`: renderiza `crear_propiedad.html` con
    contexto `{'request': request, 'form': {}, 'errores': {}}`. Traza a
    FR-001, SC-001.
  - `POST /propiedades`: recibe Form() params como `str` con default `""`
    para tolerar vacíos sin 422. Conversión manual con `try/except
    (ValueError, TypeError)`:
    - Campos requeridos (`precio_mensual`, `habitaciones`, `banos`): si
      conversión falla, mantener `""` para que Pydantic genere error.
    - Campo opcional (`area`): si `""`, convertir a `None` para que
      Pydantic aplique default 0 (FR-020, clarificación 1); si no
      parseable como int, mantener `""` para error.
    Construye `PropiedadFormIn`. Si `ValidationError`: parsea errores a
    `errores: dict[str, str]` y re-renderiza con valores previos. Llama
    `service.crear_propiedad_desde_formulario()`. Si retorna `None`:
    re-renderiza con `errores['__all__']` con mensaje de duplicado. Si
    retorna `PropiedadOut`: setea cookie `flash` firmada + `RedirectResponse`
    con `status_code=303` y `Location: /propiedades`. Traza a FR-002,
    FR-011, FR-012, FR-013.
  - Modificar `GET /propiedades`: lee cookie `flash`, si válida la agrega
    al contexto como `flash: dict`, llama `response.delete_cookie('flash')`.
    Traza a FR-011, SC-004.
- [ ] **T7.3** [REFACTOR]: Agregar helpers privados al final de
  `app/modules/propiedades/routes.py`:
  - `_firmar_flash(payload: dict, secret: str) -> str`: serializa con
    `json`, codifica con `base64.urlsafe_b64encode`, calcula
    `hmac.new(secret, payload, hashlib.sha256).hexdigest()`, retorna
    `f"{payload_b64}.{hex_digest}"`.
  - `_verificar_flash(cookie: str, secret: str) -> dict | None`: split por
    último `.`, recalcula HMAC, compara con `hmac.compare_digest`,
    decodifica o retorna `None`.
  - `_leer_y_limpiar_flash(request, response, secret) -> dict | None`:
    encapsula lectura + borrado.
  - Constantes: `FLASH_COOKIE_NAME = "flash"`, `FLASH_MAX_AGE = 60`.

## Fase 8: Calidad

- [ ] **T8.1**: `uv run ruff check .` y `uv run ruff format --check .`.
  Cero hallazgos.
- [ ] **T8.2**: `uv run mypy --strict app/modules/propiedades/`. Cero
  errores.
- [ ] **T8.3**: `uv run pytest tests/unit/propiedades
  tests/integration/propiedades -q`. Todos verdes.
- [ ] **T8.4**: `uv run pytest --cov=app/modules/propiedades
  --cov-fail-under=80`. Cobertura ≥ 80%.
- [ ] **T8.5**: `make visual-check` auditoría de trazabilidad visual.

---

## Resumen de trazabilidad

### Cobertura de requisitos funcionales

| FR | Tarea(s) |
|----|----------|
| FR-001 | T5.1, T7.1, T7.2 |
| FR-002 | T7.1, T7.2 |
| FR-003 | T4.1, T5.3, T7.1 |
| FR-004 | T1.1, T1.2, T5.1 |
| FR-005 | T1.1, T1.2 |
| FR-006 | T2.1, T2.3 |
| FR-007 | T2.1, T2.3 |
| FR-008 | T2.1, T2.2 |
| FR-009 | T2.1, T2.2, T5.2 |
| FR-010 | (cubierto por spec 004) |
| FR-011 | T5.2, T7.1, T7.2 |
| FR-012 | T1.1, T5.1, T7.1, T7.2 |
| FR-013 | T5.1, T7.1, T7.2 |
| FR-014 | T1.1, T1.2 |
| FR-015 | T1.1, T1.2 |
| FR-016 | T1.1, T1.2 |
| FR-017 | T2.3 |
| FR-018 | T5.1 |
| FR-019 | T5.1 |
| FR-020 | T1.1, T1.2, T2.3, T7.1, T7.2 |

### Cobertura de criterios de éxito

| SC | Tarea(s) |
|----|----------|
| SC-001 | T7.1, T7.2 |
| SC-002 | T7.1, T7.2 |
| SC-003 | T2.3, T7.1 |
| SC-004 | T5.2, T7.1, T7.2 |
| SC-005 | T5.3, T7.1 |
| SC-006 | T1.1, T1.2, T7.1 |
| SC-007 | T1.1, T1.2, T7.1 |
| SC-008 | T1.1, T1.2, T7.1 |
| SC-009 | T2.1, T2.2, T7.1 |
| SC-010 | T2.1, T2.4 |
| SC-011 | T7.1 |

### Marcadores visuales

| Marcador | Tarea | Archivo |
|----------|-------|---------|
| `[visual][extension]` | T4.1 | `app/static/icons/plus.svg` (nuevo) |
| `[visual][extension]` | T5.1 | `crear_propiedad.html` (nuevo) |
| `[visual][extension]` | T5.2 | `propiedades.html` (modificación) |
| `[visual][extension]` | T5.3 | `_navbar.html` (modificación) |
| `[visual][extension]` | T6.1 | `app.css` (clases nuevas) |

### Resumen

- **Total tareas**: 27 (T0.1–T8.5).
- **Fases**: 9 (Fase 0 a Fase 8).
- **Tests planeados**: 33 (12 unit schemas form + 2 unit schemas in + 6 unit service + 15 integration routes).
- **Marcadores `[visual][extension]`**: 5.
- **Marcadores `[visual]` puros**: 0.
- **Archivos a crear**: 5 (`plus.svg`, `crear_propiedad.html`, 3 archivos de test).
- **Archivos a modificar**: 8 (4 del vertical slice propiedades, navbar, css, settings, config example).
- **Archivos no modificados**: 5 (`main.py`, `base.html`, `_sidebar.html`, `models.py`, `repository.py`).
- **Dependencias nuevas**: 0.
- **Tokens visuales canónicos modificados**: 0.
- **Desviaciones documentadas en Complexity Tracking**: 4.
