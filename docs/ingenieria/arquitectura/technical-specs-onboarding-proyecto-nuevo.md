---
id: TS-007
type: Technical Specification
dependency: [FEAT-ONB-001, FEAT-005, REQ-006]
related:
  - target: ARC-004
    relationship_type: implements
    reason: Implementa el schema de base de datos con especificación de onboarding de proyectos nuevos
---

# Especificación Técnica: Onboarding de Proyecto Nuevo

Especificación técnica detallada para el onboarding de proyectos nuevos en Alejandría.

---

## Índice

1. [Visión General](#1-visión-general)
2. [Conexión de Repositorio](#2-conexión-de-repositorio)
3. [Plantillas de Documentación](#3-plantillas-de-documentación)
4. [Flujo de Onboarding](#4-flujo-de-onboarding)
5. [Requisitos No Funcionales](#5-requisitos-no-funcionales)

---

## 1. Visión General

**Propósito:**

Establecer expectativas claras sobre documentación desde el inicio, evitando acumulación de deuda documental.

**Contexto:**

Proceso guiado para incorporar proyectos que comienzan desde cero a Alejandría.

**Referencias:**

- [FEAT-002](../../producto/funcionalidades/onboarding-proyecto-nuevo.md): Onboarding de Proyecto Nuevo
- [FEAT-005](../../producto/funcionalidades/integracion-git.md): Integración con Git
- [REQ-006](../../producto/requisitos/.archived/requisitos-onboarding-proyecto-nuevo.md): Requisitos archivados

---

## 2. Conexión de Repositorio

### Autenticación con GitHub

**OAuth 2.0 Flow:**

1. Usuario hace click en "Conectar con GitHub"
2. Redirección a GitHub OAuth authorize endpoint
3. Usuario autoriza acceso a repositorios
4. GitHub redirige a callback URL con code
5. Backend intercambia code por access token
6. Token almacenado encriptado en base de datos

**Scopes requeridos:**

- `repo`: Acceso completo a repositorios privados
- `public_repo`: Acceso a repositorios públicos (alternativa)

**Token storage:**

- Encriptación AES-256 en reposo
- Refresh tokens para renovación automática
- Revocación inmediata al desconectar

### Selección de Repositorio

**Lista de repositorios:**

- Fetch de repositorios del usuario desde GitHub API
- Filtros: solo repositorios donde usuario tiene acceso de escritura
- Ordenamiento: por fecha de última actualización (descendente)

**Información mostrada por repositorio:**

- Nombre
- Descripción
- Lenguaje principal
- Última actualización
- Stars (opcional)

**Validación de acceso:**

- Verificar permisos de escritura antes de conectar
- Verificar que repositorio no está conectado a otro proyecto
- Alerta si repositorio es fork (no recomendado para proyectos nuevos)

### Validación de Acceso al Repositorio

**Checks de validación:**

1. **Permisos:**
   - GET `/repos/{owner}/{repo}` para verificar acceso
   - Verificar `permissions.push` = true

2. **Estado del repositorio:**
   - Verificar que no está archivado
   - Verificar que no es fork (opcional, warning)
   - Verificar que tiene al menos 1 commit

3. **Branch principal:**
   - Detectar branch default (main/master)
   - Verificar que branch existe
   - Verificar que no está vacío

**Error handling:**

- Mensajes de error claros al usuario
- Opción de reintentar conexión
- Soporte para múltiples proveedores (GitLab, Bitbucket)

### Soporte para Otros Proveedores de Git

**GitLab:**

- OAuth 2.0 flow similar a GitHub
- Scopes: `read_repository`, `write_repository`
- API endpoints: GitLab REST API v4

**Bitbucket:**

- OAuth 2.0 flow similar a GitHub
- Scopes: `repository:read`, `repository:write`
- API endpoints: Bitbucket API 2.0

**Abstracción de proveedor:**

- Interfaz unificada para operaciones de Git
- Adapters específicos por proveedor
- Configuración de endpoints por proyecto

---

## 3. Plantillas de Documentación

### Definición de Plantillas de Documentación Mínima

**Plantilla obligatoria (mínimo):**

```markdown
# [Nombre del Proyecto]

## Visión General

Breve descripción del proyecto (2-3 párrafos).

## Propósito

¿Qué problema resuelve este proyecto? ¿Para quién está construido?

## Stack Tecnológico

- Lenguaje principal:
- Frameworks:
- Base de datos:
- Otras tecnologías:

## Arquitectura

Descripción de alto nivel de la arquitectura del sistema.

## Getting Started

Instrucciones básicas para configurar y ejecutar el proyecto.

## Contribución

Guía breve para contribuir al proyecto.
```

**Plantilla extendida (recomendada):**

Incluye secciones adicionales:

- Decisiones arquitectónicas (ADR template)
- Guía de desarrollo
- Deployment
- Testing

### Estructura de Documentación de Decisiones Arquitectónicas

**Template de ADR:**

```markdown
# ADR-[NNN]: [Título de la Decisión]

## Estado

[Propuesto/Aceptado/Rechazado/Supersedido por ADR-XXX]

## Contexto

¿Qué problema estamos tratando de resolver?

## Decisión

¿Cuál es la decisión que tomamos?

## Consecuencias

- Positivas: ...
- Negativas: ...
- Riesgos: ...

## Alternativas Consideradas

- Alternativa 1: ...
- Alternativa 2: ...

## Referencias

- Links a discusiones, PRs, issues relacionados
```

**Ubicación:** `/docs/adr/` o `/docs/decisiones/`

### Personalización de Plantillas por Tipo de Proyecto

**Tipos de proyecto:**

1. **Web Application:**

   - Secciones de frontend/backend
   - API documentation
   - Deployment strategy

2. **Library/SDK:**

   - API reference
   - Usage examples
   - Contributing guidelines (detallado)

3. **CLI Tool:**

   - Command reference
   - Installation guide
   - Configuration options

4. **Microservice:**

   - Service endpoints
   - Data models
   - Integration patterns

**Configuración de plantilla:**

- Usuario selecciona tipo de proyecto durante onboarding
- Sistema ajusta plantilla según tipo
- Usuario puede personalizar plantilla manualmente

---

## 4. Flujo de Onboarding

### Pasos del Flujo de Onboarding

### Paso 1: Creación de Proyecto en Alejandría

- Usuario ingresa nombre del proyecto
- Usuario selecciona organización
- Usuario ingresa descripción breve
- Sistema crea proyecto en base de datos

### Paso 2: Conexión de Repositorio Git

- Usuario selecciona proveedor (GitHub, GitLab, Bitbucket)
- Usuario autoriza acceso OAuth
- Usuario selecciona repositorio de la lista
- Sistema valida acceso y permisos

### Paso 3: Selección de Plantilla de Documentación

- Sistema presenta plantillas por tipo de proyecto
- Usuario selecciona plantilla (mínima o extendida)
- Usuario puede personalizar plantilla
- Sistema guarda configuración de plantilla

### Paso 4: Creación de Documento Inicial

- Sistema crea primer documento usando plantilla
- Sistema pre-rellena campos con información del repositorio (nombre, descripción, stack)
- Usuario revisa y edita documento inicial
- Usuario guarda documento

### Paso 5: Configuración Inicial del Proyecto

- Usuario configura preferencias:
  - Frecuencia de análisis (default: cada edición)
  - Umbrales de detección (default: rating < 9)
  - Notificaciones (default: email)
- Sistema guarda configuración

### Paso 6: Inicio de Workflow de 5 Fases

- Sistema marca documento como `healthy: false, rating: 0`
- Sistema encola job de gap_detection
- Workflow normal de 5 fases comienza

### Validación de Completitud de Baseline

**Criterios de completitud:**

1. **Documento inicial creado:**
   - Documento existe en base de datos
   - Documento tiene contenido (no vacío)
   - Documento tiene estructura básica (títulos, secciones)

2. **Repositorio conectado:**
   - Repositorio está conectado
   - Permisos de escritura verificados
   - Branch principal detectado

3. **Configuración inicial:**
   - Preferencias del proyecto configuradas
   - Notificaciones configuradas (opcional)

**Validación:**

- Sistema verifica cada criterio antes de proceder
- Alerta si algún criterio no se cumple
- Usuario puede continuar con criterios faltantes (warning)

### Configuración Inicial del Proyecto

**Preferencias configurables:**

1. **Frecuencia de análisis:**
   - Cada edición (default)
   - Cada hora
   - Cada día
   - Manual (solo cuando usuario solicita)

2. **Umbrales de detección:**
   - Rating mínimo para procesar (default: < 9)
   - Prioridad mínima de gaps a detectar (default: todas)
   - Roles a considerar (default: todos)

3. **Notificaciones:**
   - Email (default)
   - Slack (opcional, requiere integración)
   - In-app (default)
   - Frecuencia: inmediato, diario, semanal

4. **Integraciones:**
   - Git integration (activado por defecto)
   - CI/CD integration (opcional)
   - Communication tools (opcional)

**Almacenamiento:**

- Tabla `project_settings`
- JSON blob para configuración flexible
- Validación de schema antes de guardar

---

## 5. Requisitos No Funcionales

### Usabilidad

**Tiempo máximo para completar onboarding:**

- Paso 1 (creación de proyecto): 1min
- Paso 2 (conexión de repositorio): 2min
- Paso 3 (selección de plantilla): 1min
- Paso 4 (creación de documento): 5min
- Paso 5 (configuración inicial): 2min
- **Total:** < 11min

**Número de pasos del flujo de onboarding:**

- 6 pasos principales
- Cada paso con validación
- Opción de saltar pasos opcionales

**Claridad de instrucciones:**

- Tooltips explicativos en cada campo
- Ejemplos de valores esperados
- Links a documentación de ayuda
- Preview de documento antes de guardar

### Integración

**Tiempo máximo de conexión con GitHub:**

- OAuth flow: 30s
- Fetch de repositorios: 10s
- Validación de acceso: 5s
- **Total:** < 45s

**Manejo de errores de conexión:**

- Reintentos con backoff exponencial (máximo 3 intentos)
- Mensajes de error claros y accionables
- Opción de reintentar manualmente
- Logging detallado para debugging

**Sincronización inicial de repositorio:**

- Clone del repositorio: < 1min (para repositorio típico)
- Extracción de metadata: < 30s
- Creación de documento inicial: < 1min
- **Total:** < 2.5min

---

## Referencias

- [FEAT-002](../../producto/funcionalidades/onboarding-proyecto-nuevo.md): Onboarding de Proyecto Nuevo
- [FEAT-005](../../producto/funcionalidades/integracion-git.md): Integración con Git
- [REQ-006](../../producto/requisitos/.archived/requisitos-onboarding-proyecto-nuevo.md): Requisitos archivados

---

*Documento generado integrando requisitos técnicos archivados con especificación de feature actual.*
