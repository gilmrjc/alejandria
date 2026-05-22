---
id: T-001
type: Task
rating: 9.0
rating-phase: document-editing
related:
  - target: ADR-003
    relationship_type: implements
    reason: Implementa la decisión de infraestructura local con Docker Compose creando estructura base
  - target: ADR-007
    relationship_type: implements
    reason: Implementa la estructura de paquetes Python definida en el ADR
---

# T-001: Crear estructura base de proyecto

**Tipo**: Task
**Prioridad**: Alta
**Estimación**: 1 hora
**Dependencias**: Ninguna

## Descripción

Crear estructura de directorios base para el proyecto con archivos de configuración inicial según ADR-007 y technology-stack.md.

La estructura de directorios sigue ADR-007 (estructura de paquetes Python) y technology-stack.md (estructura híbrida capas+dominios). La estimación de 1 hora es razonable para crear directorios base y archivos de configuración inicial sin implementación de código.

## Criterios de Aceptación

- [ ] Estructura de paquetes Python creada según ADR-007 (api/, mcp/, jobs/, shared/, tests/)
- [ ] Estructura híbrida capas+dominios creada según technology-stack.md (backend/src/core/, models/, api/, jobs/, mcp/)
- [ ] Directorio `docker/` creado con configuración de servicios
- [ ] Directorio `scripts/` creado
- [ ] Directorio `alembic/` creado con estructura básica
- [ ] Archivo `pyproject.toml` creado para gestión de dependencias con uv
- [ ] Archivo `.gitignore` actualizado con patrones de Python y Docker
- [ ] Archivo `README.md` creado con descripción del proyecto
- [ ] Archivo `run.py` creado como entry point unificado

## Criterios de Éxito

- Estructura verificada por linter de Python (ruff/flake8) sin errores
- Estructura de directorios coincide exactamente con especificaciones de ADR-007 y technology-stack.md
- Todos los archivos `__init__.py` están presentes para permitir imports de Python
- `pyproject.toml` es válido y puede ser procesado por uv

### Comandos de Verificación

Para esta fase inicial del proyecto, se usa verificación manual simple:

```bash
# Verificar estructura de directorios
tree -L 3 -I '__pycache__|*.pyc|.git'

# Verificar archivos __init__.py
find . -name "__init__.py" | sort

# Verificar directorios requeridos
find . -type d -name "api" -o -name "mcp" -o -name "jobs" -o -name "shared" -o -name "tests"
```

**Nota:** Es un one-time setup de estructura base que no cambia frecuentemente. La validación manual es suficiente para esta fase. Más adelante, si el proyecto crece y la estructura se vuelve compleja, se puede considerar validación automatizada en CI/CD.

### Validación de pyproject.toml

```bash
uv sync --dry-run
```

Este comando verifica que pyproject.toml es sintácticamente válido y que las dependencias se pueden resolver sin instalar nada. Para esta fase inicial, es suficiente verificar que uv puede procesar el archivo. Validaciones adicionales (dependencias, versiones, metadatos) pueden agregarse más adelante si surgen problemas específicos.

**Nota sobre permisos:** La especificación de permisos específicos (755 para scripts, 644 para archivos) se eliminó de los criterios de éxito porque es sobre esfuerzo para un proyecto local de desarrollo. Los permisos por defecto del sistema son adecuados para desarrollo local. No hay política de seguridad formal que justifique esta especificación. Solo es crítico en producción o ambientes multi-usuario. Los desarrolladores pueden ajustar permisos según necesidad sin impacto en el proyecto.

## Archivos a Crear

**Estructura de paquetes Python (según ADR-007):**

```text
alejandria/
├── api/                    # FastAPI application
│   ├── __init__.py
│   ├── main.py
│   ├── routes/
│   ├── dependencies/
│   └── schemas/
├── mcp/                   # FastMCP server
│   ├── __init__.py
│   ├── server.py
│   ├── tools/
│   └── prompts/
├── jobs/                  # Celery tasks
│   ├── __init__.py
│   ├── celery_app.py
│   ├── tasks/
│   └── config.py
├── shared/                # Shared code
│   ├── __init__.py
│   ├── db/
│   ├── schemas/
│   ├── services/
│   ├── config/
│   └── utils/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── pyproject.toml
├── uv.lock
└── run.py
```

**Estructura de infraestructura (según ADR-003):**

```text
docker/
  └── docker-compose.yml
scripts/
  ├── health-check.sh
  └── dev-setup.sh
alembic/
  ├── versions/
  ├── env.py
  └── script.py.mako
```

## Referencias

- [TRD - Hito 1](../propuestas/trd-milestone-1-infrastructure.md): RF-001: Docker Compose Configuration
- [ADR-003](../decisiones/adr-003-local-infrastructure-docker-compose.md): Local Infrastructure with Docker Compose
- [ADR-007](../decisiones/adr-007-python-package-structure.md): Estructura de Paquetes Python
- [technology-stack.md](../arquitectura/technology-stack.md): Stack tecnológico y estructura de proyecto

**Nota sobre relación entre documentos:** ADR-007 y technology-stack.md son documentos complementarios, no conflictivos:

- **ADR-007** define la estructura de alto nivel de paquetes Python (api/, mcp/, jobs/, shared/, tests/)
- **technology-stack.md** define la estructura híbrida capas+dominios dentro de cada paquete
- Son capas diferentes de especificación que trabajan juntas

**Regla de prioridad:** Si hay conflicto real entre documentos, la jerarquía es: ADRs > documentos de arquitectura > documentos de implementación. En caso de conflicto, actualizar el documento de menor prioridad para alinearse.

**Nota sobre evolución:** La estructura de carpetas puede evolucionar junto al proyecto, por lo que esta no es una decisión inmutable. Los documentos deben actualizarse cuando la estructura cambie significativamente.

---

## Dependencias con Otras Tareas

Esta tarea (T-001) es prerequisito para las siguientes tareas:

- **T-002** (Docker Compose): Requiere la estructura base de directorios para configurar Docker Compose
- **T-003** (Variables de entorno): Requiere que la estructura base exista para definir archivos `.env`
- **T-004** (Alembic migrations): Requiere la estructura de paquetes Python para configurar Alembic
- **T-006** (Middleware versioning): Requiere la estructura de capas para implementar middleware

Todas las tareas subsiguientes dependen de que la estructura base esté correctamente establecida.

---

## Manejo de Errores

### Estrategia de Rollback

Se usa corrección incremental como estrategia principal.

**Estrategia:**

- Eliminar solo los directorios/archivos incorrectos con `rm -rf <directorio>`
- Recrear solo lo que falta con `mkdir` o comandos equivalentes
- Es más rápido y no afecta lo que ya está correcto
- Apropiado para errores simples (directorio mal nombrado, archivo faltante)

**Fallback:** Si el error ya está commiteado, usar Git rollback con `git reset` o `git checkout` para volver al commit anterior.

**Justificación:** La estructura de directorios es simple de corregir incrementalmente. No es necesario destruir todo por un error simple.
