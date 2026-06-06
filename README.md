# Alejandria - Document Management System

**Alejandria** es un sistema de gestión de documentación técnica con integración de LLM (Large Language Models) que ayuda a mantener la documentación actualizada y completa mediante un pipeline de 5 fases: detección → agrupación → resolución → verificación → aplicación.

## Prerrequisitos

- **Docker Desktop** (última versión recomendada)
- **Git**

## Estructura del Proyecto

```
alejandria/
├── backend/               # Código Python (FastAPI, Celery, MCP)
│   ├── api/              # FastAPI application
│   ├── mcp/              # FastMCP server
│   ├── jobs/             # Celery tasks
│   ├── shared/           # Código compartido (db, schemas, services)
│   ├── alembic/          # Database migrations
│   │   ├── versions/     # Migration files
│   │   ├── env.py        # Alembic environment
│   │   └── script.py.mako # Template de migrations
│   ├── tests/            # Tests (unit, integration, e2e)
│   ├── pyproject.toml    # Dependencias y configuración
│   └── run.py            # Entry point unificado
├── docker-compose.yml    # Configuración Docker (PostgreSQL, Redis, Qdrant)
├── scripts/              # Scripts de utilidad
│   ├── health-check.sh   # Verificación de servicios
│   ├── dev-setup.sh      # Setup automatizado
│   ├── verify-redis.sh   # Verificación Redis
│   └── verify-qdrant.sh  # Verificación Qdrant
├── docs/                 # Documentación del proyecto
└── README.md             # Este archivo
```

## Setup Inicial

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd alejandria
```

### 2. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones
# Principalmente POSTGRES_PASSWORD y SECRET_KEY
```

### 3. Levantar servicios con Docker Compose

```bash
docker compose up -d
```

Esto iniciará:
- **PostgreSQL** (puerto 5432)
- **Redis** (puerto 6379)
- **Qdrant** (puertos 6333/6334)

### 4. Verificar instalación

```bash
./scripts/health-check.sh
```

Si todos los servicios están "healthy", la instalación fue exitosa.

### 5. Aplicar migrations de base de datos

```bash
docker compose --profile dev run --rm dev uv run alembic -c alembic.ini upgrade head
```

## Comandos Útiles

### Levantar stack
```bash
docker compose up -d
```

### Ver logs
```bash
# Todos los servicios
docker compose logs -f

# Servicio específico
docker compose logs -f postgresql
```

### Verificar estado
```bash
docker compose ps
./scripts/health-check.sh
```

### Restart de servicios
```bash
docker compose restart <service>
# o restart de todos
docker compose restart
```

### Limpiar todo (incluyendo datos)
```bash
docker compose down -v
```

### Acceso a servicios

#### PostgreSQL
```bash
docker compose exec postgresql psql -U alejandria -d alejandria
```

#### Redis
```bash
docker compose exec redis redis-cli
```

#### Qdrant
```bash
# Info de la instancia
curl http://localhost:6333/

# Health check
curl http://localhost:6333/health
```


## Desarrollo

### Ejecutar componentes individualmente

```bash
# API FastAPI
docker compose --profile dev run --rm dev uv run python run.py api

# Celery Worker
docker compose --profile dev run --rm dev uv run python run.py worker

# Celery Scheduler
docker compose --profile dev run --rm dev uv run python run.py scheduler

# MCP Server (HTTP transport)
docker compose --profile dev run --rm dev uv run python run.py mcp
```

**Nota sobre el MCP Server:** El servidor MCP usa transporte HTTP. Para resolver problemas de compatibilidad entre FastMCP y los tipos de SQLAlchemy Session en pydantic-core, se eliminaron los parámetros `session` de las firmas de las funciones MCP. El transporte HTTP permite:
- Autenticación API KEY nativa via headers
- Mejor integración con IDEs y herramientas MCP
- Arquitectura más apropiada para producción

El servidor MCP se expone en `http://localhost:8000/mcp`.

### Tests

```bash
# Unit tests
docker compose --profile dev run --rm dev uv run pytest tests/unit/

# Integration tests
docker compose --profile dev run --rm dev uv run pytest tests/integration/

# End-to-end tests
docker compose --profile dev run --rm dev uv run pytest tests/e2e/
```

### Migrations de base de datos

```bash
# Crear nueva migration
docker compose --profile dev run --rm dev uv run alembic -c alembic.ini revision --autogenerate -m "descripcion"

# Aplicar migrations
docker compose --profile dev run --rm dev uv run alembic -c alembic.ini upgrade head

# Revertir última migration
docker compose --profile dev run --rm dev uv run alembic -c alembic.ini downgrade -1

# Ver historial
docker compose --profile dev run --rm dev uv run alembic -c alembic.ini history
```

## Troubleshooting

### Docker Desktop no inicia
- Verifica que virtualization esté habilitada en BIOS
- En macOS: `docker context use desktop-linux`
- Reinicia Docker Desktop

### PostgreSQL no acepta conexiones
```bash
# Verificar estado
docker compose ps postgresql

# Ver logs
docker compose logs postgresql

# Verificar puerto no esté en uso
lsof -i :5432
```

### Redis no responde
```bash
# Verificar AOF está habilitado
docker compose exec redis redis-cli CONFIG GET appendonly

# Debe retornar: appendonly yes
```

### Qdrant no responde
```bash
# Verificar puertos no estén en uso
lsof -i :6333
lsof -i :6334
```


### Conflictos de puertos
Si algún puerto está en uso, modifica `docker/docker-compose.yml`:
```yaml
services:
  postgresql:
    ports:
      - "5433:5432"  # Cambiar puerto host
```

## Arquitectura de Servicios

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Network                           │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐    │
│  │  PostgreSQL  │  │    Redis     │  │     Qdrant      │    │
│  │    :5432     │  │    :6379     │  │  :6333/:6334    │    │
│  └──────────────┘  └──────────────┘  └─────────────────┘    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Backend (Python + uv)                   │   │
│  │         FastAPI, Celery, MCP Server                  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```
