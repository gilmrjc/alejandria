---
id: T-005
type: Task
rating: 9.0
rating-phase: document-editing
related:
  - target: T-004
    relationship_type: depends_on
    reason: Depende de la configuración de Alembic en T-004 para crear migration inicial
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del diseño de schema de base de datos para implementar migration
---

# T-005: Crear migration inicial de schema

**Tipo**: Task
**Prioridad**: Alta
**Estimación**: 4 horas
**Dependencias**: T-004

## Descripción

Crear migration inicial de Alembic con schema de base de datos según database-schema-design.md. La implementación específica de la migration sigue database-schema-design.md (UUIDs como primary keys, índices de performance, foreign keys con CASCADE DELETE). El orden de creación de tablas es: tablas de tenancy primero (users, organizations, projects), luego tablas core (folders, documents), luego tablas de soporte (snapshots, gaps, tags, questions, proposals), finalmente tablas de auditoría (jobs). Estrategia de rollback: eliminar en orden inverso para respetar dependencias de foreign keys.

## Criterios de Aceptación

- [ ] Migration `001_initial_schema.py` creada en `alembic/versions/`
- [ ] Tablas creadas según database-schema-design.md:
  - [ ] **Entidades Core** (database-schema-core-entities.md):
    - [ ] users
    - [ ] organizations
    - [ ] projects
    - [ ] folders
    - [ ] documents
    - [ ] document_relationships
  - [ ] **Entidades del Workflow** (database-schema-workflow-entities.md):
    - [ ] gaps
    - [ ] tags
    - [ ] gap_tags
    - [ ] questions
    - [ ] question_document_references
    - [ ] question_gap_references
    - [ ] proposals
    - [ ] proposal_documents
    - [ ] proposal_gaps
  - [ ] **Entidades de Auditoría** (database-schema-audit-entities.md):
    - [ ] document_snapshots
    - [ ] vector_sync_log
    - [ ] jobs
    - [ ] qdrant_collections
- [ ] Índices creados correctamente
- [ ] Foreign keys configurados con CASCADE DELETE apropiado
- [ ] Check constraints configurados
- [ ] Función `upgrade()` crea todas las tablas
- [ ] Función `downgrade()` elimina todas las tablas en orden correcto
- [ ] Comando `alembic upgrade head` aplica migration exitosamente
- [ ] Comando `alembic downgrade base` revierte migration exitosamente

## Criterios de Éxito

- Migration aplica sin errores y crea todas las tablas
- Schema validado contra database-schema-design.md
- Rollback funciona correctamente sin dejar datos huérfanos
- Foreign keys respetan dependencias en ambas direcciones

### Validación de Schema

Se usa validación manual con checklist de tablas y columnas.

**Proceso de validación:**

1. **Crear checklist basado en database-schema-design.md:**
   - Listar todas las tablas especificadas
   - Listar todas las columnas por tabla
   - Listar tipos de datos, constraints, índices

2. **Verificar cada item en la migration:**
   - Revisar que cada tabla está creada
   - Revisar que cada columna está definida con el tipo correcto
   - Revisar que constraints e índices están presentes

3. **Marcar items verificados en el checklist:**
   - Documentar qué items fueron verificados
   - Notar cualquier discrepancia encontrada

**Justificación:** Para esta fase inicial, la validación manual con checklist es simple y suficiente. Herramientas automatizadas de validación de schema pueden considerarse más adelante si el proyecto crece.

## Referencias

- [TRD - Hito 1](../propuestas/trd-milestone-1-infrastructure.md): RF-002: PostgreSQL Setup
- [database-schema-design.md](../arquitectura/database-schema-design.md): Diseño conceptual de schema de PostgreSQL

---

## Datos de Prueba

### Estrategia de Datos de Prueba

No se incluyen datos de prueba en la migration inicial.

**Estrategia:**

- La migration inicial solo crea schema, no datos
- Datos de prueba se manejarán por separado en scripts de seed
- Es más limpio y evita accidentes en producción
- Scripts de seed se crearán en una tarea futura

**Justificación:** Incluir datos de prueba en migrations es peligroso porque puede ejecutarse accidentalmente en producción. Separar schema de datos es una mejor práctica. Datos de prueba se gestionarán en scripts de seed específicos para desarrollo.
