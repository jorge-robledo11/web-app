---
name: 005-dashboard-datos-reales-spec
description: >
  Crea la spec 005-dashboard-datos-reales para reemplazar métricas mockeadas
  del dashboard principal por datos reales de propiedades persistidas.
spec_kit_command: "/speckit.specify"
usage: "/speckit.specify @.opencode/prompts/005-dashboard-datos-reales.spec.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

## Prompt para `speckit.specify`

**Nombre de la spec**: `005-dashboard-datos-reales`

## Contexto funcional actual

La home del proyecto Realtor ya existe y se renderiza correctamente, pero parte
de sus métricas principales todavía provienen de datos hardcodeados.

La spec previa de propiedades ya habilitó una base persistente con estados de
propiedad que permiten calcular métricas reales para:

* Propiedades disponibles.
* Propiedades rentadas.

Las métricas de ingresos y vencidos todavía no tienen un modelo de datos
suficiente para calcularse correctamente. Esta spec no debe inventar esos
cálculos.

## Objetivo

Reemplazar el mock actual del dashboard principal por datos reales de base de
datos para las métricas de propiedades disponibles y propiedades rentadas,
manteniendo la arquitectura vertical slice y el contrato de contexto de la home.

La spec debe conservar la estructura actual esperada por la vista principal y
limitarse a conectar las métricas ya representables con datos persistidos.

## Resultado esperado

Después de aplicar esta feature a nivel de especificación, el sistema debe
contar con una definición clara, verificable y trazable para:

* Obtener desde base de datos el conteo de propiedades disponibles.
* Obtener desde base de datos el conteo de propiedades rentadas.
* Reemplazar en la home los valores hardcodeados de esas métricas.
* Mantener el contrato de contexto actual de la vista principal.
* Mantener ingresos y vencidos como métricas no operativas explícitas.
* Mostrar el estado vacío del dashboard según el estado real de los datos.
* Evitar la creación de módulos, modelos o endpoints no necesarios.

## Alcance explícito

* INCLUYE: cálculo real de propiedades disponibles desde datos persistidos.
* INCLUYE: cálculo real de propiedades rentadas desde datos persistidos.
* INCLUYE: integración de esas métricas con el contexto server-rendered de la
  home.
* INCLUYE: conservación del orden y estructura de las métricas existentes en la
  vista.
* INCLUYE: conservación del orden y estructura de los accesos rápidos existentes.
* INCLUYE: estado vacío basado en datos reales de propiedades.
* INCLUYE: documentación explícita de que ingresos y vencidos quedan no
  operativos en esta spec.
* INCLUYE: tests de cálculo de métricas y render de la home con datos reales.

## Fuera de alcance

* NO INCLUYE: creación de módulos de rentas.
* NO INCLUYE: creación de módulos de pagos.
* NO INCLUYE: cálculo real de ingresos.
* NO INCLUYE: cálculo real de vencidos.
* NO INCLUYE: reporting ni analítica histórica.
* NO INCLUYE: rediseño visual.
* NO INCLUYE: cambios en tokens visuales, estilos, iconografía ni componentes
  compartidos.
* NO INCLUYE: nuevas dependencias.
* NO INCLUYE: endpoints adicionales salvo que exista valor funcional concreto
  para refresh parcial.

## Decisión arquitectónica esperada

La página principal server-rendered debe resolver sus datos mediante un servicio
de dashboard.

La spec debe definir que el dashboard obtiene las métricas reales desde el
repositorio o servicio correspondiente, respetando la arquitectura vertical slice
vigente.

Solo debe definirse un endpoint adicional si aporta valor funcional concreto
para refresh parcial. Si no hay un caso funcional claro, la spec debe declarar
explícitamente que no se requiere endpoint nuevo en esta feature.

## Historias de usuario

### P1 - Ver métricas reales de propiedades en la home

Como usuario del sistema inmobiliario, quiero que el dashboard principal muestre
la cantidad real de propiedades disponibles y rentadas para entender el estado
actual del inventario.

**Criterios de aceptación**:

* La home muestra propiedades disponibles calculadas desde base de datos.
* La home muestra propiedades rentadas calculadas desde base de datos.
* Los valores ya no provienen de constantes hardcodeadas.
* Los valores cambian cuando cambia el estado persistido de las propiedades.

### P2 - Mantener la estructura actual del dashboard

Como usuario del sistema, quiero que el dashboard conserve su estructura actual
para que la mejora de datos no cambie la experiencia visual ni la navegación.

**Criterios de aceptación**:

* Se conserva el contrato de contexto de métricas.
* Se conserva el orden de las métricas existentes.
* Se conserva el orden y estructura de accesos rápidos.
* No se rediseñan estilos, tokens ni componentes.

### P3 - Distinguir métricas reales de métricas pendientes

Como usuario o mantenedor del sistema, quiero que ingresos y vencidos queden
marcados como no operativos para evitar interpretar datos inventados como reales.

**Criterios de aceptación**:

* Ingresos no se calcula con datos inventados.
* Vencidos no se calcula con datos inventados.
* La spec declara qué información falta para calcular esas métricas en una
  feature futura.
* La home no presenta ingresos ni vencidos como métricas reales si no existen
  datos suficientes.

## Requisitos funcionales

La spec debe convertir estas reglas en requisitos funcionales numerados como
`FR-XXX`:

1. El sistema debe calcular la cantidad de propiedades con estado `disponible`
   usando datos persistidos.
2. El sistema debe calcular la cantidad de propiedades con estado `rentada`
   usando datos persistidos.
3. La home debe usar las métricas reales calculadas para propiedades disponibles
   y rentadas.
4. La home no debe depender de valores hardcodeados para propiedades disponibles
   ni rentadas.
5. El contrato de contexto de la home debe conservar la estructura esperada por
   el template actual.
6. El orden de las métricas debe permanecer estable respecto al dashboard
   existente.
7. El orden y estructura de accesos rápidos debe permanecer estable.
8. El estado vacío del dashboard debe derivarse del estado real de datos de
   propiedades.
9. Si no existen propiedades persistidas, la home debe representar ese estado de
   forma explícita.
10. Ingresos debe permanecer como métrica no operativa en esta spec.
11. Vencidos debe permanecer como métrica no operativa en esta spec.
12. El sistema no debe inventar cálculos de ingresos sin modelo de rentas,
    pagos o contratos.
13. El sistema no debe inventar cálculos de vencidos sin modelo de pagos,
    contratos o fechas de vencimiento.
14. El servicio de dashboard debe exponer una salida apta para el contexto de la
    home.
15. La lógica de cálculo debe vivir en la capa de servicio correspondiente y no
    en el template.
16. El acceso a datos debe permanecer separado de la lógica de presentación.
17. No debe crearse un endpoint adicional salvo que la spec justifique un valor
    funcional concreto para refresh parcial.

## Requisitos no funcionales y gobernanza vigente

Aplica la gobernanza vigente del proyecto definida en la constitución,
`AGENTS.md` y las instrucciones activas de OpenCode.

La spec no debe reescribir reglas globales ya definidas. Solo debe referenciar
que aplican cuando corresponda.

La spec debe declarar explícitamente:

* Aplica la arquitectura vertical slice vigente.
* Aplica la separación vigente entre rutas, servicios, repositorios y templates.
* Aplica la política vigente de calidad, typing, tests y herramientas.
* Aplica la gobernanza visual vigente.
* No se introducen dependencias nuevas.
* No se reabren decisiones técnicas heredadas de specs previas.

## Gobernanza visual

La spec debe incluir una sección de gobernanza visual con identificadores
`VTG-XXX`.

Debe declarar:

* `VTG-001`: Esta feature no modifica tokens visuales.
* `VTG-002`: Esta feature no modifica CSS.
* `VTG-003`: Esta feature no modifica iconografía.
* `VTG-004`: Esta feature no modifica componentes compartidos.
* `VTG-005`: Esta feature no rediseña la home.
* `VTG-006`: Si durante fases posteriores se toca un archivo visual protegido,
  debe quedar trazado según la regla de blindaje visual vigente.

## Entidades o conceptos clave

La spec debe describir los conceptos necesarios sin inventar modelos nuevos:

* `Propiedad`: entidad persistida existente usada como fuente de verdad para
  las métricas de inventario.
* `Estado de propiedad`: catálogo existente que permite distinguir disponibles
  y rentadas.
* `Métrica de dashboard`: elemento de contexto renderizado en la home.
* `Estado vacío`: representación del dashboard cuando no existen datos reales
  suficientes.
* `Métrica no operativa`: métrica visible o reservada cuya fuente real todavía
  no existe en el modelo de datos.

## Success Criteria obligatorios

La spec debe incluir como mínimo estos criterios de éxito numerados como
`SC-XXX`:

* `SC-001`: La home deja de usar datos hardcodeados para propiedades disponibles.
* `SC-002`: La home deja de usar datos hardcodeados para propiedades rentadas.
* `SC-003`: El conteo de propiedades disponibles refleja datos persistidos.
* `SC-004`: El conteo de propiedades rentadas refleja datos persistidos.
* `SC-005`: Al cambiar estados de propiedades en base de datos, las métricas
  renderizadas cambian acorde a esos datos.
* `SC-006`: El estado vacío responde al estado real de datos persistidos.
* `SC-007`: Ingresos queda documentado como métrica no operativa en esta spec.
* `SC-008`: Vencidos queda documentado como métrica no operativa en esta spec.
* `SC-009`: La estructura del contexto de la home permanece compatible con el
  template existente.
* `SC-010`: Los tests cubren el cálculo de métricas desde repositorio o servicio.
* `SC-011`: Los tests cubren el render de la home con valores reales.
* `SC-012`: La spec deja claramente trazado qué queda pendiente para una feature
  futura de ingresos y vencidos reales.

## Edge cases obligatorios

La spec debe listar estos edge cases:

* No existen propiedades persistidas.
* Existen propiedades, pero ninguna está disponible.
* Existen propiedades, pero ninguna está rentada.
* Existen propiedades con estados distintos a `disponible` y `rentada`.
* Existen propiedades en todos los estados del catálogo.
* La base de datos está disponible, pero el inventario está vacío.
* Ingresos no tiene modelo suficiente para cálculo real.
* Vencidos no tiene modelo suficiente para cálculo real.
* El contrato de contexto de la home recibe métricas reales y no operativas en
  el mismo arreglo o estructura.
* Se evalúa crear endpoint adicional sin caso funcional concreto.

## Riesgos y dependencias

La spec debe incluir una sección de riesgos y dependencias:

* Depende de la spec previa de propiedades persistidas.
* Depende de que los estados de propiedad existentes representen correctamente
  disponibilidad y renta.
* El cálculo de ingresos depende de modelos futuros de rentas, pagos o contratos.
* El cálculo de vencidos depende de modelos futuros de pagos, contratos o fechas
  de vencimiento.
* El principal riesgo es mezclar métricas reales con métricas no operativas sin
  diferenciarlas claramente.
* Otro riesgo es introducir endpoints o abstracciones no necesarias para una
  home server-rendered.

## Assumptions

La spec debe incluir assumptions explícitas cuando no haya ambigüedad material:

* Ya existe una fuente persistida de propiedades.
* Los estados `disponible` y `rentada` son suficientes para calcular las dos
  métricas reales incluidas.
* La home actual ya tiene un contrato de contexto que debe conservarse.
* Ingresos y vencidos no pueden calcularse correctamente en esta spec.
* No se necesita endpoint adicional si la home server-rendered puede resolver los
  datos en servidor.

## Entrega esperada

Genera o actualiza `spec.md` para `005-dashboard-datos-reales`.

La ruta canónica debe ser:

```text
specs/005-dashboard-datos-reales/spec.md
````

La carpeta `specs/` debe estar en la raíz del repositorio.

Está prohibido crear la spec bajo:

```text
.specify/specs/
```

## Estructura esperada de la spec

La spec debe seguir la estructura completa del template oficial de Spec Kit e
incluir como mínimo:

* User Scenarios & Testing.
* User Stories priorizadas como P1/P2/P3.
* Functional Requirements con identificadores `FR-XXX`.
* Gobernanza de tokens visuales con identificadores `VTG-XXX`.
* Key Entities o conceptos clave.
* Success Criteria con identificadores `SC-XXX`.
* Assumptions.
* Edge Cases.
* Riesgos y dependencias.
* Preguntas abiertas solo si faltan decisiones materiales.

## Reglas obligatorias

* No implementes código.
* No generes `plan.md`.
* No generes `tasks.md`.
* No modifiques archivos de aplicación.
* No cambies la constitución.
* Mantén todo el contenido en español.
* Respeta `AGENTS.md`.
* Respeta `.specify/memory/constitution.md`.
* Respeta `.opencode/instructions/*.instructions.md`.
* No uses Supabase.
* No uses `.yml`; usa siempre `.yaml`.
* No uses Bootstrap, Tailwind, CDN, webfonts, emojis ni iconos externos.
* No uses `pip`, `poetry`, `requirements.txt` ni `setup.py`.
* No reabras decisiones técnicas heredadas ya cerradas por la constitución.
* No inventes reglas nuevas que contradigan la constitución o este prompt.
* No cambies el alcance funcional de esta feature.
* No agregues modelos de rentas, pagos ni contratos.
* No inventes cálculos de ingresos ni vencidos.
* No rediseñes la UI.

## Preguntas interactivas

Si detectas ambigüedad material, pregunta antes de cerrar la spec.

Como mínimo, considera si hace falta preguntar:

* Si las métricas no operativas deben mostrarse con valor cero, marcador textual
  o estado explícito pendiente.
* Si el estado vacío se define como cero propiedades totales o como cero
  propiedades disponibles y rentadas.
* Si se espera refresh parcial del dashboard o basta con render server-side en
  cada request.
* Si el copy visible de ingresos y vencidos debe cambiar o solo la fuente de
  datos debe quedar documentada.
* Si hay datos actuales de propiedades suficientes en seed o tests para validar
  disponibles y rentadas.

## Recordatorios de proceso Spec Kit

* Antes de crear el directorio de la spec o el archivo `spec.md`, ejecutar el
  hook obligatorio `before_specify`.
* El hook `before_specify` incluye `speckit.git.feature`.
* El hook debe crear el branch de la feature y actualizar
  `.specify/feature.json`.
* La ubicación canónica es `specs/005-dashboard-datos-reales/` en la raíz del
  repositorio.
* `.specify/specs/` está reservado a infraestructura interna de Spec Kit.
* No actualizar todavía el marcador `SPECKIT START` en
  `.github/copilot-instructions.md`; eso corresponde a la fase de plan.

## Salida esperada

Al terminar, responde con:

```text
Archivo actualizado: specs/005-dashboard-datos-reales/spec.md
Feature: 005-dashboard-datos-reales
Siguiente comando recomendado: /speckit.clarify @.opencode/prompts/005-dashboard-datos-reales.clarify.prompt.md
```
