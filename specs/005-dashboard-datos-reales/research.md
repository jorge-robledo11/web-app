# Research: Dashboard con datos reales

**Feature**: 005-dashboard-datos-reales
**Phase**: 0 — Research
**Date**: 2026-06-15

## Decisiones técnicas investigadas

### 1. Estrategia de acceso a datos entre módulos

**Decisión**: Agregar `contar_por_estado()` y `contar_total()` al repositorio de
`propiedades` e invocarlas desde el repositorio del dashboard.

**Alternativas consideradas**:
- Consulta directa a la tabla `propiedades` desde el repositorio de dashboard:
  rechazada por acoplamiento al esquema interno de otro módulo. Si `Propiedad`
  cambia su tabla, el dashboard se rompe.
- Servicio de dashboard llama directamente al repo de propiedades: rechazada,
  viola la separación de capas (el servicio no debe conocer repositorios de otros
  módulos).
- Consulta SQL cruda con `sa.text`: rechazada, pierde type safety y validación
  del ORM.

**Fundamento**: El repositorio de dashboard actúa como fachada que invoca
funciones públicas del repositorio de `propiedades`. Esto respeta NFR-ARCH-004
(sin duplicar modelos) y la decisión de clarificación (acceso vía
`contar_por_estado()`). Las funciones en el repo de propiedades son reutilizables
por futuras features sin exposición de detalles internos.

### 2. Omisión de tendencia en métricas reales

**Decisión**: Omitir el campo `tendencia` en las métricas de disponibles y
rentadas.

**Alternativas consideradas**:
- Mostrar tendencia con placeholder neutro (`"up"`, `"—"`): rechazada, parece
  dato real y genera expectativa falsa.
- Calcular tendencia comparando con snapshot anterior: rechazada, requiere
  almacenar histórico (fuera de alcance).
- Mostrar flecha según si el valor creció o decreció: rechazada, no hay dato
  previo para comparar.

**Fundamento**: El componente `_tarjeta_metrica.html` ya soporta `tendencia` como
campo opcional (`{% if tendencia %}`). Omitirlo no rompe el template y evita
presentar datos sin respaldo histórico. En una feature futura con snapshot de
métricas, se podrá agregar tendencia real.

### 3. Representación de métricas no operativas

**Decisión**: Hardcodear ingresos y vencidos con `valor: 0` y un campo adicional
`marcador: "No disponible"` en el dict de la métrica.

**Alternativas consideradas**:
- Mostrar `"—"` en lugar de número: rechazada, el template espera `valor` como
  entero para formatear con `{:,}`.
- Ocultar ingresos y vencidos del dashboard: rechazada, FR-006 exige orden fijo
  con las 4 métricas visibles. Ocultarlas genera un vacío en el layout.
- Mostrar `"Próximamente"` como tarjeta especial: rechazada, requiere modificar
  el componente `_tarjeta_metrica.html` (VTG-004 lo prohíbe).

**Fundamento**: `valor: 0` mantiene la compatibilidad con el template.
`marcador: "No disponible"` se renderiza como texto debajo del valor en
`dashboard.html` sin tocar componentes compartidos. La decisión de clarificación
lo confirmó.

### 4. Disparador del estado vacío

**Decisión**: Activar estado vacío cuando `contar_total()` retorna `0`.

**Alternativas consideradas**:
- Activar cuando disponibles + rentadas == 0: rechazada, si hay propiedades en
  mantenimiento o inactivas, el dashboard no está vacío; simplemente no hay
  inventario disponible. El usuario debe ver sus métricas (0 disponibles, 0
  rentadas), no un mensaje de "sin datos".
- Activar cuando disponibles == 0: rechazada, ignora propiedades rentadas que sí
  son datos relevantes.

**Fundamento**: La decisión de clarificación estableció "cero filas en
`propiedades`". `contar_total()` es la consulta más simple y directa para esta
condición.

### 5. Ubicación del endpoint GET /

**Decisión**: Definir `GET /` en `app/modules/dashboard/routes.py`. `app/main.py`
solo registra el router.

**Alternativas consideradas**:
- Mantener `GET /` en `app/main.py` invocando el servicio de dashboard:
  rechazada por NFR-ARCH-002. `main.py` contendría lógica de registro de router
  + invocación de servicio, mezclando infraestructura con feature.
- Mover `GET /` sin crear router separado: rechazada, no escala cuando haya más
  endpoints del dashboard.

**Fundamento**: La decisión arquitectónica cerrada en clarificación establece que
el dashboard es un vertical slice completo. `main.py` se limita a
`app.include_router(dashboard_router)`.

### 6. Repositorio de dashboard como fachada

**Decisión**: El repositorio de dashboard (`obtener_metricas`) actúa como fachada
que invoca al repositorio de propiedades. No contiene lógica de negocio.

**Alternativas consideradas**:
- Servicio de dashboard invoca directamente el repo de propiedades: rechazada,
  rompe la separación de capas del slice (servicio → servicio, repositorio →
  repositorio).
- Un solo repositorio compartido: rechazada, viola vertical slice (cada módulo
  tiene su propio repo).

**Fundamento**: El repositorio de dashboard centraliza las consultas de conteo
que necesita el servicio. Si en el futuro el dashboard necesita datos de otros
módulos (inquilinos, pagos), el repositorio de dashboard orquesta las llamadas
sin que el servicio conozca múltiples fuentes de datos.
