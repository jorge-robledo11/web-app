---
name: 006-pagina-propiedades-cards-spec
description: >
  Crea la spec 006-pagina-propiedades-cards para la página server-rendered
  de propiedades con grid de cards responsive y endpoint dedicado.
spec_kit_command: "/speckit.specify"
usage: "/speckit.specify @.opencode/prompts/006-pagina-propiedades-cards.spec.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

## Prompt para `speckit.specify`

**Nombre de la spec**: `006-pagina-propiedades-cards`

## Contexto funcional actual

El proyecto Realtor ya tiene un dominio de propiedades persistido con modelo,
repositorio, DTOs y seed de 10 propiedades de Miami. El layout base con sidebar
y navbar ya existe. El componente `_card_propiedad.html` ya existe como
componente compartido mínimo (icono, título, detalle, badge, acción).

El enlace "Propiedades" del sidebar actualmente apunta a `#` (placeholder sin
destino). No existe una página que liste propiedades.

## Objetivo

Crear una página server-rendered que liste todas las propiedades persistidas en
un grid de cards responsive, con endpoint `GET /propiedades` dedicado y
navegación lateral corregida.

## Resultado esperado

Después de aplicar esta feature, el sistema debe contar con:

* Endpoint `GET /propiedades` que consulta propiedades reales desde BD.
* Página HTML server-rendered con grid de cards (una card por propiedad).
* Cada card muestra: imagen, título, dirección, habitaciones, baños, área,
  precio mensual y estado.
* Grid responsive: 3 columnas desktop, 2 tablet, 1 móvil.
* Enlace "Propiedades" del sidebar funcional apuntando a `/propiedades`.
* Estado vacío explícito cuando no hay propiedades.
* Placeholder visual para propiedades sin imagen.
* Textos largos truncados con ellipsis.

## Alcance explícito

* INCLUYE: endpoint `GET /propiedades` server-rendered.
* INCLUYE: consulta de propiedades desde repositorio existente (`listar()`).
* INCLUYE: grid responsive de cards con 3/2/1 columnas.
* INCLUYE: extender `_card_propiedad.html` con campos nuevos: imagen,
  habitaciones, baños, área, precio y estado.
* INCLUYE: placeholder visual (fondo + icono building-2) para imagen faltante.
* INCLUYE: formato de precio con símbolo `$` y dos decimales.
* INCLUYE: formato de área con unidad "m²" y separador de miles.
* INCLUYE: badge de estado usando `_badge_estado.html` existente.
* INCLUYE: actualizar href del sidebar de `#` a `/propiedades`.
* INCLUYE: estado vacío con mensaje descriptivo.
* INCLUYE: tests unitarios del servicio y tests de integración del render.

## Fuera de alcance

* NO INCLUYE: creación de módulos de rentas, pagos, inquilinos o contratos.
* NO INCLUYE: filtros avanzados, búsqueda, paginación ni ordenamiento.
* NO INCLUYE: nuevas dependencias.
* NO INCLUYE: rediseño del layout global, navbar o sidebar más allá del href.
* NO INCLUYE: cambios en tokens visuales canónicos ni paleta.
* NO INCLUYE: edición inline ni acciones CRUD desde esta pantalla.
* NO INCLUYE: endpoints de API JSON adicionales.

## Decisión arquitectónica esperada

La página debe vivir en el vertical slice de propiedades existente,
extendiendo `propiedades/routes.py` (actualmente placeholder) con el endpoint
`GET /propiedades`. El servicio `propiedades/service.py` debe exponer una
función que obtenga y formatee las propiedades para el template.

El template de la página debe vivir en
`app/modules/propiedades/templates/propiedades.html`.

El componente `_card_propiedad.html` debe extenderse para aceptar los 8 campos
requeridos. Si el markup actual no alcanza, se ajusta sin tocar tokens
visuales.

## Historias de usuario

### P1 - Ver listado de propiedades en grid de cards

Como usuario del sistema, quiero navegar a una página que muestre todas las
propiedades registradas en formato de cards para explorar el inventario.

**Criterios de aceptación**:

* GET /propiedades renderiza una card por propiedad persistida.
* Cada card muestra los 8 campos visibles requeridos.
* Propiedades sin imagen muestran placeholder sin romper layout.
* Textos largos se truncan con ellipsis.

### P2 - Navegar desde el menú lateral

Como usuario, quiero que el enlace "Propiedades" del sidebar me lleve a la
página de propiedades.

**Criterios de aceptación**:

* El href del enlace "Propiedades" en `_sidebar.html` es `/propiedades`.
* Hacer clic en el enlace carga la página de propiedades.

### P3 - Ver comportamiento responsive del grid

Como usuario, quiero que el grid se adapte a desktop, tablet y móvil.

**Criterios de aceptación**:

* Desktop (> 1023px): 3 columnas.
* Tablet (768px–1023px): 2 columnas.
* Móvil (< 768px): 1 columna.

### P4 - Ver estado vacío cuando no hay propiedades

Como usuario, quiero ver un mensaje claro cuando no hay propiedades registradas.

**Criterios de aceptación**:

* Sin propiedades en BD, la página muestra "No hay propiedades registradas".
* No se renderizan cards.

## Requisitos funcionales

La spec debe convertir estas reglas en requisitos funcionales numerados como
`FR-XXX`:

1. El sistema debe exponer `GET /propiedades` que consulte propiedades desde BD.
2. El endpoint debe usar el repositorio existente (`listar()`) para obtener datos.
3. El sistema debe renderizar una card por cada propiedad.
4. Cada card debe mostrar: imagen, título, dirección, habitaciones, baños,
   área, precio y estado.
5. El grid debe ser responsive: 3 columnas desktop, 2 tablet, 1 móvil.
6. El enlace "Propiedades" del sidebar debe apuntar a `/propiedades`.
7. La página debe reutilizar el layout base existente sin modificarlo.
8. Sin propiedades, la página debe mostrar estado vacío explícito.
9. Propiedades sin imagen deben mostrar placeholder visual (fondo + icono).
10. Textos largos deben truncarse con ellipsis.
11. El área debe formatearse con "m²" y separador de miles.
12. El precio debe formatearse como `$X,XXX.00`.
13. El estado debe renderizarse con `_badge_estado.html` existente.
14. La lógica de obtención debe vivir en `propiedades/service.py`.
15. El template debe vivir en `app/modules/propiedades/templates/`.

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
* `VTG-002`: Extiende CSS con clases nuevas para grid y cards. [visual][extension]
* `VTG-003`: No modifica iconografía existente. Si se requiere icono nuevo,
  tarea explícita con marcador `[visual][extension]`.
* `VTG-004`: Extiende `_card_propiedad.html`. [visual][extension]
* `VTG-005`: No modifica `base.html`, sidebar (salvo href), navbar.
* `VTG-006`: No rediseña páginas existentes.
* `VTG-007`: Cualquier modificación de token visual existente requiere
  marcador `[visual]` en `tasks.md`.

## Entidades o conceptos clave

* `Propiedad`: entidad persistida existente, fuente de datos de la card.
* `PropiedadOut`: DTO existente para transportar datos al template.
* `Card de propiedad`: componente visual extendido desde `_card_propiedad.html`.
* `Grid de propiedades`: contenedor CSS Grid responsive.
* `Estado vacío`: representación cuando `listar()` retorna lista vacía.

## Success Criteria obligatorios

Numerados como `SC-XXX`:

* `SC-001`: GET /propiedades retorna 200 con HTML y layout base.
* `SC-002`: La página muestra una card por cada propiedad persistida.
* `SC-003`: Cada card contiene los 8 campos visibles requeridos.
* `SC-004`: Grid respeta 3/2/1 columnas según breakpoint.
* `SC-005`: Enlace "Propiedades" del sidebar navega a `/propiedades`.
* `SC-006`: Cero propiedades muestra estado vacío sin cards.
* `SC-007`: Propiedad sin imagen muestra placeholder sin romper layout.
* `SC-008`: Textos largos truncados con ellipsis.
* `SC-009`: Tests unitarios cubren obtención de propiedades desde servicio.
* `SC-010`: Tests de integración cubren render HTML con datos reales y vacío.

## Edge cases obligatorios

* No existen propiedades persistidas.
* Propiedad sin imagen utilizable.
* Título o dirección con más de 100 caracteres.
* Propiedad con estado `mantenimiento` o `inactiva`.
* 50+ propiedades sin paginación.
* Área con valor grande (formato con separador de miles).
* Precio con decimales (formato moneda).
* Viewport exactamente 1024px (aplica tablet).
* Error de conexión a BD (retorna 500).

## Riesgos y dependencias

* Depende de spec 004 (propiedades base con modelo, repositorio y seed).
* El componente `_card_propiedad.html` actual puede requerir extensión
  significativa.
* Propiedades sin imagen pueden romper layout sin placeholder.
* Textos largos pueden desbordar cards sin ellipsis.
* El placeholder `propiedades/routes.py` debe ser reemplazado.

## Assumptions

* `propiedades.repository.listar()` ya existe y retorna todas las propiedades.
* `PropiedadOut` ya existe y es suficiente para el template.
* El seed de 10 propiedades contiene datos para todos los estados del catálogo.
* Los breakpoints responsive son 1023px y 767px (definidos en el sistema).
* No se requiere paginación, filtros ni búsqueda en esta spec.

## Entrega esperada

Genera `spec.md` para `006-pagina-propiedades-cards` en:

```
specs/006-pagina-propiedades-cards/spec.md
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

* Si el componente `_card_propiedad.html` existente se extiende o se crea uno
  nuevo. → Decidido: extender el existente.
* Si la imagen placeholder usa icono existente o nuevo. → Decidido: fondo +
  icono building-2 existente.
* Si el precio incluye símbolo `$` y decimales. → Decidido: `$1,500.00`.
* Si se requiere ordenamiento específico o el default del repositorio basta.
  → Preguntar si hay ambigüedad.

## Recordatorios Spec Kit

* Ejecutar hook `before_specify` (incluye `speckit.git.feature`).
* Crear branch `006-pagina-propiedades-cards`.
* Ubicación: `specs/006-pagina-propiedades-cards/` en raíz del repo.

## Salida esperada

```
Archivo actualizado: specs/006-pagina-propiedades-cards/spec.md
Feature: 006-pagina-propiedades-cards
Siguiente comando: /speckit.clarify @.opencode/prompts/006-pagina-propiedades-cards.clarify.prompt.md
```
