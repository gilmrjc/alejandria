---
id: TS-001
type: Technical Specification
related-features: [FEAT-007]
related-adrs: []
related:
  - target: FEAT-007
    relationship_type: implements
    reason: Implementa la especificación técnica detallada del feature de búsqueda semántica
  - target: PRD-001
    relationship_type: depends_on
    reason: Depende del PRD Hito 1 que define los requisitos de configuración de Qdrant (BGE-M3, 1024 dimensiones, cosine similarity)
  - target: ARC-003
    relationship_type: depends_on
    reason: Depende del Technology Stack que define Qdrant como la base de datos vectorial seleccionada
---

# Especificación Técnica: Búsqueda Semántica

Especificación técnica detallada para el sistema de búsqueda semántica de Alejandría.

---

## Índice

1. [Visión General](#1-visión-general)
2. [Transformación a Vectores](#2-transformación-a-vectores)
3. [Motor de Búsqueda](#3-motor-de-búsqueda)
4. [Base de Datos Vectorial](#4-base-de-datos-vectorial)
5. [Requisitos No Funcionales](#5-requisitos-no-funcionales)

---

## 1. Visión General

**Propósito:**

Facilitar el encuentro rápido de información relevante en proyectos con grandes volúmenes de documentación mediante búsqueda vectorial.

**Contexto:**

Sistema de búsqueda que permite encontrar información por intención y contexto, no solo por coincidencia exacta de términos.

**Referencias:**

- [FEAT-007](../../producto/funcionalidades/busqueda-semantica.md): Búsqueda Semántica
- [PRD-001](../../producto/requisitos/prd-hito-01-infraestructura-base.md): PRD Hito 1 (sección 4.3)
- [ARC-003](technology-stack.md): Technology Stack (sección Qdrant)

---

## 2. Transformación a Vectores

### Modelo de Embeddings

**Modelo seleccionado:** BGE-M3 (BAAI General Embedding)

- **Dimensiones:** 1024
- **Similarity metric:** Cosine similarity
- **Proveedor:** Hugging Face
- **Razón de selección:** Balance entre performance, tamaño de modelo y calidad de embeddings para texto técnico

**Requisitos de implementación:**

- Modelo debe cargarse en memoria para inferencia rápida
- Batch processing para transformar múltiples respuestas simultáneamente
- Caching de embeddings para documentos que no cambian frecuentemente

### Estrategia de Chunking

**Tamaño máximo de chunk:** 512 tokens

**Superposición entre chunks:** 50 tokens (10%)

**Justificación:**

- 512 tokens es el límite óptimo para BGE-M3 manteniendo calidad de embeddings
- Superposición de 10% asegura que conceptos que cruzan límites de chunk no se pierdan
- Chunking por párrafos y secciones para mantener contexto semántico

**Algoritmo de chunking:**

1. Dividir texto en párrafos
2. Agrupar párrafos hasta alcanzar ~512 tokens
3. Mantener superposición de 50 tokens entre chunks adyacentes
4. Preservar estructura de secciones (títulos, subtítulos) en metadata

### Ciclo de Vida de Vectores

**Creación de vectores:**

- Cuando se crea una nueva respuesta a una pregunta
- Cuando se regenera una respuesta existente
- Cuando se edita manualmente un documento que contiene respuestas

**Actualización de vectores:**

- Trigger: Evento de actualización de documento
- Estrategia: Re-indexación incremental (solo chunks afectados)
- Consistencia: Transacción atómica entre documento y vector
- Validación: Verificación de que vector correspondiente existe antes de búsqueda

**Eliminación de vectores:**

- Cuando se elimina un documento
- Cuando se elimina una respuesta específica
- Garbage collection periódico de vectores huérfanos

### Metadata Asociada a Vectores

**Campos de metadata obligatorios:**

- `document_id`: ID del documento fuente
- `question_id`: ID de la pregunta asociada
- `author`: Usuario que creó la respuesta
- `created_at`: Timestamp de creación
- `updated_at`: Timestamp de última actualización
- `document_type`: Tipo de documento (ADR, PRD, Feature, etc.)
- `module`: Módulo o componente asociado

**Campos de metadata opcionales:**

- `tags`: Array de tags para categorización adicional
- `priority`: Prioridad del contenido (alta, media, baja)
- `language`: Idioma del contenido (es, en, etc.)

---

## 3. Motor de Búsqueda

### Algoritmo de Búsqueda

**Tipo:** Semantic search con cosine similarity

**Proceso:**

1. Usuario ingresa query en lenguaje natural
2. Query se transforma a vector usando el mismo modelo de embeddings (BGE-M3)
3. Sistema busca vectores más similares usando cosine similarity
4. Resultados se rankean por score de similitud
5. Filtros aplicados (si especificados por usuario)
6. Top N resultados retornados al usuario

**Umbral de similitud mínimo:** 0.7 (configurable por organización)

**Ranking de resultados:**

- Score de similitud cosine (70% peso)
- Recencia de actualización (20% peso)
- Calificación del documento (10% peso)

### Filtros Disponibles

**Filtro por autor:**

- Búsqueda por ID de usuario o nombre
- Soporte para múltiples autores (OR logic)

**Filtro por rango de fechas:**

- Fecha de creación (created_at)
- Fecha de actualización (updated_at)
- Rango: [start_date, end_date]

**Filtro por tipo de documento:**

- ADR, PRD, Feature, Technical Spec, etc.
- Soporte para múltiples tipos

**Filtro por módulo/componente:**

- Basado en metadata de módulo
- Jerarquía de módulos soportada

**Combinación de filtros:**

- AND logic entre diferentes tipos de filtros
- OR logic dentro del mismo tipo de filtro
- Paréntesis para agrupación compleja

### Explicación de Relevancia

**Para cada resultado, el sistema debe mostrar:**

- Score de similitud (0.0 - 1.0)
- Fragmento de texto que mejor matchea el query (highlight)
- Motivo de relevancia (ej: "similaridad semántica en concepto X")
- Referencia al documento fuente con link

---

## 4. Base de Datos Vectorial

### Configuración de Qdrant

**Versión:** 1.7.0+

**Configuración de colección:**

```yaml
collection_name: "document_embeddings"
vector_size: 1024
distance: Cosine
```

**Índice:**

- HNSW (Hierarchical Navigable Small World)
- M: 16 (número de conexiones por nodo)
- ef_construct: 100 (parámetro de construcción de índice)

**Optimizaciones:**

- Payload indexing para filtros rápidos
- Quantization para reducción de memoria (Scalar quantization)
- Replication factor: 2 (para alta disponibilidad)

### Estrategia de Indexación

**Índices primarios:**

- Índice HNSW para búsqueda de similitud
- Payload index en document_id para joins rápidos
- Payload index en created_at para filtros temporales

**Índices secundarios:**

- Payload index en author
- Payload index en document_type
- Payload index en module

### Backup y Recovery

**Estrategia de backup:**

- Snapshots diarios de colección Qdrant
- Retención: 7 días de snapshots diarios, 4 semanas de snapshots semanales
- Almacenamiento: S3 o equivalente

**Recovery:**

- Tiempo máximo de recovery: 1 hora
- Proceso: Restaurar snapshot más reciente
- Validación: Verificar integridad de vectores post-recovery

### Migración a Qdrant Cloud (Post-MVP)

**Trigger:** Cuando número de vectores > 1M o throughput > 1000 queries/min

**Beneficios:**

- Escalabilidad horizontal automática
- Monitoreo integrado
- SLA garantizado

**Consideraciones:**

- Costo mensual adicional
- Latencia de red adicional
- Migración con downtime mínimo

---

## 5. Requisitos No Funcionales

### Performance

**Transformación texto a vectores:**

- Tiempo máximo: 500ms por chunk de 512 tokens
- Throughput: 100 chunks/segundo (batch processing)

**Búsqueda semántica:**

- Tiempo máximo de respuesta: 200ms (p95)
- Latencia objetivo: 100ms (p50)
- Throughput: 500 queries/segundo

**Aplicación de filtros:**

- Tiempo máximo: 50ms adicionales a búsqueda base

**Carga de resultados:**

- Tiempo máximo: 100ms para top 20 resultados

### Escalabilidad

**Capacidad máxima de vectores:**

- Qdrant local: 10M vectores
- Qdrant cloud: 100M+ vectores

**Estrategia de escalado:**

- Horizontal scaling de Qdrant clusters
- Sharding por document_id
- Read replicas para queries de alta frecuencia

**Optimización de almacenamiento:**

- Scalar quantization: 4 bytes por dimensión (vs 8 bytes float)
- Compresión de payload metadata
- Deduplicación de vectores idénticos

### Precisión

**Métricas de precisión:**

- Precision@10: ≥ 0.85
- Recall@20: ≥ 0.90
- MRR (Mean Reciprocal Rank): ≥ 0.75

**Estrategia de mejora con feedback:**

- Click-through rate de resultados
- Feedback explícito (thumbs up/down)
- Re-ranking basado en feedback histórico

**Manejo de falsos positivos:**

- Umbral de similitud configurable
- Diversificación de resultados (avoid similar documents)
- Exclusión de resultados irrelevantes marcados por usuario

---

## Referencias

- [FEAT-007](../../producto/funcionalidades/busqueda-semantica.md): Búsqueda Semántica
- [REQ-010](../../producto/requisitos/.archived/requisitos-busqueda-semantica.md): Requisitos archivados (fuente de detalles técnicos)
- [PRD-001](../../producto/requisitos/prd-hito-01-infraestructura-base.md): PRD Hito 1
- [ARC-003](technology-stack.md): Technology Stack

---

*Documento generado integrando requisitos técnicos archivados con especificación de feature actual.*
