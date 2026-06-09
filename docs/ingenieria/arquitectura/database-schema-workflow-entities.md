---
id: ARC-027
type: Schema Design
rating: 9
rating-phase: document-critique
related:
  - target: ARC-004
    relationship_type: implements
    reason: Implementa el diseño de schema de base de datos - entidades del workflow
---

# Database Schema: Workflow Entities — Alejandria

Este documento define las entidades del pipeline de 5 fases (detección → agrupación → resolución → verificación → aplicación). Estas entidades implementan el workflow central de Alejandria.

## Índice

1. [Visión General](#1-visión-general)
2. [Entidades del Workflow](#2-entidades-del-workflow)
3. [Relaciones y Foreign Keys](#3-relaciones-y-foreign-keys)

---

## 1. Visión General

### Propósito de las Entidades del Workflow

Las entidades del workflow implementan el pipeline de 5 fases de Alejandria:

- **Fase 1 - Detección**: gaps
- **Fase 2 - Agrupación**: tags, gap_tags
- **Fase 3 - Resolución**: questions, question_document_references, question_gap_references
- **Fase 4 - Verificación**: (estado de questions)
- **Fase 5 - Aplicación**: proposals, proposal_documents, proposal_gaps

Estas entidades están acopladas al workflow pero son independientes entre sí, permitiendo evolución del pipeline sin afectar entidades core.

### Principios de Diseño

- **Estado explícito**: Cada entidad tiene campos de status para rastrear progreso
- **Trazabilidad completa**: Todas las relaciones tienen foreign keys con CASCADE DELETE
- **Flexibilidad**: Relaciones many-to-many permiten conexiones complejas

---

## 2. Entidades del Workflow

### gaps

Preguntas identificadas durante la fase de detección que requieren resolución.

**Propósito**: Almacenar preguntas detectadas por el sistema que requieren intervención humana.

**Campos principales**:

- `document_id`: FK al documento asociado
- `question`: Texto de la pregunta detectada
- `priority`: Prioridad del gap (critical, high, medium, low)
- `status`: Estado del gap (pending, responded, rejected)
- `answer`: Respuesta pre-llenada por el LLM al detectar el gap (sugerencia), o respuesta confirmada por el usuario. NULL si el LLM no pudo generar sugerencia.
- `answered_at`: Timestamp de confirmación por usuario (NULL si pendiente o solo sugerencia)
- `answered_by`: FK UUID al usuario que confirmó la respuesta (NULL = solo sugerencia del LLM, UUID = usuario confirmó)

**Relaciones**:

- FK a `documents` (CASCADE DELETE)
- FK a `users` en `answered_by` (SET NULL on delete)

**Estados de gap**:

- `pending`: Gap detectado, puede tener `answer` pre-llenado por el LLM como sugerencia
- `responded`: Usuario confirmó o modificó la respuesta (`answered_by` y `answered_at` quedan seteados)
- `rejected`: Rechazado por usuario (no es un gap real)

### tags

Etiquetas para clasificar gaps por tema. Reemplaza el concepto de gap_groups para permitir clasificación más flexible y reutilizable entre gaps de diferentes documentos.

**Propósito**: Clasificación flexible de gaps por temas reutilizables.

**Campos principales**:

- `name`: Nombre de la etiqueta
- `project_id`/`organization_id`: Tenancy multi-organización

**Relaciones**:

- FK a `projects` (CASCADE DELETE)
- FK a `organizations` (CASCADE DELETE)

### gap_tags

Relación many-to-many entre gaps y tags.

**Propósito**: Vincular múltiples tags a un gap para clasificación múltiple.

**Campos principales**:

- `gap_id`: FK al gap
- `tag_id`: FK al tag

**Relaciones**:

- FK a `gaps` (CASCADE DELETE)
- FK a `tags` (CASCADE DELETE)

### questions

Preguntas respondidas por el sistema mediante agentes LLM (Sección de Preguntas).

**Propósito**: Almacenar preguntas generadas por el sistema y sus respuestas completas.

**Campos principales**:

- `question`: Texto de la pregunta
- `answer`: Respuesta generada por LLM (NULL si pendiente)
- `status`: Estado de la pregunta (pending, incomplete, answered, verified)
- `vector_id`: ID del vector en Qdrant para búsqueda semántica
- `project_id`/`organization_id`: Tenancy multi-organización

**Relaciones**:

- FK a `projects` (CASCADE DELETE)
- FK a `organizations` (CASCADE DELETE)

**Estados de pregunta**:

- `pending`: Pregunta generada automáticamente, esperando procesamiento
- `incomplete`: Respuesta parcial, faltan gaps por resolver para completar
- `answered`: Respuesta completa generada por LLM
- `verified`: Respuesta validada por humano como correcta

### question_document_references

Relación many-to-many entre preguntas y documentos utilizados como referencia para generar respuestas.

**Propósito**: Rastrear qué documentos fueron usados como contexto para generar cada respuesta.

**Campos principales**:

- `question_id`: FK a la pregunta
- `document_id`: FK al documento de referencia

**Relaciones**:

- FK a `questions` (CASCADE DELETE)
- FK a `documents` (CASCADE DELETE)

### question_gap_references

Relación many-to-many entre preguntas incompletas y gaps que podrían complementar la respuesta para completarla.

**Propósito**: Vincular gaps necesarios para completar respuestas incompletas.

**Campos principales**:

- `question_id`: FK a la pregunta incompleta
- `gap_id`: FK al gap necesario

**Relaciones**:

- FK a `questions` (CASCADE DELETE)
- FK a `gaps` (CASCADE DELETE)

### proposals

Propuestas de edición generadas en Fase 4 (Plan de Acción) basadas en gaps resueltos. La descripción es un prompt natural que el agente interpreta al aplicar cambios. Una propuesta puede afectar múltiples documentos.

**Propósito**: Almacenar propuestas de edición generadas automáticamente para aprobación humana.

**Campos principales**:

- `name`: Nombre descriptivo de la propuesta
- `description`: Prompt natural que el agente interpreta para aplicar cambios
- `status`: Estado de la propuesta (pending, accepted, rejected, implemented)

**Estados de propuesta**:

- `pending`: Propuesta generada automáticamente, esperando aprobación
- `accepted`: Propuesta aprobada por usuario para implementación
- `rejected`: Propuesta rechazada por usuario
- `implemented`: Propuesta implementada exitosamente

### proposal_documents

Relación many-to-many entre proposals y documentos (una propuesta puede afectar múltiples documentos).

**Propósito**: Vincular propuestas con los documentos que modifican.

**Campos principales**:

- `proposal_id`: FK a la propuesta
- `document_id`: FK al documento afectado

**Relaciones**:

- FK a `proposals` (CASCADE DELETE)
- FK a `documents` (CASCADE DELETE)

### proposal_gaps

Relación many-to-many entre proposals y gaps.

**Propósito**: Rastrear qué gaps resueltos generaron cada propuesta.

**Campos principales**:

- `proposal_id`: FK a la propuesta
- `gap_id`: FK al gap resuelto

**Relaciones**:

- FK a `proposals` (CASCADE DELETE)
- FK a `gaps` (CASCADE DELETE)

---

## 3. Relaciones y Foreign Keys

### Diagrama de Relaciones del Workflow

```mermaid
documents (1) ----< (N) gaps
documents (N) ----< (N) question_document_references ----< (N) questions
documents (N) ----< (N) proposal_documents ----< (N) proposals

gaps (N) ----< (N) gap_tags ----< (N) tags
gaps (N) ----< (N) proposal_gaps ----< (N) proposals

questions (N) ----< (N) question_gap_references ----< (N) gaps
```

### Cascade Delete Rules

- **CASCADE**: gaps, tags, gap_tags, questions, question_document_references, question_gap_references, proposals, proposal_documents, proposal_gaps

**Justificación de CASCADE DELETE**:

- **Documentos**: Al eliminar un documento, se eliminan sus gaps y propuestas (consistencia)
- **Gaps**: Al eliminar un gap, se eliminan sus tags y referencias (limpieza)
- **Questions**: Al eliminar una pregunta, se eliminan sus referencias (consistencia)
- **Proposals**: Al eliminar una propuesta, se eliminan sus documentos y gaps asociados (consistencia)

---

## Referencias

- **[database-schema-design.md](database-schema-design.md)**: Índice completo de schema de base de datos
- **[database-schema-core-entities.md](database-schema-core-entities.md)**: Entidades core del sistema
- **[database-schema-audit-entities.md](database-schema-audit-entities.md)**: Entidades de auditoría y sincronización
- **[../../producto/5-phase-workflow.md](../../producto/5-phase-workflow.md)**: Arquitectura de 5 fases
