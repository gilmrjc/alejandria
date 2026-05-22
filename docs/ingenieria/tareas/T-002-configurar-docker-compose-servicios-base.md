---
id: T-002
type: Task
rating: 9.0
rating-phase: document-editing
related:
  - target: T-001
    relationship_type: depends_on
    reason: Depende de la estructura base creada en T-001 para configurar Docker Compose
  - target: ADR-003
    relationship_type: implements
    reason: Implementa la decisión de infraestructura local con Docker Compose
---

# T-002: Configurar Docker Compose con servicios base

**Tipo**: Task
**Prioridad**: Alta
**Estimación**: 2 horas
**Dependencias**: T-001

## Descripción

Crear archivo `docker-compose.yml` con configuración de servicios base (PostgreSQL, Redis, Qdrant) según ADR-003. Ollama se ejecuta fuera de Docker, conectado vía Tailscale.

La configuración específica de Docker Compose sigue ADR-003 con versiones específicas (criterio "latest menos un minor" para estabilidad y reproducibilidad). Health checks configurados según mejores prácticas de Docker Compose.

## Criterios de Aceptación

- [ ] Archivo `docker/docker-compose.yml` creado
- [ ] Servicio PostgreSQL configurado con imagen postgres:18.3-bookworm (Versión según ADR-003: 18.3-bookworm por estabilidad y features modernas)
- [ ] Servicio Redis configurado con imagen redis:7.4.9-bookworm (Versión según ADR-003: 7.4.9-bookworm por licencia BSD3 permisiva)
- [ ] Servicio Qdrant configurado con imagen qdrant/qdrant:v1.17.1 (Versión según ADR-003: v1.17.1 por estabilidad)
- [ ] Ollama NO incluido en Docker Compose (Según ADR-003, Ollama se ejecuta fuera de Docker conectado vía Tailscale)
- [ ] Volumes Docker configurados para persistencia de datos
- [ ] Puertos expuestos correctamente para cada servicio
- [ ] Variables de entorno configuradas para cada servicio
- [ ] Health checks configurados para cada servicio
- [ ] Comando `docker-compose config` valida configuración sin errores

## Criterios de Éxito

- `docker-compose config` valida sin errores ni warnings
- `docker-compose up -d` levanta todos los servicios sin errores
- Health checks de todos los servicios pasan (servicios marcan como healthy)
- Volumes Docker se crean correctamente y persisten datos después de restart
- Servicios pueden comunicarse entre sí vía nombres de servicio Docker

### Validación de Versiones

Se usa validación manual simple combinada con documentación del proceso de actualización.

**Validación manual:**

```bash
# Verificar que las imágenes existen en Docker Hub
docker pull postgres:18.3-alpine
docker pull redis:7.4.9-alpine
docker pull qdrant/qdrant:v1.17.1
```

No hay pruebas de integración automatizadas para compatibilidad entre servicios. Se asume que si las imágenes existen, son compatibles para desarrollo local.

**Proceso si una versión no está disponible:**

1. Buscar la versión más cercana disponible en Docker Hub
2. Seguir criterio "latest menos un minor" según ADR-003
3. Actualizar docker-compose.yml con la nueva versión
4. Documentar el cambio en un commit de Git

**Justificación:** Validación manual es suficiente para desarrollo local. Pruebas de integración automatizadas son sobre esfuerzo para esta fase.

## Configuración Específica

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

## Estructura de Directorios

**Directorio docker/**:

```text
docker/
  └── docker-compose.yml
```

## Referencias

- [TRD - Hito 1](../propuestas/trd-milestone-1-infrastructure.md): RF-001: Docker Compose Configuration
- [ADR-003](../decisiones/adr-003-local-infrastructure-docker-compose.md): Local Infrastructure with Docker Compose

---

## Dependencias con Otras Tareas

Esta tarea (T-002) depende de:

- **T-001** (Estructura base): Requiere que la estructura de directorios exista para crear archivo `docker/docker-compose.yml`

Esta tarea (T-002) es prerequisito para:

- **T-003** (Variables de entorno): Requiere Docker Compose configurado para definir variables de entorno de servicios
- **T-008** (Verificación Redis): Requiere Docker Compose levantado para verificar configuración de Redis
- **T-009** (Verificación Qdrant): Requiere Docker Compose levantado para verificar configuración de Qdrant
- **T-011** (Health check): Requiere Docker Compose configurado para crear script de health check

---

## Troubleshooting

### Manejo de Conflictos de Puertos

Se usa solución manual para identificar y resolver conflictos de puertos.

**Pasos para resolver conflicto de puertos:**

1. **Identificar qué proceso está usando el puerto:**

```bash
# En macOS/Linux
lsof -i :5432  # Para PostgreSQL
lsof -i :6379  # Para Redis
lsof -i :6333  # Para Qdrant HTTP
lsof -i :6334  # Para Qdrant gRPC
```

1. **Opciones de resolución:**
   - Detener el proceso que está usando el puerto
   - Cambiar el puerto en docker-compose.yml

2. **Cambiar puerto en docker-compose.yml:**

```yaml
services:
  postgresql:
    ports:
      - "5433:5432"  # Usar puerto 5433 en host en lugar de 5432
```

**Justificación:** Es responsabilidad del desarrollador manejar conflictos de puertos en su ambiente local. La solución manual es simple y suficiente para desarrollo local.
