---
name: 004-propiedades-base-plan
description: >
Genera el plan técnico de la spec 004-propiedades-base.
spec_kit_command: "/speckit.plan"
usage: "/speckit.plan @.opencode/prompts/004-propiedades-base.plan.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

Genera `plan.md` para la feature activa `004-propiedades-base` usando el
workflow canónico de Spec Kit.

Usa la feature activa resuelta por Spec Kit. No asumas rutas fijas si el comando
ya puede resolverlas.

## Reglas

* Mantén todo en español.
* No implementes código.
* No generes `tasks.md`.
* Respeta la constitución, `AGENTS.md`, `spec.md`, clarificaciones y las
  instrucciones activas de `.opencode/instructions/*.instructions.md`.
* Respeta la gobernanza visual vigente definida por `002-blindar-tokens-visuales`.
* No agregues decisiones nuevas que no estén respaldadas por la spec o sus
  clarificaciones.
* No reabras decisiones técnicas ya cerradas por la constitución, la spec o las
  lecciones previas del proyecto.
* Si detectas una ambigüedad que bloquee el plan, pausa y pregunta antes de
  continuar.
* Registra cualquier desviación en `Complexity Tracking`.

## Alcance esperado

El plan debe cubrir, cuando aplique:

* Estructura técnica del dominio `propiedades`.
* Módulo vertical en `app/modules/propiedades/`.
* Modelo persistente de propiedades.
* Catálogo cerrado de estados de propiedad.
* Migración Alembic de estructura.
* Migración Alembic de seed inicial.
* Carga inicial idempotente de 10 propiedades de Miami.
* Reglas de upsert por clave de negocio.
* Reglas de timestamps server-side.
* Estrategia de repositorio y servicio.
* Estrategia de pruebas.
* Riesgos técnicos.
* Dependencias o restricciones detectadas.
* Validaciones de calidad.
* Reversibilidad de migraciones.
* Gobernanza visual aplicable, dejando claro que esta feature no toca UI.

## Decisiones técnicas cerradas

El plan debe tratar estas decisiones como no negociables:

* La entidad principal es `Propiedad`.
* El módulo vive en `app/modules/propiedades/`.
* El estado de propiedad debe modelarse como enum tipado.
* Los estados permitidos son:
  * `disponible`
  * `rentada`
  * `mantenimiento`
  * `inactiva`
* Está prohibido usar strings mágicos para estados.
* La identidad de negocio del seed es `titulo + direccion + ciudad`.
* El seed debe ser idempotente.
* La carga inicial debe dejar exactamente 10 propiedades de Miami.
* Re-ejecutar el seed no debe duplicar propiedades.
* Si una propiedad ya existe con la misma identidad de negocio, debe
  actualizarse en sitio.
* Las imágenes deben ser deterministas por identificador o semilla estable.
* Los timestamps deben gestionarse server-side.
* No se deben enviar `created_at` ni `updated_at` desde Python.
* Las migraciones deben tener `downgrade` real.
* Está prohibido usar `downgrade` como `pass`.
* Está prohibido usar `alembic stamp` como atajo ante fallos.
* Ante historial Alembic inconsistente, la recuperación esperada es reset de
  schema `public` y nuevo `alembic upgrade head`.

## Migraciones Alembic

El plan debe cubrir:

* Migración de estructura para crear la tabla de propiedades.
* Migración de seed para cargar las 10 propiedades iniciales.
* Creación del enum `estado_propiedad` exactamente una vez.
* Prevención de conflictos por doble creación de enum.
* Uso de `op.get_bind().execute(sa.text("..."), {...})` para SQL
  parametrizado en migraciones.
* Prohibición de `op.execute(sql, params)`.
* Uso de `CAST(:param AS uuid)` para casteos UUID.
* Prohibición de `:param::uuid` dentro de `sa.text`.
* Upsert con `ON CONFLICT (titulo, direccion, ciudad) DO UPDATE`.
* Downgrade real para estructura y seed.

## Pruebas y validaciones

El plan debe cubrir, cuando aplique:

* Pruebas del modelo de propiedades.
* Pruebas del catálogo cerrado de estados.
* Pruebas de reglas del seed.
* Pruebas de migraciones.
* Validación de que el seed contiene exactamente 10 propiedades de Miami.
* Validación de que el seed no duplica datos al ejecutarse varias veces.
* Validación de que la imagen es determinista.
* Validación de que no se envían timestamps desde Python.
* Validación de que no hay errores por mezcla de fechas naive y aware.
* Validación de reversibilidad `upgrade/downgrade`.

Comandos esperados de calidad:

```bash
uv run ruff check .
uv run mypy --strict app/modules/propiedades
uv run pytest app/modules/propiedades/tests -q
uv run alembic upgrade head
```

## Riesgos técnicos

El plan debe registrar riesgos y mitigaciones para:

* Doble creación del tipo enum `estado_propiedad`.
* Uso incorrecto de `op.execute(sql, params)`.
* Uso incorrecto de `:param::uuid`.
* Duplicación de propiedades al re-ejecutar el seed.
* Drift de imágenes entre ejecuciones.
* Errores por fechas naive vs aware.
* Downgrade incompleto.
* Historial Alembic inconsistente.
* Uso accidental de drivers no autorizados como `psycopg2` o `psycopg`.

## Gobernanza visual

Aunque esta feature no toca UI, el plan debe dejar explícito que:

* No modifica templates.
* No modifica CSS.
* No modifica componentes compartidos.
* No modifica iconografía.
* No modifica tokens visuales.
* No modifica dashboard.
* Si una fase posterior toca archivos visuales protegidos, debe quedar trazada
  en `tasks.md` según la gobernanza visual vigente.

## Contratos

Esta feature no debe generar contratos HTTP porque no incluye endpoints.

Si el plan genera archivos dentro de `contracts/*.yaml`, esos archivos DEBEN
contener YAML válido y parseable.

No escribas Markdown, texto narrativo libre ni bloques de código dentro de
archivos `.yaml`.

La estructura de cada contrato debe ser consistente, explícita y adecuada al tipo
de contrato generado por Spec Kit.

Si el contenido necesita explicación narrativa, contexto o notas de diseño, debe
ir en `plan.md`, `research.md` o `quickstart.md`, no en `contracts/*.yaml`.

Antes de finalizar, verifica que cada archivo `contracts/*.yaml` pueda abrirse
como YAML válido sin errores de sintaxis.

## Salida esperada

Al finalizar, informa:

* Ruta del `plan.md` generado o actualizado.
* Phase 0: `research.md`
* Phase 1: `data-model.md`, `quickstart.md`
* Contratos: `contracts/*.yaml` (si aplica)
* Si hubo preguntas interactivas.
* Si se registraron desviaciones en `Complexity Tracking`.
* Migraciones previstas.
* Módulos o archivos backend que podrían verse afectados.
* Confirmación de que no hay archivos visuales protegidos afectados.
* Siguiente comando recomendado.
