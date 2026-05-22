---
id: FSP-003
type: Functional Specification
rating: 8.5
rating-phase: document-editing
related:
  - target: PRD-002
    relationship_type: implements
    reason: Implementa el PRD de Hito 2 con especificación funcional de casos de uso
  - target: TRD-021
    relationship_type: implements
    reason: Implementa el TRD de Hito 2 con API REST para casos de uso
  - target: TRD-022
    relationship_type: implements
    reason: Implementa el TRD de Hito 2 con MCP Server para casos de uso
  - target: TRD-023
    relationship_type: implements
    reason: Implementa el TRD de Hito 2 con integraciones para casos de uso
  - target: STR-003
    relationship_type: implements
    reason: Implementa el roadmap técnico definiendo casos de uso del Hito 2
  - target: FSP-004
    relationship_type: references
    reason: Los casos de uso dependen de las reglas de negocio y modelos de dominio
---

# Functional Specification: Hito 2 - Casos de Uso — Alejandria

Este documento define los casos de uso detallados del Hito 2, sirviendo como puente entre los requisitos de producto (PRD-002) y los requisitos técnicos (TRD-021, TRD-022, TRD-023). Para reglas de negocio y modelos de dominio, ver [FSP-004](./functional-specification-reglas-negocio-hito-2.md). Para detalles técnicos de implementación, ver [TRD-021](./trd-milestone-2-api-rest.md), [TRD-022](./trd-milestone-2-mcp-server.md), y [TRD-023](./trd-milestone-2-integrations.md).

---

## Índice

1. [Visión General](#1-visión-general)
2. [Casos de Uso](#2-casos-de-uso)

---

## 1. Visión General

### Propósito

Esta especificación funcional traduce los requisitos de producto del Hito 2 en casos de uso detallados, describiendo las interacciones entre usuarios, agentes LLM y el sistema. El objetivo es proporcionar una descripción clara del comportamiento esperado del sistema que sirva como base para el diseño técnico y la implementación.

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

## 2. Casos de Uso

### UC-001: Gestión de Documentos

#### UC-001.1: Crear Documento

**Descripción**: Un usuario crea un nuevo documento en el sistema.

**Actores**: Usuario Final

**Precondiciones**:

- Usuario está autenticado
- Usuario tiene permisos para crear documentos en el proyecto

**Flujo Principal**:

1. Usuario invoca endpoint POST /api/v1/documents
2. Sistema valida datos de entrada (título, contenido, proyecto_id)
3. Sistema crea documento con estado "healthy": false
4. Sistema genera UUID único para el documento
5. Sistema registra timestamp de creación
6. Sistema retorna documento creado con ID

**Postcondiciones**:

- Documento existe en base de datos
- Documento tiene versión 1
- Documento está asociado al proyecto del usuario

**Flujos Alternativos**:

- **UC-001.1-A**: Datos inválidos → Sistema retorna error 400 con detalles de validación
- **UC-001.1-B**: Proyecto no existe → Sistema retorna error 404

#### UC-001.2: Leer Documento

**Descripción**: Un usuario o agente LLM lee el contenido de un documento existente.

**Actores**: Usuario Final, Agente LLM

**Precondiciones**:

- Documento existe
- Usuario tiene permisos para leer el documento

**Flujo Principal**:

1. Usuario invoca endpoint GET /api/v1/documents/{document_id} o tool MCP read_document
2. Sistema verifica que documento existe
3. Sistema verifica permisos del usuario
4. Sistema retorna contenido completo del documento con metadatos

**Postcondiciones**:

- Contenido del documento es accesible
- Metadatos (versión, timestamps, estado) son visibles

**Flujos Alternativos**:

- **UC-001.2-A**: Documento no existe → Sistema retorna error 404
- **UC-001.2-B**: Permisos insuficientes → Sistema retorna error 403

#### UC-001.3: Actualizar Documento

**Descripción**: Un usuario o agente LLM actualiza el contenido de un documento existente.

**Actores**: Usuario Final, Agente LLM

**Precondiciones**:

- Documento existe
- Usuario tiene permisos para editar el documento
- Documento no está bloqueado por otro usuario

**Flujo Principal**:

1. Usuario invoca endpoint PUT /api/v1/documents/{document_id} o tool MCP write_document
2. Sistema verifica que documento existe
3. Sistema verifica permisos del usuario
4. Sistema adquiere lock pesimista en documento
5. Sistema crea snapshot del contenido anterior (versioning automático)
6. Sistema actualiza contenido
7. Sistema incrementa versión del documento
8. Sistema actualiza timestamp de modificación
9. Sistema libera lock
10. Sistema retorna documento actualizado

**Postcondiciones**:

- Contenido del documento es actualizado
- Versión del documento es incrementada
- Snapshot del contenido anterior es preservado

**Flujos Alternativos**:

- **UC-001.3-A**: Documento no existe → Sistema retorna error 404
- **UC-001.3-B**: Permisos insuficientes → Sistema retorna error 403
- **UC-001.3-C**: Documento bloqueado → Sistema retorna error 409 con retry after

#### UC-001.4: Listar Documentos

**Descripción**: Un usuario lista todos los documentos de un proyecto con filtros opcionales.

**Actores**: Usuario Final

**Precondiciones**:

- Usuario está autenticado
- Usuario tiene permisos para listar documentos del proyecto

**Flujo Principal**:

1. Usuario invoca endpoint GET /api/v1/documents con query params (project_id, status, limit, offset)
2. Sistema aplica filtros según parámetros
3. Sistema aplica paginación
4. Sistema retorna lista de documentos con metadatos

**Postcondiciones**:

- Lista de documentos es retornada
- Metadatos de paginación (total, limit, offset) son incluidos

---

### UC-002: Pipeline de 5 Fases

#### UC-002.1: Detección de Gaps

**Descripción**: El Agente 1 analiza un documento y detecta información faltante (gaps).

**Actores**: Agente LLM (Agente 1)

**Precondiciones**:

- Documento existe
- MCP Server está disponible
- LLM provider (Ollama) está disponible

**Flujo Principal**:

1. Agente invoca tool MCP read_document
2. Agente analiza contenido desde múltiples perspectivas (senior/junior, técnica/negocio)
3. Agente invoca tool MCP create_gap para cada gap detectado
4. Sistema registra gaps con estado "pending"
5. Sistema asocia gaps al documento

**Postcondiciones**:

- Gaps son registrados en base de datos
- Gaps tienen estado "pending"
- Gaps están asociados al documento

**Reglas de Negocio**:

- Los gaps deben priorizarse (high, medium, low)
- Los gaps deben indicar el rol afectado (Senior Developer, Junior Developer, etc.)
- Los gaps deben describir el contexto faltante

#### UC-002.2: Agrupación de Gaps

**Descripción**: El Agente 2 agrupa gaps por temas afines para facilitar resolución eficiente.

**Actores**: Agente LLM (Agente 2)

**Precondiciones**:

- Gaps existen con estado "pending"
- MCP Server está disponible

**Flujo Principal**:

1. Agente invoca tool MCP list_gaps
2. Agente analiza gaps para identificar temas comunes
3. Agente invoca tool MCP create_tag para cada tema identificado
4. Agente invoca tool MCP assign_tag_to_gap para clasificar gaps
5. Sistema crea 3-5 grupos basados en temas similares

**Postcondiciones**:

- Tags son creados para temas identificados
- Gaps están clasificados por tags
- Grupos de gaps están definidos para resolución

**Reglas de Negocio**:

- Los grupos deben tener 3-5 gaps cada uno
- Los gaps en un grupo deben estar relacionados temáticamente
- Los tags deben ser reutilizables entre documentos

#### UC-002.3: Resolución de Gaps

**Descripción**: El Agente 3 facilita sesiones interactivas donde el usuario responde gaps.

**Actores**: Usuario Final, Agente LLM (Agente 3)

**Precondiciones**:

- Gaps están agrupados por temas
- Usuario está autenticado

**Flujo Principal**:

1. Usuario inicia sesión de resolución para un grupo específico
2. Agente presenta primer gap del grupo en términos simples
3. Usuario proporciona respuesta
4. Agente valida respuesta y sugiere mejoras si es necesario
5. Agente invoca tool MCP answer_gap
6. Sistema actualiza estado del gap a "responded"
7. Proceso se repite para cada gap del grupo
8. Cuando todos los gaps del grupo son respondidos, se inicia verificación

**Postcondiciones**:

- Gaps tienen estado "responded"
- Respuestas están registradas en base de datos
- Verificación es iniciada automáticamente

**Reglas de Negocio**:

- Las respuestas deben ser validadas antes de aceptarlas
- Las respuestas deben ser claras y completas
- Las respuestas valiosas pueden convertirse en preguntas reutilizables

#### UC-002.4: Verificación de Respuestas

**Descripción**: El Agente 1 verifica que las respuestas son completas y precisas.

**Actores**: Agente LLM (Agente 1 - rol de verificación)

**Precondiciones**:

- Todos los gaps de un grupo tienen estado "responded"
- MCP Server está disponible

**Flujo Principal**:

1. Agente invoca tool MCP list_gaps con status "responded"
2. Agente evalúa si cada respuesta aborda completamente el gap original
3. Agente detecta si las respuestas revelan nuevos gaps
4. Si hay nuevos gaps, Agente los crea y retorna a fase de resolución
5. Si respuestas son completas, Agente actualiza estado a "verified"
6. Sistema inicia generación de propuestas

**Postcondiciones**:

- Gaps tienen estado "verified" o retornan a "pending" (si se detectaron nuevos gaps)
- Nuevos gaps son creados si es necesario
- Generación de propuestas es iniciada

**Reglas de Negocio**:

- La verificación debe ser realizada por el Agente 1 (mismo agente que detección)
- Las respuestas que revelan nuevos gaps deben retornar a fase de resolución
- Las respuestas valiosas pueden convertirse en preguntas reutilizables

#### UC-002.5: Aplicación de Cambios

**Descripción**: El Agente 4 genera propuestas de cambios basadas en respuestas verificadas.

**Actores**: Usuario Final, Agente LLM (Agente 4)

**Precondiciones**:

- Gaps tienen estado "verified"
- Usuario está autenticado

**Flujo Principal**:

1. Agente invoca tool MCP list_gaps con status "verified"
2. Agente analiza respuestas verificadas
3. Agente genera propuesta de cambios integrando respuestas al contenido
4. Agente invoca tool MCP create_proposal
5. Sistema crea propuesta con estado "pending"
6. Usuario revisa propuesta
7. Usuario acepta o rechaza propuesta
8. Si aceptada, Agente invoca tool MCP apply_proposal
9. Sistema actualiza documento con cambios
10. Sistema actualiza estado de propuesta a "applied"
11. Sistema actualiza estado de documento a "healthy": true

**Postcondiciones**:

- Propuesta es creada y aceptada/rechazada
- Documento es actualizado si propuesta fue aceptada
- Estado de documento refleja integridad mejorada

**Reglas de Negocio**:

- Las propuestas deben ser aceptadas explícitamente por el usuario
- Los cambios deben preservar la estructura del documento
- Los cambios deben integrarse suavemente con contenido existente
- El usuario puede rechazar propuestas manualmente

---

### UC-003: Autenticación y Autorización

#### UC-003.1: Login de Usuario

**Descripción**: Un usuario se autentica en el sistema usando email y password.

**Actores**: Usuario Final

**Precondiciones**:

- Usuario tiene cuenta registrada
- Usuario conoce email y password

**Flujo Principal**:

1. Usuario invoca endpoint POST /api/v1/auth/login
2. Sistema valida email y password
3. Sistema genera token JWT con user_id en payload
4. Sistema retorna token JWT con expiración de 8 horas
5. Usuario almacena token para requests futuros

**Postcondiciones**:

- Usuario está autenticado
- Token JWT es válido por 8 horas
- Usuario puede acceder a endpoints protegidos

**Flujos Alternativos**:

- **UC-003.1-A**: Credenciales inválidas → Sistema retorna error 401
- **UC-003.1-B**: Usuario no existe → Sistema retorna error 404

#### UC-003.2: Acceso a Endpoint Protegido

**Descripción**: Un usuario accede a un endpoint protegido usando token JWT.

**Actores**: Usuario Final

**Precondiciones**:

- Usuario está autenticado
- Token JWT es válido
- Token no ha expirado

**Flujo Principal**:

1. Usuario invoca endpoint protegido con header Authorization: Bearer {token}
2. Sistema valida token JWT
3. Sistema extrae user_id del payload
4. Sistema verifica permisos del usuario
5. Sistema retorna respuesta del endpoint

**Postcondiciones**:

- Usuario accede al recurso protegido
- Request es procesado exitosamente

**Flujos Alternativos**:

- **UC-003.2-A**: Token inválido → Sistema retorna error 401
- **UC-003.2-B**: Token expirado → Sistema retorna error 401
- **UC-003.2-C**: Permisos insuficientes → Sistema retorna error 403

---

## Referencias

- **[PRD-002](../producto/requisitos/prd-hito-02-api-mcp.md)**: Product Requirements Document
- **[TRD-021](./trd-milestone-2-api-rest.md)**: Technical Requirements Document - API REST
- **[TRD-022](./trd-milestone-2-mcp-server.md)**: Technical Requirements Document - MCP Server
- **[TRD-023](./trd-milestone-2-integrations.md)**: Technical Requirements Document - Integraciones
- **[STR-003](../estrategia/estrategia/technical-roadmap.md)**: Technical Roadmap
- **[FSP-004](./functional-specification-reglas-negocio-hito-2.md)**: Functional Specification - Reglas de Negocio y Modelos de Dominio
