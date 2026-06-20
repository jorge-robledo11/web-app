---
name: graphify
description: >
  Usa el grafo de conocimiento del repo para responder preguntas de arquitectura,
  impacto, trazabilidad SDD, relaciones entre specs, módulos, documentación y código.
  Actívalo para /graphify, graphify, knowledge graph, mapa del repo, arquitectura,
  impacto de cambios o preguntas sobre cómo se conectan artefactos del proyecto.
license: MIT
---

# Graphify

Graphify es el vendor de contexto estructural del repo. Su trabajo es evitar que
el agente navegue archivos a ciegas cuando ya existe un grafo con relaciones
entre specs, documentación, código, módulos, contratos, tests y decisiones.

## Cuándo usarlo

Usa Graphify antes de leer archivos sueltos cuando la pregunta sea sobre:

- arquitectura del repo;
- impacto de un cambio;
- relación entre specs, `tasks.md`, `plan.md` e implementación;
- módulos centrales o dependencias;
- rutas entre conceptos, features o archivos;
- revisión SDD de cobertura y trazabilidad;
- explicación de un componente, spec, contrato o flujo.

## Comandos

- `/graphify .`: genera el grafo inicial.
- `/graphify update .`: actualiza el grafo después de cambios.
- `/graphify query "<pregunta>"`: consulta el grafo con lenguaje natural.
- `/graphify path "<origen>" "<destino>"`: busca relación entre dos nodos.
- `/graphify explain "<concepto>"`: explica un nodo o concepto.

También existen comandos de conveniencia:

- `/graphify-query <pregunta>`
- `/graphify-path <origen> <destino>`
- `/graphify-explain <concepto>`

## Reglas de uso

1. Si `graphify-out/graph.json` existe, consulta el grafo antes de abrir archivos
   para preguntas de codebase.
2. Para preguntas amplias, empieza con `graphify query`.
3. Para relaciones entre dos cosas, usa `graphify path`.
4. Para un concepto puntual, usa `graphify explain`.
5. Lee `graphify-out/GRAPH_REPORT.md` solo si necesitas una revisión amplia o la
   consulta no devuelve suficiente contexto.
6. Si existe `graphify-out/wiki/index.md`, úsalo para navegación general.
7. Si Graphify falla porque faltan API keys, reporta el error y ofrece opciones:
   configurar `GEMINI_API_KEY`, `GOOGLE_API_KEY`, `OPENAI_API_KEY`,
   `ANTHROPIC_API_KEY`, `DEEPSEEK_API_KEY` o `MOONSHOT_API_KEY`, o excluir docs e
   imágenes con `.graphifyignore` para un grafo solo de código.
8. No escribas ni sugieras API keys en archivos versionados.
9. Después de modificar código, intenta `graphify update .`; si falla por backend
   LLM, explica que el cambio de código puede quedar sin actualización semántica.

## SDD

En este proyecto, Graphify debe tratar `specs/`, `AGENTS.md`,
`.opencode/instructions/`, contratos, tests y `app/` como artefactos conectados.
Para una revisión SDD, buscar siempre:

- specs sin implementación clara;
- implementación sin spec relacionada;
- tareas sin archivo o módulo asociado;
- contratos no reflejados en rutas, schemas o tests;
- cambios de frontend que violen gobernanza visual;
- cambios de backend/database/tests que contradigan instrucciones del área.
