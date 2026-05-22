---
id: T-020
type: Task
rating: 10
rating-phase: document-editing
related:
  - target: EPC-002
    relationship_type: implements
    reason: Implementa la épica de API REST y MCP Server con endpoints de users y auth
  - target: T-016
    relationship_type: depends_on
    reason: Depende de los schemas Pydantic implementados en T-016 para validación de users
---

# T-020: Implementar API Endpoints - Users y Auth

**Tipo**: Task
**Prioridad**: Alta
**Estimación**: 5 horas

**Nota sobre metodología de estimación**: Las estimaciones están basadas en experiencia previa del desarrollador. No hay un criterio estandarizado documentado para todas las estimaciones; implementation-strategy.md menciona estimación de esfuerzo considerando dependencias pero no detalla la metodología específica. Para esta tarea específica, la estimación de 5 horas se basa en la experiencia del desarrollador en implementar endpoints de autenticación JWT con FastAPI.
**Dependencias**: EPC-002, T-016

## Descripción

Implementar endpoints básicos para usuarios y autenticación JWT.

## Criterios de Aceptación

- [ ] POST /api/v1/users - Crear usuario
- [ ] GET /api/v1/users - Listar usuarios (todos los usuarios autenticados, sin restricción de admin en MVP)
- [ ] POST /api/v1/auth/login - Obtener token JWT
- [ ] Middleware de autenticación JWT en endpoints protegidos
- [ ] **NO APLICA**: Refresh tokens para renovación (post-MVP). Para MVP bootstrapped, no se implementan refresh tokens. Access tokens expiran en 8 horas y el usuario debe volver a autenticarse. Refresh tokens se implementarán en hitos posteriores post-MVP.
- [ ] **NO APLICA**: Sistema RBAC con roles y permisos (post-MVP). Para MVP bootstrapped, no se implementa sistema RBAC detallado. Todos los usuarios autenticados tienen los mismos permisos. El claim `role` no se incluye en el token JWT. Sistema RBAC completo con roles granulares se implementará en hitos posteriores post-MVP.

## Archivos a Crear

```
app/api/
  ├── users.py
  └── auth.py
app/services/
  └── auth_service.py
app/middleware/
  └── auth.py
```

## Referencias

- [TRD - Hito 2](../propuestas/trd-milestone-2-api-mcp.md): RF-006: API REST Endpoints - Users y Organizations
- [API Specification](../arquitectura/api-specification.md): Endpoints de Users y Auth
