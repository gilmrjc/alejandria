---
id: ADR-007
type: Architecture Decision Record
related:
  - target: ARC-003
    relationship_type: implements
    reason: Implementa la arquitectura general del sistema definiendo la estructura de paquetes Python
  - target: ADR-008
    relationship_type: implements
    reason: Implementa la estructura de paquetes con gestión de dependencias uv
---

# ADR-007: Estructura de Paquetes Python y Organización de Módulos

## Contexto y Problema

Alejandria requiere definir una estructura de paquetes Python consistente para el stack unificado (FastAPI + Celery + FastMCP). El código Python se organiza en múltiples componentes (API, MCP Server, Jobs, shared code) y es necesario establecer una estructura clara que:

- Mantenga separación de responsabilidades entre componentes
- Permita reutilización de código compartido
- Facilite testing y mantenimiento
- Sea escalable para crecimiento futuro
- Siga mejores prácticas del ecosistema Python

## Decisiones

**Decisión**: Usar una estructura de paquetes basada en capas con módulos compartidos:

```text
alejandria/
├── api/                    # FastAPI application
│   ├── __init__.py
│   ├── main.py            # FastAPI app entry point
│   ├── routes/            # API endpoints
│   │   ├── __init__.py
│   │   ├── documents.py
│   │   ├── jobs.py
│   │   └── health.py
│   ├── dependencies/     # FastAPI dependencies
│   │   ├── __init__.py
│   │   └── auth.py
│   └── schemas/          # Pydantic models for API
│       ├── __init__.py
│       ├── document.py
│       └── job.py
├── mcp/                   # FastMCP server
│   ├── __init__.py
│   ├── server.py          # FastMCP server entry point
│   ├── tools/             # MCP tools
│   │   ├── __init__.py
│   │   ├── document_analysis.py
│   │   └── gap_detection.py
│   └── prompts/           # MCP prompts
│       ├── __init__.py
│       └── review.py
├── jobs/                  # Celery tasks
│   ├── __init__.py
│   ├── celery_app.py      # Celery application
│   ├── tasks/             # Celery task definitions
│   │   ├── __init__.py
│   │   ├── gap_detection.py
│   │   ├── suggestion_application.py
│   │   ├── vector_sync.py
│   │   └── question_generation.py
│   └── config.py          # Celery configuration
├── shared/                # Shared code across components
│   ├── __init__.py
│   ├── db/               # Database models and session
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── session.py
│   │   └── base.py
│   ├── schemas/          # Shared Pydantic models
│   │   ├── __init__.py
│   │   ├── document.py
│   │   └── job.py
│   ├── services/         # Business logic services
│   │   ├── __init__.py
│   │   ├── document_service.py
│   │   └── job_service.py
│   ├── config/           # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py
│   └── utils/            # Utility functions
│       ├── __init__.py
│       └── logging.py
├── tests/                # Test suite
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_services.py
│   │   └── test_schemas.py
│   ├── integration/
│   │   ├── test_api.py
│   │   └── test_jobs.py
│   └── e2e/
│       └── test_pipeline.py
├── pyproject.toml        # uv dependency management
├── uv.lock              # uv lock file
└── run.py               # Unified entry point
```

**Principios de organización**:

1. **Separación por componente**: Cada componente principal (api, mcp, jobs) tiene su propio paquete
2. **Código compartido en `shared/`**: Lógica de negocio, modelos de datos, configuración y utilidades compartidas
3. **Módulos por funcionalidad**: Dentro de cada componente, los módulos se organizan por funcionalidad (routes, tools, tasks)
4. **Test suite separada**: Tests organizados por tipo (unit, integration, e2e)
5. **Entry point unificado**: `run.py` como punto de entrada único para iniciar API, workers o MCP server

## Justificación

### Ventajas de la Estructura Propuesta

**Separación de responsabilidades**:

- Cada componente (api, mcp, jobs) es independiente y puede desarrollarse por separado
- El código compartido está centralizado en `shared/`, evitando duplicación
- Los desarrolladores pueden entender rápidamente dónde encontrar código específico

**Reutilización de código**:

- Modelos de base de datos (`shared/db/models.py`) se usan en API, MCP y jobs
- Servicios de negocio (`shared/services/`) se reutilizan en todos los componentes
- Schemas Pydantic compartidos (`shared/schemas/`) aseguran consistencia de datos

**Testing facilitado**:

- Tests organizados por tipo (unit, integration, e2e) para ejecución selectiva
- Mocking simplificado al tener módulos bien delimitados
- Bases de datos separadas en docker-compose se integran fácilmente con estructura de paquetes

**Escalabilidad**:

- Estructura modular permite agregar nuevos componentes sin refactorización
- Nuevas funcionalidades se agregan como módulos dentro de componentes existentes
- Crecimiento del código base mantiene organización clara

**Alineación con mejores prácticas Python**:

- Uso de `__init__.py` para paquetes explícitos
- Imports relativos dentro de paquetes para claridad
- Estructura sigue convenciones de proyectos Python modernos

### Alineación con Stack Unificado (ADR-002)

**Integración FastAPI-FastMCP**:

- `api/` y `mcp/` son paquetes separados pero comparten código vía `shared/`
- Shared state se maneja vía `shared/db/` (PostgreSQL) y Redis configurado en `shared/config/`
- No hay comunicación HTTP entre API y MCP, ambos acceden directamente a datos compartidos

**Integración Celery**:

- `jobs/` contiene aplicación Celery y tareas
- Tareas Celery importan servicios desde `shared/services/`
- Configuración Celery en `jobs/config.py` usa settings desde `shared/config/`

**Despliegue Docker**:

- Estructura de paquetes se empaqueta en Docker container
- `run.py` es entry point unificado que inicia componente según argumentos
- `uv` instala dependencias desde `pyproject.toml` con lock file reproducible

## Trade-offs

### Desventajas

- **Complejidad inicial**: Estructura de múltiples paquetes puede ser compleja para proyectos pequeños
- **Imports más largos**: Imports desde `shared/` pueden ser verbosos (e.g., `from shared.db.models import Document`)
- **Curva de aprendizaje**: Desarrolladores nuevos necesitan entender estructura de paquetes

### Mitigación

- **Documentación clara**: Este ADR y `development-setup.md` explican estructura
- **Imports con alias**: Usar imports con alias para reducir verbosidad cuando necesario
- **Ejemplos de código**: Incluir ejemplos de imports y patrones de uso en documentación

## Alternativas Consideradas

### Estructura Plana (Monolito Único)

**Ventaja**: Simplicidad inicial, imports más cortos

**Desventaja**: Difícil mantener separación de responsabilidades, código compartido se duplica

**Decisión**: Rechazada porque no escala bien con múltiples componentes (API, MCP, jobs)

### Estructura por Capa (api_layer, mcp_layer, jobs_layer)

**Ventaja**: Separación clara por componente

**Desventaja**: Código compartido se duplica o requiere imports complejos entre capas

**Decisión**: Rechazada porque no facilita reutilización de código compartido

### Microservicios Separados (Repositorios Independientes)

**Ventaja**: Independencia total de componentes

**Desventaja**: Complejidad operacional alta, duplicación de código, overhead de comunicación

**Decisión**: Rechazada porque aumenta fricción operacional, contrario a principio de baja fricción

## Consecuencias

### Impacto Positivo

- **Organización clara**: Estructura predecible facilita navegación y mantenimiento
- **Reutilización**: Código compartido reduce duplicación y asegura consistencia
- **Testing**: Estructura modular facilita testing aislado y integration tests
- **Escalabilidad**: Estructura soporta crecimiento sin refactorización mayor

### Impacto Negativo

- **Complejidad inicial**: Nueva estructura requiere aprendizaje para desarrolladores
- **Setup inicial**: Configuración de múltiples paquetes requiere más trabajo inicial

### Requerimientos de Implementación

- Crear estructura de directorios según definición
- Configurar `pyproject.toml` con uv para gestión de dependencias
- Implementar `run.py` como entry point unificado
- Configurar imports relativos dentro de paquetes
- Documentar patrones de imports y uso en `development-setup.md`
- Asegurar que tests sigan estructura de paquetes

## Referencias

- ADR-002: Python Unified Stack
- technology-stack.md: Estructura de proyecto
- Python Packaging User Guide: <https://packaging.python.org/en/latest/tutorials/packaging-projects/>
