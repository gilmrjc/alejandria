---
id: T-016
type: Task
rating: 9
rating-phase: document-editing
related:
  - target: EPC-002
    relationship_type: implements
    reason: Implementa la épica de API REST y MCP Server con schemas Pydantic
  - target: T-014
    relationship_type: depends_on
    reason: Depende de la estructura Python configurada en T-014 para implementar schemas
---

# T-016: Implementar Pydantic Schemas

**Tipo**: Task
**Prioridad**: Alta
**Estimación**: 4 horas
**Dependencias**: EPC-002, T-014

## Descripción

Implementar schemas Pydantic para validación de request/response de API según api-specification.md. Incluye sanitización de input con Bleach para markdown.

## Criterios de Aceptación

- [ ] Schemas para Document (create, update, response)
- [ ] Schemas para Session (create, response)
- [ ] Schemas para Gap (create, answer, response)
- [ ] Schemas para Job (response)
- [ ] Schemas para User (create, response)
- [ ] Sanitización de markdown con Bleach implementada (whitelist conservativa: tags p, br, strong, em, u, code, pre, blockquote, ul, ol, li, h1-h6, a; atributos permitidos: a: href con http/https, title; code: class para syntax highlighting; protocolos: http, https)

## Archivos a Crear

```
app/schemas/
  ├── __init__.py
  ├── document.py
  ├── session.py
  ├── gap.py
  ├── job.py
  └── user.py
```

## Referencias

- [TRD - Hito 2](../propuestas/trd-milestone-2-api-mcp.md): RF-001: FastAPI Application Setup
- [API Specification](../arquitectura/api-specification.md): Especificación de API REST

