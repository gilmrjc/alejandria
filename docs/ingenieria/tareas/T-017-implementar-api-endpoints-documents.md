---
id: T-017
type: Task
rating: 9
rating-phase: document-editing
related:
  - target: EPC-002
    relationship_type: implements
    reason: Implementa la épica de API REST y MCP Server con endpoints de documents
  - target: T-015
    relationship_type: depends_on
    reason: Depende de las migrations configuradas en T-015 para persistencia de documents
  - target: T-016
    relationship_type: depends_on
    reason: Depende de los schemas Pydantic implementados en T-016 para validación
---

# T-017: Implementar API Endpoints - Documents

**Tipo**: Task
**Prioridad**: Alta
**Estimación**: 6 horas
**Dependencias**: EPC-002, T-015, T-016

## Descripción

Implementar endpoints CRUD para documentos según api-specification.md.

### Detalles de Implementación

**Middleware de Versioning Automático**: Se implementa usando SQLAlchemy event listeners con `@event.listens_for(Document, 'before_update')`. Captura el estado actual antes de cada UPDATE, verifica cambio de contenido antes de crear snapshot (evita duplicados), y garantiza transacción atómica entre snapshot y UPDATE según ADR-006.

**Manejo de Concurrencia**: Se usa pessimistic locking con SQLAlchemy `with_for_update()`. Configuración: timeout 5 segundos, 3 reintentos con backoff exponencial (100ms, 500ms, 1000ms). Manejo de deadlock detection: PostgreSQL detecta deadlocks automáticamente, rollback transacción y reintentar con backoff según ADR-006.

## Criterios de Aceptación

- [ ] POST /api/v1/documents - Crear documento
- [ ] GET /api/v1/documents/{id} - Leer documento
- [ ] GET /api/v1/documents - Listar documentos con paginación
- [ ] PUT /api/v1/documents/{id} - Actualizar documento
- [ ] DELETE /api/v1/documents/{id} - Eliminar documento
- [ ] GET /api/v1/documents/{id}/snapshots - Obtener snapshots
- [ ] POST /api/v1/documents/{id}/snapshots/{snapshot_id}/restore - Restaurar snapshot
- [ ] Middleware de versioning automático antes de cada UPDATE (implementado con SQLAlchemy event listeners)
- [ ] Manejo de concurrencia para ediciones simultáneas (pessimistic locking con with_for_update)

## Archivos a Crear

```
app/api/
  ├── __init__.py
  └── documents.py
app/services/
  └── document_service.py
```

## Referencias

- [TRD - Hito 2](../propuestas/trd-milestone-2-api-mcp.md): RF-002: API REST Endpoints - Documents
- [API Specification](../arquitectura/api-specification.md): Endpoints de Documents
- [ADR-006](../decisiones/adr-006-document-versioning.md): Versioning de Documentos

