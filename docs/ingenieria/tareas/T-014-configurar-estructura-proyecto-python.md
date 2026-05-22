---
id: T-014
type: Task
rating: 10
rating-phase: document-editing
related:
  - target: EPC-002
    relationship_type: implements
    reason: Implementa la épica de API REST y MCP Server configurando estructura Python
---

# T-014: Configurar Estructura de Proyecto Python

**Tipo**: Task
**Prioridad**: Alta
**Estimación**: 2 horas

**Nota sobre metodología de estimación**: Las estimaciones están basadas en experiencia previa del desarrollador. No hay un criterio estandarizado documentado para todas las estimaciones; implementation-strategy.md menciona estimación de esfuerzo considerando dependencias pero no detalla la metodología específica. Para esta tarea específica, la estimación de 2 horas se basa en la experiencia del desarrollador en configurar estructuras de proyecto Python con FastAPI y herramientas de linting.
**Dependencias**: EPC-002

## Descripción

Crear estructura base del proyecto Python con FastAPI, configurar dependencias con uv y establecer convenciones de código. Ruff para linting y formatting (reemplaza Black, isort, flake8). Configuración recomendada: line-length=88, select=[E, F, I, N, W, UP, B], formatter con quote-style=double, indent-style=space, docstring-code-format=true. Type hints requiere mypy separado si se desea type checking.

## Criterios de Aceptación

- [ ] Estructura de directorios: app/, models/, services/, api/, tests/
- [ ] pyproject.toml configurado con dependencias (FastAPI 0.135.0, SQLAlchemy, Alembic, etc.)
- [ ] uv lock file generado
- [ ] .gitignore configurado para Python
- [ ] README con instrucciones de setup
- [ ] Comando `uvicorn app.main:app --reload` inicia servidor de desarrollo
- [ ] Ruff configurado para linting y formatting (line-length=88, select=[E, F, I, N, W, UP, B])

## Archivos a Crear

```
app/
  ├── __init__.py
  ├── main.py
  ├── models/
  ├── services/
  └── api/
tests/
  ├── __init__.py
  └── conftest.py
pyproject.toml
uv.lock
.gitignore
README.md
```

## Referencias

- [TRD - Hito 2](../propuestas/trd-milestone-2-api-mcp.md): RF-001: FastAPI Application Setup
- [ADR-002](../decisiones/adr-002-python-unified-stack.md): Stack Unificado en Python
