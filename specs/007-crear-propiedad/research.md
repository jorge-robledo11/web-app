# Research: Crear propiedad

**Feature**: 007-crear-propiedad
**Phase**: 0 — Research
**Date**: 2026-06-20

## Decisiones técnicas investigadas

### 1. Mecanismo de flash post-acción

**Decisión**: Cookie firmada con HMAC-SHA256 usando solo stdlib de Python
(`hmac`, `hashlib`, `base64`, `json`), sin middleware de sesión.

**Alternativas consideradas**:

- **A) `SessionMiddleware` de Starlette** (canónico para FastAPI):
  rechazado porque requiere `itsdangerous`, que **no está disponible en el
  entorno actual** del proyecto y la constitución prohíbe introducir nuevas
  dependencias explícitas (NFR-ARCH-005).
- **B) Cookie sin firma** (JSON puro en el value): rechazado por
  vulnerabilidad de tampering. Un usuario podría inyectar mensajes flash
  falsos a su propia sesión (bajo impacto funcional porque solo afecta
  su UX, pero违背 principios de seguridad por defecto).
- **C) Query parameter `?flash=success`** visible en la URL: rechazado
  por UX (URL fea, bookmarkeable, loggeada en proxies) y por
  anti-idiomaticidad.
- **D) HTMX OOB swap a `#flash-zone`** (patrón canónico de
  `frontend.instructions.md` §7 y §10): rechazado porque la spec eligió
  POST tradicional con redirect 303 (clarificación 3), no submit HTMX.

**Fundamento**: HMAC-SHA256 con stdlib provee:

- **Tamper resistance**: el cliente no puede falsificar mensajes válidos
  sin conocer el secret.
- **Timing-safe comparison**: uso de `hmac.compare_digest()` evita
  ataques de timing.
- **Cero dependencias nuevas**: solo módulos stdlib disponibles en
  cualquier instalación Python 3.13.
- **YAGNI**: no abstraer hasta tener 2+ consumidores. Helper local en
  `routes.py` del módulo `propiedades`; candidato a extracción a
  `app/core/flash.py` cuando rentas/pagos/contratos lo necesiten.

**Limitaciones reconocidas**:

- Sin revocación inmediata de un secret rotado (los flashes en tránsito
  quedan inválidos, comportamiento aceptable).
- Sin scoping por usuario (no hay auth aún; cuando se introduzca, el
  helper debe incluir el user_id en el payload firmado).

### 2. Dedicación de DTO: nuevo `PropiedadFormIn` vs modificar `PropiedadIn`

**Decisión**: Crear un DTO nuevo `PropiedadFormIn` con solo los campos
que el usuario completa en el formulario (`titulo`, `direccion`,
`precio_mensual`, `habitaciones`, `banos`, `area`). `PropiedadIn` se
conserva como contrato canónico del modelo con todos los campos
obligatorios.

**Alternativas consideradas**:

- **A) Modificar `PropiedadIn` para hacer `estado`, `imagen`, `area`
  opcionales**: rechazado porque rompe el contrato canónico del modelo
  (cualquier consumidor externo de `PropiedadIn` que asumía esos campos
  obligatorios se rompería). También diluye la diferencia entre
  "form input" y "data model input".
- **B) Reutilizar `Form(...)` de FastAPI directamente sin DTO Pydantic
  específico**: rechazado porque dispersa la validación en annotations
  de FastAPI, pierde la trazabilidad de Pydantic v2 (`frozen=True`,
  `model_validate` para errores) y complica la generación de mensajes
  de error estructurados.
- **C) Construir `Propiedad` SQLAlchemy directamente en el servicio,
  sin pasar por `PropiedadIn`**: rechazado porque rompe el contrato
  canónico del slice (`PropiedadIn` es la entrada validada de la capa
  de servicio).

**Fundamento**: `PropiedadFormIn` cumple el principio de **boundary DTO**
de la constitución XIV: "Las respuestas HTTP se mapean a DTOs Pydantic"
y "Los límites del sistema validan entradas antes de ejecutar lógica
de negocio". El form HTTP es un límite del sistema; su entrada merece
su propio DTO con sus propias reglas de validación
(`min_length=1, max_length=255, le=20, le=10`).

**Modificación secundaria necesaria**: `PropiedadIn.area` se modifica de
`Field(gt=0)` a `Field(ge=0, default=0)` para que el servicio pueda
construir el DTO canónico con `area=0` cuando el formulario lo omite.
Los tests existentes en `test_schemas.py` siguen pasando porque usan
`area=850`.

### 3. Validación: rango de `habitaciones` y `banos`

**Decisión**: `habitaciones ∈ [1, 20]` y `banos ∈ [1, 10]` (rangos
residenciales urbanos).

**Alternativas consideradas**:

- **A) Sin límite superior** (`ge=1` solo): rechazado porque permite
  valores absurdos (500 habitaciones) que ensucian la base de datos y
  el render de cards.
- **B) Rangos más altos** (`le=50` y `le=20`): rechazado por decisión
  de clarificación. El realtor gestiona propiedades residenciales
  urbanas, no hoteles ni complejos.
- **C) Validación solo en el servicio** (no en Pydantic): rechazado
  por la constitución XIV: "Los límites del sistema validan entradas
  antes de ejecutar lógica de negocio". Rangos numéricos caben en
  Pydantic v2 con `Field(ge=, le=)`.

**Fundamento**: Los rangos cubren el 99% de propiedades residenciales
urbanas y filtran inputs claramente erróneos. Documentado en la
clarificación 6 de la spec.

### 4. Parseo de formulario: `Form(...)` por campo vs modelo

**Decisión**: `Form(...)` por campo en la firma de la ruta, con
construcción manual de `PropiedadFormIn` dentro de `try/except
ValidationError`. Los campos numéricos se reciben como `str` con
default `""` para tolerar vacíos sin 422 de FastAPI.

**Alternativas consideradas**:

- **A) Binding directo a un Pydantic BaseModel con `Form(...)`**: no
  soportado nativamente por FastAPI. Existen workarounds con
  `python-multipart` + `pydantic.fields.Field` pero añaden complejidad.
- **B) `Form(...)` con tipos nativos (`int`, `Decimal`)**: rechazado
  porque campos vacíos o malformados lanzan 422 antes de llegar a
  Pydantic, rompiendo el flujo de "form re-renderizado con error
  inline". 422 retorna JSON, no HTML.
- **C) `request.form()` manual** en el cuerpo de la ruta: rechazado
  porque pierde la inyección de dependencias de FastAPI y la
  validación automática.

**Fundamento**: La opción B con `str` + `try/except` permite:

- Tolerar inputs malformados sin generar 422.
- Distinguir entre campos requeridos (que propagan el error) y el
  opcional `area` (que se convierte a `None` para usar el default).
- Mantener `PropiedadFormIn` como contrato de validación centralizado
  en Pydantic, no disperso en annotations de FastAPI.

**Limitación reconocida**: Si en el futuro hay muchos más campos
numéricos, considerar un parser genérico con `Annotated[int | None,
Form()]` y pre-validación. Por ahora YAGNI.

### 5. Generación de imagen con picsum.photos

**Decisión**: Función `_generar_url_imagen(ancho=800, alto=600) -> str`
síncrona que construye `f"https://picsum.photos/{ancho}/{alto}"`. Si el
formato falla (caso extremo), retorna `""` para activar el placeholder
visual del listado.

**Alternativas consideradas**:

- **A) HTTP call al endpoint de picsum.photos al crear** (descargar
  bytes, almacenar local): rechazado por costo innecesario (latencia,
  almacenamiento, dependencia de red en escritura).
- **B) Hash determinista del titulo** para generar URL estable:
  rechazado por spec 005 bugfix (`test_seed_no_usa_hashlib_para_imagenes`)
  que eliminó el patrón de hashes inventados.
- **C) Lista curada de imágenes** por índice/titulo: rechazado por
  esfuerzo de mantenimiento y por decisión de la spec (F8: "imagen
  generada automáticamente").
- **D) URL fija sin cache-buster**: aceptable pero menos resistente a
  cache de browser que muestre la misma imagen para todas las
  propiedades.

**Fundamento**: picsum.photos retorna la misma imagen para la misma
URL; sin cache-buster todas las cards mostrarían la misma foto. La
URL `https://picsum.photos/800/600` sin parámetros adicionales
funciona porque picsum cachea por path. Si en el futuro se quiere
imágenes variadas, agregar `?random=<uuid>` o `?lock=<prop.id>`.

**Fallback**: El "fallback a string vacío" es **defensivo**. La URL se
construye siempre correctamente (formato determinista). La falla real
del servicio `picsum.photos` ocurre **client-side** al cargar la
imagen; el componente `_card_propiedad.html` ya maneja este caso con
`onerror` que activa el placeholder (implementado en spec 006).

### 6. Manejo de duplicados vía `IntegrityError`

**Decisión**: Capturar `sqlalchemy.exc.IntegrityError` en
`service.crear_propiedad_desde_formulario()`, llamar
`await session.rollback()`, log warning y retornar `None`. La ruta
interpreta `None` como "duplicado" y re-renderiza con error global en
`__all__`.

**Alternativas consideradas**:

- **A) Pre-validación con `SELECT` antes de `INSERT`**: rechazado por
  race condition (entre el SELECT y el INSERT otro request puede
  insertar la misma combinación). La constraint UNIQUE de DB es la
  única fuente de verdad.
- **B) `try/except` en la ruta**: rechazado porque la constitución IV
  establece que `service.py` contiene la lógica de negocio, no la
  ruta. La captura debe estar en la capa de servicio.
- **C) `try/except` en el repositorio**: rechazado porque la
  constitución IV establece que el repositorio solo hace acceso a
  datos, sin reglas de negocio ni transformación de errores.
- **D) Levantar una excepción de dominio tipada (`DuplicateProperty`)**
  y manejarla en la ruta: elegante pero YAGNI. El retorno `None` es
  suficiente para esta feature; un `Enum` de razones de fallo puede
  venir cuando haya 2+ razones de fallo distintas.

**Fundamento**: El contrato `Optional[PropiedadOut]` (puede ser `None`)
es explícito y simple. La ruta solo verifica `if resultado is None: ...`.
Cuando crezca el número de razones de fallo (ej. "sin permisos",
"estado inválido", etc.), refactorizar a un `Enum ResultadoCrear` o
excepciones de dominio.

### 7. Ubicación del flash: `{% block content %}` vs `#flash-zone`

**Decisión**: Renderizar el flash dentro de `{% block content %}` al
inicio de `propiedades.html`, **no** en el `<div id="flash-zone">` de
`base.html`.

**Alternativas consideradas**:

- **A) Modificar `base.html` con `[visual][extension]`** para agregar
  un bloque `{% block flash %}` dentro de `#flash-zone`: rechazado
  porque **VTG-005 prohíbe explícitamente modificar `base.html`** y
  `_sidebar.html` en esta feature.
- **B) HTMX OOB swap** al `#flash-zone` (patrón canónico): rechazado
  porque el flujo es POST tradicional con redirect 303, no HTMX.
- **C) Re-render del POST sin redirect** (renderizar directamente la
  página de listado con flash inline): rechazado porque viola FR-011
  (redirect 303 post-creación) y crea problemas de refresh del
  navegador (re-POST al refrescar).

**Fundamento**: La desviación se documenta en `Complexity Tracking` del
plan. Funcionalmente equivalente: el flash aparece visible en la
página, usando `_alerta.html` con clases y tokens existentes. Si una
futura feature usa HTMX para el submit, debe volver al patrón
canónico de flash (HTMX OOB a `#flash-zone`).

### 8. Helper de cookie firmada: local vs abstracción compartida

**Decisión**: Helpers privados `_firmar_flash`, `_verificar_flash` y
`_leer_y_limpiar_flash` definidos al final de
`app/modules/propiedades/routes.py`.

**Alternativas consideradas**:

- **A) Extraer a `app/core/flash.py`** ahora: rechazado por YAGNI
  (constitución IV: "La lógica compartida solo se extrae cuando exista
  duplicación real demostrable, nunca por anticipación").
- **B) Usar `starlette.middleware.sessions.SessionMiddleware`**:
  rechazado por dependencia de `itsdangerous` no disponible (ver §1).

**Fundamento**: Cuando una segunda feature (rentas, pagos, contratos)
necesite el mismo mecanismo, refactorizar a `app/core/flash.py`. El
docstring del helper debe mencionar explícitamente: "Candidato a
extracción tras 2+ consumidores".

### 9. Configuración de `session_secret`

**Decisión**: Nuevo campo requerido `session_secret: str` en
`Settings` (cargado de `config/app.yaml` o env var
`SESSION_SECRET`). Documentado en `config/app.example.yaml` con
placeholder.

**Alternativas consideradas**:

- **A) Default generado con `secrets.token_urlsafe(32)` al vuelo**:
  rechazado por inconsistencia entre reinicios (los flashes en tránsito
  quedan inválidos al reiniciar) y por seguridad (no auditable).
- **B) Hardcoded en código**: rechazado por seguridad (secret en
  git).
- **C) Solo env var** (sin YAML): rechazado por consistencia con el
  patrón del proyecto (todas las configs en `config/app.yaml`).

**Fundamento**: Sigue el patrón de la constitución X: "`config/app.yaml`
nunca debe versionarse con secretos reales" y "`config/app.example.yaml`
debe existir como plantilla". Riesgo menor: devs que no actualicen
`config/app.yaml` verán `PydanticValidationError` al arrancar. Mitigación
documentada en commit message y en `quickstart.md` §0.

## Decisiones heredadas de specs previas

| Decisión | Spec origen | Aplicación en 007 |
|----------|-------------|-------------------|
| `func.gen_random_uuid()` para PK | 004 | Sin cambios; id autogenerado por DB |
| Constraint `uq_propiedades_identidad_negocio` | 004 | Usado para detectar duplicados vía `IntegrityError` |
| `EstadoPropiedad` enum cerrado | 004 | Default al crear: `DISPONIBLE` |
| `_card_propiedad.html` con placeholder visual | 006 | Reutilizado cuando `imagen` es `""` |
| Iconografía Lucide vendoreada | 002 | Nuevo icono `plus` agregado con `[visual][extension]` |
| Componente `_form_field.html` | 002 | Reutilizado para cada campo del formulario |
| `_alerta.html` con 4 variantes | 002 | Reutilizado para flash y errores globales |
| `make visual-check` para auditoría | 002 | Ejecutado en Fase 8 (T8.5) |
