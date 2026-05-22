---
id: TS-003
type: Technical Specification
related-features: [FEAT-005]
related-adrs: []
dependency: [FEAT-005, REQ-008, ENG-ARC-010]
related:
  - target: FEAT-005
    relationship_type: implements
    reason: Implementa la especificación técnica detallada del feature de integración Git
  - target: REQ-008
    relationship_type: implements
    reason: Implementa los requisitos de integración Git
  - target: ARC-010
    relationship_type: implements
    reason: Implementa la especificación de integración Git con detalles técnicos
---

# Especificación Técnica: Integración con Git

Especificación técnica detallada para la integración de Alejandría con repositorios Git.

---

## Índice

1. [Visión General](#1-visión-general)
2. [Lectura de Repositorios](#2-lectura-de-repositorios)
3. [Escritura de Archivos](#3-escritura-de-archivos)
4. [Análisis de Código](#4-análisis-de-código)
5. [Requisitos No Funcionales](#5-requisitos-no-funcionales)

---

## 1. Visión General

**Propósito:**

Conectar Alejandría con repositorios de código para onboarding, arqueología de código y aplicación automática de cambios.

**Contexto:**

Sistema para leer y escribir archivos en repositorios Git, permitiendo conexión de proyectos y aplicación de cambios.

**Referencias:**

- [FEAT-005](../../producto/funcionalidades/integracion-git.md): Integración con Git
- [REQ-008](../../producto/requisitos/.archived/requisitos-integracion-git.md): Requisitos archivados
- [git-integration-specification.md](git-integration-specification.md): Especificación existente

---

## 2. Lectura de Repositorios

### Autenticación con Proveedores de Git

**Proveedores soportados:**

- GitHub (OAuth 2.0 + Personal Access Token)
- GitLab (OAuth 2.0 + Personal Access Token)
- Bitbucket (OAuth 2.0 + App Password)

**Mecanismos de autenticación:**

1. **OAuth 2.0 (recomendado para usuarios):**
   - Flow: Authorization Code Grant
   - Scopes mínimos: `repo` (GitHub), `read_repository` (GitLab), `repository:read` (Bitbucket)
   - Refresh tokens para renovación automática
   - Token storage encriptado en base de datos

2. **Personal Access Token (alternativa):**
   - Almacenamiento encriptado
   - Expiración configurable
   - Rotación automática antes de expiración

**Almacenamiento seguro de credenciales:**

- Encriptación AES-256 en reposo
- Tokens en memoria solo durante request activo
- Logs no contienen tokens
- Revocación inmediata al desconectar repositorio

### Selección de Branch

**Branch por defecto:** `main` o `master` (detectado automáticamente)

**Selección manual:**

- Usuario puede seleccionar branch específico durante onboarding
- Cambio de branch posterior requiere re-configuración
- Soporte para múltiples branches por proyecto (feature futuro)

**Validación:**

- Verificar que branch existe antes de conectar
- Verificar que usuario tiene permisos de lectura en branch
- Alerta si branch está desactualizado vs default branch

### Límite de Commits Históricos

**Política por defecto:** Últimos 1000 commits

**Configuración por proyecto:**

- Mínimo: 100 commits
- Máximo: 10,000 commits
- Default: 1000 commits

**Justificación:**

- 1000 commits es suficiente para arqueología de código típica
- Más de 10,000 commits puede causar performance issues
- Usuario puede ajustar según necesidades específicas

**Estrategia de recuperación:**

- Fetch incremental (solo commits nuevos desde última sincronización)
- Paginación para repositorios con muchos commits
- Caching de commits en base de datos local

### Manejo de Repositorios Privados vs Públicos

**Repositorios públicos:**

- Autenticación opcional (rate limits más altos con autenticación)
- Solo lectura por defecto
- Escritura requiere autenticación explícita

**Repositorios privados:**

- Autenticación obligatoria
- Verificación de permisos antes de conectar
- Solo repositorios donde usuario tiene acceso son visibles

### Manejo de Errores de Conexión

**Tipos de errores:**

- Autenticación fallida (401, 403)
- Repositorio no encontrado (404)
- Rate limit exceeded (429)
- Network timeout
- Repository locked

**Estrategia de manejo:**

- Reintentos con backoff exponencial (máximo 3 intentos)
- Mensajes de error claros al usuario
- Logging detallado para debugging
- Alerta al usuario si error persiste

---

## 3. Escritura de Archivos

### Creación de Commits Automáticos

**Estrategia de branch:**

- Branch dedicado: `alejandria-changes`
- Creación automática de branch si no existe
- Pull request automático al branch principal

**Formato de commit message:**

```text
feat: apply Alejandría documentation improvements

- Updated ADR-002 with new context
- Added decision rationale for feature X
- Fixed typos in API specification

Related gaps: gap-123, gap-456
Related proposal: proposal-789
```

**Validación antes de commit:**

- Verificar que cambios no rompen sintaxis (ej: Markdown válido)
- Verificar que no hay conflictos con branch principal
- Verificar que tamaño de cambios es razonable (< 1MB)

### Integración con Pull Requests

**Creación automática de PR:**

- Título: "Alejandría: Documentation improvements"
- Descripción: Resumen de cambios aplicados
- Labels: `documentation`, `automated`
- Reviewers: Configurables por proyecto

**Estado de PR:**

- Draft por defecto (requiere aprobación manual)
- Opción de merge automático (configurable por proyecto)
- Notificación a equipo cuando PR está listo

### Validación de Cambios Antes de Aplicar

**Validaciones técnicas:**

- Sintaxis de Markdown válida
- No hay caracteres corruptos
- Encoding UTF-8 válido
- Tamaño de archivo razonable (< 5MB)

**Validaciones de contenido:**

- No hay cambios en código fuente (solo documentación)
- No hay cambios en archivos binarios
- No hay cambios en archivos de configuración sensible

**Validaciones de permisos:**

- Usuario tiene permisos de escritura en repositorio
- Branch no está protegido contra cambios directos
- No hay bloqueos de administración en repositorio

### Rollback de Cambios Aplicados

**Estrategia de rollback:**

1. Identificar commit que aplicó cambios
2. Crear commit de reversión (revert)
3. Push al branch `alejandria-changes`
4. Actualizar PR o cerrar PR según configuración

**Alternativa:**

- Cerrar PR sin merge
- Eliminar branch `alejandria-changes`
- Documentar rollback en sistema Alejandría

---

## 4. Análisis de Código

### Integración con Tree-sitter

**Propósito:** Análisis sintáctico de código para extraer estructura

**Lenguajes soportados (MVP):**

- Python
- JavaScript/TypeScript
- Go
- Rust

**Lenguajes futuros:**

- Java
- C#
- Ruby
- PHP

**Uso de Tree-sitter:**

- Parsear código fuente a AST
- Extraer estructura de funciones, clases, módulos
- Identificar dependencias entre archivos
- Extraer comentarios y docstrings

### Análisis AST para Extraer Estructura de Código

**Información extraída:**

- Nombres de funciones y clases
- Parámetros de funciones
- Tipos de retorno
- Imports y dependencias
- Comentarios y docstrings
- Decoradores y anotaciones

**Almacenamiento:**

- AST simplificado en base de datos
- Relaciones entre archivos (imports)
- Metadata de complejidad (líneas de código, cyclomatic complexity)

### Generación de Grafo Código-Documentos

**Nodos del grafo:**

- Archivos de código
- Documentos Alejandría
- Funciones/clases (nodos secundarios)

**Edges del grafo:**

- Código → Documento (referencia)
- Documento → Código (documenta)
- Código → Código (dependencia)
- Documento → Documento (referencia)

**Algoritmo de construcción:**

1. Parsear código con Tree-sitter
2. Extraer referencias a documentación (comentarios, docstrings)
3. Mapear archivos de código a documentos Alejandría
4. Construir grafo con NetworkX o librería similar
5. Persistir grafo en base de datos (Neo4j o PostgreSQL + graph extension)

### Actualización del Grafo con Cambios en Código

**Trigger de actualización:**

- Push al repositorio conectado
- Webhook desde GitHub/GitLab
- Sincronización periódica (cada hora)

**Estrategia de actualización:**

- Actualización incremental (solo archivos cambiados)
- Recálculo de edges afectados
- Invalidación de caché para consultas afectadas

**Performance:**

- Tiempo máximo de actualización: 30s para cambios < 100 archivos
- Tiempo máximo de actualización: 5min para cambios < 1000 archivos
- Para cambios mayores: job en background

### Soporte para Múltiples Lenguajes de Programación

**Abstracción de lenguaje:**

- Interfaz unificada para análisis de código
- Adapters específicos por lenguaje
- Configuración de parsers por proyecto

**Mapeo de conceptos:**

- Funciones (Python) ≈ Methods (Java) ≈ Functions (JavaScript)
- Clases (Python) ≈ Classes (Java) ≈ Classes (TypeScript)
- Modules (Python) ≈ Packages (Java) ≈ Modules (JavaScript)

---

## 5. Requisitos No Funcionales

### Seguridad

**Almacenamiento seguro de credenciales:**

- Encriptación AES-256 en reposo
- Tokens en memoria solo durante request activo
- Rotación automática de tokens
- Revocación inmediata al desconectar

**Autenticación OAuth:**

- PKCE (Proof Key for Code Exchange) para apps móviles
- State parameter para prevenir CSRF
- Token validation en cada request
- Refresh tokens con rotación

**Permisos mínimos requeridos (scope):**

- GitHub: `repo` (o `public_repo` para repos públicos)
- GitLab: `read_repository` + `write_repository` (si aplica)
- Bitbucket: `repository:read` + `repository:write` (si aplica)

**Validación de acceso:**

- Verificar permisos antes de conectar repositorio
- Verificar permisos antes de cada operación de escritura
- Alerta si permisos revocados

### Performance

**Tiempo máximo para clonar repositorio:**

- Repositorios < 100MB: 30s
- Repositorios 100MB - 1GB: 2min
- Repositorios > 1GB: 10min (clone shallow)

**Tiempo máximo para leer commits históricos:**

- 100 commits: 5s
- 1000 commits: 30s
- 10000 commits: 5min

**Tiempo máximo para aplicar cambios:**

- Cambios < 10 archivos: 10s
- Cambios 10-100 archivos: 1min
- Cambios > 100 archivos: 5min

**Tiempo máximo para generar grafo de relaciones:**

- Proyectos < 100 archivos: 30s
- Proyectos 100-1000 archivos: 2min
- Proyectos > 1000 archivos: 10min

### Escalabilidad

**Capacidad máxima de tamaño de repositorio:**

- Límite duro: 5GB
- Límite blando: 1GB (alerta si excede)
- Para repositorios > 1GB: clone shallow (últimos 100 commits)

**Estrategia para repositorios muy grandes:**

- Clone shallow por defecto
- Paginación de commits
- Caching agresivo de resultados
- Job en background para análisis pesado

**Límite de archivos por repositorio:**

- Límite duro: 50,000 archivos
- Límite blando: 10,000 archivos (alerta si excede)
- Para repositorios > 10,000 archivos: análisis selectivo (solo archivos principales)

### Compatibilidad

**Soporte para sistemas de Git self-hosted:**

- GitHub Enterprise Server
- GitLab Self-Managed
- Bitbucket Server/Data Center

**Requisitos:**

- API compatible con versión cloud
- Configuración de endpoint base
- Certificados SSL válidos o whitelisting

**Versiones de API soportadas:**

- GitHub REST API v3 (mínimo)
- GitLab API v4 (mínimo)
- Bitbucket API 2.0 (mínimo)

---

## Referencias

- [FEAT-005](../../producto/funcionalidades/integracion-git.md): Integración con Git
- [REQ-008](../../producto/requisitos/.archived/requisitos-integracion-git.md): Requisitos archivados
- [git-integration-specification.md](git-integration-specification.md): Especificación existente

---

*Documento generado integrando requisitos técnicos archivados con especificación de feature actual.*
