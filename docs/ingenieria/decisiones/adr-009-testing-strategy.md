---
id: ADR-009
type: Architecture Decision Record
related:
  - target: ARC-005
    relationship_type: implements
    reason: Implementa la estrategia de arquitectura para testing del stack unificado Python
  - target: ARC-014
    relationship_type: references
    reason: Referencia el development-setup para documentación de fixtures y patrones de testing
---

# ADR-009: Estrategia de Testing Python para Stack Unificado

## Contexto y Problema

Alejandria requiere una estrategia de testing para el stack unificado Python (FastAPI + Celery + FastMCP). El sistema necesita:

- Cobertura de código alta para asegurar calidad
- Testing de componentes asíncronos (Celery jobs, FastMCP servers)
- Testing de integración con base de datos y servicios externos
- Testing end-to-end del pipeline de 5 fases
- Ejecución rápida de tests para desarrollo iterativo

El stack incluye componentes con características especiales: FastAPI (async web framework), Celery (distributed task queue), y FastMCP (MCP server), lo que requiere una estrategia de testing adaptada a estos componentes.

## Decisiones

**Decisión**: Usar estrategia de testing híbrida con pytest, bases de datos de pruebas separadas en docker-compose, y fixtures especializados para componentes asíncronos.

**Stack de testing**:

- **pytest**: Framework de testing principal
- **pytest-asyncio**: Testing de código async
- **pytest-cov**: Medición de cobertura de código
- **faker**: Generación de datos de prueba
- **respx**: Mocking de HTTP requests para tests unitarios

**Distribución de tests**:

- **Unit tests (70-80%)**: Lógica de negocio, services, schemas sin dependencias externas
- **Integration tests (15-20%)**: DB real (bases de datos separadas en docker-compose: POSTGRES_TEST_DB, REDIS_TEST_URL) y mocks hacia otras capas
- **E2E tests (5-10%)**: Flujos completos del pipeline de 5 fases, solo happy paths

**Cobertura objetivo**: >90%

**Configuración pytest** (`pyproject.toml`):

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--cov=alejandria",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=90"
]
```

## Justificación

### Ventajas de la Estrategia Propuesta

**Enfoque híbrido**:

- Unit tests rápidos (<1s cada uno) para feedback rápido en desarrollo
- Integration tests con DB real para validar interacciones con PostgreSQL y Redis
- E2E tests limitados a happy paths para validar flujos críticos sin overhead excesivo

**Testing de componentes asíncronos**:

- pytest-asyncio permite testing natural de código async (FastAPI, Celery, FastMCP)
- Fixtures async crean clientes in-memory para FastMCP sin overhead de red
- Mocking de Redis broker para unit tests de Celery, Redis real (bases de datos separadas en docker-compose) para integration tests

**Bases de datos separadas para integration tests**:

- PostgreSQL y Redis reales usando bases de datos separadas configuradas en docker-compose (POSTGRES_TEST_DB, REDIS_TEST_URL)
- Transaction rollback para asegurar aislamiento entre tests
- Consistencia con entorno de despliegue (Docker Compose según ADR-003)

**Cobertura alta (>90%)**:

- Asegura que la mayoría del código está testeado
- pytest-cov genera reportes detallados de cobertura
- CI/CD puede fallar si cobertura cae debajo de 90%

### Testing por Componente

**FastAPI (API Backend)**:

- Unit tests: endpoints con mocks de servicios y DB
- Integration tests: endpoints con DB real (POSTGRES_TEST_DB)
- Fixtures pytest para FastAPI TestClient
- Testing de validación Pydantic en schemas

**Celery (Jobs y Orquestación)**:

- Unit tests: tasks con mocks de broker Redis y DB
- Integration tests: tasks con Redis real (REDIS_TEST_URL) y DB real
- Testing de retry policies y error handling
- Testing de idempotencia con locks en DB

**FastMCP (MCP Server)**:

- Unit tests: tools y prompts con mocks
- Integration tests: FastMCP Client in-memory con fixtures async
- Testing de tools sin overhead de red
- Testing de prompts y respuestas

**Servicios compartidos (shared/)**:

- Unit tests: services con mocks de DB y dependencias externas
- Integration tests: services con DB real (POSTGRES_TEST_DB)
- Testing de lógica de negocio aislada de API/MCP/jobs

### Alineación con ADR-002 y ADR-007

**Stack unificado (ADR-002)**:

- ADR-002 especifica estrategia de testing con pytest y cobertura >90%
- Esta ADR implementa detalles específicos para el stack Python unificado
- Testing de Celery jobs y FastMCP servers como especificado en ADR-002

**Estructura de paquetes (ADR-007)**:

- Tests organizados según estructura de paquetes (tests/unit/, tests/integration/, tests/e2e/)
- Imports de tests siguen estructura de paquetes (e.g., `from shared.services import document_service`)
- Fixtures pytest reutilizables para componentes compartidos

## Trade-offs

### Desventajas

- **Tiempo de execution**: Integration tests con DB real son más lentos que unit tests
- **Curva de aprendizaje**: pytest-asyncio y fixtures async requieren aprendizaje

### Mitigación

- **Ejecución selectiva**: Permitir ejecutar solo unit tests en desarrollo rápido
- **Documentación de fixtures**: Documentar fixtures pytest en `development-setup.md`

## Detalles de Implementación

### Unit Tests

**Características**:

- <1s de ejecución por test
- Mocks de todas las dependencias externas (DB, Redis, HTTP APIs)
- Testing de lógica de negocio pura
- Testing de validación Pydantic en schemas

**Ejemplo de unit test**:

```python
# tests/unit/test_document_service.py
import pytest
from unittest.mock import Mock
from shared.services.document_service import DocumentService

def test_create_document():
    db_mock = Mock()
    service = DocumentService(db_mock)
    document = service.create_document(title="Test", content="Content")
    assert document.title == "Test"
    db_mock.add.assert_called_once()
```

### Integration Tests

**Características**:

- DB real (bases de datos separadas en docker-compose: POSTGRES_TEST_DB, REDIS_TEST_URL)
- Mocks de servicios externos (LLM APIs, etc.)
- Testing de interacciones con DB y cache
- 15-20% del total de tests

**Ejemplo de integration test**:

```python
# tests/integration/test_api.py
import pytest
from fastapi.testclient import TestClient
from api.main import app

@pytest.fixture(scope="function")
def db_session():
    """
    Fixture to provide a database session using docker-compose test PostgreSQL.
    Uses transaction rollback for test isolation.
    """
    from shared.config.settings import settings
    from shared.db.session import get_engine, get_session_maker
    from alembic.config import Config
    from alembic import command

    # Create engine with test database URL
    test_db_url = settings.test_database_url or settings.database_url
    test_db_url = test_db_url.replace("localhost", "postgresql")
    engine = get_engine(test_db_url)

    # Apply Alembic migrations to test database
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", test_db_url)
    command.upgrade(alembic_cfg, "head")

    # Create session with transaction rollback
    session_local = get_session_maker(engine)
    session = session_local()

    yield session

    # Cleanup: rollback transaction
    session.rollback()
    session.close()

def test_create_document_integration(db_session):
    client = TestClient(app)
    response = client.post("/documents", json={"title": "Test", "content": "Content"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test"
```

### E2E Tests

**Características**:

- Flujos completos del pipeline de 5 fases
- Solo happy paths (no testing de edge cases)
- 5-10% del total de tests
- Validación de integración end-to-end

**Ejemplo de E2E test**:

```python
# tests/e2e/test_pipeline.py
import pytest

@pytest.fixture(scope="function")
def db_session():
    """
    Fixture to provide a database session using docker-compose test PostgreSQL.
    Uses transaction rollback for test isolation.
    """
    from shared.config.settings import settings
    from shared.db.session import get_engine, get_session_maker
    from alembic.config import Config
    from alembic import command

    # Create engine with test database URL
    test_db_url = settings.test_database_url or settings.database_url
    test_db_url = test_db_url.replace("localhost", "postgresql")
    engine = get_engine(test_db_url)

    # Apply Alembic migrations to test database
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", test_db_url)
    command.upgrade(alembic_cfg, "head")

    # Create session with transaction rollback
    session_local = get_session_maker(engine)
    session = session_local()

    yield session

    # Cleanup: rollback transaction
    session.rollback()
    session.close()

def test_five_phase_pipeline_happy_path(db_session):
    # Test completo del pipeline de 5 fases
    # 1. Upload document
    # 2. Gap detection
    # 3. Suggestion application
    # 4. Vector sync
    # 5. Question generation
    assert True  # Placeholder
```

### Testing de Celery Jobs

**Unit tests** (mock broker Redis):

```python
# tests/unit/test_gap_detection_task.py
import pytest
from unittest.mock import Mock, patch
from jobs.tasks.gap_detection import gap_detection_task

@patch('jobs.tasks.gap_detection.celery_app')
def test_gap_detection_task_unit(celery_mock):
    result = gap_detection_task.apply_async(args=[1])
    assert result.status == "SUCCESS"
```

**Integration tests** (Redis real con base de datos separada en docker-compose):

```python
# tests/integration/test_gap_detection_task.py
import pytest
from jobs.tasks.gap_detection import gap_detection_task

@pytest.fixture(scope="function")
def redis_session():
    """
    Fixture to provide a Redis session using docker-compose test Redis.
    Uses REDIS_TEST_URL (database 1) for test isolation.
    """
    from shared.config.settings import settings
    import redis

    # Use test database (database 1 instead of 0)
    test_redis_url = settings.redis_test_url or settings.redis_url
    client = redis.from_url(test_redis_url)

    yield client

    # Cleanup: flush test database
    client.flushdb()
    client.close()

def test_gap_detection_task_integration(redis_session):
    result = gap_detection_task.apply_async(args=[1])
    assert result.get(timeout=10) is not None
```

### Testing de FastMCP Servers

**Unit tests** (mock tools):

```python
# tests/unit/test_mcp_tools.py
import pytest
from unittest.mock import Mock
from mcp.tools.document_analysis import analyze_document

def test_analyze_document_unit():
    llm_mock = Mock()
    result = analyze_document(llm_mock, "document content")
    assert result is not None
```

**Integration tests** (FastMCP Client in-memory):

```python
# tests/integration/test_mcp_server.py
import pytest
from mcp.server import FastMCP
from mcp.client import FastMCPClient

@pytest.fixture
async def mcp_client():
    server = FastMCP("test-server")
    server.add_tool(analyze_document)
    async with FastMCPClient(server) as client:
        yield client

@pytest.mark.asyncio
async def test_mcp_tool_integration(mcp_client):
    result = await mcp_client.call_tool("analyze_document", {"content": "test"})
    assert result is not None
```

## Alternativas Consideradas

### Solo Unit Tests

**Ventaja**: Ejecución muy rápida

**Desventaja**: No valida integraciones con DB y servicios externos

**Decisión**: Rechazada porque no valida comportamiento real del sistema

### Solo Integration Tests

**Ventaja**: Valida comportamiento real

**Desventaja**: Ejecución lenta, no escalable para desarrollo iterativo

**Decisión**: Rechazada porque no permite feedback rápido en desarrollo

### Unittest Framework (Built-in)

**Ventaja**: No requiere dependencias externas

**Desventaja**: Menos features que pytest, sin plugins para async y coverage

**Decisión**: Rechazada porque pytest proporciona mejor experiencia de desarrollo

## Consecuencias

### Impacto Positivo

- **Cobertura alta**: >90% asegura calidad de código
- **Feedback rápido**: Unit tests <1s permiten desarrollo iterativo
- **Validación real**: Integration tests con bases de datos separadas en docker-compose validan comportamiento real
- **Testing asíncrono**: pytest-asyncio y fixtures async facilitan testing de componentes asíncronos

### Impacto Negativo

- **Complejidad**: Requiere configuración de fixtures async
- **Dependencia de Docker**: Integration tests requieren Docker en entorno de CI/CD
- **Curva de aprendizaje**: pytest-asyncio y fixtures async requieren aprendizaje

### Requerimientos de Implementación

- Configurar pytest en `pyproject.toml` con plugins (pytest-asyncio, pytest-cov)
- Crear estructura de directorios de tests (tests/unit/, tests/integration/, tests/e2e/)
- Implementar fixtures pytest reutilizables (DB, Redis, FastAPI TestClient, FastMCP Client)
- Configurar bases de datos separadas en docker-compose (POSTGRES_TEST_DB, REDIS_TEST_URL)
- Documentar patrones de testing en `development-setup.md`
- Configurar CI/CD para ejecutar tests con Docker support
- Asegurar que覆盖率 >90% se mantenga en cada commit

## Referencias

- ADR-002: Python Unified Stack (estrategia de testing)
- ADR-007: Python Package Structure
- pytest documentation: <https://docs.pytest.org/>
- pytest-asyncio documentation: <https://pytest-asyncio.readthedocs.io/>
