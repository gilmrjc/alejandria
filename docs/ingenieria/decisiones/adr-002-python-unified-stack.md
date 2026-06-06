---
id: ADR-002
type: Architecture Decision Record
rating: 9
rating-phase: document-editing
related:
  - target: ARC-003
    relationship_type: implements
    reason: Implementa la arquitectura general del sistema con stack unificado Python
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del schema de base de datos para persistencia
  - target: ARC-021
    relationship_type: references
    reason: Referencia el testing-strategy para estrategia de testing del stack Python
  - target: ADR-001
    relationship_type: reinforces
    reason: Refuerza la decisión de MCP al definir FastMCP como implementación específica
  - target: ADR-004
    relationship_type: extends
    reason: Extiende las decisiones de jobs con estrategia específica de Celery
  - target: ADR-005
    relationship_type: extends
    reason: Extiende las decisiones de jobs con estrategia de idempotencia
  - target: ADR-006
    relationship_type: extends
    reason: Extiende el stack con estrategia de versioning de documentos
---

# ADR-002: Stack Unificado en Python (FastAPI + Celery + FastMCP)

## Contexto y Problema

Alejandria requiere seleccionar un stack tecnológico para implementar su arquitectura de 5 fases. El sistema requiere:

- API REST para orquestación de entidades y gestión de estados
- Sistema de cola de trabajos para ejecución de tareas efímeras
- MCP Server para comunicación con LLMs
- Integración profunda con herramientas LLM y MCP

Alternativas consideradas inicialmente incluyeron Rails 8 vs Elixir/Phoenix para API, y Nomad vs Sidekiq/Oban para jobs, pero estas no consideraban la madurez del ecosistema Python para LLM/MCP.

## Decisiones

**Decisión**: Usar un stack unificado en Python para todos los componentes backend:

1. **API Backend**: Python (FastAPI)
2. **Jobs y Orquestación**: Python (Celery)
3. **MCP Server**: Python (FastMCP)

**Implementación específica**:

- FastAPI 0.135.0 para API REST con async nativo y type safety con Pydantic
- Celery 5.5.0 para sistema de colas nativo de Python
- FastMCP 3.2.0 para MCP Server con integración nativa con FastAPI
- PostgreSQL como base de datos con Alembic 1.17.0 para migrations
- Pydantic 2.12.0 para validación de datos y type safety
- uv para gestión de dependencias Python (lock files reproducibles, pyproject.toml estándar)

**Criterio de versionado**: Aplicar "última versión estable menos un minor" para todas las dependencias del stack Python. Este criterio balancea estabilidad con features recientes y permite upgrades predecibles con semver. ADR-003 seguirá esta convención para infraestructura.

## Justificación

### Ventajas del Ecosistema Python para LLM/MCP

**Ecosistema maduro de herramientas para LLM**:

- La generación del servidor MCP está más desarrollada en Python
- Bibliotecas extensas para MCP y integraciones LLM
- Comunidades activas en LangChain, OpenAI, Anthropic, etc.
- Herramientas de orquestación y tool calling bien establecidas

**Integración nativa y reducción de complejidad**:

- Usar un stack unificado en Python permite integración directa entre componentes
- Elimina la necesidad de bridges o APIs entre diferentes lenguajes
- Reduce complejidad operacional al tener un solo lenguaje de backend
- Facilita debugging y troubleshooting al tener consistencia tecnológica

**Type safety y async nativo**:

- FastAPI proporciona type safety con Pydantic
- Async nativo para mejor performance en operaciones I/O intensivas
- Validación automática de requests y responses
- Documentación automática de API con OpenAPI/Swagger

### Alineación con Principios Estratégicos

**Baja Fricción**:

- Stack unificado reduce fricción operacional
- Menor curva de aprendizaje al tener un solo lenguaje
- Integración nativa elimina necesidad de configurar bridges entre componentes

**Calidad Automática**:

- Pydantic proporciona validación automática de datos
- Type safety reduce bugs en tiempo de desarrollo
- Ecosistema Python maduro con herramientas de testing robustas (pytest)

### Análisis por Componente

**API Backend (FastAPI)**:

- Ventajas: Ecosistema maduro de herramientas para LLM, bibliotecas extensas para MCP y integraciones LLM, type safety con Pydantic, async nativo, comunidad activa
- Casos de uso: Ideal cuando se requiere integración profunda con herramientas LLM y MCP
- Justificación: La generación del servidor MCP, las herramientas y las integraciones LLM están más desarrolladas en Python. Usar Python permite aprovechar este ecosistema maduro y reduce la fricción de integración.

**Jobs y Orquestación (Celery)**:

- Ventajas: Ecosistema nativo de Python, integración directa con FastAPI, simplicidad operacional, menor overhead, soporte para async, features avanzadas de monitoreo y retry
- Casos de uso: Ideal cuando se usa Python para el API backend y se quiere integración nativa sin infraestructura distribuida compleja
- Justificación: Usar Celery como sistema de colas nativo de Python permite integración directa con el stack de Python, reduce complejidad operacional y elimina la necesidad de Nomad. Celery fue seleccionado sobre RQ por sus features avanzadas de monitoreo, retry policies, y mejor ecosistema de herramientas. RQ fue descartado en favor de Celery por su robustez y capacidades superiores para el sistema de colas de Alejandria.

**MCP Server (FastMCP)**:

- Ventajas: Ecosistema maduro de herramientas para LLM, bibliotecas extensas, comunidad activa, integración nativa con FastAPI
- Casos de uso: Ideal cuando el stack backend es Python y se requiere integración profunda con herramientas LLM
- Justificación: Dado que el API backend es Python, usar Python para el MCP Server permite integración nativa y aprovecha el ecosistema maduro de herramientas LLM en Python. FastAPI y FastMCP se ejecutan como procesos separados pero no se comunican vía HTTP. Dado que MCP está dentro de la misma infraestructura y tiene acceso al mismo código, puede obtener la información y realizar procesos de forma directa. El shared state se maneja vía PostgreSQL y Redis compartidos, permitiendo que FastMCP acceda directamente a datos y código sin overhead de comunicación HTTP.

**Justificación técnica detallada de FastMCP**:

FastMCP se eligió sobre el SDK oficial de MCP y otras implementaciones por las siguientes razones:

1. **Integración nativa con stack Python unificado**: Reduce complejidad operacional al tener un solo lenguaje (FastAPI + Celery + FastMCP)
2. **API minimalista**: Con un solo decorator `@mcp.tool()` cualquier función se registra como tool, eliminando boilerplate repetitivo del SDK oficial
3. **Soporte múltiple de transporte**: SSE (streaming real-time), Stdio (CLI local), Memory (testing), HTTP/REST (FastAPI integration)
4. **Integración seamless con FastAPI**: Genera automáticamente documentación OpenAPI
5. **Ecosistema maduro**: FastMCP es el framework estándar de Python para MCP, powering 70% de MCP servers worldwide
6. **Compatibilidad con SDK oficial**: FastMCP es un wrapper sobre el MCP Python SDK oficial
7. **Alineación con estrategia de jobs efímeros (ADR-004)**: FastMCP se integra nativamente con Celery para ejecución asíncrona de tools
8. **Testing simplificado**: FastMCP Client con pytest-asyncio permite testing in-memory sin overhead de red (alineado con testing-strategy.md)

## Trade-offs

### Desventajas

- **Performance vs Elixir/Phoenix**: Python puede ser más lento que Elixir para concurrencia masiva
- **Menor fault tolerance que Nomad**: Celery no tiene las capacidades de fault tolerance y auto-scaling de Nomad
- **Global Interpreter Lock (GIL)**: Python tiene limitaciones para true parallelism en CPU-bound tasks

### Mitigación

- **Async nativo**: FastAPI y Celery soportan async para mejor performance en I/O operations
- **Jobs efímeros**: Implementar jobs efímeros con Redis distributed locks (celery_once) para idempotencia. Jobs efímeros son tareas asíncronas de corta duración que se ejecutan en workers de Celery para procesar operaciones específicas del pipeline de 5 fases. No mantienen estado persistente entre ejecuciones; su estado se guarda en la base de datos (tabla `jobs`) para trazabilidad.

  **Lifecycle de jobs efímeros**:
  1. Encolado por API
  2. Ejecución por worker Celery
  3. Retry si falla (backoff exponencial, máximo 5 reintentos)
  4. Completado (`completed` en tabla `jobs`) o Fallido (`failed` con error_message)
  5. Cleanup del proceso
- **Escalabilidad horizontal**: API stateless con load balancer para distribuir carga
- **Optimización de queries**: PostgreSQL con connection pooling y caching con Redis
- **Performance**: FastAPI maneja ~15,000-20,000 req/s (benchmarks independientes). Para MVP Bootstrapped, carga esperada es <10 documentos/día, <100 jobs/día, <10 req/s. FastAPI es >1000x suficiente para carga esperada.

  **Análisis Python vs Elixir**:
  - Ecosistema LLM Python es maduro (LangChain, OpenAI, Anthropic, FastMCP)
  - Elixir tiene ecosistema limitado para LLM/MCP
  - Phoenix (Elixir): >300,000 conexiones WebSocket concurrentes en servidor 4-core/16GB RAM gracias a BEAM VM
  - La capacidad de Phoenix para millones de conexiones es overkill para MVP Bootstrapped
  - Conclusión: ecosistema LLM maduro de Python outweighs ventaja de performance de Elixir para fase actual; post-MVP se puede migrar si se requiere escalabilidad masiva

## Alternativas Consideradas

### Rails 8 para API Backend

**Ventaja**: Ecosistema Rails maduro, convención sobre configuración

**Desventaja**: Menor madurez en integraciones LLM/MCP comparado con Python

**Decisión**: Rechazada porque el ecosistema Python para LLM/MCP es más maduro y proporciona mejor integración con MCP Server.

### Elixir/Phoenix para API Backend

**Ventaja**: Mejor performance para concurrencia masiva, fault tolerance superior

**Desventaja**: Menor ecosistema de herramientas LLM/MCP, curva de aprendizaje más alta

**Decisión**: Rechazada porque el ecosistema Python para LLM/MCP es más maduro y proporciona mejor integración con MCP Server. La diferencia en performance no es crítica para la fase bootstrapped.

### Nomad para Jobs y Orquestación

**Ventaja**: Cloud-native, escalabilidad horizontal robusta, soporte para jobs efímeros

**Desventaja**: Mayor complejidad operacional, curva de aprendizaje más alta

**Decisión**: Rechazada para fase bootstrapped porque Celery proporciona integración nativa con stack Python y menor complejidad operacional. Nomad puede considerarse en fase post-inversión si se requiere escalabilidad masiva.

### Stack Híbrido (Python + Otro Lenguaje)

**Ventaja**: Podría aprovechar fortalezas de múltiples lenguajes

**Desventaja**: Mayor complejidad operacional, bridges entre componentes, curva de aprendizaje más alta

**Decisión**: Rechazada porque un stack unificado reduce complejidad operacional y proporciona mejor integración entre componentes.

## Consecuencias

### Impacto Positivo

- **Integración nativa**: Todos los componentes backend en Python permiten integración directa
- **Menor complejidad operacional**: Un solo lenguaje reduce curva de aprendizaje y debugging
- **Ecosistema LLM/MCP maduro**: Aprovechamiento de herramientas y bibliotecas bien establecidas
- **Type safety**: Pydantic proporciona validación automática y reduce bugs

### Impacto Negativo

- **Performance**: Python puede ser más lento que alternativas como Elixir para concurrencia masiva
- **Escalabilidad**: Celery no tiene las capacidades de auto-scaling de Nomad
- **GIL**: Limitaciones para true parallelism en CPU-bound tasks

### Requerimientos de Implementación

**Stack Tecnológico**:

- FastAPI con Pydantic para type safety y validación
- Celery para sistema de colas con Redis como broker
- FastMCP para MCP Server con integración con FastAPI
- PostgreSQL con Alembic para migrations
- Redis para caching y broker de colas
- uv para gestión de dependencias Python

**Estrategia de Jobs (Celery)**:

- Retry policy con backoff exponencial con jitter aleatorio (1s, 2s, 4s, 8s, 16s con ±20% jitter)
- Máximo 5 reintentos por defecto
- Timeout de 5 minutos para todos los jobs
- Excepciones retryables: network errors, timeouts, temporary failures
- Excepciones no retryables: validation errors, data integrity errors, business logic errors
- Dead letter queue: jobs que fallan después de 5 reintentos se marcan como `failed` en tabla `jobs` con error_message

**Observabilidad**:

- Logging estructurado JSON con request IDs para correlación manual
- Log aggregation vía Docker Compose logs (`docker-compose logs`)
- Health checks básicos en Docker Compose para verificar disponibilidad
- Sin metrics (Prometheus/Grafana), sin distributed tracing, sin alerting automático para MVP Bootstrapped

**Despliegue**:

- Dockerfile multi-stage (stage 1: uv para instalar dependencias, stage 2: runtime)
- Docker Compose incluye servicio de aplicación Python que depende de servicios de datos
- Script run.py es punto de entrada unificado para iniciar API, workers, o MCP server dentro del container
- Frontend (React) en Docker container separado

**Estrategia de Testing**:

- Cobertura objetivo: >90% con pytest
- Unit tests (70-80%, <1s cada uno): lógica de negocio, services, schemas sin dependencias externas
- Integration tests (15-20%): DB real (bases de datos separadas en docker-compose: POSTGRES_TEST_DB, REDIS_TEST_URL) y mocks hacia otras capas
- E2E tests (5-10%): flujos completos del pipeline de 5 fases, solo happy paths
- Testing de jobs asíncronos (Celery): pytest-asyncio, mockear broker Redis para unit tests, usar Redis real (REDIS_TEST_URL) para integration tests
- Testing de MCP servers: FastMCP Client con pytest-asyncio y fixtures async que crean Client in-memory para interactuar con servidor MCP sin overhead de red
- Configuración pytest: `asyncio_mode = "auto"` en pyproject.toml

## Referencias

- technology-strategy.md: Sección "Stack Tecnológico Recomendado"
- technology-strategy.md: Sección "Jobs y Orquestación"
- technology-strategy.md: Sección "MCP Server"
