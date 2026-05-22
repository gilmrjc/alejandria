---
id: T-016
type: Task
rating:
rating-phase:
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

---

## Análisis de Documento

**ESTADO DEL ANÁLISIS**

- Análisis previo: NO
- Fecha del análisis: 2026-05-27
- Versión del análisis: 1
- Gaps pendientes: 2
- Gaps respondidos: 0
- Gaps NO APLICA: 0

**CLASIFICACIÓN DEL DOCUMENTO**

- Tipo: Documento de Proyecto (Task)
- Rol Principal: Desarrollador/Ingeniero
- Roles a Revisar: Desarrollador + Arquitecto + Gerente de Proyecto
- Enfoque: Implementación de schemas Pydantic para validación de API
- Perspectiva: Senior + Junior
- Fecha de análisis: 2026-05-27
- Versión del análisis: 1

### Gaps Identificados

**IMPLEMENTACIÓN TÉCNICA**

**GAP: Validación de input y sanitización adicional** [PRIORIDAD: Alto] [ESTADO: PENDIENTE]

- **Pregunta**: La tarea menciona "Validación de input y sanitización adicional" como GAP. ¿Qué sanitización adicional más allá de Pydantic se requiere? ¿Bleach para markdown? ¿Qué whitelist específica de tags HTML se permite?
- **Contexto faltante**: Detalles de la estrategia de sanitización de input, incluyendo herramientas específicas (ej. Bleach) y configuración de whitelist de tags permitidos según api-specification.md.
- **Rol afectado**: Desarrollador Senior
- **Referencia**: Línea 33 del documento actual, api-specification.md líneas 219-254
- **Fecha de identificación**: 2026-05-27

**GESTIÓN DE PROYECTO**

**GAP: Criterios para estimación de esfuerzo** [PRIORIDAD: Bajo] [ESTADO: PENDIENTE]

- **Pregunta**: La tarea tiene una estimación de 4 horas. ¿Qué criterios se usaron para esta estimación? ¿Es basada en experiencia previa? ¿Referencias externas?
- **Contexto faltante**: Justificación de la estimación de esfuerzo para esta tarea específica.
- **Rol afectado**: Gerente de Proyecto
- **Referencia**: Línea 19 del documento actual
- **Fecha de identificación**: 2026-05-27
