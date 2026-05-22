---
id: ARC-033
type: Architecture
rating: 10
rating-phase: document-editing
related:
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del schema de base de datos para persistencia de vectores
  - target: ADR-002
    relationship_type: implements
    reason: Implementa el stack unificado Python con integración Qdrant
  - target: FEAT-007
    relationship_type: implements
    reason: Implementa la funcionalidad de búsqueda semántica
---

# Semantic Search Implementation — Alejandria

Este documento define la implementación de búsqueda semántica en Alejandria, incluyendo configuración de embeddings, estrategia de chunking, y actualización de vectores.

---

## 1. Visión General

### Propósito

La búsqueda semántica permite encontrar documentos y preguntas basándose en intención y contexto, no solo coincidencia exacta. Esta funcionalidad es fundamental para reutilizar conocimiento acumulado y encontrar contexto relevante para resolver gaps.

### Stack Tecnológico

- **Base de datos vectorial**: Qdrant
- **Modelo de embeddings**: BGE-M3
- **Dimensiones**: 1024
- **Similarity**: Cosine similarity

Cosine similarity se eligió por su invarianza a magnitud (mide dirección del vector, no magnitud, crítico para embeddings donde textos similares pueden tener diferentes magnitudes), normalización implícita que simplifica cálculo, y por ser estándar de industria para RAG y búsqueda semántica. Qdrant está optimizado para cosine con HNSW. Alternativas rechazadas: Euclidean (sensible a magnitud, requiere normalización manual) y Dot Product (sensible a magnitud, resultados inconsistentes sin normalización).

---

## 2. Configuración de Embeddings

### Modelo BGE-M3

**Modelo**: BGE-M3 (BAAI General Embedding Multilingual Model)

**Características**:

- 1024 dimensiones
- Soporte multilingüe (español, inglés, etc.)
- Optimizado para retrieval semántico
- Alta precisión en tareas de búsqueda

**Configuración**:

- Ejecución vía Ollama para MVP bootstrapped
- API externa para producción (post-MVP)
- Parámetros por defecto del modelo

BGE-M3 se eligió específicamente por: (1) Alta precisión: 63.0 MTEB score, 5-8% mejor retrieval accuracy que all-MiniLM-L6-v2. (2) Multilingüe: 100+ languages, entrenado en 170+ languages (español e inglés). (3) 1024 dimensiones: balance entre riqueza y performance. (4) Disponible en Ollama: integración simple con stack existente. (5) Open-source: sin costos de API. Alternativas rechazadas: all-MiniLM-L6-v2 (menor retrieval accuracy, poor performance según reports de usuarios), OpenAI/Cohere (costos de API).

**Comandos de configuración Ollama**:

- Descargar modelo: `ollama pull bge-m3`
- Verificar instalación: `ollama list`
- API para embeddings: `curl http://localhost:11434/api/embeddings -d '{"model": "bge-m3", "prompt": "texto"}'`

BGE-M3 usa parámetros por defecto del modelo en Ollama. Se eligió Ollama sobre PyTorch por simplicidad y mejor performance de inferencia para MVP bootstrapped.

---

## 3. Estrategia de Chunking

### Objetivo

Dividir documentos largos en chunks manejables para embeddings, preservando contexto y estructura semántica.

### Parámetros de Chunking

- **Tamaño máximo de chunk**: 256 tokens
- **Superposición entre chunks**: 25 tokens (10%)
- **Algoritmo**: División por párrafos con agrupación inteligente

El tamaño de 256 tokens (192 palabras, ~7 párrafos) se basa en: (1) Tamaño promedio párrafo español: 35 tokens. 512 tokens agruparía ~15 párrafos (demasiado contexto). (2) Prácticas RAG: 256-512 tokens es rango estándar, 256 mejor para Q&A técnico. (3) 10% superposición (25 tokens) preserva contexto en límites sin duplicación excesiva. Valores no basados en benchmarks empíricos específicos, son estándar de industria para MVP bootstrapped.

### Algoritmo de Chunking

La implementación es simple: dividir el texto usando saltos de línea como delimitadores y agregar un margen de unas cuantas palabras hacia atrás y adelante para preservar contexto. No se usa librería externa de chunking.

### Metadata Asociada

Cada vector incluye metadata para filtros:

- `document_id`: UUID del documento origen
- `section_title`: Título de la sección (si aplica)
- `chunk_index`: Índice del chunk dentro del documento
- `created_at`: Timestamp de creación

---

## 4. Estrategia de Actualización de Vectores

### Cuándo Actualizar

Los vectores se actualizan cuando:

- Un documento se crea (nuevo)
- Un documento se actualiza (modificación de contenido)
- Un documento se elimina (cascada delete)

### Algoritmo de Actualización

**Para documentos nuevos**:

1. Aplicar chunking al contenido completo
2. Generar embeddings para cada chunk
3. Insertar vectores en Qdrant con metadata
4. Registrar en `vector_sync_log`

El registro se realiza dentro de proceso con transacción en Python. Si falla la vectorización, se hace rollback del registro. Esto garantiza atomicidad: o se registra y se vectoriza exitosamente, o no se registra nada. vector_sync_log permite consistencia eventual PostgreSQL-Qdrant según database-schema-audit-entities.md.

**Para documentos actualizados**:

1. Eliminar vectores existentes del documento
2. Aplicar chunking al contenido actualizado
3. Generar embeddings para cada chunk nuevo
4. Insertar vectores en Qdrant con metadata
5. Actualizar `vector_sync_log`

El registro se realiza dentro de proceso con transacción en Python. Si falla la vectorización, se hace rollback del registro. Esto garantiza atomicidad: o se registra y se vectoriza exitosamente, o no se registra nada. vector_sync_log permite consistencia eventual PostgreSQL-Qdrant según database-schema-audit-entities.md.

**Para documentos eliminados**:

1. Eliminar vectores por `document_id`
2. Actualizar `vector_sync_log` con timestamp de eliminación

### Performance

- Actualización incremental (no regenerar toda la colección)
- Batch processing para documentos grandes
- Timeout configurable para operaciones Qdrant

Dado que es un MVP bootstrapped, no es necesario tener métricas de performance definidas por ahora. El timeout configurable para operaciones Qdrant se definirá según necesidad durante implementación. Monitoreo básico mediante logging estructurado según mcp-tools-specification.md es suficiente para fase inicial.

MVP Bootstrapped usa colección por proyecto (project_{project_id}) para escalar naturalmente. Qdrant v1.17.1 soporta hasta 1M vectores con latencias p50 <5ms, suficiente para MVP. No requiere sharding/replicación. Post-MVP: Estrategia (sharding, replicación, optimización HNSW) se definirá cuando se alcance transición post-MVP según ADR-003 (validación ajuste problema-solución, escalabilidad horizontal requerida).

---

## 5. Integración con Qdrant

### Cliente HTTP

- Cliente HTTP para comunicación con API de Qdrant
- Configuración de conexión (host, port, API key)
- Manejo de timeouts y errores de conexión

A nivel protocolo MCP no hay retry (MCP Server es stateless según mcp-tools-specification.md). Cuando es un job, se hace con backoff exponencial y jitter aleatorio (±20%) según ADR-005. Es una estrategia del proceso que interactúa (cliente LLM/jobs) no específica de Qdrant. Timeout configurable definido según necesidad durante implementación.

### Operaciones Principales

- **Crear colección**: `create_collection` con configuración de dimensiones
- **Insertar vectores**: `upsert` con batch de vectores y metadata
- **Buscar por similitud**: `search` con query vector y filtros
- **Eliminar vectores**: `delete` por `document_id` o filtros

### Configuración de Colección

```json
{
  "name": "documents",
  "dimension": 1024,
  "metric": "Cosine",
  "payload_schema": {
    "document_id": "uuid",
    "section_title": "text",
    "chunk_index": "integer",
    "created_at": "datetime"
  }
}
```

### Configuración de Despliegue

Configuración de Docker Compose para Qdrant según ADR-003:

```yaml
qdrant:
  image: qdrant/qdrant:v1.17.1
  ports:
    - "6333:6333"  # HTTP API
    - "6334:6334"  # gRPC API
  volumes:
    - qdrant_data:/qdrant/storage
  environment:
    - QDRANT__SERVICE__GRPC_PORT=6334
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:6333/health"]
    interval: 30s
    timeout: 10s
    retries: 3
  restart: unless-stopped

volumes:
  qdrant_data:
    driver: local
```

Verificación: `curl http://localhost:6333/health`

MVP Bootstrapped usa health check básico (`curl http://localhost:6333/health`), health check Docker Compose configurado (interval 30s), logging estructurado (`docker-compose logs qdrant`). Sin métricas avanzadas (no Prometheus/Grafana, no distributed tracing, no alerting automático). Debugging: verificar dimensiones (1024), tipo de distancia (Cosine), normalización. Comandos T-008 para pruebas.

---

## 6. MCP Tool: search_similar_documents

### Descripción

Tool MCP que permite buscar documentos similares usando búsqueda semántica en Qdrant.

### Parámetros

```json
{
  "query": "arquitectura de 5 fases",
  "limit": 5
}
```

### Respuesta

```json
{
  "results": [
    {
      "document_id": "uuid",
      "title": "Technical Brief",
      "similarity": 0.95,
      "relevant_content": "El sistema opera en cinco fases..."
    }
  ]
}
```

### Uso

No es necesario hacer un mapping explícito hacia las fases del workflow. La tool `search_similar_documents` está disponible para todos los agentes del pipeline según mcp-tools-specification.md, y su uso es determinado por cada agente según necesidad específica durante el procesamiento.

---

## 7. Referencias

- **[database-schema-audit-entities.md](database-schema-audit-entities.md)**: Tabla `vector_sync_log` para trazabilidad
- **[mcp-tools-specification.md](mcp-tools-specification.md)**: Tool `search_similar_documents`
- **[ADR-002](../decisiones/adr-002-python-unified-stack.md)**: Stack unificado Python con Qdrant
- **[FEAT-007](../../producto/funcionalidades/busqueda-semantica.md)**: Requisitos de búsqueda semántica
