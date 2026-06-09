---
name: 001-bootstrap-proyecto-clarify
description: >
  Identifica ambigüedades y guía la clarificación interactiva de la spec
  001-bootstrap-proyecto.
---

/speckit.clarify

Revisa la spec `001-bootstrap-proyecto`.

Identifica ambigüedades, decisiones implícitas o gaps que puedan aflorar durante
el plan o la implementación.

Áreas con foco especial:

- Breakpoints exactos del responsive para la sidebar colapsable.
- Comportamiento de `GET /health` cuando falla la base de datos:
  código HTTP y forma del JSON.
- Valores de las 3 tarjetas de métrica: label, número e icono.
- Alcance de los componentes estructurales:
  HTML + CSS completo o esqueletos con placeholders.
- Generación de los 13 SVG de Lucide:
  inline por el agente o descargados manualmente.
- Migración baseline:
  vacía o con extensión `pgcrypto` para `gen_random_uuid()`.
- Política de logging en `/health` y `/`.

## Modo interactivo — reglas obligatorias

1. Haz una sola pregunta a la vez. No lances todas las preguntas juntas. Espera
   mi respuesta antes de pasar a la siguiente.

2. Usa este formato para cada pregunta:

```text
Pregunta [N de TOTAL] — [tema corto]
─────────────────────────────────────
[Enunciado claro de la pregunta]

Por qué importa: [1 línea explicando el impacto de decidir mal]

A) [opción concreta con valor específico]
B) [opción concreta con valor específico] ← Recomendado
C) [opción concreta con valor específico]
D) Otro — escribe tu respuesta

> Responde con la letra (A, B, C o D) o escribe tu respuesta libre.
```

3. La opción recomendada siempre debe estar marcada con `← Recomendado`. Debe
   ser la opción más alineada con FastAPI, PostgreSQL local, Docker, `uv`,
   Python 3.13+ y la constitución del proyecto.

4. Si respondo `D` o escribo texto libre, acepta mi respuesta, confírmala en una
   línea y pasa a la siguiente pregunta.

5. Si respondo solo con una letra (`A`, `B` o `C`), confirma la elección en una
   línea con el valor concreto elegido y pasa inmediatamente a la siguiente
   pregunta.

6. Después de la última pregunta, muestra un resumen de todas las decisiones
   tomadas y actualiza `spec.md` añadiendo la sección `Clarificaciones` con las
   respuestas integradas.

7. Para preguntas binarias, usa este formato simplificado:

```text
Pregunta [N de TOTAL] — [tema corto]
─────────────────────────────────────
[Enunciado de la pregunta]

Por qué importa: [1 línea]

S) Sí ← Recomendado
N) No

> Responde S o N.
```

Empieza ahora con la Pregunta 1.