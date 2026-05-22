---
id: T-006
type: Task
rating: 9.0
rating-phase: document-editing
related:
  - target: T-005
    relationship_type: depends_on
    reason: Depende de la migration inicial creada en T-005 para implementar middleware
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del diseño de schema de base de datos para implementar middleware
---

# T-006: Implementar middleware de versioning en código

**Tipo**: Task
**Prioridad**: Media
**Estimación**: 4 horas
**Dependencias**: T-005

## Descripción

Implementar middleware en código Python (FastAPI/SQLAlchemy) para versioning automático de documentos y actualización automática de `updated_at`.

**Nota**: Según database-schema-design.md (líneas 647-654), el versioning se implementa en código (middleware) en lugar de triggers de base de datos por:

- **Visibilidad**: Lógica de negocio visible en código
- **Control**: Mayor control sobre cuándo crear snapshots
- **Testing**: Más fácil de unit test
- **Flexibilidad**: Permite lógica condicional compleja

## Criterios de Aceptación

- [ ] Middleware SQLAlchemy event listener implementado para `before_update` en documents
- [ ] Snapshot se crea automáticamente antes de UPDATE en documents.content
- [ ] `updated_at` se actualiza automáticamente en cada UPDATE
- [ ] Lógica condicional: solo crea snapshot si contenido realmente cambió
- [ ] Transacción atómica: snapshot y UPDATE en la misma transacción
- [ ] Unit tests para middleware
- [ ] Middleware incluido en módulo de base de datos

## Implementación de Middleware

```python
# middleware/document_versioning.py
from sqlalchemy import event
from sqlalchemy.orm import Session
from datetime import datetime
from models import Document, DocumentSnapshot

@event.listens_for(Document, 'before_update')
def create_document_snapshot(mapper, connection, target):
    """Crea snapshot antes de UPDATE si el contenido cambió."""
    # Solo crear snapshot si el contenido realmente cambió
    if target.content != target._old_content:
        snapshot = DocumentSnapshot(
            document_id=target.id,
            old_content=target._old_content,
            new_content=target.content,
            diff_type='full',  # Estrategia configurable según tiempo
            rating=target.rating,
            created_by=target.updated_by
        )
        connection.add(snapshot)

@event.listens_for(Document, 'before_update')
def update_timestamp(mapper, connection, target):
    """Actualiza updated_at automáticamente."""
    target.updated_at = datetime.utcnow()
```

### Validaciones de Integridad

Se incluye validación básica en el middleware para asegurar integridad mínima de snapshots.

**Validaciones básicas en el middleware:**

1. **Validar que campos no sean null:**
   - Verificar que `old_content` y `new_content` no sean null
   - Verificar que `document_id` no sea null

2. **Validar que document_id existe:**
   - Verificar que el document_id existe en la tabla documents
   - Evitar snapshots huérfanos

3. **Validar que contenido realmente cambió:**
   - Ya implementado en el middleware: `if target.content != target._old_content`
   - Evita snapshots duplicados sin cambios

**Nota:** Validación de integridad con checksums (SHA-256) y verificaciones más complejas se implementarán en una tarea futura de monitoreo.

**Justificación:** Para esta fase inicial, validaciones básicas en el middleware son suficientes. Checksums y validaciones más complejas pueden agregarse más adelante si se requiere mayor robustez.

## Criterios de Éxito

- Middleware funciona en transacciones atómicas sin crear snapshots duplicados
- Unit tests pasan para todos los escenarios de versioning
- `updated_at` se actualiza automáticamente en cada UPDATE
- Snapshots se crean solo cuando el contenido realmente cambió
- Rollback de transacciones no deja snapshots huérfanos

## Referencias

- [TRD - Hito 1](../propuestas/trd-milestone-1-infrastructure.md): RF-002: PostgreSQL Setup
- [database-schema-design.md](../arquitectura/database-schema-design.md): Líneas 647-654 (justificación de middleware vs triggers)
- [ADR-006](../decisiones/adr-006-document-versioning.md): Decisión de versioning de documentos
