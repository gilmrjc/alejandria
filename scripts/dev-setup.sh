#!/bin/bash
# Script de setup automatizado para Alejandria (T-012)
# Automatiza todo el proceso de setup inicial

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Load common functions
source scripts/common.sh

# Colores adicionales
BLUE='\033[0;34m'

echo "=========================================="
echo "Alejandria - Automated Setup"
echo "=========================================="
echo ""

# ============================================
# Funciones de ayuda
# ============================================

print_step() {
    echo ""
    echo -e "${BLUE}[Step $1/$2]${NC} $3"
    echo "=========================================="
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# ============================================
# Step 1: Verificar prerrequisitos
# ============================================
TOTAL_STEPS=6
print_step 1 $TOTAL_STEPS "Verificando prerrequisitos"

# Verificar Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker no está instalado. Por favor instala Docker Desktop."
    exit 1
fi
print_success "Docker encontrado"

# Verificar Docker Compose (versión moderna)
if ! docker compose version &> /dev/null; then
    print_error "Docker Compose no está disponible. Actualiza Docker Desktop."
    exit 1
fi
print_success "Docker Compose disponible"

# Verificar Git
if ! command -v git &> /dev/null; then
    print_error "Git no está instalado."
    exit 1
fi
print_success "Git encontrado"

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.yml" ]; then
    print_error "No se encuentra docker-compose.yml. ¿Estás en el directorio raíz del proyecto?"
    exit 1
fi

print_success "Estructura del proyecto verificada"

# ============================================
# Step 2: Configurar variables de entorno
# ============================================
print_step 2 $TOTAL_STEPS "Configurando variables de entorno"

if [ -f ".env" ]; then
    print_warning ".env ya existe. ¿Deseas sobrescribirlo? (s/N)"
    read -r response
    if [[ ! "$response" =~ ^[Ss]$ ]]; then
        print_success "Manteniendo .env existente"
    else
        cp .env.example .env
        print_success ".env creado desde .env.example"
        print_warning "Recuerda editar .env con tus configuraciones personalizadas"
    fi
else
    cp .env.example .env
    print_success ".env creado desde .env.example"
    print_warning "Recuerda editar .env con tus configuraciones personalizadas"
fi

# ============================================
# Step 3: Levantar servicios con Docker Compose
# ============================================
print_step 3 $TOTAL_STEPS "Levantando servicios con Docker Compose"

# Detener servicios existentes si hay
print_warning "Deteniendo servicios existentes si los hay..."
docker compose down 2>/dev/null || true

# Levantar servicios
print_success "Iniciando PostgreSQL, Redis y Qdrant..."
docker compose up -d

# Esperar a que PostgreSQL esté listo
print_warning "Esperando a que PostgreSQL esté listo..."
if wait_for_service "PostgreSQL" "docker compose exec -T postgresql pg_isready -U alejandria" 30 2; then
    print_success "PostgreSQL listo"
else
    print_error "PostgreSQL no se inició"
    exit 1
fi

# Esperar a que Redis esté listo
print_warning "Esperando a que Redis esté listo..."
if wait_for_service "Redis" "docker compose exec -T redis redis-cli ping" 30 2; then
    print_success "Redis listo"
else
    print_error "Redis no se inició"
    exit 1
fi

# Esperar a que Qdrant esté listo
print_warning "Esperando a que Qdrant esté listo..."
if wait_for_service "Qdrant" "curl -f -s http://localhost:6333/" 30 2; then
    print_success "Qdrant listo"
else
    print_error "Qdrant no se inició"
    exit 1
fi


# ============================================
# Step 4: Aplicar migrations de base de datos
# ============================================
print_step 4 $TOTAL_STEPS "Aplicando migrations de base de datos"

print_success "Aplicando migrations dentro del contenedor dev..."
docker compose --profile dev run --rm dev uv run alembic -c alembic.ini upgrade head
if [ $? -eq 0 ]; then
    print_success "Migrations aplicados correctamente"
else
    print_error "Error aplicando migrations"
    print_warning "Verifica que las tablas no existan ya"
    exit 1
fi

# ============================================
# Step 4.5: Crear base de datos de pruebas
# ============================================
print_warning "Creando base de datos de pruebas..."
docker compose exec -T postgresql psql -U alejandria -c "CREATE DATABASE alejandria_test;" 2>/dev/null || print_warning "La base de datos de pruebas ya existe"

print_success "Aplicando migrations a base de datos de pruebas..."
docker compose --profile dev run --rm dev sh -c "cd /workspace && DATABASE_URL=postgresql://alejandria:changeme@postgresql:5432/alejandria_test uv run alembic upgrade head"
if [ $? -eq 0 ]; then
    print_success "Migrations de pruebas aplicados correctamente"
else
    print_error "Error aplicando migrations de pruebas"
    exit 1
fi

# ============================================
# Step 5: Health check
# ============================================
print_step 5 $TOTAL_STEPS "Ejecutando verificación de servicios"

if ./scripts/health-check.sh; then
    print_success "Todos los servicios están healthy"
else
    print_error "Algunos servicios no responden"
    echo ""
    echo "Puedes verificar manualmente con:"
    echo "  docker compose ps"
    echo "  docker compose logs [servicio]"
    exit 1
fi

# ============================================
# Step 6: Resumen
# ============================================
print_step 6 $TOTAL_STEPS "Setup completado"

echo ""
echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN}    Alejandria está listo para usar!${NC}"
echo -e "${GREEN}==========================================${NC}"
echo ""
echo "Servicios disponibles:"
echo "  - PostgreSQL: localhost:5432"
echo "  - Redis:      localhost:6379"
echo "  - Qdrant:     localhost:6333"
echo ""
echo "Próximos pasos:"
echo "  1. Ejecuta backend: cd backend && python run.py api"
echo "  2. Visita: http://localhost:8000/docs"
echo ""
echo "Comandos útiles:"
echo "  - Ver logs: cd docker && docker compose logs -f"
echo "  - Health check: ./scripts/health-check.sh"
echo "  - Verificar Redis: ./scripts/verify-redis.sh"
echo "  - Verificar Qdrant: ./scripts/verify-qdrant.sh"
echo ""
echo "Documentación:"
echo "  - README.md"
echo "  - docs/ingenieria/"
echo "  - docs/producto/"
echo ""
print_success "Setup completado exitosamente"
