---
id: T-003
type: Task
rating: 9.0
rating-phase: document-editing
related:
  - target: T-002
    relationship_type: depends_on
    reason: Depende de la configuración de Docker Compose para definir variables de entorno de servicios
  - target: TRD-001
    relationship_type: implements
    reason: Implementa el requisito RF-006 de configuración de variables de entorno
  - target: ADR-003
    relationship_type: implements
    reason: Implementa la configuración de variables de entorno según ADR-003
---

# T-003: Configurar variables de entorno

**Tipo**: Task
**Prioridad**: Media
**Estimación**: 1 hora
**Dependencias**: T-002

## Descripción

Crear archivos de configuración de variables de entorno para desarrollo local según ADR-003.

## Criterios de Aceptación

- [ ] Archivo `.env.example` creado con todas las variables requeridas
- [ ] Archivo `.env` creado con valores de desarrollo local
- [ ] Variables documentadas en README
- [ ] `.env` incluido en `.gitignore`
- [ ] Script de validación verifica variables requeridas

## Criterios de Éxito

- Script de validación funcional y detecta variables faltantes
- Variables documentadas correctamente con descripciones claras
- `.env.example` contiene todas las variables requeridas sin valores sensibles
- `.env` no está commiteado a Git (verificado en `.gitignore`)

**Nota sobre validación de variables sensibles:** Se usa estrategia simple: solo .gitignore. Asegurar que `.env` está en `.gitignore`, documentar que `.env` nunca debe commitearse, y depende de la disciplina del desarrollador para seguir esta regla. Para desarrollo local, .gitignore es suficiente. Pre-commit hooks o herramientas de secret scanning son sobre esfuerzo para esta fase. Si el proyecto crece o se requiere para producción, se puede agregar pre-commit hooks más adelante.

## Variables de Entorno

```bash
# PostgreSQL
POSTGRES_DB=alejandria
POSTGRES_USER=alejandria
POSTGRES_PASSWORD=changeme

# Redis
REDIS_URL=redis://localhost:6379/0

# Qdrant
QDRANT_URL=http://localhost:6333

# Ollama
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen:3.5
```

### Descripción de Variables

- **POSTGRES_DB**: Nombre de la base de datos PostgreSQL (default: alejandria)
- **POSTGRES_USER**: Usuario de PostgreSQL (default: alejandria)
- **POSTGRES_PASSWORD**: Password de PostgreSQL (requerido, cambiar en producción)
- **REDIS_URL**: URL de conexión a Redis (formato: `redis://host:port/db`)
- **QDRANT_URL**: URL de conexión a Qdrant (formato: `http://host:port`)
- **OLLAMA_URL**: URL de conexión a Ollama (formato: `http://host:port`)
- **OLLAMA_MODEL**: Modelo de Ollama a usar (default: qwen:3.5)

## Referencias

- [TRD - Hito 1](../propuestas/trd-milestone-1-infrastructure.md): RF-006: Environment Configuration
- [ADR-003](../decisiones/adr-003-local-infrastructure-docker-compose.md): Local Infrastructure with Docker Compose (sección "Configuración de Variables de Entorno")

---

## Dependencias con Otras Tareas

Esta tarea (T-003) depende de:

- **T-002** (Docker Compose): Requiere Docker Compose configurado para definir variables de entorno de servicios

Esta tarea (T-003) es prerequisito para:

- **T-010** (Configuración Ollama): Requiere variables de entorno OLLAMA_URL y OLLAMA_MODEL definidas
- **T-011** (Health check): Requiere variables de entorno para conectar a servicios
- **T-013** (Script setup): Requiere variables de entorno documentadas para script automatizado

---

## Seguridad

### Rotación de Secrets

No hay rotación programada de secrets en desarrollo local.

**Estrategia:**

- Los passwords de desarrollo son para uso local solamente
- No hay rotación programada ni frecuencia definida
- Cambiar solo si hay un incidente de seguridad o cuando el desarrollador lo decida
- Es suficiente para desarrollo local

**Justificación:** Para desarrollo local, la rotación programada de secrets es sobre esfuerzo. Los passwords son para uso local y no están expuestos externamente. Rotación puede considerarse más adelante si el proyecto se mueve a producción.
