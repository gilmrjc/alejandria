#!/bin/bash
# Script de verificación de Qdrant (T-008)
# Verifica que Qdrant está configurado correctamente

set -e

echo "=========================================="
echo "Verificación de Qdrant"
echo "=========================================="

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Cambiar al directorio raíz para encontrar docker-compose.yml
cd "$(dirname "$0")/.."

QDRANT_URL="${QDRANT_URL:-http://localhost:6333}"

# Verificar que Qdrant HTTP responde
echo -n "Qdrant HTTP API: "
if curl -f -s "$QDRANT_URL/" > /dev/null; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAILED${NC}"
    exit 1
fi

# Verificar health endpoint
echo -n "Health check: "
if curl -f -s "$QDRANT_URL/" > /dev/null; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAILED${NC}"
    exit 1
fi

# Crear colección de prueba
echo "Creando colección de prueba..."
TEST_COLLECTION="test_collection_$(date +%s)"
if curl -f -s -X PUT "$QDRANT_URL/collections/$TEST_COLLECTION" \
    -H 'Content-Type: application/json' \
    -d '{
        "vectors": {
            "size": 1024,
            "distance": "Cosine"
        }
    }' > /dev/null; then
    echo -e "  ${GREEN}OK${NC} (colección creada)"
else
    echo -e "  ${RED}FAILED${NC} (no se pudo crear colección)"
    exit 1
fi

# Insertar vector de prueba
echo "Insertando vector de prueba..."
VECTOR_DATA='{"points": [{"id": 1, "vector": ['
for i in $(seq 1 1024); do
    if [ $i -eq 1024 ]; then
        VECTOR_DATA="${VECTOR_DATA}0.001"
    else
        VECTOR_DATA="${VECTOR_DATA}0.001,"
    fi
done
VECTOR_DATA="${VECTOR_DATA}], \"payload\": {\"test\": true}}]}"

if curl -f -s -X PUT "$QDRANT_URL/collections/$TEST_COLLECTION/points" \
    -H 'Content-Type: application/json' \
    -d "$VECTOR_DATA" > /dev/null; then
    echo -e "  ${GREEN}OK${NC} (vector insertado)"
else
    echo -e "  ${RED}FAILED${NC} (no se pudo insertar vector)"
    exit 1
fi

# Buscar vector
echo "Probando búsqueda semántica..."
QUERY_VECTOR='['
for i in $(seq 1 1024); do
    if [ $i -eq 1024 ]; then
        QUERY_VECTOR="${QUERY_VECTOR}0.001"
    else
        QUERY_VECTOR="${QUERY_VECTOR}0.001,"
    fi
done
QUERY_VECTOR="${QUERY_VECTOR}]"

RESULT=$(curl -f -s -X POST "$QDRANT_URL/collections/$TEST_COLLECTION/points/search" \
    -H 'Content-Type: application/json' \
    -d "{\"vector\": $QUERY_VECTOR, \"limit\": 1}" || echo "{}")

if echo "$RESULT" | grep -q '"result"'; then
    echo -e "  ${GREEN}OK${NC} (búsqueda funciona)"
else
    echo -e "  ${RED}FAILED${NC} (búsqueda falló)"
    exit 1
fi

# Eliminar colección de prueba
curl -f -s -X DELETE "$QDRANT_URL/collections/$TEST_COLLECTION" > /dev/null
echo "  Colección de prueba eliminada"

echo ""
echo -e "${GREEN}✓ Qdrant verificado exitosamente${NC}"
