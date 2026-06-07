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

## Flujo de desarrollo y calidad

### Flujo SDD + TDD obligatorio

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

### Artefactos esperados por feature

Cada feature debe poder generar o mantener estos artefactos:

```text
spec.md
plan.md
tasks.md
test-plan.md
traceability.md
```

#### spec.md

Debe describir la funcionalidad desde el punto de vista del usuario y del negocio.

#### plan.md

Debe explicar la estrategia técnica de implementación.

#### tasks.md

Debe dividir el trabajo en tareas pequeñas, verificables y ordenadas.

#### test-plan.md

Debe definir los tests necesarios antes de la implementación.

Debe incluir:

- Tests unitarios.
- Tests de integración.
- Tests de endpoints.
- Tests de plantillas o respuestas HTML cuando aplique.
- Casos límite.
- Casos de error.

#### traceability.md

Debe mapear cada requisito con sus pruebas y archivos de implementación.

Ejemplo:

| Requisito | Criterio de aceptación | Test | Código | Estado |
|---|---|---|---|---|
| Crear propiedad | Usuario puede registrar una propiedad válida | `test_create_property_success` | `create_property/handler.py` | Passing |

### Reglas para agentes de IA

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

### Calidad y pruebas

Todas las pruebas deben poder ejecutarse localmente. Las pruebas deben ser deterministas y no depender de servicios externos innecesarios.

Reglas mínimas:

- Las pruebas unitarias deben ejecutarse con `pytest`.
- Las pruebas de integración deben usar `Testcontainers` cuando requieran PostgreSQL.
- La base de datos de pruebas debe estar aislada.
- Las pruebas deben ser claras, legibles y enfocadas en comportamiento.
- Se debe priorizar cobertura de reglas de negocio sobre cobertura superficial.
- Las pruebas de integración pueden usar PostgreSQL en Docker o mediante contenedores efímeros de Testcontainers.

### Base de datos y entorno local

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

## Gobernanza de la constitución

- Todo cambio a la constitución debe estar justificado.
- Los cambios deben registrarse en un historial.
- Las reglas de la constitución tienen prioridad sobre preferencias puntuales del agente.
- Si una instrucción entra en conflicto con la constitución, el agente debe advertirlo antes de continuar.

### Decisiones arquitectónicas

Cada decisión arquitectónica importante debe registrarse con:

| Campo | Descripción |
|---|---|
| Contexto | Situación o problema que motiva la decisión. |
| Decisión tomada | Solución adoptada. |
| Alternativas consideradas | Opciones evaluadas antes de decidir. |
| Consecuencias | Impacto esperado de la decisión. |
| Fecha | Momento en que se tomó la decisión. |
| Estado | Propuesto, aprobado, obsoleto o revisado. |

### Historial de cambios

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

**Version**: 1.0 | **Ratified**: 2026-06-07 | **Last Amended**: 2026-06-07
