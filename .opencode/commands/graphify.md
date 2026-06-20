---
description: Ejecuta o consulta Graphify para el grafo de conocimiento del repo
agent: build
---

Usa Graphify para el repositorio actual.

Argumentos recibidos:

```text
$ARGUMENTS
```

Comportamiento esperado:

1. Si no hay argumentos, o el argumento es `.`, ejecuta `graphify .` desde la raíz del repo.
2. Si hay argumentos, ejecuta `graphify $ARGUMENTS` desde la raíz del repo.
3. Si `graphify` no existe en PATH, prueba `uv tool run graphifyy $ARGUMENTS`.
4. Si falla por falta de API key para docs, PDFs o imágenes, explica que el grafo de solo código no requiere key, pero la extracción semántica sí. No inventes credenciales.
5. Después de ejecutar, resume el resultado y menciona los artefactos relevantes: `graphify-out/graph.json`, `graphify-out/GRAPH_REPORT.md` y `graphify-out/graph.html`.
6. Para SDD, prioriza preguntas sobre trazabilidad entre `specs/`, `tasks.md`, `plan.md`, `AGENTS.md`, instrucciones de `.opencode/instructions/` e implementación en `app/`.
