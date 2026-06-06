---
id: T-028
type: Task Implementation
rating: 9.0
rating-phase: document-editing
related:
  - target: EPC-002
    relationship_type: implements
    reason: Implementa endpoints de organizations y projects para la épica API REST y MCP Server Básico
  - target: TRD-021
    relationship_type: implements
    reason: Implementa endpoints de organizations y projects según TRD Hito 2
  - target: PRD-002
    relationship_type: implements
    reason: Implementa requisitos de organizations y projects del PRD Hito 2
---

# T-028: Implementar API Endpoints - Organizations y Projects

**Estado**: ✅ COMPLETADO

**Descripción**: Implementar endpoints CRUD básicos para organizaciones y proyectos según api-specification.md. Estos endpoints permiten gestionar la estructura organizacional del sistema, donde los usuarios pueden crear organizaciones personales y proyectos dentro de ellas.

---

## Referencias

- **[../../arquitectura/api-specification.md](../../arquitectura/api-specification.md)**: Especificación de API REST
- **[../decisiones/adr-006-document-versioning.md](../decisiones/adr-006-document-versioning.md)**: ADR-006
- **[../../producto/requisitos/prd-hito-02-api-mcp.md](../../producto/requisitos/prd-hito-02-api-mcp.md)**: PRD Hito 2

---

## Criterios de Aceptación

- [ ] POST /api/v1/organizations - Crear organización
- [ ] GET /api/v1/organizations - Listar organizaciones del usuario actual
- [ ] GET /api/v1/organizations/{org_id} - Obtener organización por ID
- [ ] POST /api/v1/projects - Crear proyecto
- [ ] GET /api/v1/projects - Listar proyectos del usuario actual
- [ ] GET /api/v1/projects/{project_id} - Obtener proyecto por ID
- [ ] Validación de slug uniqueness implementada (organizations y projects)
- [ ] Relación usuario-organización-proyecto implementada
- [ ] Creación automática de organización personal en registro de usuario
- [ ] Validación de que usuario es creador de organización/proyecto

---

## Implementación

### Pydantic Schemas

Implementar schemas en `shared/schemas/organization.py` y `shared/schemas/project.py`:

**Organization schemas**:
- `OrganizationBase`: name, slug
- `OrganizationCreate`: name, slug, is_personal (default=False)
- `OrganizationResponse`: id, name, slug, is_personal, created_by, created_at, updated_at
- `OrganizationListItem`: id, name, slug, is_personal, created_at

**Project schemas**:
- `ProjectBase`: name, slug, description (opcional)
- `ProjectCreate`: name, slug, description, organization_id
- `ProjectResponse`: id, name, slug, description, organization_id, created_by, created_at, updated_at
- `ProjectListItem`: id, name, slug, description, organization_id, created_at

### API Endpoints

Implementar endpoints en `api/routes/organizations.py` y `api/routes/projects.py`:

**Organizations**:
- `POST /api/v1/organizations`: Crear organización
  - Validar slug uniqueness global
  - Asociar created_by al usuario actual
  - Retornar 201 Created
- `GET /api/v1/organizations`: Listar organizaciones
  - Solo organizaciones donde user es creador
  - Retornar lista de OrganizationListItem
- `GET /api/v1/organizations/{org_id}`: Obtener organización
  - Solo si user es creador
  - Retornar 404 si no existe o no tiene acceso

**Projects**:
- `POST /api/v1/projects`: Crear proyecto
  - Validar que organización existe y user es creador
  - Validar slug uniqueness dentro de organización
  - Asociar created_by al usuario actual
  - Retornar 201 Created
- `GET /api/v1/projects`: Listar proyectos
  - Solo proyectos en organizaciones donde user es creador
  - Retornar lista de ProjectListItem
- `GET /api/v1/projects/{project_id}`: Obtener proyecto
  - Solo si user es creador de la organización del proyecto
  - Retornar 404 si no existe o no tiene acceso

### Integración con Auth

Modificar `api/routes/auth.py` para crear automáticamente una organización personal al registrar usuario:

- En `POST /api/v1/auth/register`, después de crear usuario:
  - Crear Organization con is_personal=True
  - Asociar created_by al nuevo usuario
  - Slug: `personal-{username}`

---

## GAPs

Ninguno identificado.

---

## Dependencias

- T-016: Implementar Pydantic Schemas (requiere schemas base)
- T-020: Implementar API Endpoints - Users y Auth (requiere JWT authentication)

---

## Testing

### Unit Tests

- Test de validación de slug uniqueness para organizations
- Test de validación de slug uniqueness para projects (scope: organization)
- Test de creación de organización personal en registro
- Test de acceso denegado a organizations/projects de otros usuarios

### Integration Tests

- Test de flujo completo: registro → organización personal creada → crear proyecto
- Test de listado de organizations/projects filtrado por usuario
- Test de validación de acceso a organizations/projects

---

## Estimación de Esfuerzo

**Estimación**: 4 horas

Desglose:
- Implementación de schemas: 1h
- Implementación de endpoints organizations: 1h
- Implementación de endpoints projects: 1h
- Integración con auth (organización personal): 0.5h
- Testing: 0.5h

---

## Notas

- Para MVP, no se implementan endpoints de update/delete para organizations/projects
- Solo el creador puede acceder a sus organizations/projects (sin compartir en MVP)
- Slug uniqueness:
  - Organizations: global (único en todo el sistema)
  - Projects: scope por organización (único dentro de la organización)
