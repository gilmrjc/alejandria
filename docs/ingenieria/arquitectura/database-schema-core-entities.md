---
id: ARC-026
type: Schema Design
rating: 9
rating-phase: document-critique
related:
  - target: ARC-004
    relationship_type: implements
    reason: Implementa el diseño de schema de base de datos - entidades core
---

# Database Schema: Core Entities — Alejandria

Este documento define las entidades core del esquema de base de datos para Alejandria. Estas entidades son fundamentales para el funcionamiento del sistema y se utilizan en todos los hitos.

## Índice

1. [Visión General](#1-visión-general)
2. [Entidades Core](#2-entidades-core)
3. [Relaciones y Foreign Keys](#3-relaciones-y-foreign-keys)

---

## 1. Visión General

### Propósito de las Entidades Core

Las entidades core forman la fundación del sistema y son utilizadas por todas las funcionalidades. Incluyen:

- **Tenancy**: organizations, projects, users
- **Document Management**: folders, documents
- **Document Relationships**: document_relationships

Estas entidades no están acopladas a fases específicas del workflow y son reutilizables across todo el sistema.

### Principios de Diseño

- **UUIDs como primary keys**: UUIDs en lugar de auto-increment para distribuidos y seguridad
- **Tenancy multi-organización**: organization_id denormalizado para queries eficientes
- **Integridad referencial**: Foreign keys con CASCADE DELETE apropiado
- **Performance**: Índices en campos de query frecuentes

---

## 2. Entidades Core

### users

Usuarios del sistema.

**Propósito**: Autenticación y autorización de usuarios.

**Campos principales**:

- `email`: Email único del usuario
- `username`: Username único del usuario
- `password_hash`: Hash de contraseña (no almacenar texto plano)

### organizations

Organizaciones (personales o empresariales) que contienen proyectos.

**Propósito**: Tenancy multi-organización para aislamiento de datos.

**Campos principales**:

- `name`: Nombre de la organización
- `slug`: Slug único para URLs
- `is_personal`: TRUE = espacio personal (único por usuario), FALSE = organización
- `created_by`: FK al usuario creador

**Relaciones**:

- FK a `users` (CASCADE DELETE)

**Tipos de organización**:

- `is_personal = TRUE`: Espacio personal generado automáticamente al crear cuenta (único por usuario)
- `is_personal = FALSE`: Organización empresarial, non-profit, open source, etc.

### projects

Proyectos dentro de una organización (análogos a repositorios en GitHub).

**Propósito**: Contenedor de documentos y configuración por proyecto.

**Campos principales**:

- `organization_id`: FK a la organización padre
- `name`: Nombre del proyecto
- `slug`: Slug único dentro de la organización
- `description`: Descripción del proyecto
- `created_by`: FK al usuario creador

**Relaciones**:

- FK a `organizations` (CASCADE DELETE)
- FK a `users` (CASCADE DELETE)

### folders

Estructura jerárquica de carpetas para navegación en frontend y gestión de documentos. Usa `ltree` de PostgreSQL para queries eficientes de subárbol.

**Propósito**: Organizar documentos en estructura jerárquica similar a sistemas de archivos.

**Campos principales**:

- `parent_folder_id`: FK recursiva para estructura jerárquica (NULL para carpeta raíz)
- `path`: Ruta como ltree para queries jerárquicas eficientes (ej: `docs.ingenieria.arquitectura`)
- `name`: Nombre de la carpeta para display en frontend
- `project_id`/`organization_id`: Tenancy multi-organización

**Relaciones**:

- FK a `projects` (CASCADE DELETE)
- FK a `organizations` (CASCADE DELETE)
- FK recursiva a `folders` (CASCADE DELETE)

**Consideraciones de diseño**:

- Usa extensión `ltree` de PostgreSQL para queries jerárquicas eficientes
- Índices GIST y BTREE en `path` para optimizar queries de subárbol
- Constraint único en `(project_id, path)` para prevenir duplicados

### documents

Almacena los documentos del sistema que son analizados y enriquecidos por el pipeline.

**Propósito**: Contenedor principal de contenido de documentos procesados por el sistema.

**Campos principales**:

- `title`: Título del documento
- `content`: Contenido completo del documento (TEXT)
- `folder_id`: FK a tabla `folders` para navegación jerárquica
- `filename`: Nombre del archivo (ej: database-schema.md). Combinado con folder_id y project_id forma ruta única.
- `rating`: Calificación de calidad del documento (0-10). Documentos con rating ≥ 9 no se procesan en detección.
- `vector_id`: ID del vector en Qdrant para búsqueda semántica. Se gestiona vía workers de sincronización.
- `project_id`/`organization_id`: Tenancy multi-organización
- `created_by`/`updated_by`: UUIDs para trazabilidad de quién creó/actualizó el documento

**Relaciones**:

- FK a `folders` (CASCADE DELETE)
- FK a `projects` (CASCADE DELETE)
- FK a `organizations` (CASCADE DELETE)
- FK a `users` (SET NULL) para created_by
- FK a `jobs` (SET NULL) para updated_by

**Cálculo de healthy en tiempo real**:

Un documento se considera "healthy" si cumple dos condiciones:

1. `rating >= 9`
2. No tiene gaps con status `pending` asociados al documento

Esta lógica se implementa en queries de negocio, no como constraint de base de datos.

### document_relationships

Relaciones directas entre documentos para visualización de grafos y trazabilidad de dependencias.

**Propósito**: Capturar conexiones semánticas entre documentos para facilitar visualización de grafos en la UI con información rica desde el inicio, permitiendo análisis de impacto, dependencias y estructura del conocimiento.

**Campos principales**:

- `source_document_id`: FK al documento origen
- `target_document_id`: FK al documento destino
- `relationship_type`: Tipo de relación (depends_on, explains, reinforces, contradicts, references, implements, extends)
- `direction`: Dirección del flujo de información ('inflow' o 'outflow')
- `reason`: Descripción detallada de la relación (texto libre para contexto humano)
- `created_by`: FK a users (NULL = generado automáticamente, no NULL = creado manualmente)

**Relaciones**:

- FK a `documents` (CASCADE DELETE) para source_document_id
- FK a `documents` (CASCADE DELETE) para target_document_id
- FK a `users` (SET NULL) para created_by

**Tipos de relación y dirección**:

Todas las relaciones son direccionales. La simetría emerge de los datos (ej: si A refuerza B y B refuerza A, se crean dos registros).

El campo `direction` se almacena explícitamente para facilitar queries eficientes sin depender de lógica derivada de `relationship_type`.

- **Outflow (A → B)**: Cambios en B afectan a A
  - `depends_on`: A depende de B (ej: ADR depende de technical-brief)
  - `references`: A cita B sin dependencia fuerte (ej: "ver también")
  - `implements`: A concreta B (ej: código implementa diseño)
  - `supersedes`: A reemplaza B (ej: ADR v2 reemplaza ADR v1)
  - `reinforces`: A refuerza B (ej: ejemplo valida principio)
  - `contradicts`: A contradice B (ej: diseño vs implementación divergente)

- **Inflow (A ← B)**: A aporta contexto a B
  - `explains`: A explica conceptos de B (ej: tutorial explica ADR)
  - `extends`: A deriva/extiende B (ej: deep dive de concepto general)

**Razones de contexto (campo `reason`)**:

El campo `reason` debe capturar:

- **Por qué existe la relación**: "Este ADR implementa la decisión X del technical-brief"
- **Contexto temporal**: "Versión 2 contradice versión 1 debido a cambio Y"
- **Evidencia**: "Validado por ejemplo en documento Z"
- **Impacto**: "Si cambia B, debe revisarse A"

**Consideraciones de diseño**:

- Constraint único en `(source_document_id, target_document_id, relationship_type)` para prevenir duplicados
- Índice compuesto en `(source_document_id, target_document_id)` para queries eficientes de grafo
- Índice en `relationship_type` para filtrado por tipo de conexión
- Índice en `direction` para queries eficientes de inflow/outflow
- Dirección de la relación se almacena explícitamente en el campo `direction` para facilitar queries
- Todas las relaciones son direccionales; la simetría emerge de los datos (ej: A refuerza B y B refuerza A = dos registros)

---

## 3. Relaciones y Foreign Keys

### Diagrama de Relaciones Core

```mermaid
organizations (1) ----< (N) projects
organizations (N) ----> (1) users (via created_by)

organizations (1) ----< (N) documents (via organization_id)
organizations (1) ----< (N) folders (via organization_id)

projects (1) ----< (N) documents
projects (1) ----< (N) folders
projects (N) ----> (1) users (via created_by)

folders (1) ----< (N) documents
folders (N) ----< (N) folders (recursiva)

documents (N) ----< (N) document_relationships ----< (N) documents

users (N) ----> (N) documents (via created_by)
users (N) ----> (N) organizations (via created_by)
users (N) ----> (N) projects (via created_by)
users (N) ----> (N) document_relationships (via created_by)
```

### Cascade Delete Rules

- **CASCADE**: organizations, projects, folders, documents, document_relationships
- **SET NULL**: created_by, updated_by

**Justificación de CASCADE DELETE**:

- **Organizaciones**: Al eliminar una organización, se eliminan todos sus proyectos y datos asociados (limpieza completa)
- **Proyectos**: Al eliminar un proyecto, se eliminan todos sus documentos y configuración
- **Documentos**: Al eliminar un documento, se eliminan sus relaciones (consistencia)
- **SET NULL para trazabilidad**: created_by y updated_by se setean a NULL en lugar de eliminar el registro para preservar datos de negocio

### Tenancy y Organization Immutability

- **organization_id denormalizado**: Agregado en documents, folders para queries multi-tenant eficientes sin joins
- **Organización inmutable**: Un proyecto no puede cambiar de organización. Esto se garantiza mediante:
  - No permitir UPDATE en `projects.organization_id` a nivel de aplicación
  - Trigger opcional en PostgreSQL para bloquear cambios en producción
  - El campo `organization_id` en tablas hijas se sincroniza con `projects.organization_id` al crear registros

**Justificación de denormalización**:

- Queries multi-tenant son muy frecuentes (casi todas las queries filtran por organization_id)
- Evitar joins en cada query mejora performance significativamente
- El costo de mantener consistencia es bajo dado que organization_id es inmutable

---

## Referencias

- **[database-schema-design.md](database-schema-design.md)**: Índice completo de schema de base de datos
- **[database-schema-workflow-entities.md](database-schema-workflow-entities.md)**: Entidades del pipeline de 5 fases
- **[database-schema-audit-entities.md](database-schema-audit-entities.md)**: Entidades de auditoría y sincronización
- **[document-relationships-strategy.md](document-relationships-strategy.md)**: Estrategia de implementación para relaciones entre documentos
