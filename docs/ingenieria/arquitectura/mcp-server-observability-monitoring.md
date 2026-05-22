---
id: ARC-039
type: Architecture
rating: 9.0
rating-phase: document-editing
related:
  - target: ARC-030
    relationship_type: implements
    reason: Implementa la arquitectura definida en mcp-server-architecture.md
  - target: ARC-036
    relationship_type: extends
    reason: Extiende la especificación de tools con detalles de observabilidad y monitoreo
  - target: ARC-032
    relationship_type: references
    reason: Referencia la estrategia de deployment y testing para monitoreo
---

# MCP Server Observability & Monitoring — Alejandria

Este documento define las estrategias de observabilidad y monitoreo del MCP Server de Alejandria. Para la especificación de tools, ver [mcp-tools-specification.md](./mcp-tools-specification.md). Para la arquitectura general, ver [mcp-server-architecture.md](./mcp-server-architecture.md). Para deployment y testing, ver [mcp-deployment-testing.md](./mcp-deployment-testing.md).

---

## 1. Logging

### Logging Estructurado

El MCP Server usa logging estructurado en formato JSON para facilitar análisis y debugging.

**Formato de logs**:

```json
{
  "timestamp": "2026-06-02T12:00:00Z",
  "level": "INFO",
  "request_id": "uuid",
  "tool_name": "read_document",
  "parameters": {"document_id": "uuid", "include_metadata": false},
  "result": "success",
  "latency_ms": 15,
  "error": null
}
```

**Campos incluidos**:

- `timestamp`: Timestamp del evento
- `level`: Nivel de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `request_id`: ID único de la request para correlación
- `tool_name`: Nombre de la tool invocada
- `parameters`: Parámetros de la tool (sanitizados)
- `result`: Resultado de la ejecución (success, error)
- `latency_ms`: Latencia de ejecución en milisegundos
- `error`: Error message si aplica

### Niveles de Logging

**DEBUG**: Información detallada para debugging

- Internal state changes
- Database queries
- Validation steps

**INFO**: Información general de operación

- Tool invocations
- Successful operations
- System events

**WARNING**: Eventos inesperados pero no críticos

- Retries de operaciones
- Slow queries (>1s)
- Rate limiting接近 límites

**ERROR**: Errores que no interrumpen operación

- Validation errors
- Transient failures
- External service errors

**CRITICAL**: Errores críticos que interrumpen operación

- Database connection failures
- System crashes
- Security violations

### Request IDs

Cada request MCP tiene un `request_id` único para correlación de logs:

- Generado al inicio de la request
- Incluido en todos los logs de esa request
- Permite tracear el flujo completo de una request
- Facilita debugging de problemas complejos

---

## 2. Métricas

### Métricas para MVP Bootstrapped

Para MVP Bootstrapped, el MCP Server incluye métricas básicas:

**Latencia de ejecución de tools**:

- Media, p95, p99 de latencia por tool
- Latencia total de requests
- Latencia de operaciones de base de datos

**Throughput**:

- Requests por segundo
- Tools invocadas por segundo
- Errors por segundo

**Error rate**:

- Total de errors
- Error rate por tool
- Error rate por tipo de error

**Health checks básicos**:

- Disponibilidad del servidor
- Conectividad con PostgreSQL
- Conectividad con Qdrant
- Conectividad con Redis

### Métricas Post-MVP

Post-MVP se implementarán métricas avanzadas:

**System metrics**:

- CPU usage
- Memory usage
- Disk I/O
- Network I/O

**Database metrics**:

- Connection pool utilization
- Query latency
- Lock wait time
- Deadlocks

**Cache metrics**:

- Cache hit rate
- Cache miss rate
- Cache size
- Eviction rate

**Business metrics**:

- Documents processed
- Gaps detected
- Proposals created
- Sessions completed

---

## 3. Health Checks

### Health Check Endpoint

El MCP Server expone un endpoint de health check para monitoreo de disponibilidad.

**Endpoint**: `GET /health`

**Response**:

```json
{
  "status": "healthy",
  "timestamp": "2026-06-02T12:00:00Z",
  "checks": {
    "database": "healthy",
    "qdrant": "healthy",
    "redis": "healthy"
  }
}
```

**Checks realizados**:

- **Database**: Conectividad con PostgreSQL
- **Qdrant**: Conectividad con Qdrant
- **Redis**: Conectividad con Redis

**Estados posibles**:

- `healthy`: Todos los checks pasan
- `degraded`: Algunos checks fallan pero el servidor funciona
- `unhealthy`: Checks críticos fallan, servidor no funciona

### Liveness Probe

Verifica que el servidor esté respondiendo:

- Simplemente verifica que el endpoint `/health` responda
- No verifica dependencias externas
- Usado por Kubernetes/docker para reiniciar si no responde

### Readiness Probe

Verifica que el servidor esté listo para recibir tráfico:

- Verifica que todas las dependencias estén disponibles
- Verifica que el servidor pueda procesar requests
- Usado por Kubernetes/docker para enrutar tráfico

---

## 4. Retry Strategy

### Estrategia Actual

Según mcp-server-architecture.md y ADR-005, el MCP Server es stateless y no implementa retry automático.

**Justificación**:

- El cliente LLM es responsable de reintentar tools cuando fallan
- El MCP Server solo retorna códigos de error JSON-RPC apropiados
- Esto simplifica la implementación del servidor
- Permite que el cliente decida la estrategia de retry apropiada

### Códigos de Error JSON-RPC

El MCP Server retorna códigos de error para que el cliente decida si reintentar:

- `-32603` (Internal Error): Error inesperado, puede ser seguro reintentar
- `-32000` (Server Error): Error del servidor, puede ser seguro reintentar
- `-32001` (Request Failed): Error específico de la request, revisar antes de reintentar
- `-32700` (Parse Error): Error de parseo, no reintentar
- `-32600` (Invalid Request): Request inválida, no reintentar
- `-32601` (Method Not Found): Tool no existe, no reintentar
- `-32602` (Invalid Params): Parámetros inválidos, no reintentar

### Retry Strategy del Cliente

ADR-005 especifica backoff exponencial con jitter aleatorio (±20%) para reducir presión en sistemas externos:

```python
def retry_with_backoff(func, max_retries=5):
    for attempt in range(max_retries):
        try:
            return func()
        except RetryableError as e:
            if attempt == max_retries - 1:
                raise
            delay = (2 ** attempt) * 1000  # backoff exponencial
            jitter = random.uniform(-0.2, 0.2) * delay  # jitter ±20%
            time.sleep(max(0, delay + jitter))
```

---

## 5. Circuit Breakers

### Estrategia Actual

Para MVP Bootstrapped, no se implementan circuit breakers específicos.

**Justificación**:

- MVP Bootstrapped tiene bajo volumen
- No requiere protección avanzada contra cascading failures
- La estrategia de retry del cliente es suficiente

### Estrategia Post-MVP

Post-MVP se implementarán circuit breakers para proteger contra cascading failures:

**Implementación**:

- Circuit breaker por servicio externo (PostgreSQL, Qdrant, Redis)
- Estados: CLOSED, OPEN, HALF_OPEN
- Thresholds configurables (failure rate, timeout)
- Auto-recovery después de cooldown period

**Beneficios**:

- Previene cascading failures
- Permite degradación graceful
- Mejora resiliencia del sistema

---

## 6. Distributed Tracing

### Estrategia para MVP Bootstrapped

Para MVP Bootstrapped, no se implementa distributed tracing.

**Justificación**:

- MVP Bootstrapped tiene arquitectura simple
- Request IDs son suficientes para correlación
- Distributed tracing añade complejidad operacional

### Estrategia Post-MVP

Post-MVP se implementará distributed tracing con OpenTelemetry:

**Implementación**:

- Traces distribuidos across MCP Server, FastAPI, Celery
- Spans para cada operación significativa
- Integración con Jaeger o similar
- Correlación con request IDs existentes

**Beneficios**:

- Visibilidad end-to-end de requests
- Identificación de cuellos de botella
- Debugging de problemas complejos
- Análisis de performance

---

## 7. Alerting

### Estrategia para MVP Bootstrapped

Para MVP Bootstrapped, el alerting es manual basado en logs:

- Revisión periódica de logs
- Monitoreo manual de health checks
- Alertas informales via Slack/email

### Estrategia Post-MVP

Post-MVP se implementará alerting automático:

**Alertas críticas**:

- Server down (health check falla)
- Error rate > 5%
- Latencia p99 > 1s
- Database connection failures

**Alertas de warning**:

- Error rate > 1%
- Latencia p95 > 500ms
- CPU usage > 80%
- Memory usage > 80%

**Canales de alerting**:

- PagerDuty para alertas críticas
- Slack para alertas de warning
- Email para resúmenes diarios

---

## 8. Dashboards

### Estrategia para MVP Bootstrapped

Para MVP Bootstrapped, no se implementan dashboards automatizados.

**Justificación**:

- MVP Bootstrapped tiene bajo volumen
- Revisión manual de logs es suficiente
- Dashboards añaden complejidad operacional

### Estrategia Post-MVP

Post-MVP se implementarán dashboards con Grafana:

**Dashboards principales**:

- **Overview**: Métricas generales del sistema
- **Performance**: Latencia y throughput
- **Errors**: Error rate y tipos de errores
- **Infrastructure**: CPU, memory, disk, network
- **Business**: Documents, gaps, proposals, sessions

**Beneficios**:

- Visibilidad en tiempo real del sistema
- Identificación rápida de problemas
- Análisis de tendencias
- Capacity planning

---

## Referencias

- [mcp-server-architecture.md](./mcp-server-architecture.md): Arquitectura general del MCP Server
- [mcp-tools-specification.md](./mcp-tools-specification.md): Especificación de tools
- [mcp-deployment-testing.md](./mcp-deployment-testing.md): Deployment y testing
- [ADR-005](../decisiones/adr-005-job-idempotency.md): Idempotencia y retry strategy
