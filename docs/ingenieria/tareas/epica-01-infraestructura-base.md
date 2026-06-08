---
id: EPC-001
type: Epic Implementation
rating: 9.5
rating-phase: document-editing
related:
  - target: TRD-001
    relationship_type: implements
    reason: Implementa el TRD de Hito 1 con tareas de infraestructura base
  - target: T-001
    relationship_type: implements
    reason: Implementa la tarea de creación de estructura base del proyecto
  - target: T-002
    relationship_type: implements
    reason: Implementa la tarea de configuración de Docker Compose
  - target: T-003
    relationship_type: implements
    reason: Implementa la tarea de configuración de variables de entorno
  - target: T-004
    relationship_type: implements
    reason: Implementa la tarea de configuración de Alembic migrations
  - target: T-005
    relationship_type: implements
    reason: Implementa la tarea de creación de migration inicial del schema
  - target: T-006
    relationship_type: implements
    reason: Implementa la tarea de configuración de middleware de versioning
  - target: T-007
    relationship_type: implements
    reason: Implementa la tarea de verificación de configuración de Redis
  - target: T-008
    relationship_type: implements
    reason: Implementa la tarea de verificación de configuración de Qdrant
  - target: T-009
    relationship_type: implements
    reason: Implementa la tarea de configuración de descarga automática de modelo Qwen
  - target: T-010
    relationship_type: implements
    reason: Implementa la tarea de script de health check
  - target: T-011
    relationship_type: implements
    reason: Implementa la tarea de README con instrucciones de setup
  - target: T-012
    relationship_type: implements
    reason: Implementa la tarea de script de setup automatizado
---

# Epica 1: Infraestructura Base

**Estado**: ✅ COMPLETADO - Infraestructura operativa y validada

**Objetivo**: Establecer la infraestructura base del proyecto con todos los servicios necesarios (PostgreSQL, Qdrant, Redis, Ollama) configurados y operativos. Esta épica establece los fundamentos técnicos sobre los cuales se construirán las siguientes capas del sistema: API REST, MCP server, y frontend React.

## Criterios de Éxito de la Épica

La épica se considerará completada exitosamente cuando se cumplan los siguientes criterios:

### Infraestructura Operativa

- Todos los servicios base (PostgreSQL, Redis, Qdrant) levantan correctamente con `docker-compose up -d` ✅
- Health checks de todos los servicios pasan exitosamente (`scripts/health-check.sh` retorna exit code 0) ✅
- Ollama es accesible vía Tailscale y el modelo Qwen 3.5 está instalado y funcional ✅
- Datos persisten correctamente después de restart de contenedores (volumes Docker configurados) ✅

**Evidencia de validación** (Jun 7, 2026):
- `docker-compose ps` muestra todos los servicios operativos:
  - alejandria-postgres: Up 28 minutes (healthy)
  - alejandria-redis: Up 28 minutes (healthy)
  - alejandria-qdrant: Up 28 minutes
  - alejandria-api: Up 27 minutes
  - alejandria-mcp: Up 27 minutes

### Base de Datos Configurada

- Alembic está configurado y migrations pueden ejecutarse (`alembic upgrade head` funciona)
- Schema inicial de base de datos está creado con todas las tablas requeridas
- Middleware de versioning está implementado y crea snapshots automáticamente

### Documentación y Automatización

- README.md contiene instrucciones claras y reproducibles para setup del entorno
- Un desarrollador nuevo puede configurar el stack en menos de 15 minutos (asumiendo Docker Desktop pre-instalado)
- Script `scripts/dev-setup.sh` automatiza el setup inicial y es idempotente
- Variables de entorno están documentadas y `.env.example` está disponible

### Calidad y Mantenibilidad

- Estructura de proyecto sigue el layout híbrido capas+dominios definido
- Todas las referencias a documentos externos (TRD, ADR, technical-roadmap) son válidas y accesibles
- Dependencias entre tareas están documentadas y respetadas en la implementación
- Código de ejemplo en documentos es sintácticamente correcto y ejecutable

---

## Referencias

- **[../../estrategia/estrategia/technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md)**: Roadmap técnico, Hito 1
- **[../arquitectura/technology-stack.md](../arquitectura/technology-stack.md)**: Stack tecnológico
- **[../arquitectura/database-schema-design.md](../arquitectura/database-schema-design.md)**: Diseño conceptual de esquema de base de datos
- **[../propuestas/trd-milestone-1-infrastructure.md](../propuestas/trd-milestone-1-infrastructure.md)**: TRD de Hito 1

---

## Tareas de la Épica

Esta épica se implementa mediante las siguientes tareas (T-001 a T-012). Para detalles de implementación específicos de cada tarea, consultar los documentos individuales de cada tarea.

- **T-001**: Crear estructura base del proyecto
- **T-002**: Configurar Docker Compose con servicios base
- **T-003**: Configurar variables de entorno
- **T-004**: Configurar Alembic migrations
- **T-005**: Crear migration inicial del schema
- **T-006**: Implementar middleware de versioning
- **T-007**: Verificar configuración de Redis
- **T-008**: Verificar configuración de Qdrant
- **T-009**: Configurar descarga automática de modelo Qwen
- **T-010**: Crear script de health check
- **T-011**: Crear README con instrucciones de setup
- **T-012**: Crear script de setup automatizado

---

## Dependencias entre Tareas

Las tareas de esta épica tienen dependencias secuenciales que deben respetarse para una implementación exitosa:

### Flujo Principal de Infraestructura

- **T-001** (Estructura base) → **T-002** (Docker Compose) → **T-003** (Variables de entorno)
  - La estructura base es prerequisito para configurar Docker Compose
  - Docker Compose debe estar configurado antes de definir variables de entorno

### Flujo de Base de Datos

- **T-004** (Alembic migrations) → **T-005** (Migration inicial) → **T-006** (Middleware versioning)
  - Alembic debe configurarse antes de crear migrations
  - Migration inicial debe existir antes de implementar middleware de versioning

### Flujo de Verificación de Servicios

- **T-002** (Docker Compose) → **T-007** (Verificación Redis) → **T-008** (Verificación Qdrant) → **T-009** (Configuración Ollama)
  - Docker Compose debe levantar servicios antes de verificar su configuración
  - Verificaciones de Redis y Qdrant son independientes entre sí
  - Configuración de Ollama es independiente pero requiere Tailscale configurado

### Flujo de Scripts de Automatización

- **T-007, T-008, T-009** (Verificaciones) → **T-010** (Health check)
  - Health check depende de que todos los servicios estén verificados
- **T-010** (Health check) → **T-011** (README) → **T-012** (Script setup automatizado)
  - Health check debe existir antes de documentarlo en README
  - README debe estar completo antes de crear script automatizado que lo referencia

### Diagrama de Dependencias

```text
T-001 → T-002 → T-003
           ↓
       T-004 → T-005 → T-006
           ↓
       T-007, T-008, T-009 (paralelas)
           ↓
           T-010 → T-011 → T-012
```

---

*Fin del documento de Épica 1. Para detalles de implementación de cada tarea, consultar los documentos individuales T-001 a T-012.*
