---
name: 007-crear-propiedad-specify
description: >
  Crea la spec 007-crear-propiedad para el alta de propiedades con formulario
  server-rendered, validaciones obligatorias, valores por defecto y generación
  automática de imagen vía picsum.photos.
spec_kit_command: "/speckit.specify"
usage: "/speckit.specify @.opencode/prompts/007-crear-propiedad.specify.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

## Prompt para `speckit.specify`

**Nombre de la spec**: `007-crear-propiedad`

## Contexto funcional actual

El proyecto Realtor ya tiene el módulo de propiedades con modelo (`Propiedad`),
repositorio (`crear()`, `listar()`, `obtener_por_id()`), DTOs (`PropiedadIn`,
`PropiedadOut`) y servicio (`crear_propiedad()`, `listar_propiedades()`). La
página de listado en `GET /propiedades` ya funciona con grid de cards.

El navbar (`_navbar.html`) actualmente solo muestra breadcrumbs y el usuario.
No existe un botón "Nueva propiedad" ni una página de creación.

El modelo `Propiedad` tiene las columnas: `id` (UUID auto-generado), `titulo`,
`direccion`, `ciudad` (default 'Miami'), `precio_mensual`, `habitaciones`,
`banos`, `area`, `estado` (enum), `imagen`, `created_at`, `updated_at`.

El DTO `PropiedadIn` ya valida: `precio_mensual > 0`, `habitaciones >= 1`,
`banos >= 1`, `area > 0`, y estado del catálogo.

## Objetivo

Crear una página server-rendered con formulario para dar de alta nuevas
propiedades, con validaciones obligatorias, valores por defecto (estado
`disponible`, ciudad `Miami`) y generación automática de imagen usando
el servicio https://picsum.photos.

## Resultado esperado

Después de aplicar esta feature, el sistema debe contar con:

* Botón "Nueva propiedad" en el navbar que navega a la página de creación.
* Página HTML server-rendered con formulario de creación.
* Endpoint `GET /propiedades/nueva` que renderiza el formulario vacío.
* Endpoint `POST /propiedades` que procesa el formulario.
* Validación de campos obligatorios: titulo, direccion, precio_mensual,
  habitaciones, banos.
* Campos con solo espacios tratados como vacíos.
* Estado por defecto `disponible` al crear.
* Imagen generada automáticamente vía `https://picsum.photos` con fallback
  definido si el servicio falla.
* ID autogenerado por la base de datos.
* Redirección a `/propiedades` tras creación exitosa con mensaje flash.
* Errores de validación mostrados inline en el formulario.
* Tests unitarios y de integración.

## Alcance explícito

* INCLUYE: botón "Nueva propiedad" en `_navbar.html`.
* INCLUYE: página de creación con formulario server-rendered.
* INCLUYE: endpoint `GET /propiedades/nueva` para renderizar formulario.
* INCLUYE: endpoint `POST /propiedades` para procesar creación.
* INCLUYE: validación de campos obligatorios (titulo, direccion,
  precio_mensual, habitaciones, banos).
* INCLUYE: tratamiento de campos con solo espacios como vacíos.
* INCLUYE: estado por defecto `disponible`.
* INCLUYE: generación automática de imagen vía `https://picsum.photos`.
* INCLUYE: política de fallback si picsum.photos falla.
* INCLUYE: redirección post-creación con mensaje flash.
* INCLUYE: errores de validación inline en el formulario.
* INCLUYE: tests unitarios del servicio y tests de integración del endpoint.

## Fuera de alcance

* NO INCLUYE: edición de propiedades existentes.
* NO INCLUYE: eliminación de propiedades.
* NO INCLUYE: filtros avanzados, búsqueda ni paginación.
* NO INCLUYE: subida de imágenes por el usuario.
* NO INCLUYE: nuevas dependencias de paquetes Python.
* NO INCLUYE: rediseño del layout global, sidebar o navbar más allá del botón.
* NO INCLUYE: cambios en tokens visuales canónicos ni paleta.
* NO INCLUYE: creación de módulos de rentas, pagos, inquilinos o contratos.
* NO INCLUYE: endpoints de API JSON adicionales.

## Decisión arquitectónica esperada

La página de creación debe vivir en el vertical slice de propiedades existente.
El endpoint `GET /propiedades/nueva` renderiza el formulario. El endpoint
`POST /propiedades` procesa la creación usando `service.crear_propiedad()` que
ya existe.

El template del formulario debe vivir en
`app/modules/propiedades/templates/crear_propiedad.html`.

El botón "Nueva propiedad" se agrega en `_navbar.html` dentro de la sección
de acciones.

La generación de imagen se gestiona en `service.py` antes de persistir.

## Historias de usuario

### P1 - Crear una nueva propiedad desde el formulario

Como usuario del sistema, quiero acceder a una página con formulario para
registrar una nueva propiedad con los datos obligatorios.

**Criterios de aceptación**:

* El formulario tiene campos: titulo, direccion, precio_mensual, habitaciones,
  banos.
* Al enviar datos válidos, se crea la propiedad con id autogenerado, estado
  `disponible` e imagen generada automáticamente.
* Tras creación exitosa, el usuario es redirigido a `/propiedades` con mensaje
  flash de éxito.

### P2 - Navegar a la página de creación desde el navbar

Como usuario, quiero que el botón "Nueva propiedad" del navbar me lleve a la
página de creación.

**Criterios de aceptación**:

* El navbar contiene un botón o enlace "Nueva propiedad".
* Hacer clic navega a `GET /propiedades/nueva`.

### P3 - Ver errores de validación al enviar datos inválidos

Como usuario, quiero ver mensajes de error claros cuando envío datos inválidos
para corregirlos.

**Criterios de aceptación**:

* Campos obligatorios vacíos muestran error inline.
* Campos con solo espacios se tratan como vacíos.
* precio_mensual no numérico o <= 0 muestra error.
* habitaciones y banos no numéricos o fuera de rango muestran error.
* El formulario conserva los datos ingresados al mostrar errores.

### P4 - Generación automática de imagen

Como sistema, necesito generar automáticamente una imagen para la propiedad
usando `https://picsum.photos`.

**Criterios de aceptación**:

* La URL de imagen se genera automáticamente al crear.
* Si picsum.photos falla temporalmente, se aplica la política de fallback
  definida (imagen vacía o placeholder).

## Requisitos funcionales

La spec debe convertir estas reglas en requisitos funcionales numerados como
`FR-XXX`:

1. El sistema DEBE exponer `GET /propiedades/nueva` que renderice el formulario
   de creación.
2. El sistema DEBE exponer `POST /propiedades` que procese los datos del
   formulario.
3. El botón "Nueva propiedad" del navbar DEBE navegar a `/propiedades/nueva`.
4. Los campos obligatorios son: titulo, direccion, precio_mensual, habitaciones,
   banos.
5. Campos con solo espacios en blanco DEBEN considerarse vacíos.
6. El estado por defecto al crear DEBE ser `disponible`.
7. La ciudad por defecto DEBE ser `Miami` (ya definido en el modelo).
8. La imagen DEBE generarse automáticamente usando `https://picsum.photos`.
9. Si `https://picsum.photos` falla, el sistema DEBE aplicar fallback
   (definir política: string vacío para usar placeholder visual existente).
10. El id DEBE ser autogenerado por la base de datos (UUID).
11. Tras creación exitosa, el sistema DEBE redirigir a `/propiedades` con
    mensaje flash de éxito.
12. Los errores de validación DEBEN mostrarse inline junto al campo
    correspondiente.
13. El formulario DEBE conservar los datos ingresados al mostrar errores
    (re-popular campos).
14. precio_mensual DEBE ser numérico y mayor que cero.
15. habitaciones DEBE ser entero mayor o igual a 1.
16. banos DEBE ser entero mayor o igual a 1.
17. La lógica de creación DEBE usar `service.crear_propiedad()` existente.
18. El template del formulario DEBE vivir en
    `app/modules/propiedades/templates/`.
19. El formulario DEBE usar el componente `_form_field.html` existente.
20. El `area` no es campo obligatorio en el formulario; se puede omitir o
    definir un default razonable.

## Requisitos no funcionales y gobernanza vigente

Aplica la gobernanza vigente del proyecto. La spec no debe reescribir reglas
globales. Solo debe referenciar que aplican.

La spec debe declarar explícitamente:

* Aplica arquitectura vertical slice vigente.
* Aplica separación rutas/servicios/repositorios/templates.
* Aplica política de calidad, typing, tests y herramientas.
* Aplica gobernanza visual vigente.
* No se introducen dependencias nuevas.
* No se reabren decisiones técnicas heredadas.

## Gobernanza visual

La spec debe incluir sección de gobernanza visual con identificadores `VTG-XXX`:

* `VTG-001`: No modifica tokens visuales canónicos.
* `VTG-002`: Extiende CSS con clases nuevas para formulario y página de
  creación. [visual][extension]
* `VTG-003`: No modifica iconografía existente. Si se requiere icono nuevo
  para el botón, tarea explícita con `[visual][extension]`.
* `VTG-004`: Modifica `_navbar.html` para agregar botón "Nueva propiedad".
  [visual][extension]
* `VTG-005`: No modifica `base.html` ni sidebar.
* `VTG-006`: No rediseña páginas existentes.
* `VTG-007`: Cualquier modificación de token visual existente requiere
  marcador `[visual]` en `tasks.md`.

## Entidades o conceptos clave

* `Propiedad`: entidad persistida existente, destino de la creación.
* `PropiedadIn`: DTO de entrada existente para crear propiedad.
* `PropiedadOut`: DTO de salida existente.
* `EstadoPropiedad`: enum con catálogo cerrado de estados.
* `Formulario de creación`: página server-rendered con campos obligatorios.
* `Servicio picsum.photos`: generador externo de imágenes placeholder.
* `Fallback de imagen`: política cuando picsum.photos no está disponible.

## Edge cases obligatorios

* `precio_mensual` vacío: error de validación inline.
* `precio_mensual` no numérico (texto): error de validación inline.
* `precio_mensual` <= 0 (negativo o cero): error de validación inline.
* `habitaciones` vacío: error de validación inline.
* `habitaciones` no numérico: error de validación inline.
* `habitaciones` fuera de rango de negocio (ej. > 100): error de validación.
* `banos` vacío: error de validación inline.
* `banos` no numérico: error de validación inline.
* `banos` fuera de rango de negocio (ej. > 100): error de validación.
* Campos con solo espacios en blanco: tratados como vacíos, error de
  validación.
* Falla temporal de `https://picsum.photos`: fallback a string vacío
  (placeholder visual existente se usa en listado).
* `titulo` o `direccion` con más de 255 caracteres: error de validación o
  truncamiento según modelo.
* Duplicado de `titulo` + `direccion` + `ciudad` (constraint único): error
  de negocio manejado gracefully.

## Success Criteria obligatorios

Numerados como `SC-XXX`:

* `SC-001`: GET /propiedades/nueva retorna 200 con formulario HTML y layout
  base.
* `SC-002`: POST /propiedades con datos válidos crea la propiedad y redirige
  a /propiedades con mensaje flash.
* `SC-003`: La propiedad creada tiene id autogenerado, estado `disponible` e
  imagen generada.
* `SC-004`: POST con datos inválidos retorna 422 o re-renderiza formulario
  con errores inline.
* `SC-005`: Botón "Nueva propiedad" del navbar navega a /propiedades/nueva.
* `SC-006`: Campos con solo espacios se tratan como vacíos.
* `SC-007`: precio_mensual <= 0 o no numérico muestra error.
* `SC-008`: habitaciones y banos fuera de rango muestran error.
* `SC-009`: Si picsum.photos falla, se aplica fallback sin romper la creación.
* `SC-010`: Tests unitarios cubren validaciones y creación exitosa.
* `SC-011`: Tests de integración cubren flujo completo de creación.

## Riesgos y dependencias

* Depende de spec 004 (propiedades base con modelo, repositorio y seed).
* Depende de spec 006 (página de propiedades con cards para redirección
  post-creación).
* `service.crear_propiedad()` ya existe pero puede requerir ajuste para
  generar imagen automáticamente.
* `https://picsum.photos` es un servicio externo que puede fallar; se
  requiere política de fallback clara.
* El constraint único `uq_propiedades_identidad_negocio` (titulo + direccion
  + ciudad) puede generar error de duplicado que debe manejarse.
* El campo `area` es obligatorio en el modelo pero no está en los campos
  requeridos del formulario; necesita default o inclusión.

## Assumptions

* `service.crear_propiedad()` ya existe y acepta `PropiedadIn`.
* `repository.crear()` ya existe y persiste la propiedad.
* El modelo `Propiedad` ya tiene todas las columnas necesarias.
* El id se autogenera vía `func.gen_random_uuid()` en la base de datos.
* El estado `disponible` existe en `EstadoPropiedad`.
* El componente `_form_field.html` existe y es reutilizable.
* `https://picsum.photos` retorna una URL de imagen válida con formato
  `https://picsum.photos/<width>/<height>` (ej. `/800/600`).
* El router de propiedades ya está registrado en `app/main.py`.
* El campo `area` se incluirá en el formulario o tendrá un default razonable.

## Entrega esperada

Genera `spec.md` para `007-crear-propiedad` en:

```
specs/007-crear-propiedad/spec.md
```

## Estructura esperada

* User Scenarios & Testing.
* User Stories P1/P2/P3/P4.
* Functional Requirements `FR-XXX`.
* Gobernanza visual `VTG-XXX`.
* Key Entities.
* Success Criteria `SC-XXX`.
* Edge Cases.
* Riesgos y dependencias.
* Assumptions.
* Checklist en `checklists/requirements.md`.

## Reglas obligatorias

* No implementes código.
* No generes `plan.md` ni `tasks.md`.
* No modifiques archivos de aplicación.
* No cambies la constitución.
* Mantén todo en español.
* Respeta `AGENTS.md`, constitución e instrucciones.
* No uses Supabase, `.yml`, Bootstrap, Tailwind, CDN, webfonts, emojis.
* No uses `pip`, `poetry`, `requirements.txt`, `setup.py`.
* No reabras decisiones técnicas cerradas.
* No agregues modelos de rentas, pagos ni contratos.

## Preguntas interactivas

Si detectas ambigüedad material, pregunta antes de cerrar. Como mínimo:

* Si el campo `area` se incluye en el formulario o se define un default.
  → Preguntar si hay ambigüedad.
* Si el formulario usa HTMX para envío asíncrono o POST tradicional con
  redirect. → Preguntar si hay ambigüedad.
* Si el fallback de imagen usa string vacío o una URL fija de placeholder.
  → Preguntar si hay ambigüedad.
* Si se vendorea un icono nuevo para el botón "Nueva propiedad" (ej.
  `plus` o `plus-circle` de Lucide). → Preguntar si hay ambigüedad.

## Recordatorios Spec Kit

* Ejecutar hook `before_specify` (incluye `speckit.git.feature`).
* Crear branch `007-crear-propiedad`.
* Ubicación: `specs/007-crear-propiedad/` en raíz del repo.

## Salida esperada

```
Archivo actualizado: specs/007-crear-propiedad/spec.md
Feature: 007-crear-propiedad
Siguiente comando: /speckit.clarify @.opencode/prompts/007-crear-propiedad.clarify.prompt.md
```
