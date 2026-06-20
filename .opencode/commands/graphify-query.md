---
description: Consulta el grafo de Graphify con lenguaje natural
agent: build
---

Consulta el grafo de conocimiento del repo con esta pregunta:

```text
$ARGUMENTS
```

Ejecuta desde la raíz del repo:

```bash
graphify query "$ARGUMENTS"
```

Si `graphify-out/graph.json` no existe, indica que primero debe generarse con `/graphify .`.
Usa la salida para responder, sin leer archivos en bruto salvo que el resultado sea insuficiente.
