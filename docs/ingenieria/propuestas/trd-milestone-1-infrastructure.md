---
id: TRD-001
type: Technical Requirements Document
rating: 9
rating-phase: document-editing
dependency: [ADR-003]
related:
  - target: STR-003
    relationship_type: implements
    reason: Implementa el Hito 1 del roadmap técnico con requisitos detallados
  - target: ARC-003
    relationship_type: implements
    reason: Implementa el stack tecnológico con especificación de infraestructura
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del schema de base de datos para configuración de servicios
  - target: ADR-003
    relationship_type: implements
    reason: Implementa la decisión de Docker Compose con requisitos específicos
---

# TRD - Hito 1: Infraestructura Base

## Visión General

### Objetivo del Hito

Configurar la infraestructura base para el entorno de desarrollo local, permitiendo orquestar los servicios de datos (PostgreSQL, Redis, Qdrant) mediante Docker Compose. Ollama se ejecuta fuera de Docker, conectado vía Tailscale.

### Propósito

Establecer la base técnica sobre la cual se construirán los hitos subsiguientes (API REST, MCP Server, Frontend, entre otros). Este hito constituye el fundamento del MVP Bootstrapped y debe completarse antes de iniciar cualquier desarrollo de aplicación.

### Referencias del Hito

- [technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md): Hito 1 - Infraestructura Base
- [ADR-003](../decisiones/adr-003-local-infrastructure-docker-compose.md): Local Infrastructure with Docker Compose
- [technology-stack.md](../arquitectura/technology-stack.md): Stack tecnológico recomendado
- [database-schema-design.md](../arquitectura/database-schema-design.md): Diseño conceptual de schema de PostgreSQL

---

## Alcance y Límites del Documento

Este TRD se enfoca en definir **QUÉ** se debe implementar (requisitos funcionales, criterios de aceptación, casos de uso), mientras que la información operacional detallada (**CÓMO** implementarlo paso a paso) y conceptual (**POR QUÉ** funciona así) se documenta en archivos dedicados específicamente para esos propósitos. Esta separación de responsabilidades permite:

- **TRD enfocado y conciso**: Para desarrolladores que necesitan saber QUÉ implementar sin saturación de detalles operacionales
- **Documentos de implementación dedicados**: `development-setup.md` contiene guías paso a paso (ej: configuración de Tailscale para Ollama, pasos de configuración de Alembic)
- **Documentos de conceptos técnicos dedicados**: `qdrant.md` contiene explicaciones de conceptos fundamentales (ej: BGE-M3, cosine similarity, búsqueda vectorial)
- **Documentos de decisión (ADRs)**: `ADR-003` contiene el razonamiento estratégico de POR QUÉ se eligieron estas tecnologías

Esta estructura modular sigue el principio de separación de responsabilidades donde cada tipo de documento tiene un propósito específico en la documentación de Alejandria. El TRD incluye referencias a estos documentos dedicados para orientar a desarrolladores junior hacia la información operacional y conceptual que necesitan.

---

## Requisitos Funcionales

### RF-001: Docker Compose Configuration

#### Descripción - RF-001

Configurar Docker Compose para orquestar los servicios base del stack tecnológico.

#### Criterios de Aceptación - RF-001

- [ ] Docker Compose file (`docker-compose.yml`) define todos los servicios requeridos
- [ ] Cada servicio tiene versión específica de imagen Docker
- [ ] Servicios exponen puertos correctos para comunicación entre componentes
- [ ] Volumes Docker configurados para persistencia de datos
- [ ] Variables de entorno configuradas para cada servicio
- [ ] Comando `docker-compose up -d` levanta todos los servicios sin errores
- [ ] Comando `docker-compose down` detiene todos los servicios correctamente
- [ ] Comando `docker-compose logs` muestra logs de todos los servicios

#### Servicios Requeridos - RF-001

1. **PostgreSQL 18.3-bookworm**
   - Puerto: 5432
   - Database: alejandria
   - User: alejandria
   - Password: variable de entorno
   - Volume: postgres_data

2. **Redis 7.4.9-bookworm**
   - Puerto: 6379
   - Persistencia: AOF enabled
   - Volume: redis_data

3. **Qdrant v1.17.1**
   - Puerto HTTP: 6333
   - Puerto gRPC: 6334
   - Volume: qdrant_data

**Nota**: Ollama se ejecuta fuera de Docker (en el host o máquina remota), conectado mediante Tailscale. No se gestiona como servicio en Docker Compose.

#### Configuración de Referencia - RF-001

```yaml
version: '3.8'

services:
  postgresql:
    image: postgres:18.3-bookworm
    container_name: alejandria-postgres
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-alejandria}
      POSTGRES_USER: ${POSTGRES_USER:-alejandria}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-alejandria}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7.4.9-bookworm
    container_name: alejandria-redis
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  qdrant:
    image: qdrant/qdrant:v1.17.1
    container_name: alejandria-qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:6333/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5

# Ollama se ejecuta fuera de Docker, conectado vía Tailscale
# Ver ADR-003 para justificación

volumes:
  postgres_data:
  redis_data:
  qdrant_data:
```

#### Prioridad - RF-001: Alta

### RF-002: PostgreSQL Setup

#### Descripción - RF-002

Configurar PostgreSQL con el schema inicial y las migraciones de Alembic.

#### Criterios de Aceptación - RF-002

- [ ] PostgreSQL acepta conexiones en puerto 5432
- [ ] Database `alejandria` creada automáticamente
- [ ] Schema inicial versionado con Alembic (migration 001_initial_schema)
- [ ] Tablas core creadas según database-schema.md:
  - [ ] folders
  - [ ] documents
  - [ ] document_snapshots
  - [ ] gaps
  - [ ] tags
  - [ ] gap_tags
  - [ ] questions
  - [ ] question_document_references
  - [ ] question_gap_references
  - [ ] proposals
  - [ ] proposal_documents
  - [ ] proposal_gaps
  - [ ] qdrant_collections
  - [ ] vector_sync_log
  - [ ] users
  - [ ] organizations
  - [ ] projects
  - [ ] jobs
- [ ] Índices creados correctamente
- [ ] Middleware de versioning configurado en código (según ADR-006, no triggers de base de datos)
- [ ] Schema versionado con Alembic (migration 001_initial_schema)
- [ ] Comando `alembic current` muestra versión actual
- [ ] Comando `alembic upgrade head` aplica migrations pendientes
- [ ] Comando `alembic downgrade base` revierte migrations

#### Prioridad - RF-002: Alta

### RF-003: Redis Setup

#### Descripción - RF-003

Configurar Redis como broker para Celery y como cache del sistema.

#### Criterios de Aceptación - RF-003

- [ ] Redis acepta conexiones en puerto 6379
- [ ] AOF (Append Only File) habilitado para durabilidad
- [ ] Comando `redis-cli ping` responde `PONG`
- [ ] Persistencia de datos verificada (datos sobreviven restart de contenedor)
- [ ] Configuración optimizada para uso como broker y cache (AOF enabled para durabilidad, rol dual)

#### Prioridad - RF-003: Alta

### RF-004: Qdrant Setup

#### Descripción - RF-004

Configurar Qdrant para la búsqueda semántica y el almacenamiento de embeddings.

#### Criterios de Aceptación - RF-004

- [ ] Qdrant acepta conexiones HTTP en puerto 6333
- [ ] Qdrant acepta conexiones gRPC en puerto 6334
- [ ] Colección de prueba puede crearse vía API
- [ ] Embeddings pueden almacenarse y recuperarse (BGE-M3, 1024 dimensions, cosine similarity)
- [ ] Búsqueda semántica funciona con vectores de prueba
- [ ] Persistencia de datos verificada (colecciones sobreviven restart)

#### Prioridad - RF-004: Alta

### RF-005: Ollama Setup (Fuera de Docker)

#### Descripción - RF-005

Configurar Ollama con el modelo Qwen 3.5 como proveedor de LLM local, ejecutándose fuera de Docker (en el host o máquina remota) y conectado mediante Tailscale.

#### Criterios de Aceptación - RF-005

- [ ] Ollama está instalado y corriendo en el host o máquina remota
- [ ] Ollama es accesible desde contenedores Docker mediante Tailscale
- [ ] Modelo Qwen 3.5 está instalado (`ollama list` muestra qwen:3.5)
- [ ] Comando `ollama run qwen:3.5` responde a prompts de prueba
- [ ] API de Ollama responde a requests HTTP vía Tailscale
- [ ] Latencia de respuesta aceptable para desarrollo local
- [ ] Documentación de configuración de Tailscale incluida en README

#### Prioridad - RF-005: Alta

### RF-006: Environment Configuration

#### Descripción - RF-006

Configurar las variables de entorno y la gestión de secrets para el entorno de desarrollo local.

#### Criterios de Aceptación - RF-006

- [ ] Archivo `.env.example` creado con todas las variables requeridas
- [ ] Archivo `.env` creado con valores de desarrollo local
- [ ] Variables de entorno documentadas en README
- [ ] Secrets sensibles (passwords, API keys) no commiteados a Git
- [ ] `.env` incluido en `.gitignore`
- [ ] Script de validación verifica que todas las variables requeridas estén seteadas

#### Variables de Entorno Requeridas - RF-006

- `POSTGRES_PASSWORD`: Password de PostgreSQL
- `POSTGRES_DB`: Nombre de database (alejandria)
- `POSTGRES_USER`: Usuario de PostgreSQL (alejandria)
- `REDIS_URL`: URL de conexión a Redis
- `QDRANT_URL`: URL de conexión a Qdrant
- `OLLAMA_URL`: URL de conexión a Ollama (vía Tailscale, e.g., http://TAILSCALE_IP:11434)
- `OLLAMA_MODEL`: Modelo a usar (qwen:3.5)

#### Prioridad - RF-006: Media

### RF-007: Health Checks

#### Descripción - RF-007

Implementar health checks para verificar que todos los servicios se encuentren operativos.

#### Criterios de Aceptación - RF-007

- [ ] Script `scripts/health-check.sh` verifica estado de todos los servicios
- [ ] Health check de PostgreSQL: conexión exitosa
- [ ] Health check de Redis: comando `ping` responde
- [ ] Health check de Qdrant: API responde a `/health` (endpoint estándar)
- [ ] Health check de Ollama: API responde a `/api/version` vía Tailscale (endpoint ligero para verificar servicio corriendo)
- [ ] Script retorna exit code 0 si todos los servicios healthy, 1 si algún servicio falla
- [ ] Script puede ejecutarse como parte de CI/CD

#### Prioridad - RF-007: Media

### RF-008: Documentation

#### Descripción - RF-008

Documentar la configuración inicial, el troubleshooting y los workflows de desarrollo local.

#### Criterios de Aceptación - RF-008

- [ ] README.md con instrucciones de setup inicial
- [ ] Guía paso a paso para instalar Docker Desktop
- [ ] Guía paso a paso para levantar stack local
- [ ] Sección de troubleshooting con problemas comunes y soluciones
- [ ] Documentación de comandos útiles (logs, restart, cleanup)
- [ ] Diagrama de arquitectura de servicios locales
- [ ] Guía de acceso a cada servicio (psql, redis-cli, etc.)

#### Prioridad - RF-008: Media

---

## Requisitos No Funcionales

### RNF-001: Usabilidad

#### Criterios - RNF-001

- [ ] Un desarrollador nuevo puede configurar el stack en menos de 15 minutos (alineado con ADR-003, asume Docker Desktop pre-instalado)
- [ ] Los comandos de Docker Compose son intuitivos y están bien documentados
- [ ] Los logs de los servicios son claros y permiten debugging efectivo
- [ ] Los errores de configuración presentan mensajes claros

### RNF-002: Mantenibilidad

#### Criterios - RNF-002

- [ ] El archivo de Docker Compose está versionado en Git
- [ ] Las versiones de las imágenes Docker están documentadas
- [ ] Las migraciones de la base de datos están versionadas con Alembic
- [ ] La configuración está centralizada en Docker Compose (centraliza la configuración de servicios en un archivo YAML + .env, minimizando archivos de configuración dispersos)

**Nota sobre Portabilidad**: Docker Desktop soporta macOS, Linux (Docker Engine) y Windows (WSL2). El stack no tiene dependencias específicas del sistema operativo. Validado en macOS; otros sistemas operativos pendientes de validación.

---

## Casos de Uso

### UC-001: Setup Inicial de Desarrollo Local

#### Actor - UC-001: Desarrollador nuevo

#### Precondiciones - UC-001

- Docker Desktop instalado
- Git clonado
- En directorio raíz del proyecto

#### Flujo Principal - UC-001

1. El desarrollador copia `.env.example` a `.env`
2. El desarrollador configura las variables de entorno en `.env`
3. El desarrollador ejecuta `docker-compose up -d`
4. Todos los servicios se levantan sin errores
5. El desarrollador ejecuta `scripts/health-check.sh`
6. El health check confirma que todos los servicios están operativos
7. El desarrollador puede comenzar el desarrollo

#### Postcondiciones - UC-001

- El stack local se encuentra en ejecución
- Todos los servicios son accesibles
- La base de datos está inicializada con el schema

### UC-002: Verificación de Servicios

#### Actor - UC-002: Desarrollador

#### Precondiciones - UC-002

- Stack local corriendo

#### Flujo Principal - UC-002

1. El desarrollador ejecuta `docker-compose ps`
2. El desarrollador verifica que todos los servicios se encuentren en estado "Up"
3. El desarrollador ejecuta `scripts/health-check.sh`
4. El health check confirma el estado de cada servicio
5. Si algún servicio falla, el desarrollador revisa los logs con `docker-compose logs <service>`

#### Postcondiciones - UC-002

- El estado de los servicios es conocido
- Los problemas se identifican si existen

### UC-003: Restart de Servicios

#### Actor - UC-003: Desarrollador

#### Precondiciones - UC-003

- Stack local corriendo
- Algún servicio requiere restart

#### Flujo Principal - UC-003

1. El desarrollador ejecuta `docker-compose restart <service>`
2. El servicio específico se reinicia
3. El desarrollador ejecuta `scripts/health-check.sh`
4. El health check confirma que el servicio se encuentra operativo nuevamente

#### Postcondiciones - UC-003

- El servicio se ha reiniciado
- Los datos persisten (sin pérdida de información)

---

## Dependencias

### Dependencias Externas

- Docker Desktop (última versión estable)
- Git (para clonar el repositorio)
- Python 3.11+ (para ejecutar Alembic localmente si es necesario)

### Dependencias Internas

- database-schema.md: Schema inicial de PostgreSQL
- ADR-003: Decisión de usar Docker Compose
- technology-stack.md: Versiones específicas de las tecnologías

### Dependencias de Otros Hitos

- Ninguna (hito inicial)

---

## Criterios de Completitud del Hito

Basado en technical-roadmap.md, el Hito 1 se considera completo cuando:

- [ ] Docker Compose levanta todos los servicios de datos sin errores
- [ ] PostgreSQL acepta conexiones y tiene schema versionado
- [ ] Redis acepta conexiones como broker
- [ ] Qdrant acepta conexiones y permite crear colecciones
- [ ] Ollama (fuera de Docker) responde a prompts con Qwen 3.5 vía Tailscale

### Criterios Adicionales de este PRD

- [ ] Todos los requisitos funcionales (RF-001 a RF-008) están cumplidos
- [ ] Todos los requisitos no funcionales (RNF-001 a RNF-002) están cumplidos
- [ ] La documentación está completa y es usable
- [ ] Los health checks están funcionando
- [ ] El stack es reproducible en diferentes máquinas

---

## Criterio de Éxito

**Objetivo cualitativo**: El stack local es usable para el desarrollo sin fricción significativa.

Justificación: Para el MVP Bootstrapped (desarrollo local, un usuario), las métricas numéricas como tickets de soporte y satisfacción no aplican. El criterio de completitud del hito (líneas 345-358) define qué significa "completado" desde la perspectiva técnica.

---

## Riesgos y Mitigación

### Riesgo 1: Docker Desktop no funciona en la máquina del desarrollador

**Mitigación**: Documentar alternativas (Docker Engine en Linux, WSL2 en Windows). Proporcionar una máquina de desarrollo cloud preconfigurada si es necesario.

### Riesgo 2: Ollama requiere recursos excesivos de CPU/Memoria

**Mitigación**: Documentar los requisitos mínimos de hardware (16GB RAM, 4 núcleos CPU según ADR-003). Ejecutar Ollama fuera de Docker permite mejor aislamiento y flexibilidad. Permitir usar Ollama en una máquina separada conectada vía Tailscale o en un servicio cloud durante el desarrollo.

---

## Referencias Adicionales

- [technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md): Hito 1 - Infraestructura Base
- [ADR-003](../decisiones/adr-003-local-infrastructure-docker-compose.md): Local Infrastructure with Docker Compose
- [technology-stack.md](../arquitectura/technology-stack.md): Stack tecnológico recomendado
- [database-schema-design.md](../arquitectura/database-schema-design.md): Diseño conceptual de schema de PostgreSQL
- [architecture-overview.md](../arquitectura/architecture-overview.md): Decisiones de diseño arquitectónico

---

*Documento generado como PRD para Hito 1 del roadmap técnico.*
*Fecha de creación: 2026-05-23.*
*Última revisión: 2026-05-25*
