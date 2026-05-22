---
id: ARC-032
type: Architecture
rating: 9.4
rating-phase: document-editing
related:
  - target: ARC-030
    relationship_type: implements
    reason: Implementa la arquitectura definida en mcp-server-architecture.md
  - target: ADR-003
    relationship_type: implements
    reason: Implementa la estrategia de infraestructura local definida en ADR-003
  - target: ADR-002
    relationship_type: references
    reason: Referencia la estrategia de observabilidad y testing definida en ADR-002
---

# MCP Server Deployment y Testing — Alejandria

---

Este documento define la estrategia de deployment, monitoreo y testing del MCP Server de Alejandria. Para la arquitectura general, ver [mcp-server-architecture.md](./mcp-server-architecture.md). Para la especificación de tools, ver [mcp-tools-specification.md](./mcp-tools-specification.md).

---

## 1. Despliegue

El MCP Server se despliega en producción usando Docker Compose, alineado con la estrategia de infraestructura local definida en ADR-003. La configuración del transporte (stdio vs HTTP) se maneja mediante variables de entorno.

### Estrategia de Despliegue

**Docker Compose**:

El MCP Server se despliega como servicio en Docker Compose, junto con FastAPI, PostgreSQL, Redis y Qdrant. Según la arquitectura definida en mcp-server-architecture.md sección 5, FastAPI y FastMCP se ejecutan como procesos separados pero pueden estar en el mismo container o containers separados según requerimientos de escalabilidad.

**Configuración de Transporte**:

El modo de transporte se configura mediante variable de entorno:

- `MCP_TRANSPORT=stdio`: Para desarrollo local (cliente lanza servidor como subprocess)
- `MCP_TRANSPORT=http`: Para producción (servidor maneja múltiples conexiones concurrentes)

### Variables de Entorno

La configuración del MCP Server se maneja mediante variables de entorno que controlan el modo de transporte, conexiones a bases de datos y comportamiento del logging.

**Variables requeridas** controlan aspectos fundamentales del funcionamiento del servidor:

- `MCP_TRANSPORT`: Define el modo de transporte (stdio para desarrollo local, http para producción)
- `DATABASE_URL`: URL de conexión a PostgreSQL para persistencia de datos
- `REDIS_URL`: URL de conexión a Redis para cache y message broker
- `QDRANT_URL`: URL de conexión a Qdrant para búsqueda semántica
- `LOG_LEVEL`: Nivel de logging (DEBUG, INFO, WARNING, ERROR) para controlar verbosidad

**Variables opcionales** permiten personalizar el comportamiento en modo HTTP:

- `MCP_HOST`: Host para modo HTTP (default: 0.0.0.0 para aceptar conexiones externas)
- `MCP_PORT`: Puerto para modo HTTP (default: 8000)
- `SERVER_VERSION`: Versión del servidor para registro en MCP Registry

### Integración con Infraestructura

**Desarrollo local**:

- MCP_TRANSPORT=stdio
- Cliente LLM lanza servidor como subprocess
- Comunicación vía stdin/stdout con JSON-RPC delimitado por newlines

**Producción**:

- MCP_TRANSPORT=http
- Servidor corre como proceso independiente
- Comunicación vía HTTP con auth vía Authorization header
- Escalable para multi-tenancy

### Backup y Disaster Recovery

El MCP Server comparte PostgreSQL y Redis con FastAPI (según database-schema-design.md y ADR-002). La estrategia de backup se aplica a nivel de infraestructura compartida, no específicamente al MCP Server:

- PostgreSQL tiene backups regulares (según database-schema-design.md)
- Redis es cache/broker y no requiere backup crítico para MVP Bootstrapped (puede reconstruirse desde PostgreSQL)
- El versioning de documentos (ADR-006) proporciona snapshots automáticos que actúan como backup a nivel de documento, permitiendo rollback a versiones anteriores sin necesidad de backup de base de datos completo
- RPO/RTO se definirán en fase post-MVP cuando se implemente producción

**Procedimiento de Disaster Recovery para MVP Bootstrapped**:

Para MVP Bootstrapped, el procedimiento de disaster recovery es manual usando `pg_dump` para PostgreSQL. Redis y Qdrant pueden reconstruirse desde PostgreSQL o regenerarse desde documentos. El versioning de documentos (ADR-006) proporciona snapshots automáticos para rollback a nivel de documento.

**Backup de PostgreSQL**:

```bash
docker exec postgres pg_dump -U postgres alejandria > backup.sql
```

**Restore de PostgreSQL**:

```bash
docker exec -i postgres psql -U postgres alejandria < backup.sql
```

**Reconstrucción de Redis y Qdrant**:

- Redis: Puede reconstruirse desde PostgreSQL (cache puede regenerarse)
- Qdrant: Puede regenerarse desde documentos usando el pipeline de ingestión

---

## 2. Monitoreo y Observabilidad

El MCP Server usa observabilidad básica alineada con ADR-002, sin métricas avanzadas para MVP Bootstrapped. El enfoque es logging estructurado, log aggregation y health checks básicos.

### Logging Estructurado

El MCP Server implementa logging estructurado en formato JSON para facilitar el parsing y análisis automatizado. Cada entrada de log incluye información contextual como request IDs para correlación manual entre componentes.

**Formato JSON**:

El siguiente ejemplo muestra la estructura de un log de invocación de tool:

```json
{
  "timestamp": "2026-05-26T12:00:00Z",
  "level": "INFO",
  "request_id": "uuid",
  "tool": "read_document",
  "document_id": "uuid",
  "latency_ms": 150,
  "status": "success"
}
```

Este formato permite filtrar logs por request_id específico para rastrear el flujo completo de una operación a través del sistema.

**Información logueada**:

- Invocaciones de tools (tool name, parámetros, resultado)
- Errores y excepciones (tipo, mensaje, stack trace)
- Latencia de ejecución de tools
- Request IDs para correlación manual

### Log Aggregation

**Docker Compose Logs**:

Los logs se agregan vía `docker-compose logs` para debugging y troubleshooting. No hay sistema centralizado de log aggregation (ej: ELK stack) para MVP Bootstrapped.

```bash
docker-compose logs mcp-server
docker-compose logs -f mcp-server  # Follow logs
```

### Troubleshooting Común

**Conexión fallida a PostgreSQL**:

- Síntoma: Error "connection refused" o "could not connect to server"
- Diagnóstico: `docker-compose ps postgres` (verificar si está corriendo)
- Diagnóstico: `docker-compose logs postgres` (verificar errores de inicio)
- Solución: `docker-compose restart postgres`

**Timeout de Redis**:

- Síntoma: Error "Redis connection timeout" o "connection refused"
- Diagnóstico: `docker exec redis redis-cli ping` (verificar si responde)
- Diagnóstico: `docker-compose logs redis` (verificar errores)
- Solución: `docker-compose restart redis`

**Error de Qdrant**:

- Síntoma: Error "Qdrant connection failed" o "collection not found"
- Diagnóstico: `curl http://localhost:6333/healthz` (verificar health check)
- Diagnóstico: `docker-compose logs qdrant` (verificar errores)
- Solución: `docker-compose restart qdrant` o recrear colección

**Variable de entorno faltante**:

- Síntoma: Error "KeyError" o "Environment variable not set"
- Diagnóstico: `docker-compose config` (verificar configuración)
- Diagnóstico: Verificar archivo `.env` existe y tiene variables requeridas
- Solución: Agregar variable faltante a `.env` y `docker-compose up -d`

**Proceso de Debugging**:

1. **Verificar health check**: `curl http://localhost:8000/health` o verificar `docker-compose ps`
2. **Revisar logs de MCP Server**: `docker-compose logs mcp-server` con filtros por request_id
3. **Revisar logs de servicios dependientes**: `docker-compose logs postgres`, `docker-compose logs redis`, `docker-compose logs qdrant`
4. **Verificar conectividad de red**: `docker network inspect`, verificar puertos mapeados
5. **Validar configuración de variables de entorno**: `docker-compose config`, verificar archivo `.env`

### Health Checks

**Health Check Básico**:

El MCP Server expone un endpoint básico de health check para verificar disponibilidad:

```http
GET /health
```

**Response**:

```json
{
  "status": "healthy",
  "timestamp": "2026-05-26T12:00:00Z",
  "version": "1.0.0"
}
```

**Integración con Docker Compose**:

Docker Compose usa health checks para verificar que el MCP Server esté disponible antes de iniciar servicios dependientes.

**Thresholds de Health Check**:

Para MVP Bootstrapped, los thresholds se enfocan en health checks y conexiones de base de datos:

- Health check falla: Verificar si servicio está corriendo (`docker-compose ps`)
- Health check falla > 3 veces consecutivas: Reiniciar servicio (`docker-compose restart <servicio>`)

**Thresholds de Database Connection**:

- Connection errors en PostgreSQL: Verificar si contenedor está corriendo
- Connection errors en Redis: Verificar si Redis acepta conexiones (`docker exec redis redis-cli ping`)
- Connection errors en Qdrant: Verificar si Qdrant está accesible en puerto 6333

### Sin Métricas Avanzadas

Para MVP Bootstrapped, el MCP Server no incluye:

- **Sin Prometheus/Grafana**: No hay métricas de time series
- **Sin distributed tracing**: No hay tracing distribuido (ej: OpenTelemetry)
- **Sin alerting automático**: No hay alertas automáticas basadas en métricas
- **Sin dashboards**: No hay dashboards de monitoreo en tiempo real

Esta alineación con ADR-002 (líneas 198-203) reduce complejidad operacional para fase bootstrapped. Métricas avanzadas pueden considerarse en fase post-MVP si se requiere escalabilidad masiva.

---

## 3. Estrategia de Testing

El MCP Server usa una estrategia de testing alineada con ADR-002, basada en pytest, testcontainers y FastMCP Client. La distribución de tests es unit (70-80%), integration (15-20%), E2E (5-10%) con cobertura objetivo >90%.

### Stack de Testing

El stack de testing combina herramientas estándar de Python con FastMCP Client para testing de MCP servers. Esta combinación permite tests rápidos y confiables sin overhead de red.

**Herramientas**:

- **pytest**: Framework de testing principal para organizar y ejecutar tests
- **pytest-asyncio**: Soporte para tests asíncronos necesario para MCP operations
- **testcontainers**: Bases de datos reales para integration tests (PostgreSQL, Redis)
- **FastMCP Client**: Cliente MCP para testing de servers in-memory sin overhead de red

**Configuración**:

La configuración de pytest habilita el modo automático para tests asíncronos:

```toml
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

### Distribución de Tests

La distribución de tests sigue el principio de testing pyramid con énfasis en unit tests para MVP Bootstrapped. Esta distribución balancea velocidad de ejecución con confianza en el comportamiento del sistema.

**Unit Tests (70-80%)**:

Unit tests validan lógica de negocio de tools sin dependencias externas, incluyendo validación de schemas con Pydantic. Estos tests son rápidos (<1s cada uno) y proporcionan feedback inmediato durante desarrollo.

**Integration Tests (15-20%)**:

Integration tests validan la integración del MCP Server con FastMCP Client in-memory y bases de datos reales usando testcontainers (PostgreSQL, Redis). Se mockean otras capas cuando no son críticas para el test. Estos tests toman 1-5s cada uno y validan que los componentes funcionen correctamente juntos.

**E2E Tests (5-10%)**:

E2E tests validan flujos completos del pipeline con LLM real (Ollama) y comunicación end-to-end vía protocolo MCP. Estos tests son más lentos (5-30s cada uno) pero proporcionan confianza en que el sistema funciona en condiciones reales.

### Testing de MCP Servers

**FastMCP Client**:

FastMCP Client permite testing de MCP servers in-memory sin overhead de red, lo que hace tests más rápidos y confiables. El cliente se crea directamente desde la instancia del servidor sin necesidad de configuración de red.

```python
from fastmcp import Client

async def test_read_document():
    client = Client.from_server(mcp_server)
    result = await client.call_tool("read_document", {"document_id": "uuid"})
    assert result["title"] == "Technical Brief"
```

Este enfoque permite validar la lógica de tools sin preocuparse por configuración de transporte o conectividad de red.

**Fixtures Async**:

Fixtures async crean Client in-memory para cada test, asegurando aislamiento entre tests y cleanup automático:

```python
@pytest_asyncio.fixture
async def mcp_client():
    server = create_test_mcp_server()
    client = Client.from_server(server)
    yield client
    await client.close()
```

El fixture crea un servidor de prueba, inicializa el cliente, lo yield al test, y asegura que el cliente se cierre correctamente después del test.

### Testing con Testcontainers

**PostgreSQL y Redis Reales**:

Integration tests usan bases de datos reales con testcontainers para validar que el código funciona con bases de datos reales, no solo mocks. Testcontainers maneja el ciclo de vida de los contenedores automáticamente.

```python
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

@pytest_asyncio.fixture
async def postgres_container():
    with PostgresContainer("postgres:15") as postgres:
        yield postgres.get_connection_url()

@pytest_asyncio.fixture
async def redis_container():
    with RedisContainer("redis:7") as redis:
        yield redis.get_connection_url()
```

Los fixtures crean contenedores temporales, yield la URL de conexión, y aseguran que los contenedores se detengan y limpien después del test.

### Estrategia de Mocking

**Mock de LLM Provider**:

Para unit tests, se mockea el LLM provider para evitar dependencias externas y hacer tests determinísticos:

```python
from unittest.mock import AsyncMock

@pytest_asyncio.fixture
async def mock_llm_client():
    client = AsyncMock()
    client.generate.return_value = {"content": "Test response"}
    yield client
```

El mock permite controlar la respuesta del LLM y testear lógica de negocio sin llamar al LLM real.

**Mock de Dependencias Externas**:

Qdrant y Ollama se mockean en integration tests cuando no son críticos para el test, reduciendo dependencias y tiempo de ejecución:

```python
@pytest_asyncio.fixture
async def mock_qdrant_client():
    client = AsyncMock()
    client.search.return_value = []
    yield client
```

Este enfoque permite testear lógica que depende de Qdrant sin iniciar un contenedor real.

### Cobertura Objetivo

**Cobertura >90%**:

Según ADR-002, el objetivo es >90% de cobertura con distribución:

- Unit tests: 70-80%
- Integration tests: 15-20%
- E2E tests: 5-10%

**Medición de Cobertura**:

La cobertura se mide usando pytest-cov con reportes HTML y terminal:

```bash
pytest --cov=app --cov-report=html --cov-report=term
```

El reporte HTML permite ver qué líneas de código no están cubiertas por tests, mientras que el reporte terminal muestra un resumen rápido.

### Testing de Errores

**Test de Errores Específicos**:

Cada tool debe tener tests para sus errores específicos, asegurando que el manejo de errores sea correcto:

```python
async def test_read_document_not_found():
    with pytest.raises(DocumentNotFoundError):
        await read_document(document_id="nonexistent")
```

Este test verifica que la excepción correcta se lance cuando un documento no existe.

**Test de Retry Logic**:

Tests para verificar retry logic con backoff exponencial, asegurando que el sistema se recupere de errores transitorios:

```python
async def test_tool_retry_on_server_error():
    with patch("tool.execute", side_effect=[ServerError(), ServerError(), "success"]):
        result = await tool.execute()
        assert result == "success"
```

Este test simula dos fallos seguidos de un éxito, verificando que la retry logic funcione correctamente.

### Testing de Idempotencia

**Test de Idempotencia**:

Tests para verificar que tools son idempotentes según ADR-005, asegurando que operaciones repetidas no creen duplicados:

```python
async def test_create_gap_idempotent():
    gap1 = await create_gap(document_id="uuid", question="Test?")
    gap2 = await create_gap(document_id="uuid", question="Test?")
    assert gap1["id"] == gap2["id"]  # Same gap, not duplicate
```

Este test verifica que crear el mismo gap dos veces devuelve el mismo gap en lugar de crear duplicados.

### Testing de Versioning

**Test de Versioning de Documentos**:

Tests para verificar versioning automático según ADR-006, asegurando que cada cambio cree una nueva versión:

```python
async def test_document_versioning():
    doc = await read_document(document_id="uuid")
    await write_document(document_id="uuid", content="Updated")
    versions = await list_document_versions(document_id="uuid")
    assert len(versions) == 2
```

Este test verifica que cada escritura cree una nueva versión del documento.

### Testing de Performance

**Test de Latencia**:

Tests para verificar latencia aceptable, asegurando que las operaciones no sean lentas:

```python
async def test_tool_latency():
    start = time.time()
    await read_document(document_id="uuid")
    latency = time.time() - start
    assert latency < 1.0  # <1s latency
```

Este test verifica que la operación complete en menos de 1 segundo, identificando regresiones de performance.

### CI/CD Integration

**GitHub Actions**:

GitHub Actions ejecuta tests automáticamente en cada push y pull request, asegurando que el código siempre pase tests antes de merge:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest --cov=app --cov-report=xml
      - uses: codecov/codecov-action@v3
```

El workflow instala dependencias, ejecuta tests con cobertura, y reporta cobertura a Codecov para tracking histórico.
