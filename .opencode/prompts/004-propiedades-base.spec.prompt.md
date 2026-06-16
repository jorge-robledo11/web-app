---
name: 004-propiedades-base-spec
description: >
Crea la spec 004-propiedades-base para habilitar la base persistente inicial
de propiedades inmobiliarias del proyecto Realtor.
spec_kit_command: "/speckit.specify"
usage: "/speckit.specify @.opencode/prompts/004-propiedades-base.spec.prompt.md"
execution_context: primary-build
model_policy: inherit-primary
---

## Prompt para `speckit.specify`

**Nombre de la spec**: `004-propiedades-base`

## Contexto de negocio

El dashboard actual muestra métricas en cero porque todavía no existe una fuente
persistente de datos de propiedades en el sistema.

Necesitamos habilitar una base inicial de propiedades inmobiliarias para que el
producto deje de operar con datos vacíos y permita validar reportes,
comportamiento funcional y futuras pantallas con casos realistas.

Esta feature es fundacional: habilita el dominio `propiedades` para que features
posteriores como listado, alta, búsqueda, reportes y dashboard real puedan
apoyarse en datos existentes.

## Resultado esperado

Después de aplicar esta feature a nivel de especificación, el sistema debe
contar con una definición clara, verificable y trazable para:

* Una base persistente de propiedades con atributos de negocio relevantes para
  alquiler residencial.
* Un conjunto inicial de 10 propiedades de prueba ubicadas en Miami, USA.
* Una carga inicial repetible, idempotente y sin duplicados.
* Estados operativos de propiedad controlados por catálogo cerrado.
* Evoluciones de datos reversibles y seguras frente a zonas horarias.
* Reglas explícitas para evitar errores conocidos en migraciones, enums,
  timestamps, UUIDs y seeds.
* Criterios de éxito medibles que permitan a `speckit.plan` y `speckit.tasks`
  continuar sin reabrir decisiones ya cerradas.

## Alcance explícito

* INCLUYE: definición de la entidad de propiedades.
* INCLUYE: estructura persistente de propiedades.
* INCLUYE: catálogo cerrado de estados de propiedad.
* INCLUYE: carga inicial idempotente de 10 propiedades de Miami con imágenes
  asociadas.
* INCLUYE: validaciones de calidad, reversibilidad y consistencia de datos.
* INCLUYE: reglas de migración y seed derivadas de la constitución y de
  lecciones aprendidas del proyecto.
* NO INCLUYE: endpoints HTTP.
* NO INCLUYE: vistas, templates ni cambios visibles en el dashboard.
* NO INCLUYE: rediseño visual.
* NO MODIFICA: tokens visuales, paleta, tipografía, espaciados, radios, sombras,
  layout base ni componentes compartidos.

## Reglas de negocio obligatorias

La spec debe convertir estas reglas en requisitos funcionales numerados como
`FR-XXX`:

1. Una propiedad debe tener como mínimo:
   * Título.
   * Dirección.
   * Ciudad.
   * Precio mensual.
   * Habitaciones.
   * Baños.
   * Área.
   * Estado.
   * Imagen.
   * Marca temporal de creación.
   * Marca temporal de actualización.
2. El estado de una propiedad solo puede tomar estos valores:
   * `disponible`;
   * `rentada`;
   * `mantenimiento`;
   * `inactiva`.
3. Cualquier estado fuera del catálogo permitido debe rechazarse.
4. La identidad de negocio del seed debe ser la combinación:
   `título + dirección + ciudad`.
5. Re-ejecutar la carga inicial nunca debe duplicar propiedades.
6. Si una propiedad ya existe con la misma identidad de negocio, debe
   actualizarse en sitio.
7. Las marcas temporales deben ser gestionadas por la base de datos.
8. La carga inicial nunca debe enviar `created_at` ni `updated_at` desde Python.
9. Cada propiedad inicial debe tener una imagen determinista por identificador o
   semilla visual estable.
10. Las evoluciones deben ser aplicables y reversibles en entorno limpio.
11. La actualización completa no debe producir errores por mezcla de fechas con
    y sin zona horaria.

## Restricciones técnicas heredadas de la constitución

Estas reglas vienen de `.specify/memory/constitution.md`, `AGENTS.md`,
`.opencode/instructions/*.instructions.md` y lecciones previas del repositorio.

Deben quedar enumeradas como requisitos adicionales, preferiblemente bajo una
categoría de requisitos no funcionales o gobernanza técnica, para que
`speckit.plan` y `speckit.tasks` no las reabran ni propongan alternativas.

### Migraciones de base de datos

* Cada tipo enumerado del dominio se crea exactamente una vez por evolución de
  estructura.
* El enum debe declararse en la columna y materializarse por el DDL de creación
  de tabla.
* Está prohibido invocar la creación explícita del tipo en paralelo a su
  declaración en columna sin desactivar la creación implícita.
* El SQL parametrizado dentro de migraciones debe ejecutarse usando la conexión
  enlazada:
  `op.get_bind().execute(sa.text("..."), {...})`.
* Está prohibido usar `op.execute(sql, params)`.
* Los casteos a UUID en SQL parametrizado deben usar `CAST(:param AS uuid)`.
* Está prohibido usar la forma `:param::uuid` dentro de `sa.text`.
* La plantilla `alembic/script.py.mako` debe estar versionada antes de generar
  nuevas revisiones.
* Está prohibido usar `alembic stamp` como atajo ante fallos.
* Ante un estado inconsistente del historial de evoluciones, la recuperación
  obligatoria es reiniciar el esquema:
  `DROP SCHEMA public CASCADE` + `CREATE SCHEMA public`
  y reaplicar `alembic upgrade head` desde base limpia.
* Las migraciones deben ser reversibles reales.
* `downgrade` nunca puede ser `pass`.
* El seed debe ser idempotente por clave de negocio usando
  `ON CONFLICT (...) DO UPDATE`.
* Los timestamps deben ser server-side.
* No se deben enviar `created_at` ni `updated_at` desde Python en migraciones ni
  seeds.

### Dominio y código

* Usar SQLAlchemy 2.x async.
* Usar `Mapped[...]`, `mapped_column` y `AsyncSession`.
* Está prohibido el estilo legacy de SQLAlchemy:
  `Column` en clase, `Query` y sesiones sync.
* Los estados de dominio deben modelarse como enum tipado.
* Usar `StrEnum` y `Enum` de SQLAlchemy.
* Están prohibidos los strings mágicos para estados de dominio.
* Usar Pydantic v2.
* Los DTOs deben usar `model_config = ConfigDict(frozen=True)`.
* Respetar Vertical Slice Architecture.
* El módulo debe vivir en `app/modules/propiedades/`.
* La estructura esperada del slice debe considerar:
  `routes.py`, `schemas.py`, `models.py`, `repository.py`, `service.py`,
  `templates/` y `tests/`, aunque esta spec no debe implementar código.
* La lógica de negocio debe vivir solo en `service.py`.
* `routes.py` debe mantenerse delgado.
* `repository.py` debe limitarse al acceso a datos.
* No se deben exponer entidades SQLAlchemy en respuestas HTTP.
* Las funciones de I/O deben ser async.
* `def` sync solo debe usarse para cómputo puro.

### Calidad

* Ruff debe finalizar sin hallazgos.
* `mypy --strict` no debe reportar errores en `app/modules/propiedades`.
* Las pruebas deben usar `pytest`, `pytest-asyncio` y `httpx.AsyncClient` cuando
  aplique.

### Herramientas autorizadas

* Cualquier script auxiliar de mantenimiento de base de datos debe usar
  `asyncpg` vía `create_async_engine`.
* Está prohibido depender de `psycopg2` o `psycopg`.

## Gobernanza visual

La spec debe incluir una sección de gobernanza visual, aunque la feature no
modifique frontend.

Debe declarar explícitamente:

* Esta feature no modifica tokens visuales.
* Esta feature no modifica templates.
* Esta feature no modifica CSS.
* Esta feature no modifica iconografía.
* Esta feature no modifica componentes compartidos.
* Si en fases posteriores se toca algún archivo visual protegido, deberá quedar
  trazado en `tasks.md` según la regla de blindaje visual vigente.

## Success Criteria obligatorios

La spec debe incluir como mínimo estos criterios de éxito numerados como
`SC-XXX`:

* `alembic upgrade head` sobre `public` recién creado finaliza en verde sin
  intervención manual y sin uso de `stamp`.
* La carga inicial deja exactamente 10 propiedades de Miami.
* La carga inicial mantiene exactamente 10 propiedades después de dos
  ejecuciones consecutivas.
* El 100% de las propiedades iniciales tiene estado dentro del catálogo
  permitido.
* El 100% de las propiedades iniciales tiene una imagen asociada con semilla
  estable.
* El ciclo completo `upgrade/downgrade` finaliza con éxito en el 100% de las
  ejecuciones de validación.
* La actualización completa de base de datos no reporta errores por fechas naive
  vs aware.
* `mypy --strict` en el módulo de propiedades no reporta errores.
* Ningún script auxiliar de mantenimiento usa `psycopg2` ni `psycopg`.
* La materialización del catálogo de estados no produce conflictos por
  declaración duplicada al aplicar la evolución de estructura.

## Edge cases obligatorios

La spec debe listar estos edge cases:

* Intentar registrar una propiedad con estado fuera del catálogo.
* Ejecutar la carga inicial varias veces en entornos con datos parcialmente
  presentes.
* Aplicar la actualización completa en un entorno donde el esquema previo quedó
  en estado inconsistente.
* Alembic reporta una revisión que no existe en `alembic/versions/`.
* La mitigación ante revisión inexistente debe ser reset de schema `public` +
  `upgrade head`, nunca `stamp`.
* `CREATE TYPE` choca con un enum preexistente.
* La mitigación de conflicto de enum debe ser crear el enum una sola vez vía DDL
  implícito de la tabla.
* Inserciones con SQL parametrizado usando `:param::uuid`.
* La mitigación de UUID debe ser `CAST(:param AS uuid)`.
* Carga parcial del seed.
* La mitigación de carga parcial debe ser upsert por clave compuesta de negocio.
* Ejecución del seed dos veces consecutivas.
* La mitigación debe ser cardinalidad estable y actualización in-place.
* Detección de diferencias de zona horaria entre datos generados por aplicación
  y datos gestionados por la base de datos.

## Entrega esperada

Genera o actualiza `spec.md` para `004-propiedades-base`.

La ruta canónica debe ser:

```text
specs/004-propiedades-base/spec.md
```

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
* Key Entities.
* Success Criteria con identificadores `SC-XXX`.
* Assumptions.
* Edge Cases.
* Trazabilidad de reglas de negocio y restricciones técnicas.
* Checklist de calidad en `checklists/requirements.md`.

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
* No agregues endpoints, vistas ni cambios visibles en dashboard.

## Preguntas interactivas

Si detectas ambigüedad material, pregunta antes de cerrar la spec.

Como mínimo, considera si hace falta preguntar:

* Si las 10 propiedades iniciales deben tener datos concretos definidos por el
  usuario o pueden generarse como dataset realista de prueba.
* Si el precio mensual debe expresarse como entero en centavos, decimal o tipo
  monetario.
* Si el área debe almacenarse en pies cuadrados, metros cuadrados o ambos.
* Si la imagen debe ser una URL externa, una ruta local vendoreada o una semilla
  para generar URL determinista.
* Si la ciudad debe quedar fija como `Miami` o si debe contemplarse expansión
  futura a otras ciudades.
* Si el estado inicial de las 10 propiedades debe distribuirse entre los cuatro
  estados o concentrarse en `disponible`.

## Recordatorios de proceso Spec Kit

* Antes de crear el directorio de la spec o el archivo `spec.md`, ejecutar el
  hook obligatorio `before_specify`.
* El hook `before_specify` incluye `speckit.git.feature`.
* El hook debe crear el branch de la feature y actualizar
  `.specify/feature.json`.
* La ubicación canónica es `specs/004-propiedades-base/` en la raíz del
  repositorio.
* `.specify/specs/` está reservado a infraestructura interna de Spec Kit.
* No actualizar todavía el marcador `SPECKIT START` en
  `.github/copilot-instructions.md`; eso corresponde a la fase de plan.

## Salida esperada

Al terminar, responde con:

```text
Archivo actualizado: specs/004-propiedades-base/spec.md
Feature: 004-propiedades-base
Siguiente comando recomendado: /speckit.clarify @.opencode/prompts/004-propiedades-base.clarify.prompt.md
```
