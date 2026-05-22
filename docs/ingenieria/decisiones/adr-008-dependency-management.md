---
id: ADR-008
type: Architecture Decision Record
related:
  - target: ADR-007
    relationship_type: implements
    reason: Implementa la estructura de paquetes con gestión de dependencias uv
  - target: ARC-003
    relationship_type: implements
    reason: Implementa la arquitectura general con estrategia de dependencias reproducibles
---

# ADR-008: Estrategia de Gestión de Dependencias Python con uv

## Contexto y Problema

Alejandria requiere una estrategia de gestión de dependencias Python para el stack unificado (FastAPI + Celery + FastMCP). El sistema necesita:

- Gestión reproducible de dependencias para consistencia entre entornos
- Lock files para asegurar versiones exactas en despliegues
- Integración con Docker para despliegue consistente
- Velocidad en instalación de dependencias para desarrollo iterativo
- Alineación con criterio de versionado establecido en ADR-002 ("última versión estable menos un minor")

Alternativas consideradas incluyen pip, poetry, pipenv, y otras herramientas de gestión de dependencias Python.

## Decisiones

**Decisión**: Usar uv para gestión de dependencias Python con las siguientes convenciones:

**Herramienta**: uv (escrito en Rust, moderno y rápido)

**Archivos de configuración**:

- `pyproject.toml`: Definición de dependencias y metadata del proyecto
- `uv.lock`: Lock file reproducible con versiones exactas de todas las dependencias
- `.python-version`: Especificar versión de Python (recomendado: 3.12)

**Criterio de versionado**:

- Aplicar criterio de ADR-002: "última versión estable menos un minor" para dependencias directas
- Dependencias directas en `pyproject.toml` con rangos semver (e.g., `fastapi>=0.134.0,<0.136.0`)
- Lock file `uv.lock` contiene versiones exactas resueltas
- Actualizaciones de dependencias requieren revisión manual y regeneración de lock file

**Comandos uv principales**:

```bash
# Inicializar proyecto
uv init

# Agregar dependencia
uv add fastapi==0.135.0

# Agregar dependencia de desarrollo
uv add --dev pytest

# Actualizar dependencias (respetando rangos en pyproject.toml)
uv lock --upgrade

# Instalar dependencias
uv sync

# Ejecutar comando en entorno virtual
uv run python run.py
```

**Integración con Docker**:

```dockerfile
# Stage 1: Instalar dependencias con uv
FROM python:3.12-slim as builder
COPY pyproject.toml uv.lock ./
RUN pip install uv
RUN uv sync --frozen

# Stage 2: Runtime
FROM python:3.12-slim
COPY --from=builder /app/.venv /app/.venv
COPY . .
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "run.py"]
```

## Justificación

### Ventajas de uv

**Velocidad**:

- uv está escrito en Rust, significativamente más rápido que Poetry/pip
- Instalación de dependencias 10-100x más rápida que pip
- Resolución de dependencias eficiente incluso para proyectos grandes

**Reproducibilidad**:

- Lock file `uv.lock` asegura versiones exactas en todos los entornos
- `uv sync --frozen` instala exactamente las versiones en lock file
- Integración nativa con Docker para despliegue consistente

**Simplicidad**:

- Usa estándar `pyproject.toml` (PEP 518)
- Comandos simples e intuitivos
- No requiere configuración compleja

**Features modernas**:

- Soporte para dependencias de desarrollo separadas
- Integración con herramientas de testing (pytest, coverage)
- Compatible con ecosistema Python existente

### Alineación con ADR-002 y ADR-006

**Criterio de versionado**:

- ADR-002 establece "última versión estable menos un minor" para stack Python
- uv permite especificar rangos semver en `pyproject.toml` (e.g., `fastapi>=0.134.0,<0.136.0`)
- Lock file contiene versión exacta resuelta (e.g., `fastapi==0.135.0`)
- ADR-006 (Document Versioning) establece convención de versionado para consistencia

**Integración con Docker**:

- ADR-002 especifica despliegue mediante Docker con Dockerfile multi-stage
- uv se integra naturalmente con Dockerfile multi-stage
- `uv sync --frozen` asegura reproducibilidad en despliegue

**Gestión de dependencias compartidas**:

- Estructura de paquetes (ADR-007) tiene código compartido en `shared/`
- uv maneja dependencias del proyecto monorepo de forma unificada
- No hay conflicto entre componentes (api, mcp, jobs) al compartir dependencias

### Comparación con Alternativas

**vs pip**:

- pip no tiene lock file nativo (requiere pip-tools)
- pip es más lento que uv
- pip no maneja grupos de dependencias (dev vs prod) de forma nativa

**vs Poetry**:

- Poetry es más lento que uv (escrito en Python)
- Poetry usa `poetry.lock` (propio) vs `uv.lock` (estándar)
- uv tiene mejor integración con herramientas modernas

**vs pipenv**:

- pipenv está en mantenimiento limitado
- pipenv es más lento que uv
- uv tiene mejor soporte para features modernas

## Trade-offs

### Desventajas

- **Herramienta relativamente nueva**: uv es más nueva que Poetry/pip, comunidad más pequeña
- **Curva de aprendizaje**: Desarrolladores familiarizados con Poetry/pip necesitan aprender comandos uv
- **Dependencia de Rust**: uv requiere binario compilado de Rust (no issue en práctica)

### Mitigación

- **Documentación clara**: Este ADR y `development-setup.md` documentan comandos uv
- **Ejemplos de uso**: Incluir ejemplos de comandos comunes en documentación
- **Binario estático**: uv distribuye binarios estáticos, no requiere Rust en entorno de runtime

## Estrategia de Actualización de Dependencias

**Actualizaciones de seguridad**:

- Monitorear advisories de seguridad (e.g., via GitHub Dependabot)
- Actualizar dependencias afectadas inmediatamente
- Regenerar lock file con `uv lock --upgrade`
- Validar con tests antes de desplegar

**Actualizaciones de features**:

- Revisar changelogs de dependencias antes de actualizar
- Actualizar una dependencia a la vez para aislar cambios
- Ejecutar suite de tests completa después de cada actualización
- Regenerar lock file solo después de validación

**Actualizaciones de Python**:

- Seguir criterio de ADR-002 para versión de Python
- Actualizar `.python-version` y `pyproject.toml` cuando sea necesario
- Validar compatibilidad de dependencias con nueva versión de Python
- Probar en entorno de desarrollo antes de desplegar

## Alternativas Consideradas

### pip con pip-tools

**Ventaja**: Herramientas estándar del ecosistema Python

**Desventaja**: Requiere múltiples herramientas (pip + pip-tools), más lento que uv

**Decisión**: Rechazada porque uv proporciona mejor experiencia de desarrollo y features modernas

### Poetry

**Ventaja**: Herramienta estable con comunidad grande

**Desventaja**: Más lento que uv, lock file propietario vs estándar

**Decisión**: Rechazada porque uv es más rápido y usa estándar `pyproject.toml`

### pipenv

**Ventaja**: Gestión unificada de dependencias y entornos virtuales

**Desventaja**: En mantenimiento limitado, más lento que uv

**Decisión**: Rechazada porque pipenv no está activamente mantenido y uv es más moderno

## Consecuencias

### Impacto Positivo

- **Velocidad**: Instalación de dependencias significativamente más rápida
- **Reproducibilidad**: Lock file asegura consistencia entre entornos
- **Simplicidad**: Comandos intuitivos y estándar `pyproject.toml`
- **Integración Docker**: Natural integración con Dockerfile multi-stage

### Impacto Negativo

- **Curva de aprendizaje**: Desarrolladores necesitan aprender comandos uv
- **Herramienta nueva**: Comunidad más pequeña que Poetry/pip

### Requerimientos de Implementación

- Instalar uv en entorno de desarrollo
- Configurar `pyproject.toml` con dependencias del stack Python
- Generar `uv.lock` inicial con `uv lock`
- Configurar Dockerfile multi-stage con uv
- Documentar comandos uv en `development-setup.md`
- Configurar CI/CD para usar `uv sync --frozen` en despliegues

## Referencias

- ADR-002: Python Unified Stack (criterio de versionado)
- ADR-006: Document Versioning
- ADR-007: Python Package Structure
- uv documentation: <https://github.com/astral-sh/uv>
- PEP 518: pyproject.toml specification
