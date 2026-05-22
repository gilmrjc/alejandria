---
id: ARC-028
type: Schema Design
rating: 9
rating-phase: document-critique
related:
  - target: ARC-004
    relationship_type: implements
    reason: Implementa el diseño de schema de base de datos - entidades de auditoría
---

# Database Schema: Audit & Sync Entities — Alejandria

Este documento define las entidades de auditoría, versioning y sincronización del sistema. Estas entidades proporcionan trazabilidad, reversibilidad y consistencia eventual entre PostgreSQL y Qdrant.

## Índice

1. [Visión General](#1-visión-general)
2. [Entidades de Auditoría y Sincronización](#2-entidades-de-auditoría-y-sincronización)
3. [Relaciones y Foreign Keys](#3-relaciones-y-foreign-keys)

---

## 1. Visión General

### Propósito de las Entidades de Auditoría

Las entidades de auditoría y sincronización proporcionan:

- **Versioning de documentos**: document_snapshots para rollback y auditoría
- **Sincronización vectorial**: vector_sync_log para consistencia eventual PostgreSQL-Qdrant
- **Audit trail de jobs**: jobs para rastrear operaciones asíncronas
- **Metadatos de Qdrant**: qdrant_collections para gestión de colecciones vectoriales

Estas entidades son transversales al sistema y soportan todas las funcionalidades.

### Principios de Diseño

- **Versioning en código**: document_snapshots se gestionan vía middleware (no triggers)
- **Consistencia eventual**: vector_sync_log permite retry y sincronización asíncrona
- **Audit trail completo**: Todas las operaciones asíncronas se registran en jobs
- **Storage optimizado**: Estrategia de compresión y retención para snapshots

---

## 2. Entidades de Auditoría y Sincronización

### document_snapshots

Diffs comprimidos de cambios en documentos para versioning y rollback (ver ADR-006). Estrategia similar a wikis (MediaWiki, Git) para optimizar storage.

**Propósito**: Mantener historial de cambios en documentos para rollback y auditoría.

**Campos principales**:

- `document_id`: FK al documento versionado
- `old_content`: Contenido anterior (NULL para primera versión)
- `new_content`: Contenido nuevo (diff o snapshot completo)
- `diff_type`: Tipo de snapshot ('full' o 'diff')
- `rating`: Rating del documento en este snapshot
- `created_by`: UUID de usuario si fue manual, NULL si fue proceso automático

**Relaciones**:

- FK a `documents` (CASCADE DELETE)
- FK a `users` (SET NULL) para created_by

**Estrategia de Storage**:

- **Últimos 30 días**: Snapshots completos (`diff_type = 'full'`) para rollback rápido
- **>30 días**: Diffs comprimidos (`diff_type = 'diff'`) usando unified diff format
- **Compresión**: PostgreSQL TOAST comprime automáticamente TEXT fields (80-90% reducción en diffs)
- **Retención**: Configurable via `system_settings.retention_days` (default: 5 años)

### vector_sync_log

Log de sincronización para mantener consistencia eventual entre PostgreSQL y Qdrant.

**Propósito**: Rastrear operaciones de sincronización de vectores para retry y consistencia eventual.

**Campos principales**:

- `entity_type`: Tipo de entidad ('document' o 'question')
- `entity_id`: ID de la entidad en PostgreSQL
- `vector_id`: ID del vector en Qdrant
- `sync_status`: Estado de sincronización (synced, pending, failed)
- `sync_action`: Acción realizada (create, update, delete)
- `error_message`: Mensaje de error si falló (NULL si exitoso)
- `retry_count`: Número de reintentos realizados

**Estados de sincronización**:

- `pending`: Operación pendiente de procesar por worker
- `synced`: Operación completada exitosamente
- `failed`: Operación falló (requiere retry o intervención manual)

**Acciones de sincronización**:

- `create`: Crear nuevo vector en Qdrant
- `update`: Actualizar vector existente en Qdrant
- `delete`: Eliminar vector de Qdrant

### jobs

Registro de jobs completados en el sistema (Celery/RQ). Solo registra el resultado final para trazabilidad.

**Propósito**: Audit trail de jobs ejecutados por el sistema.

**Campos principales**:

- `job_type`: Tipo de job ejecutado
- `entity_type`: Tipo de entidad afectada
- `entity_id`: ID de la entidad afectada
- `status`: Estado del job (completed, failed)
- `completed_at`: Timestamp de finalización
- `error_message`: Mensaje de error si falló (NULL si exitoso)

**Tipos de job**:

- `gap_detection`: Detección de gaps en un documento
- `suggestion_application`: Aplicación de cambios propuestos
- `vector_sync`: Sincronización de vectores con Qdrant
- `question_generation`: Generación de preguntas

**Estados de job**:

- `completed`: Job completado exitosamente
- `failed`: Job falló con error

**Retry strategy** (ver ADR-004):

- Backoff exponencial con jitter aleatorio
- Máximo 5 reintentos por defecto
- Timeout: 5 minutos para todos los jobs

### qdrant_collections

Gestión de colecciones en Qdrant para búsqueda semántica por proyecto.

**Propósito**: Mantener metadatos de colecciones vectoriales en Qdrant.

**Campos principales**:

- `collection_name`: Nombre único de la colección en Qdrant (típicamente `project_{project_id}`)
- `vector_size`: Dimensión de los vectores (768 para modelos como sentence-transformers)
- `distance_metric`: Métrica de similitud (cosine, euclidean, dot)
- `embedding_model`: Modelo de embeddings utilizado

**Relaciones**:

- FK a `projects` (CASCADE DELETE)
- FK a `organizations` (CASCADE DELETE)

---

## 3. Relaciones y Foreign Keys

### Diagrama de Relaciones de Auditoría

```mermaid
documents (1) ----< (N) document_snapshots
documents (N) ----> (1) jobs (via updated_by)

vector_sync_log (N) ----> (1) documents (via entity_id when entity_type='document')
vector_sync_log (N) ----> (1) questions (via entity_id when entity_type='question')

projects (1) ----< (N) qdrant_collections
organizations (1) ----< (N) qdrant_collections
```

### Cascade Delete Rules

- **CASCADE**: document_snapshots, qdrant_collections
- **CASCADE para vector_sync_log**: Cuando se elimina un documento o pregunta, los registros de sync log se eliminan (gestionado vía código/workers)
- **SET NULL**: created_by, updated_by

**Justificación de CASCADE DELETE**:

- **Documentos**: Al eliminar un documento, se eliminan sus snapshots (consistencia)
- **Qdrant Collections**: Al eliminar un proyecto, se eliminan sus colecciones (limpieza)
- **SET NULL para trazabilidad**: created_by y updated_by se setean a NULL para preservar datos de negocio

---

## Referencias

- **[database-schema-design.md](database-schema-design.md)**: Índice completo de schema de base de datos
- **[database-schema-core-entities.md](database-schema-core-entities.md)**: Entidades core del sistema
- **[database-schema-workflow-entities.md](database-schema-workflow-entities.md)**: Entidades del pipeline de 5 fases
- **[../decisiones/adr-006-document-versioning.md](../decisiones/adr-006-document-versioning.md)**: Versioning de documentos (middleware en código)
- **[../decisiones/adr-004-ephemeral-jobs.md](../decisiones/adr-004-ephemeral-jobs.md)**: Jobs efímeros y retry strategy
