---
id: T-027
type: Task
rating: 9.0
rating-phase: document-editing
related:
  - target: EPC-002
    relationship_type: implements
    reason: Implementa la épica de API REST y MCP Server con testing básico
  - target: T-016
    relationship_type: depends_on
    reason: Depende de los schemas Pydantic en T-016 para testing
  - target: T-023
    relationship_type: depends_on
    reason: Depende del MCP Server en T-023 para testing
---

# T-027: Implementar Testing Básico

**Tipo**: Task
**Prioridad**: Alta
**Estimación**: 8 horas
**Dependencias**: EPC-002, T-016, T-023

## Descripción

Implementar unit tests básicos para componentes principales. Integration tests usan bases de datos separadas para testing (POSTGRES_TEST_DB y REDIS_TEST_URL) para aislar el ambiente de pruebas del ambiente de desarrollo. Testing de MCP servers usa FastMCP Client in-memory. Testing de jobs asíncronos usa pytest-asyncio con modo automático.

## Criterios de Aceptación

- [ ] pytest configurado
- [ ] Unit tests para Pydantic schemas
- [ ] Unit tests para services de negocio
- [ ] Integration tests usando bases de datos separadas (POSTGRES_TEST_DB y REDIS_TEST_URL)
- [ ] Testing de MCP servers con FastMCP Client in-memory
- [ ] Testing de funciones async de FastMCP con pytest-asyncio (asyncio_mode = auto, testing directo de funciones async, fixture genérica para async + fixtures específicas para dependencias, estrategia mixta: mockear para unit tests, usar reales para integration tests async)
- [ ] Cobertura >70% objetivo inicial

## Archivos a Crear

```
tests/
  ├── __init__.py
  ├── conftest.py
  ├── test_schemas/
  │   ├── __init__.py
  │   ├── test_document.py
  │   ├── test_session.py
  │   └── test_user.py
  └── test_services/
      ├── __init__.py
      ├── test_document_service.py
      └── test_auth_service.py
pytest.ini
```

### Estrategia de Integration Tests

Los integration tests utilizan bases de datos separadas para aislar el ambiente de pruebas del ambiente de desarrollo. PostgreSQL usa POSTGRES_TEST_DB y Redis usa REDIS_TEST_URL (database 1 en lugar de 0). Qdrant NO se testea en integration tests. La configuración de fixtures pytest usa transaction rollback para asegurar aislamiento entre tests. Para los datos de prueba se utiliza factory pattern.

**Servicios a testear:**
- PostgreSQL: Base de datos relacional para persistencia (POSTGRES_TEST_DB)
- Redis: Cache y gestión de sesiones (REDIS_TEST_URL con database 1)
- Qdrant: NO se testea en integration tests

**Configuración de fixtures pytest:**
- Bases de datos separadas: POSTGRES_TEST_DB para PostgreSQL, REDIS_TEST_URL para Redis
- Transaction rollback: Los datos se rollback entre cada test individual para asegurar aislamiento
- Factory pattern: Se utiliza factory pattern para generar datos de prueba consistentes

### Estrategia de Testing MCP

El testing de MCP servers utiliza FastMCP Client en modo memory. Se implementa un fixture genérico para el servidor y fixtures específicas para escenarios de testing comunes. El testing incluye tools + integración con bases de datos (PostgreSQL, Redis).

**Configuración:**
- FastMCP Client en modo memory: Sin dependencias externas para unit tests
- Fixture genérico para el servidor: Configuración compartida del servidor MCP
- Fixtures específicas para escenarios comunes: Escenarios predefinidos de testing
- Testing de tools: Validación de cada tool individual
- Integración con bases de datos: Tests de integración con PostgreSQL y Redis

## Referencias

- [TRD - Hito 2](../propuestas/trd-milestone-2-api-rest.md): RNF-004: Testing
- [ADR-002](../decisiones/adr-002-python-unified-stack.md): Stack Unificado en Python
