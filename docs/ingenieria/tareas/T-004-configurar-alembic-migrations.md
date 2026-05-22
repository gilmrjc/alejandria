---
id: T-004
type: Task
rating: 9.0
rating-phase: document-editing
related:
  - target: T-001
    relationship_type: depends_on
    reason: Depende de la estructura base creada en T-001 para configurar Alembic
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del diseño de schema de base de datos para configurar migrations
---

# T-004: Configurar Alembic para migrations

**Tipo**: Task
**Prioridad**: Alta
**Estimación**: 2 horas
**Dependencias**: T-001

## Descripción

Configurar Alembic 1.17.0 para migrations de base de datos con estructura inicial según ADR-002 y technology-stack.md. La configuración específica de Alembic sigue ADR-002 (Alembic 1.17.0 para migrations con PostgreSQL). SQLAlchemy models se usan para type safety y consistencia con stack Python unificado.

## Criterios de Éxito

- Alembic 1.17.0 instalado en environment virtual
- `alembic init` ejecutado
- `alembic.ini` configurado con connection string de PostgreSQL
- `env.py` configurado para usar SQLAlchemy models
- Script `script.py.mako` personalizado con template de migrations
- Comando `alembic current` funciona correctamente
- Comando `alembic revision --autogenerate -m "initial"` crea migration

### Comandos de Migrations

**Aplicar migrations:**

```bash
# Aplicar todas las migrations pendientes
alembic upgrade head

# Aplicar hasta una migration específica
alembic upgrade +1
```

**Rollback de migrations:**

```bash
# Revertir la última migration
alembic downgrade -1

# Revertir todas las migrations (volver a estado inicial)
alembic downgrade base
```

**Nota:** Manejo de migrations en producción con proceso de aprobación y ejecución controlada está fuera de scope de T-004. Se considerará en tareas futuras de deployment.

### Validación de Migrations

**Ver SQL sin ejecutar (dry-run):**

```bash
# Ver el SQL que se generaría sin ejecutarlo
alembic upgrade head --sql
```

**Validar migration específica:**

```bash
# Ver SQL de una migration específica
alembic upgrade <revision_id> --sql
```

**Nota:** Validación en ambiente de staging antes de producción está fuera de scope de T-004. Se considerará en tareas futuras de deployment.

## Configuración de alembic.ini

```ini
[alembic]
script_location = alembic
file_template = %%(year)d%%(month).2d%%(day).2d_%%(rev)s_%%(slug)s
sqlalchemy.url = postgresql://alejandria:changeme@localhost:5432/alejandria

[post_write_hooks]

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

## Referencias

- [TRD - Hito 1](../propuestas/trd-milestone-1-infrastructure.md): RF-002: PostgreSQL Setup
- [ADR-002](../decisiones/adr-002-python-unified-stack.md): Stack unificado en Python (Alembic 1.17.0)
- [database-schema-design.md](../arquitectura/database-schema-design.md): Diseño conceptual de schema de PostgreSQL

---

## Troubleshooting

### Resolución de Conflictos de Migrations

Se usa proceso de resolución manual con `alembic merge` cuando surjan conflictos.

**Proceso de resolución de conflictos:**

1. **Identificar migrations en conflicto:**

```bash
# Ver historial de migrations
alembic history
```

1. **Crear migration de merge:**

```bash
# Combinar dos migrations en conflicto
alembic merge <revision_id_1> <revision_id_2> -m "Merge conflict resolution"
```

1. **Editar la migration de merge:**

- Abrir el archivo de migration generado
- Revisar y corregir el SQL generado
- Asegurar que los cambios sean compatibles

1. **Aplicar la migration de merge:**

```bash
alembic upgrade head
```

**Nota:** Para esta fase inicial del proyecto con un solo desarrollador, los conflictos de migrations no son un problema actual. Este proceso se usará cuando el equipo crezca.

**Justificación:** `alembic merge` es la herramienta estándar para resolver conflictos de migrations. Es suficiente cuando surja el problema en el futuro.
