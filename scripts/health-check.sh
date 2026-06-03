#!/bin/bash
# Script de Health Check para todos los servicios (T-010)
# Verifica el estado de PostgreSQL, Redis, Qdrant y Ollama

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Load common functions
source scripts/common.sh

echo "=========================================="
echo "Alejandria - Health Check"
echo "=========================================="
echo ""

# Cargar variables de entorno si existen
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs 2>/dev/null || true)
fi

# Verificar PostgreSQL
echo "Verificando PostgreSQL..."
check_service "PostgreSQL" "docker compose exec -T postgresql pg_isready -U ${POSTGRES_USER:-alejandria}"
POSTGRES_STATUS=$?

# Verificar Redis
echo "Verificando Redis..."
check_service "Redis" "docker compose exec -T redis redis-cli ping"
REDIS_STATUS=$?

# Verificar Qdrant
echo "Verificando Qdrant..."
QDRANT_URL="${QDRANT_URL:-http://localhost:6333}"
check_service "Qdrant" "curl -f ${QDRANT_URL}/"
QDRANT_STATUS=$?


# Resumen
echo ""
echo "=========================================="
echo "Resumen de Health Check"
echo "=========================================="

if [ $POSTGRES_STATUS -eq 0 ] && [ $REDIS_STATUS -eq 0 ] && [ $QDRANT_STATUS -eq 0 ]; then
    echo -e "${GREEN}✓ Servicios Docker (PostgreSQL, Redis, Qdrant) están healthy${NC}"
    echo ""
    echo "El stack está listo para usar!"
    exit 0
else
    echo -e "${RED}✗ Algunos servicios Docker fallaron${NC}"
    echo ""

    if [ $POSTGRES_STATUS -ne 0 ]; then
        echo "  PostgreSQL: Verifica 'docker compose ps postgresql' y logs"
    fi
    if [ $REDIS_STATUS -ne 0 ]; then
        echo "  Redis: Verifica 'docker compose ps redis' y logs"
    fi
    if [ $QDRANT_STATUS -ne 0 ]; then
        echo "  Qdrant: Verifica 'docker compose ps qdrant' y logs"
    fi

    echo ""
    echo "Para más información, revisa los logs:"
    echo "  docker compose logs [servicio]"

    exit 1
fi
