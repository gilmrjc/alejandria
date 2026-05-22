---
id: T-011
type: Task
rating: 9.0
rating-phase: document-editing
related:
  - target: T-003
    relationship_type: depends_on
    reason: Depende de las variables de entorno configuradas para documentar en README
  - target: T-010
    relationship_type: depends_on
    reason: Depende del script de health check para documentar en README
---

# T-011: Crear README con instrucciones de setup

**Tipo**: Task
**Prioridad**: Media
**Estimación**: 2 horas
**Dependencias**: T-003, T-010

## Descripción

Crear README.md con instrucciones completas de setup y troubleshooting según ADR-003. La estimación de 2 horas es razonable para documentar setup completo con troubleshooting. El nivel de detalle sigue mejores prácticas de documentación técnica (prerrequisitos, setup paso a paso, comandos útiles, troubleshooting). El diagrama de arquitectura puede ser ASCII o Mermaid por simplicidad. Los problemas "comunes" incluyen: Docker Desktop no inicia, puertos en uso, Ollama no accesible vía Tailscale.

## Criterios de Aceptación

- [ ] README.md creado con descripción del proyecto
- [ ] Guía paso a paso para instalar Docker Desktop
- [ ] Guía paso a paso para configurar variables de entorno
- [ ] Guía paso a paso para levantar stack local
- [ ] Sección de troubleshooting con problemas comunes
- [ ] Documentación de comandos útiles (logs, restart, cleanup)
- [ ] Diagrama de arquitectura de servicios locales
- [ ] Guía de acceso a cada servicio (psql, redis-cli, etc.)
- [ ] Documentación de configuración de Tailscale para Ollama

## Estructura del README

```markdown
# Alejandria - Local Development Setup

## Prerrequisitos

- Docker Desktop (última versión)
- Git
- Python 3.11+ (opcional, para Alembic local)

## Setup Inicial

1. Clonar repositorio
2. Configurar variables de entorno
3. Levantar stack con Docker Compose
4. Verificar health checks

## Comandos Útiles

### Levantar stack
docker-compose up -d

### Ver logs
docker-compose logs -f

### Verificar estado
docker-compose ps
./scripts/health-check.sh

### Restart de servicios
docker-compose restart <service>

### Limpiar todo
docker-compose down -v

## Acceso a Servicios

### PostgreSQL
docker-compose exec postgresql psql -U alejandria -d alejandria

### Redis
docker-compose exec redis redis-cli

### Qdrant
curl http://localhost:6333/

### Ollama (vía Tailscale)
curl $OLLAMA_URL/api/tags

## Troubleshooting

### Docker Desktop no inicia
...

### PostgreSQL no acepta conexiones
...

### Ollama no descarga modelo
...
```

## Mantenimiento

### Estrategia de Actualización del README

Se usa actualización del README según necesidad por el desarrollador.

**Cambios que requieren actualización del README:**

- Variables de entorno (nuevas variables, cambios de nombres)
- Puertos de servicios (cambios en docker-compose.yml)
- Comandos de setup (nuevos comandos, cambios en sintaxis)
- Estructura de servicios (nuevos servicios, cambios en arquitectura)
- Procedimientos de troubleshooting (nuevos problemas, soluciones actualizadas)

**Proceso:**

- El desarrollador actualiza el README cuando hace cambios relevantes
- Verificar que las instrucciones siguen siendo reproducibles después de cambios
- Documentar cambios en el commit message para rastreo

**Justificación:** Para desarrollo local, la actualización según necesidad es suficiente. Procesos formales de revisión periódica o validación automatizada pueden agregarse más adelante si el proyecto crece.

### Validación de Reproducibilidad

Se usa validación manual por el desarrollador siguiendo las instrucciones del README.

**Proceso de validación:**

- El desarrollador sigue las instrucciones del README después de cambios relevantes
- Verificar que cada paso funciona correctamente
- Ejecutar `./scripts/health-check.sh` al final para validar que todos los servicios están operativos
- Documentar cualquier discrepancia encontrada

**Justificación:** Para desarrollo local, la validación manual es suficiente. Pruebas automatizadas que sigan las instrucciones del README pueden agregarse más adelante si se requiere para CI/CD.

## Criterios de Éxito

- README es reproducible y completo
- Desarrollador nuevo configura stack en <15 minutos
- Troubleshooting resuelve problemas comunes
- Comandos útiles documentados correctamente

## Referencias

- [TRD - Hito 1](../propuestas/trd-milestone-1-infrastructure.md): RF-008: Documentation
