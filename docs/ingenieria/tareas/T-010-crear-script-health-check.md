---
id: T-010
type: Task
rating: 9.0
rating-phase: document-editing
related:
  - target: T-007
    relationship_type: depends_on
    reason: Depende de la verificación de Redis para incluir en health check
  - target: T-008
    relationship_type: depends_on
    reason: Depende de la verificación de Qdrant para incluir en health check
  - target: T-009
    relationship_type: depends_on
    reason: Depende de la verificación de Ollama para incluir en health check
  - target: TRD-001
    relationship_type: implements
    reason: Implementa el requisito RF-007 de health checks
---

# T-010: Crear script de health check

**Tipo**: Task
**Prioridad**: Media
**Estimación**: 2 horas
**Dependencias**: T-007, T-008, T-009

## Descripción

Crear script `scripts/health-check.sh` que verifica estado de todos los servicios según ADR-003.

Bash se usa por portabilidad y simplicidad para scripts de health check. La estimación de 2 horas es razonable para implementar verificaciones de 4 servicios con manejo de errores y output legible. Ollama se verifica vía OLLAMA_URL (variable de entorno) porque se ejecuta fuera de Docker conectado vía Tailscale según ADR-003.

## Criterios de Aceptación

- [ ] Script `scripts/health-check.sh` creado
- [ ] Script verifica estado de PostgreSQL
- [ ] Script verifica estado de Redis
- [ ] Script verifica estado de Qdrant
- [ ] Script verifica estado de Ollama
- [ ] Script retorna exit code 0 si todos los servicios healthy
- [ ] Script retorna exit code 1 si algún servicio falla
- [ ] Script puede ejecutarse como parte de CI/CD
- [ ] Script tiene output legible con estado de cada servicio

## Criterios de Éxito

- Script ejecuta sin errores de sintaxis bash
- Exit codes correctos (0 para éxito, 1 para fallo)
- Output legible con colores y mensajes claros
- Script puede ejecutarse en CI/CD sin interacción manual
- Verificaciones de servicios funcionan correctamente

## Contenido de health-check.sh

```bash
#!/bin/bash

# Cargar variables de entorno
if [ -f .env ]; then
  export $(cat .env | grep -v '^#' | xargs)
fi

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Función para verificar servicio
check_service() {
  local service_name=$1
  local check_command=$2
  local max_retries=3
  local retry_delay=2
  local timeout=5

  for i in $(seq 1 $max_retries); do
    if timeout $timeout bash -c "$check_command" > /dev/null 2>&1; then
      echo -e "${GREEN}✓${NC} $service_name: OK"
      return 0
    else
      if [ $i -lt $max_retries ]; then
        echo -e "${YELLOW}⚠${NC} $service_name: Retry $i/$max_retries..."
        sleep $retry_delay
      fi
    fi
  done

  echo -e "${RED}✗${NC} $service_name: FAILED"
  return 1
}

# Verificar PostgreSQL
check_service "PostgreSQL" "docker-compose exec -T postgresql pg_isready -U ${POSTGRES_USER:-alejandria}"
POSTGRES_STATUS=$?

# Verificar Redis
check_service "Redis" "docker-compose exec -T redis redis-cli ping"
REDIS_STATUS=$?

# Verificar Qdrant
check_service "Qdrant" "curl -f ${QDRANT_URL:-http://localhost:6333}/health"
QDRANT_STATUS=$?

# Verificar Ollama (usa OLLAMA_URL de variables de entorno porque se ejecuta fuera de Docker)
check_service "Ollama" "curl -f ${OLLAMA_URL:-http://localhost:11434}/api/tags"
OLLAMA_STATUS=$?

# Exit code
if [ $POSTGRES_STATUS -eq 0 ] && [ $REDIS_STATUS -eq 0 ] && [ $QDRANT_STATUS -eq 0 ] && [ $OLLAMA_STATUS -eq 0 ]; then
  echo -e "\n${GREEN}Todos los servicios están healthy${NC}"
  exit 0
else
  echo -e "\n${RED}Algunos servicios fallaron${NC}"
  exit 1
fi
```

## Referencias

- [TRD - Hito 1](../propuestas/trd-milestone-1-infrastructure.md): RF-007: Health Checks

---

## Dependencias con Otras Tareas

Esta tarea (T-010) depende de:

- **T-007** (Verificación Redis): Requiere verificación de Redis para incluir en health check
- **T-008** (Verificación Qdrant): Requiere verificación de Qdrant para incluir en health check
- **T-009** (Configuración Ollama): Requiere verificación de Ollama para incluir en health check

Esta tarea (T-010) es prerequisito para:

- **T-011** (README): Requiere health check funcional para documentarlo en README
- **T-012** (Script setup): Requiere health check para verificar estado después de setup automatizado
