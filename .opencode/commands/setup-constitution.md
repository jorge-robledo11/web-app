---
name: setup-constitution
description: Crea o modifica el archivo constitution.md del proyecto Realtor
handoffs:
  - label: Build Specification
    agent: speckit.specify
    prompt: Implement the feature specification based on the updated constitution. I want to build...
---

## Pre-Execution Checks

**Check for extension hooks (before constitution update)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_constitution` key
- If the YAML cannot be parsed or is invalid, skip hook checking silently and continue normally
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- For each executable hook, output the following based on its `optional` flag:
  - **Optional hook** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Pre-Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```
  - **Mandatory hook** (`optional: false`):
    ```
    ## Extension Hooks

    **Automatic Pre-Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}

    Wait for the result of the hook command before proceeding to the Outline.
    ```
- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

## Outline

You are filling the template at `.specify/memory/constitution.md` with the Realtor project constitution. You MUST replace each placeholder token while preserving the template's Markdown heading hierarchy (H1 → H2 → H3). Do NOT overwrite the file with a completely different structure.

**Note**: If `.specify/memory/constitution.md` does not exist yet, copy `.specify/templates/constitution-template.md` to `.specify/memory/constitution.md` first.

Follow this execution flow:

1. Load the template at `.specify/memory/constitution.md`.

2. Apply the following replacements. The source content for each placeholder is found in the Realtor constitution below (between `<!-- CONSTITUTION_START -->` and `<!-- CONSTITUTION_END -->`).

### a) Metadata placeholders — replace directly

| Placeholder | Value |
|---|---|
| `[PROJECT_NAME]` | `Realtor` |
| `[CONSTITUTION_VERSION]` | `1.0` |
| `[RATIFICATION_DATE]` | `2026-06-07` |
| `[LAST_AMENDED_DATE]` | `2026-06-07` |

### b) Heading translations — replace the template's English headings

| Template line | Replace with |
|---|---|
| `# [PROJECT_NAME] Constitution` | `# Constitución del Proyecto Realtor` |
| `## Core Principles` | `## Principios fundamentales` |
| `## [SECTION_2_NAME]` | `## Reglas tecnológicas` |
| `## [SECTION_3_NAME]` | `## Flujo de desarrollo y calidad` |
| `## Governance` | `## Gobernanza de la constitución` |

### c) Insert sections before `## Principios fundamentales`

Between the title line (`# Constitución del Proyecto Realtor`) and `## Principios fundamentales`, insert:

- `## Propósito` — copy the entire `## Propósito` section from the Realtor constitution below (heading + paragraph).
- `## Contexto del proyecto` — copy the entire `## Contexto del proyecto` section from the Realtor constitution below (heading + paragraph).

### d) Principle placeholders — fill from Realtor constitution

| Placeholder | Source location in Realtor constitution |
|---|---|
| `[PRINCIPLE_1_NAME]` | `### Spec-Driven Development` (heading text) |
| `[PRINCIPLE_1_DESCRIPTION]` | All content under `### Spec-Driven Development` (bullet list + closing sentence) |
| `[PRINCIPLE_2_NAME]` | `### Test-Driven Development` (heading text) |
| `[PRINCIPLE_2_DESCRIPTION]` | All content under `### Test-Driven Development` (numbered cycle + 5 mandatory rules) |
| `[PRINCIPLE_3_NAME]` | `### Vertical Slice Architecture` (heading text) |
| `[PRINCIPLE_3_DESCRIPTION]` | All content under `### Vertical Slice Architecture` (explanation + example tree + slice components list) |
| `[PRINCIPLE_4_NAME]` | `### Monolito modular` (heading text) |
| `[PRINCIPLE_4_DESCRIPTION]` | All content under `### Monolito modular` (explanation + 4 modularity rules) |

**Realtor has 4 principles, not 5.** Remove the entire 5th principle slot: the `### [PRINCIPLE_5_NAME]` line, its `[PRINCIPLE_5_DESCRIPTION]` line, and any adjacent HTML comment lines.

### e) Section content placeholders

| Placeholder | Source from Realtor constitution |
|---|---|
| `[SECTION_2_NAME]` | Already replaced via heading translation — skip |
| `[SECTION_2_CONTENT]` | Copy all `###` sub-sections under `## Reglas tecnológicas`: FastAPI, Jinja2 + HTMX, SQLAlchemy async + PostgreSQL, uv, Scalar. Each kept as `###` with their full text. |
| `[SECTION_3_NAME]` | Already replaced via heading translation — skip |
| `[SECTION_3_CONTENT]` | Copy the following sections as `###` sub-headings with their full content: `## Flujo SDD + TDD obligatorio`, `## Artefactos esperados por feature` (demote its nested `###` sub-sections for spec.md/plan.md/etc. to `####`), `## Reglas para agentes de IA`, `## Calidad y pruebas`, `## Base de datos y entorno local`. |

### f) Governance placeholder

| Placeholder | Source from Realtor constitution |
|---|---|
| `[GOVERNANCE_RULES]` | Copy the bullet points under `## Gobernanza de la constitución` (the 5 rules). Then append as `###` sub-sections: `### Decisiones arquitectónicas` (table definition) and `### Historial de cambios` (version table). Both taken from their respective `##` sections in the Realtor constitution. |

### g) Remove leftover HTML comments

Delete all lines matching `<!-- Example: ... -->` and any other HTML comments that were part of the original template scaffolding.

3. After applying all replacements, validate:
   - No `[BRACKET_PLACEHOLDER]` tokens remain in the file.
   - The metadata line reads exactly: `**Version**: 1.0 | **Ratified**: 2026-06-07 | **Last Amended**: 2026-06-07`.
   - All headings respect H1 → H2 → H3 hierarchy (no skipped levels).

4. Write the completed constitution to `.specify/memory/constitution.md`.

5. Output a summary:
   - File updated: `.specify/memory/constitution.md`
   - Version: `1.0`
   - Suggested commit: `docs: set up Realtor project constitution v1.0`

Reference — full Realtor constitution (source for all replacements above):

<!-- CONSTITUTION_START -->

# Constitución del Proyecto Realtor

## Propósito

Esta constitución define las reglas obligatorias para el desarrollo del proyecto **Realtor**, un monolito web construido con Python. Su objetivo es guiar a agentes de IA y a personas desarrolladoras para entregar funcionalidades de forma consistente, verificable y alineada con la arquitectura del sistema.

## Contexto del proyecto

Realtor es una aplicación inmobiliaria construida con un flujo de trabajo guiado por especificaciones, pruebas y arquitectura por funcionalidades. El proyecto prioriza claridad, trazabilidad, mantenibilidad y evolución incremental.

## Stack tecnológico

El stack principal del proyecto es el siguiente:

- Python.
- FastAPI.
- Jinja2.
- HTMX.
- SQLAlchemy async.
- PostgreSQL.
- Docker o Docker Compose para ejecutar la base de datos local.
- uv para gestión del proyecto, dependencias, entorno virtual y ejecución de comandos.
- Scalar como documentación interactiva de la API.
- pytest para pruebas unitarias.
- Testcontainers para pruebas de integración.

La base de datos no usará Supabase. PostgreSQL debe ejecutarse localmente mediante Docker o Docker Compose.

## Principios fundamentales

### Spec-Driven Development

Todo desarrollo debe comenzar desde una especificación clara. Ninguna funcionalidad debe implementarse sin antes definir:

- Problema a resolver.
- Objetivo funcional.
- Alcance.
- Reglas de negocio.
- Criterios de aceptación.
- Casos límite.
- Comportamiento esperado.
- Comportamiento fuera de alcance.

La especificación es la fuente de verdad para agentes de IA y personas desarrolladoras.

### Test-Driven Development

El proyecto debe seguir un ciclo TDD estricto:

1. Red: escribir primero una prueba que falle por el motivo correcto.
2. Green: implementar el código mínimo necesario para que la prueba pase.
3. Refactor: mejorar el diseño sin cambiar el comportamiento observable.

Reglas obligatorias:

- No se debe escribir código de producción antes de tener una prueba asociada.
- Toda regla de negocio debe estar cubierta por pruebas.
- Toda corrección de bug debe comenzar con una prueba que reproduzca el fallo.
- No se debe marcar una tarea como terminada si sus pruebas no pasan.
- La refactorización solo puede hacerse con la suite de pruebas en verde.

### Vertical Slice Architecture

El proyecto debe organizarse por **features** o **casos de uso**, no por capas técnicas globales excesivas. Cada slice debe contener lo necesario para entregar una funcionalidad completa.

Ejemplo orientativo:

```text
src/
  realtor/
    features/
      properties/
        create_property/
          endpoint.py
          schemas.py
          handler.py
          tests.py
        list_properties/
          endpoint.py
          schemas.py
          handler.py
          tests.py
    shared/
      database/
      templates/
      auth/
      config/
```

Cada slice puede incluir:

- Endpoint o ruta.
- Schemas o DTOs.
- Handler o caso de uso.
- Validaciones.
- Acceso a datos, si aplica.
- Plantillas Jinja2, si aplica.
- Pruebas relacionadas.

### Monolito modular

El sistema debe mantenerse como un monolito con límites internos claros. No se deben crear microservicios salvo que una decisión arquitectónica futura lo justifique explícitamente.

La modularidad debe lograrse mediante:

- Features bien delimitadas.
- Código compartido mínimo.
- Separación clara entre lógica de negocio, infraestructura y presentación.
- Evitar dependencias circulares entre módulos.

## Reglas tecnológicas

### FastAPI

FastAPI será el framework principal de la aplicación web. Debe usarse para:

- Definir rutas HTTP.
- Gestionar dependencias.
- Validar entradas cuando aplique.
- Integrar respuestas HTML y JSON según el caso de uso.

### Jinja2 + HTMX

La interfaz será principalmente server-rendered usando Jinja2. HTMX debe usarse para interacciones dinámicas sin convertir la aplicación en una SPA.

Reglas:

- Preferir HTML renderizado desde el servidor.
- Usar HTMX para interacciones parciales.
- Evitar complejidad innecesaria en JavaScript.
- Mantener las plantillas cercanas al slice cuando sean específicas de una funcionalidad.

### SQLAlchemy async + PostgreSQL

El acceso a datos debe usar SQLAlchemy en modo async. PostgreSQL será la base de datos principal.

Reglas:

- No usar Supabase como base de datos del proyecto.
- La base de datos local debe levantarse con Docker.
- Las migraciones deben gestionarse de forma explícita, preferiblemente con Alembic si el proyecto lo requiere.
- Las sesiones de base de datos deben manejarse mediante dependencias controladas.

### uv

`uv` será la herramienta estándar para:

- Inicializar el proyecto.
- Gestionar dependencias.
- Crear y sincronizar el entorno virtual.
- Ejecutar comandos.
- Mantener el lockfile.

Comandos esperados:

```bash
uv sync
uv run pytest
uv run fastapi dev
```

Si se definen scripts del proyecto, deben documentarse claramente.

### Scalar

Scalar será la documentación interactiva de la API para el proyecto. La documentación debe mantenerse alineada con los endpoints reales de FastAPI y actualizarse cuando cambie la superficie pública de la API.

## Flujo SDD + TDD obligatorio

Cada nueva funcionalidad debe seguir este orden:

1. Crear o actualizar la especificación.
2. Definir criterios de aceptación.
3. Usar `/speckit.clarify` cuando existan ambigüedades o decisiones sin resolver.
4. Crear plan de pruebas.
5. Ejecutar `/speckit.checklist` después del plan para validar completitud y consistencia.
6. Crear plan técnico.
7. Crear tareas pequeñas y verificables.
8. Ejecutar `/speckit.analyze` antes de implementar para detectar inconsistencias entre especificación, plan y tareas.
9. Escribir una prueba fallida.
10. Implementar el mínimo código necesario.
11. Ejecutar pruebas.
12. Refactorizar.
13. Actualizar documentación si aplica.
14. Registrar trazabilidad entre especificación, tests y código.

No se debe permitir que el agente de IA implemente directamente sin pasar por especificación y pruebas.

## Artefactos esperados por feature

Cada feature debe poder generar o mantener estos artefactos:

```text
spec.md
plan.md
tasks.md
test-plan.md
traceability.md
```

### spec.md

Debe describir la funcionalidad desde el punto de vista del usuario y del negocio.

### plan.md

Debe explicar la estrategia técnica de implementación.

### tasks.md

Debe dividir el trabajo en tareas pequeñas, verificables y ordenadas.

### test-plan.md

Debe definir los tests necesarios antes de la implementación.

Debe incluir:

- Tests unitarios.
- Tests de integración.
- Tests de endpoints.
- Tests de plantillas o respuestas HTML cuando aplique.
- Casos límite.
- Casos de error.

### traceability.md

Debe mapear cada requisito con sus pruebas y archivos de implementación.

Ejemplo:

| Requisito | Criterio de aceptación | Test | Código | Estado |
|---|---|---|---|---|
| Crear propiedad | Usuario puede registrar una propiedad válida | `test_create_property_success` | `create_property/handler.py` | Passing |

## Reglas para agentes de IA

El agente debe:

- Leer la especificación antes de modificar código.
- Confirmar el alcance antes de implementar.
- Crear o actualizar pruebas antes del código de producción.
- Mantener los cambios pequeños.
- Trabajar por vertical slices.
- Evitar abstracciones prematuras.
- No crear capas globales innecesarias.
- No introducir dependencias sin justificación.
- No modificar partes no relacionadas del sistema.
- No eliminar pruebas para hacer pasar la suite.
- No declarar una tarea completa sin pruebas verdes.
- Usar `/speckit.clarify`, `/speckit.checklist` y `/speckit.analyze` cuando corresponda dentro del flujo.

El agente debe rechazar o pausar una implementación si:

- No existe especificación.
- No hay criterios de aceptación.
- No hay plan de pruebas.
- La petición contradice la constitución.
- Requiere una decisión técnica no documentada.

## Calidad y pruebas

Todas las pruebas deben poder ejecutarse localmente. Las pruebas deben ser deterministas y no depender de servicios externos innecesarios.

Reglas mínimas:

- Las pruebas unitarias deben ejecutarse con `pytest`.
- Las pruebas de integración deben usar `Testcontainers` cuando requieran PostgreSQL.
- La base de datos de pruebas debe estar aislada.
- Las pruebas deben ser claras, legibles y enfocadas en comportamiento.
- Se debe priorizar cobertura de reglas de negocio sobre cobertura superficial.
- Las pruebas de integración pueden usar PostgreSQL en Docker o mediante contenedores efímeros de Testcontainers.

## Base de datos y entorno local

El entorno local debe poder levantarse de forma reproducible.

Debe existir una estrategia para:

- Levantar PostgreSQL con Docker.
- Configurar variables de entorno.
- Ejecutar migraciones.
- Correr pruebas.
- Reiniciar el entorno local si es necesario.

Ejemplo esperado:

```text
docker-compose.yml
.env.example
```

La constitución debe indicar que `.env` nunca debe versionarse con secretos reales.

## Decisiones arquitectónicas

Cada decisión arquitectónica importante debe registrarse con:

| Campo | Descripción |
|---|---|
| Contexto | Situación o problema que motiva la decisión. |
| Decisión tomada | Solución adoptada. |
| Alternativas consideradas | Opciones evaluadas antes de decidir. |
| Consecuencias | Impacto esperado de la decisión. |
| Fecha | Momento en que se tomó la decisión. |
| Estado | Propuesto, aprobado, obsoleto o revisado. |

## Gobernanza de la constitución

- Versión inicial: `1.0`.
- Todo cambio a la constitución debe estar justificado.
- Los cambios deben registrarse en un historial.
- Las reglas de la constitución tienen prioridad sobre preferencias puntuales del agente.
- Si una instrucción entra en conflicto con la constitución, el agente debe advertirlo antes de continuar.

## Historial de cambios

| Versión | Cambios |
|---|---|
| v1.0 | Constitución inicial del proyecto Realtor. |
| v1.0 | Definición del flujo SDD + TDD. |
| v1.0 | Adopción de Vertical Slice Architecture. |
| v1.0 | Uso de FastAPI, Jinja2, HTMX, SQLAlchemy async y PostgreSQL. |
| v1.0 | Uso de Scalar como documentación de API. |
| v1.0 | Uso de pytest para unit tests y Testcontainers para integración. |
| v1.0 | Uso de uv como gestor principal del proyecto. |
| v1.0 | Integración de comandos opcionales de Spec Kit dentro del workflow: `clarify`, `checklist` y `analyze`. |

<!-- CONSTITUTION_END -->

## Post-Execution Checks

**Check for extension hooks (after constitution update)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.after_constitution` key
- If the YAML cannot be parsed or is invalid, skip hook checking silently and continue normally
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- For each executable hook, output the following based on its `optional` flag:
  - **Optional hook** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```
  - **Mandatory hook** (`optional: false`):
    ```
    ## Extension Hooks

    **Automatic Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}
    ```
- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently