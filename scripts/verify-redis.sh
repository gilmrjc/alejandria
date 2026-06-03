#!/bin/bash
# Script de verificación de Redis (T-007)
# Verifica que Redis está configurado correctamente con AOF

set -e

echo "=========================================="
echo "Verificación de Redis"
echo "=========================================="

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Cambiar al directorio raíz para encontrar docker-compose.yml
cd "$(dirname "$0")/.."

# Verificar que Redis responde
echo -n "Redis ping: "
if docker compose exec -T redis redis-cli ping | grep -q "PONG"; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAILED${NC}"
    exit 1
fi

# Verificar AOF está habilitado
echo -n "AOF persistencia: "
AOF_RESULT=$(docker compose exec -T redis redis-cli CONFIG GET appendonly | tail -1)
if [ "$AOF_RESULT" = "yes" ]; then
    echo -e "${GREEN}OK${NC} (AOF habilitado)"
else
    echo -e "${RED}FAILED${NC} (AOF deshabilitado)"
    exit 1
fi

# Test de persistencia
echo "Test de persistencia:"
TEST_KEY="test_$(date +%s)"
TEST_VALUE="test_value_$(date +%s)"

docker compose exec -T redis redis-cli SET "$TEST_KEY" "$TEST_VALUE" > /dev/null
echo -n "  - Guardar dato: "
echo -e "${GREEN}OK${NC}"

# Reiniciar Redis
docker compose restart redis > /dev/null 2>&1
echo -n "  - Reiniciar Redis: "
echo -e "${GREEN}OK${NC}"

# Esperar a que Redis esté listo
sleep 3

# Verificar que el dato persiste
echo -n "  - Verificar persistencia: "
RESULT=$(docker compose exec -T redis redis-cli GET "$TEST_KEY" 2>/dev/null || echo "NIL")
if [ "$RESULT" = "$TEST_VALUE" ]; then
    echo -e "${GREEN}OK${NC}"
    docker compose exec -T redis redis-cli DEL "$TEST_KEY" > /dev/null
else
    echo -e "${RED}FAILED${NC} (dato no persistió)"
    exit 1
fi

# Medir latencia (simple)
echo "Latencia de Redis:"
LATENCY=$(docker compose exec -T redis redis-cli --latency 2>/dev/null | head -1 || echo "N/A")
echo "  - $LATENCY"

echo ""
echo -e "${GREEN}✓ Redis verificado exitosamente${NC}"
