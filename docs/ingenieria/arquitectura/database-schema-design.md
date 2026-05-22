---
id: ARC-004
type: Schema Design
rating: 9
rating-phase: document-critique
related:
  - target: ARC-003
    relationship_type: implements
    reason: Implementa el stack tecnológico definiendo schema de base de datos PostgreSQL
  - target: ARC-009
    relationship_type: references
    reason: Referencia el document-relationships-strategy para estrategia de relaciones
  - target: ARC-026
    relationship_type: references
    reason: Referencia las entidades core del sistema
  - target: ARC-027
    relationship_type: references
    reason: Referencia las entidades del workflow de 5 fases
  - target: ARC-028
    relationship_type: references
    reason: Referencia las entidades de auditoría y sincronización
---

# Database Schema Design — Alejandria

Este documento es el índice del diseño conceptual del esquema de base de datos para Alejandria usando PostgreSQL. El schema soporta el pipeline de 5 fases (detección → agrupación → resolución → verificación → aplicación) con versioning de documentos, idempotencia de jobs, y trazabilidad completa.

El diseño está dividido en tres documentos por funcionalidad lógica:

- **[database-schema-core-entities.md](database-schema-core-entities.md)**: Entidades core del sistema (tenancy, documentos, relaciones)
- **[database-schema-workflow-entities.md](database-schema-workflow-entities.md)**: Entidades del pipeline de 5 fases (gaps, questions, proposals)
- **[database-schema-audit-entities.md](database-schema-audit-entities.md)**: Entidades de auditoría y sincronización (snapshots, jobs, sync log)

## Índice

1. [Visión General](#1-visión-general)
2. [Documentos del Schema](#2-documentos-del-schema)
3. [Decisiones Arquitectónicas](#3-decisiones-arquitectónicas)
4. [Referencias](#4-referencias)

---

## 1. Visión General

### Stack de Base de Datos

- **PostgreSQL**: Base de datos relacional principal (ACID, integridad de datos)
- **Qdrant**: Base de datos vectorial para búsqueda semántica (contexto acumulativo)
- **Redis**: Broker para Celery y cache del sistema
- **Alembic**: Herramienta de migrations para versionar cambios de schema

### Principios de Diseño

- **Versioning automático**: Snapshots antes de cada UPDATE en documentos vía middleware en código (ver ADR-006)
- **Idempotencia de jobs**: Locks en documents para prevenir duplicación (ver ADR-005)
- **Trazabilidad completa**: Audit trail de todos los cambios (created_by, updated_by)
- **Integridad referencial**: Foreign keys con CASCADE DELETE apropiado
- **Performance**: Índices en campos de query frecuentes
- **Lógica explícita**: Versioning y updated_at manejados en código para mayor visibilidad y control
- **UUIDs como primary keys**: UUIDs en lugar de auto-increment para distribuidos y seguridad

### Conceptos Clave de PostgreSQL

#### UUID vs Auto-Increment

**Decisión**: Usar UUIDs (gen_random_uuid()) como primary keys en todas las tablas en lugar de auto-increment integers.

**Ventajas de UUIDs**:

- **Distribuidos**: UUIDs pueden generarse en cualquier nodo sin conflicto, facilitando arquitectura distribuida futura
- **Seguridad**: UUIDs no revelan información sobre el volumen de datos (auto-increment expone número de registros)
- **No lock contention**: No requiere locks de secuencia para generar IDs, mejor performance en alta concurrencia
- **Offline-friendly**: Pueden generarse sin conexión a base de datos, útil para operaciones asíncronas

**Desventajas de UUIDs**:

- **Storage**: 16 bytes vs 4 bytes (int) o 8 bytes (bigint)
- **Performance**: Índices B-tree menos eficientes con UUIDs aleatorios vs secuenciales
- **Legibilidad**: Más difíciles de leer/debug manualmente que integers

**Mitigación para MVP Bootstrapped**:

- Para MVP Bootstrapped (desarrollo local), las desventajas de performance son aceptables
- PostgreSQL optimiza UUIDs con gen_random_uuid() que genera UUIDs version 4
- Si se requiere optimización post-MVP, considerar UUIDs ordenados (ULID) o combinar con sharding

---

## 2. Documentos del Schema

El diseño del schema está dividido en tres documentos por funcionalidad lógica:

### [database-schema-core-entities.md](database-schema-core-entities.md)

Entidades core del sistema que son fundamentales para todas las funcionalidades:

- **users**: Autenticación y autorización
- **organizations**: Tenancy multi-organización
- **projects**: Contenedor de documentos y configuración
- **folders**: Estructura jerárquica de carpetas
- **documents**: Contenedor principal de contenido
- **document_relationships**: Relaciones semánticas entre documentos

### [database-schema-workflow-entities.md](database-schema-workflow-entities.md)

Entidades del pipeline de 5 fases (detección → agrupación → resolución → verificación → aplicación):

- **gaps**: Preguntas identificadas en fase de detección
- **tags**: Clasificación de gaps por tema
- **gap_tags**: Relación many-to-many entre gaps y tags
- **questions**: Preguntas respondidas por agentes LLM
- **question_document_references**: Documentos usados como contexto
- **question_gap_references**: Gaps necesarios para completar respuestas
- **proposals**: Propuestas de edición generadas automáticamente
- **proposal_documents**: Documentos afectados por propuestas
- **proposal_gaps**: Gaps resueltos que generaron propuestas

### [database-schema-audit-entities.md](database-schema-audit-entities.md)

Entidades de auditoría, versioning y sincronización:

- **document_snapshots**: Historial de cambios para rollback
- **vector_sync_log**: Sincronización PostgreSQL-Qdrant
- **jobs**: Audit trail de operaciones asíncronas
- **qdrant_collections**: Metadatos de colecciones vectoriales

---

## 3. Decisiones Arquitectónicas

### Índices de Performance

Los índices específicos por tabla están documentados en los documentos individuales del schema. Ver:

- **[database-schema-core-entities.md](database-schema-core-entities.md)**: Índices para entidades core
- **[database-schema-workflow-entities.md](database-schema-workflow-entities.md)**: Índices para entidades del workflow
- **[database-schema-audit-entities.md](database-schema-audit-entities.md)**: Índices para entidades de auditoría

### Versioning Automático

El versioning de documentos se implementa en código (middleware) en lugar de triggers de base de datos por las siguientes razones:

- **Visibilidad**: Lógica de negocio visible en código, no oculta en triggers
- **Control**: Mayor control sobre cuándo crear snapshots (ej: solo si contenido realmente cambió)
- **Testing**: Más fácil de unit test que triggers
- **Flexibilidad**: Permite lógica condicional compleja (ej: estrategia de storage basada en tiempo)

Ver ADR-006 para detalles de implementación.

### Idempotencia de Jobs

La idempotencia de jobs se implementa mediante Redis distributed locks con celery_once para prevenir duplicación de procesamiento:

- Redis distributed locks previenen ejecución duplicada de jobs
- celery_once con backend Redis maneja locks distribuidos de forma nativa
- Esto previene procesamiento duplicado cuando jobs se reintentan

Ver ADR-005 para detalles de implementación.

### Estrategia de Migrations

- **Backwards-compatible**: Todas las migrations incluyen downgrade scripts
- **Zero-downtime**: Migrations en producción sin interrupciones (fase post-MVP)
- **Versionado**: Cada migration tiene un número de versión incremental
- **Testing**: Migrations se prueban en ambiente de staging antes de producción
- **PENDIENTE**: Versión específica de Alembic por definir en fase de implementación

Las migrations específicas (código Alembic) residen en el repositorio de código, no en este documento de diseño.

---

## 4. Referencias

- **[database-schema-core-entities.md](database-schema-core-entities.md)**: Entidades core del sistema (tenancy, documentos, relaciones)
- **[database-schema-workflow-entities.md](database-schema-workflow-entities.md)**: Entidades del pipeline de 5 fases (gaps, questions, proposals)
- **[database-schema-audit-entities.md](database-schema-audit-entities.md)**: Entidades de auditoría y sincronización (snapshots, jobs, sync log)
- **[technology-stack.md](technology-stack.md)**: Stack tecnológico y decisiones
- **[document-relationships-strategy.md](document-relationships-strategy.md)**: Estrategia de implementación para relaciones entre documentos
- **[../decisiones/adr-004-ephemeral-jobs.md](../decisiones/adr-004-ephemeral-jobs.md)**: Jobs efímeros y retry strategy
- **[../decisiones/adr-006-document-versioning.md](../decisiones/adr-006-document-versioning.md)**: Versioning de documentos (middleware en código)
- **[../decisiones/adr-005-job-idempotency.md](../decisiones/adr-005-job-idempotency.md)**: Idempotencia de jobs
- **[../../producto/5-phase-workflow.md](../../producto/5-phase-workflow.md)**: Arquitectura de 5 fases
