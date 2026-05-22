---
id: ARC-038
type: Architecture
rating: 9.0
rating-phase: document-editing
related:
  - target: ARC-030
    relationship_type: implements
    reason: Implementa la arquitectura definida en mcp-server-architecture.md
  - target: ARC-036
    relationship_type: extends
    reason: Extiende la especificación de tools con detalles de performance y escalabilidad
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del schema de base de datos para estrategias de escalabilidad
---

# MCP Server Performance & Scalability — Alejandria

Este documento define las estrategias de performance y escalabilidad del MCP Server de Alejandria. Para la especificación de tools, ver [mcp-tools-specification.md](./mcp-tools-specification.md). Para la arquitectura general, ver [mcp-server-architecture.md](./mcp-server-architecture.md).

---

## 1. Rate Limiting

### Estrategia para MVP Bootstrapped

Para MVP Bootstrapped, no se implementa rate limiting.

**Justificación**:

- MVP Bootstrapped tiene pocos usuarios
- No requiere rate limiting inicial
- El sistema confía en auth con API keys como mecanismo de control de acceso suficiente para fase inicial

### Estrategia Post-MVP

Rate limiting se implementará en fase post-MVP cuando haya más usuarios y mayor tráfico.

**Consideraciones de implementación**:

- Rate limiting por usuario/organización
- Rate limiting por endpoint/tool
- Configuración de límites según plan de usuario
- Integración con Redis para distributed rate limiting

---

## 2. Escalabilidad de Búsqueda Semántica

### Estrategia Actual

Según database-schema-audit-entities.md, Qdrant usa una colección por proyecto (collection name: `project_{project_id}`).

**Beneficios**:

- Permite escalar por proyecto naturalmente
- Cada proyecto tiene su propia colección vectorial con sus propios metadatos (vector_size, distance_metric, embedding_model)
- Aislamiento de datos entre proyectos
- Flexibilidad para configurar parámetros por proyecto

**Para MVP Bootstrapped**:

- Esta estrategia es suficiente
- No requiere sharding o replicación compleja
- Performance adecuada para volumen esperado

### Estrategia Post-MVP

Estrategia de escalabilidad post-MVP se definirá cuando sea necesario:

**Sharding**:

- Dividir colecciones grandes en múltiples shards
- Distribuir shards entre múltiples nodos Qdrant
- Estrategia de routing de queries a shards apropiados

**Replicación**:

- Replicar colecciones para alta disponibilidad
- Load balancing de queries entre réplicas
- Consistency models (eventual vs strong)

**Optimización HNSW**:

- Tuning de parámetros HNSW (M, ef_construction)
- Balance entre precision y performance
- Estrategias de reindexing

---

## 3. Caching

### Estrategia para MVP Bootstrapped

Para MVP Bootstrapped, no se implementa caching de tools de lectura.

**Justificación**:

- MVP Bootstrapped tiene bajo volumen
- Caching añade complejidad de invalidation que no es necesaria en fase inicial
- Redis se usa solo como broker de Celery

### Estrategia Post-MVP

Caching se implementará en fase post-MVP cuando se identifiquen cuellos de botella de performance.

**Consideraciones de implementación**:

- Caching de tools de lectura (read_document, list_gaps, etc.)
- TTL configurado por tipo de tool
- Estrategia de invalidation (time-based, event-based)
- Caching distribuido con Redis

**Casos de uso de caching**:

- `read_document`: Cachear documentos frecuentemente accedidos
- `list_gaps`: Cachear listas de gaps con TTL corto
- `search_similar_documents`: Cachear resultados de búsqueda semántica

---

## 4. Performance de Transacciones

### Optimización de Queries

**Connection Pooling**:

- SQLAlchemy connection pooling configurado
- Pool size configurado según carga esperada
- Max overflow para picos de tráfico

**Query Optimization**:

- Índices en columnas frecuentemente consultadas
- Uso de `SELECT FOR UPDATE` solo cuando necesario
- Evitar N+1 queries con eager loading

**Batch Operations**:

- Batch inserts cuando sea posible
- Batch updates para operaciones masivas
- Considerar bulk operations para herramientas que procesan múltiples entidades

### Performance de Versioning

Según ADR-006, el versioning de documentos tiene overhead de performance:

**Impacto esperado**:

- Overhead estimado: SQLAlchemy before_update (<1ms) + PostgreSQL INSERT con TOAST (5-15ms para 50KB) = 6-16ms total
- Mitigación: solo snapshot si contenido cambió
- TOAST compresión automática (LZ4 60-70% más rápido en PG14)
- Estrategia híbrida (30 días full, >30 días diff)

**Criterios de aceptación**:

- <20ms por UPDATE
- <5% tiempo total de operaciones

---

## 5. Escalabilidad Horizontal

### MCP Server

**Transporte Stdio (Desarrollo Local)**:

- Un proceso por usuario
- No escala bien para múltiples usuarios
- Adecuado para desarrollo local

**Transporte HTTP (Producción)**:

- Escalable (multi-tenancy)
- Auth vía Authorization header
- Gateway centralizado
- Mejor para múltiples usuarios
- Puede escalar horizontalmente con load balancer

### Base de Datos

**PostgreSQL**:

- Connection pooling para manejar múltiples conexiones
- Read replicas para queries de lectura (post-MVP)
- Partitioning de tablas grandes (post-MVP)

**Qdrant**:

- Colecciones por proyecto para aislamiento
- Sharding para colecciones grandes (post-MVP)
- Replicación para alta disponibilidad (post-MVP)

**Redis**:

- Usado como broker de Celery
- Puede escalar con Redis Cluster (post-MVP)
- Sentinel para alta disponibilidad (post-MVP)

---

## 6. Monitoreo de Performance

### Métricas Clave

**Para MVP Bootstrapped**:

- Latencia de ejecución de tools (media, p95, p99)
- Throughput (requests por segundo)
- Error rate
- Database query latency
- Lock wait time

**Post-MVP**:

- CPU, memory, disk usage
- Network I/O
- Cache hit rate
- Connection pool utilization

### Alertas

**Para MVP Bootstrapped**:

- Alertas básicas en logs
- Monitoreo manual de health checks

**Post-MVP**:

- Alertas automáticas basadas en umbrales
- Dashboards de métricas en tiempo real
- Alerting proactivo antes de degradación

---

## 7. Capacity Planning

### MVP Bootstrapped

**Carga esperada**:

- <10 documentos/día
- <100 jobs/día
- <10 req/s
- <5 usuarios concurrentes

**Infraestructura requerida**:

- 1 instancia de MCP Server (stdio)
- 1 instancia de PostgreSQL
- 1 instancia de Qdrant
- 1 instancia de Redis

### Post-MVP

**Escalado vertical**:

- Aumentar recursos de CPU/memory
- Optimizar queries y código
- Implementar caching

**Escalado horizontal**:

- Múltiples instancias de MCP Server (HTTP)
- Load balancer para distribución de tráfico
- Read replicas de PostgreSQL
- Sharding de Qdrant

---

## Referencias

- [mcp-server-architecture.md](./mcp-server-architecture.md): Arquitectura general del MCP Server
- [mcp-tools-specification.md](./mcp-tools-specification.md): Especificación de tools
- [database-schema-design.md](./database-schema-design.md): Schema de base de datos
- [ADR-006](../decisiones/adr-006-document-versioning.md): Versioning de documentos
