# Data Model: Rediseñar Home principal

**Feature**: `003-redisenar-home` | **Phase**: 1

## Estructuras de datos para el endpoint `GET /`

### Métricas

```python
metrica: dict = {
    "label": str,        # Etiqueta descriptiva
    "valor": int,        # Valor numérico
    "icono": str,        # Nombre del icono Lucide
    "tendencia": {       # Opcional
        "direccion": "up" | "down",
        "texto": str,    # Ej: "+12% vs mes anterior"
    },
    "estado": "datos",   # "datos" | "carga" | "error" (para tests manuales)
}
```

### Métricas específicas (hardcodeadas)

```python
metricas = [
    {
        "label": "Propiedades activas",
        "valor": 124,
        "icono": "building-2",
        "tendencia": {"direccion": "up", "texto": "+8% vs mes anterior"},
        "estado": "datos",
    },
    {
        "label": "Inquilinos al día",
        "valor": 87,
        "icono": "users",
        "tendencia": {"direccion": "up", "texto": "+3% vs mes anterior"},
        "estado": "datos",
    },
    {
        "label": "Contratos vigentes",
        "valor": 53,
        "icono": "file-text",
        "tendencia": {"direccion": "down", "texto": "-5% vs mes anterior"},
        "estado": "datos",
    },
]
```

### Accesos rápidos

```python
acceso: dict = {
    "icono": str,    # Nombre del icono Lucide
    "label": str,    # Texto visible
    "url": str,      # URL de destino o "#" si no existe aún
}
```

### Accesos rápidos específicos (hardcodeados)

```python
accesos = [
    {"icono": "building-2", "label": "Propiedades", "url": "#"},
    {"icono": "users",       "label": "Inquilinos",  "url": "#"},
    {"icono": "file-text",   "label": "Contratos",   "url": "#"},
    {"icono": "wallet",      "label": "Pagos",       "url": "#"},
]
```

### Actividad reciente

```python
actividad_item: dict = {
    "tipo": str,              # "propiedad" | "contrato" | "pago"
    "descripcion": str,       # Texto descriptivo
    "fecha": str,             # Fecha relativa o ISO
    "badge_variante": str,    # "success" | "warning" | "danger" | "accent" | "info"
    "estado": "datos",        # "datos" | "vacio" | "error" (para tests manuales)
}
```

### Actividad reciente específica (hardcodeada)

```python
actividad = [
    {
        "tipo": "propiedad",
        "descripcion": "Nueva propiedad registrada: Av. Reforma 245, Col. Centro",
        "fecha": "Hace 2 horas",
        "badge_variante": "accent",
        "estado": "datos",
    },
    {
        "tipo": "contrato",
        "descripcion": "Contrato por vencer: Depto. Condesa — vence en 3 días",
        "fecha": "Hace 5 horas",
        "badge_variante": "warning",
        "estado": "datos",
    },
    {
        "tipo": "pago",
        "descripcion": "Pago recibido: $15,000 — Renta Depto. Polanco",
        "fecha": "Ayer",
        "badge_variante": "success",
        "estado": "datos",
    },
]
```

### Contexto del template

```python
context: dict = {
    "request": Request,       # Objeto request de FastAPI
    "metricas": list[metrica],
    "accesos": list[acceso],
    "actividad": list[actividad_item],
}
```

### Mapping de tipo de actividad a badge

| Tipo | Badge variante | Color token |
|------|---------------|-------------|
| `propiedad` | `accent` | `--color-accent` |
| `contrato` | `warning` | `--color-warning` |
| `contrato` (urgente, < 7 días) | `danger` | `--color-danger` |
| `pago` | `success` | `--color-success` |
