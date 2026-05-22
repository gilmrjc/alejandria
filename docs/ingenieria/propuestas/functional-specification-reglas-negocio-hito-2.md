---
id: FSP-004
type: Functional Specification
rating: 8.5
rating-phase: document-editing
related:
  - target: PRD-002
    relationship_type: implements
    reason: Implementa el PRD de Hito 2 con especificación funcional de reglas de negocio
  - target: TRD-021
    relationship_type: implements
    reason: Implementa el TRD de Hito 2 con API REST para reglas de negocio
  - target: TRD-022
    relationship_type: implements
    reason: Implementa el TRD de Hito 2 con MCP Server para reglas de negocio
  - target: TRD-023
    relationship_type: implements
    reason: Implementa el TRD de Hito 2 con integraciones para reglas de negocio
  - target: ARC-004
    relationship_type: implements
    reason: Implementa el schema de base de datos con modelos de dominio
  - target: FSP-003
    relationship_type: references
    reason: Las reglas de negocio y modelos de dominio soportan los casos de uso
---

# Functional Specification: Hito 2 - Reglas de Negocio y Modelos de Dominio — Alejandria

Este documento define las reglas de negocio y modelos de dominio del Hito 2, sirviendo como base para los casos de uso detallados (FSP-003) y los requisitos técnicos (TRD-021, TRD-022, TRD-023). Para casos de uso detallados, ver [FSP-003](./functional-specification-casos-uso-hito-2.md). Para detalles técnicos de implementación, ver [TRD-021](./trd-milestone-2-api-rest.md), [TRD-022](./trd-milestone-2-mcp-server.md), y [TRD-023](./trd-milestone-2-integrations.md).

---

## Índice

1. [Visión General](#1-visión-general)
2. [Reglas de Negocio](#2-reglas-de-negocio)
3. [Requisitos de Integración](#3-requisitos-de-integración)
4. [Modelos de Dominio](#4-modelos-de-dominio)

---

## 1. Visión General

### Propósito

Esta especificación funcional traduce los requisitos de producto del Hito 2 en reglas de negocio y modelos de dominio, definiendo las restricciones, comportamientos y estructuras de datos que guían el diseño técnico y la implementación. El objetivo es proporcionar una descripción clara de las reglas que el sistema debe seguir y los modelos de datos que debe implementar.

### Alcance

El Hito 2 abarca:

- API REST para gestión de documentos, usuarios y organizaciones
- MCP Server para interacción con agentes LLM
- Integración con Ollama (LLM provider)
- Integración con Qdrant (búsqueda semántica)
- Sistema de autenticación básico

### Actores

- **Usuario Final**: Desarrollador o ingeniero que usa Alejandria para mejorar documentación
- **Agente LLM**: Sistema automatizado que ejecuta el pipeline de 5 fases
- **Administrador**: Usuario con permisos para configurar el sistema (post-MVP)

---

## 2. Reglas de Negocio

### BR-001: Versioning de Documentos

**Descripción**: Todos los cambios a documentos deben ser versionados automáticamente.

**Reglas**:

- Cada UPDATE a un documento debe crear un snapshot del contenido anterior
- Los snapshots deben ser inmutables
- Los snapshots deben incluir timestamp y user_id/job_id del creador
- Los usuarios pueden restaurar versiones anteriores
- La versión actual del documento debe ser siempre accesible

### BR-002: Concurrencia en Documentos

**Descripción**: Los documentos deben usar locking pesimista para evitar conflictos.

**Reglas**:

- Antes de editar un documento, el sistema debe adquirir lock pesimista
- El lock debe ser liberado automáticamente al commit de la transacción
- Si el lock falla, el sistema debe reintentar con backoff exponencial
- El lock debe ser específico por documento (no por tabla completa)

### BR-003: Priorización de Gaps

**Descripción**: Los gaps deben ser priorizados según su impacto en la comprensión del documento.

**Reglas**:

- Los gaps deben tener prioridad: high, medium, low
- Los gaps de prioridad "high" deben impedir comprensión crítica
- Los gaps de prioridad "medium" deben impedir comprensión importante pero no crítica
- Los gaps de prioridad "low" deben ser mejoras opcionales

### BR-004: Agrupación de Gaps

**Descripción**: Los gaps deben agruparse por temas afines para resolución eficiente.

**Reglas**:

- Los grupos deben tener 3-5 gaps cada uno
- Los gaps en un grupo deben estar relacionados temáticamente
- Los tags deben ser reutilizables entre documentos
- Un gap puede tener múltiples tags

### BR-005: Verificación de Respuestas

**Descripción**: Las respuestas a gaps deben ser verificadas antes de aplicar cambios.

**Reglas**:

- Las respuestas deben abordar completamente el gap original
- Las respuestas que revelan nuevos gaps deben retornar a fase de resolución
- Las respuestas valiosas pueden convertirse en preguntas reutilizables
- La verificación debe ser realizada por el Agente 1 (mismo agente que detección)

### BR-006: Aplicación de Cambios

**Descripción**: Los cambios sugeridos deben ser aplicados solo tras aceptación explícita.

**Reglas**:

- Las propuestas deben ser aceptadas explícitamente por el usuario
- Los cambios deben preservar la estructura del documento
- Los cambios deben integrarse suavemente con contenido existente
- El usuario puede rechazar propuestas manualmente

### BR-007: Autenticación JWT

**Descripción**: La autenticación debe usar tokens JWT con expiración fija.

**Reglas**:

- Los tokens JWT deben expirar después de 8 horas
- Los tokens deben incluir user_id en el payload
- Los tokens deben ser validados en cada request a endpoints protegidos
- No se implementan refresh tokens para MVP

---

## 3. Requisitos de Integración

### RI-001: Integración API REST ↔ MCP Server

**Descripción**: La API REST y el MCP Server deben compartir módulos Python.

**Requisitos**:

- FastAPI y FastMCP deben ejecutarse como procesos separados
- Ambos deben compartir módulos Python (services, repositories, schemas)
- Ambos deben compartir PostgreSQL y Redis
- No debe haber comunicación HTTP entre FastAPI y FastMCP
- El shared state debe manejarse vía bases de datos compartidas

### RI-002: Integración MCP Server ↔ Ollama

**Descripción**: El MCP Server debe comunicarse con Ollama para invocar LLM.

**Requisitos**:

- MCP Server debe tener cliente HTTP para API de Ollama
- MCP Server debe configurar modelo Qwen 3.5
- MCP Server debe manejar timeouts y errores de conexión
- MCP Server debe tener función helper para enviar prompts y recibir respuestas

### RI-003: Integración MCP Server ↔ Qdrant

**Descripción**: El MCP Server debe comunicarse con Qdrant para búsqueda semántica.

**Requisitos**:

- MCP Server debe tener cliente HTTP para API de Qdrant
- MCP Server debe crear colecciones, insertar vectores, buscar por similitud
- MCP Server debe integrarse con modelo de embeddings BGE-M3
- Los vectores deben actualizarse cuando documentos cambian

### RI-004: Integración API REST ↔ PostgreSQL

**Descripción**: La API REST debe persistir datos en PostgreSQL.

**Requisitos**:

- API REST debe usar SQLAlchemy para ORM
- API REST debe usar Alembic para migrations
- API REST debe manejar conexiones con connection pooling
- API REST debe usar transacciones para operaciones atómicas

### RI-005: Integración API REST ↔ Redis

**Descripción**: La API REST debe usar Redis para cache y locks.

**Requisitos**:

- API REST debe usar Redis para locks distribuidos (idempotencia)
- API REST debe usar Redis para cache de resultados frecuentes
- API REST debe usar Redis como broker para jobs (Hito 4)

---

## 4. Modelos de Dominio

### MD-001: Document

**Descripción**: Entidad principal que representa un documento de documentación.

**Atributos**:

- id: UUID (primary key)
- title: string
- content: text
- file_path: string
- healthy: boolean
- version: integer
- project_id: UUID (foreign key)
- created_at: datetime
- updated_at: datetime

**Relaciones**:

- belongs_to: Project
- has_many: DocumentSnapshot
- has_many: Gap
- has_many: Proposal

### MD-002: Gap

**Descripción**: Representa información faltante en un documento.

**Atributos**:

- id: UUID (primary key)
- document_id: UUID (foreign key)
- question: string
- context_missing: string
- priority: enum (high, medium, low)
- role_affected: string
- status: enum (pending, responded, verified)
- created_at: datetime
- answered_at: datetime (nullable)

**Relaciones**:

- belongs_to: Document
- has_many: GapTag
- has_many: GapQuestion

### MD-003: Tag

**Descripción**: Etiqueta para clasificar gaps por tema.

**Atributos**:

- id: UUID (primary key)
- name: string
- created_at: datetime

**Relaciones**:

- has_many: GapTag

### MD-004: Proposal

**Descripción**: Propuesta de cambios basada en respuestas verificadas.

**Atributos**:

- id: UUID (primary key)
- document_id: UUID (foreign key)
- description: string
- status: enum (pending, accepted, rejected, applied)
- created_at: datetime
- accepted_at: datetime (nullable)
- applied_at: datetime (nullable)

**Relaciones**:

- belongs_to: Document
- has_many: ContextEntry

### MD-005: User

**Descripción**: Usuario del sistema.

**Atributos**:

- id: UUID (primary key)
- email: string (unique)
- password_hash: string
- created_at: datetime

**Relaciones**:

- has_many: OrganizationMember
- belongs_to: Organization (personal)

### MD-006: Organization

**Descripción**: Organización (personal u organizacional).

**Atributos**:

- id: UUID (primary key)
- name: string
- type: enum (personal, organizational)
- created_at: datetime

**Relaciones**:

- has_many: OrganizationMember
- has_many: Project

### MD-007: Project

**Descripción**: Proyecto dentro de una organización.

**Atributos**:

- id: UUID (primary key)
- name: string
- organization_id: UUID (foreign key)
- created_at: datetime

**Relaciones**:

- belongs_to: Organization
- has_many: Document

---

## Referencias

- **[PRD-002](../producto/requisitos/prd-hito-02-api-mcp.md)**: Product Requirements Document
- **[TRD-021](./trd-milestone-2-api-rest.md)**: Technical Requirements Document - API REST
- **[TRD-022](./trd-milestone-2-mcp-server.md)**: Technical Requirements Document - MCP Server
- **[TRD-023](./trd-milestone-2-integrations.md)**: Technical Requirements Document - Integraciones
- **[ARC-004](../arquitectura/database-schema-design.md)**: Database Schema Design
- **[FSP-003](./functional-specification-casos-uso-hito-2.md)**: Functional Specification - Casos de Uso
