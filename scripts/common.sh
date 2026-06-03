#!/bin/bash
# Common functions for Alejandria scripts

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Función para verificar servicio con reintentos
wait_for_service() {
    local service_name=$1
    local check_command=$2
    local max_retries=${3:-30}
    local retry_delay=${4:-2}

    for i in $(seq 1 $max_retries); do
        if eval "$check_command" > /dev/null 2>&1; then
            echo -e "${GREEN}✓${NC} $service_name: OK"
            return 0
        else
            if [ $i -lt $max_retries ]; then
                echo -n "."
                sleep $retry_delay
            fi
        fi
    done

    echo -e "${RED}✗${NC} $service_name: FAILED"
    return 1
}

# Función para verificar servicio con reintentos y mensajes
check_service() {
    local service_name=$1
    local check_command=$2
    local max_retries=${3:-3}
    local retry_delay=${4:-2}

    for i in $(seq 1 $max_retries); do
        if eval "$check_command" > /dev/null 2>&1; then
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
