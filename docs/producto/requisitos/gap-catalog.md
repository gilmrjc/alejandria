---
id: REQ-003
type: Requirements
rating:
rating-phase:
related:
  - target: FEA-001
    relationship_type: implements
    reason: Implementa el workflow de 5 fases con catálogo de gaps
  - target: STR-001
    relationship_type: implements
    reason: Implementa la visión y misión definiendo gaps de contexto
---

# Catálogo de Gaps de Contexto — Alejandria

Este documento define el catálogo de gaps de contexto que el sistema Alejandria detecta y resuelve, basado en la documentación existente.

---

## Índice

1. [Visión General](#1-visión-general)
2. [Definición de Gap de Contexto](#2-definición-de-gap-de-contexto)
3. [Tipos de Gaps](#3-tipos-de-gaps)
4. [Criterios de Identificación](#4-criterios-de-identificación)
5. [Ejemplos por Tipo de Documento](#5-ejemplos-por-tipo-de-documento)
6. [Metadata de Gaps](#6-metadata-de-gaps)

---

## 1. Visión General

**Propósito:**

Definir el catálogo de gaps de contexto que el sistema detecta sistemáticamente en documentación técnica, proporcionando ejemplos específicos y criterios de identificación.

**Valor:**

El catálogo de gaps permite al sistema identificar patrones de información faltante de forma consistente, asegurando que la detección sea reproducible y completa.

**Referencias:**

- [STR-001](../../estrategia/estrategia/vision-mission.md): Vision and Mission Statement
- [FEA-001](../funcionalidades/5-phase-workflow.md): Flujo de Trabajo de 5 Fases
- [ARC-001](../../ingenieria/arquitectura/technical-brief.md): Technical Brief

---

## 2. Definición de Gap de Contexto

**Definición:**

Un gap de contexto es información faltante o ambigua en un documento que impide una comprensión completa, toma de decisiones informada, o implementación correcta.

**Características:**

- No es simplemente información ausente, sino omisiones que bloquean comprensión profunda
- Es relativo al contexto y audiencia esperada del documento
- Puede manifestarse en patrones identificables que el sistema detecta sistemáticamente

**Referencia:** Definición de "gaps de contexto" en technical-brief.md (proceso de resolución de gaps)

---

## 3. Tipos de Gaps

### Gap de Definición

**Descripción:**

Términos técnicos, acrónimos o conceptos utilizados sin explicación o definición.

**Ejemplos:**

- Uso de acrónimos sin expandir (ej. "API" sin definir qué significa)
- Términos de dominio específicos sin contexto (ej. "event sourcing" sin explicar el patrón)
- Jerga técnica sin aclaración para audiencia junior

**Rol Afectado:**

- Desarrollador Junior
- Nuevo miembro del equipo
- Stakeholders no técnicos

**Severidad:**

- Media a Alta (dependiendo de la frecuencia del término)

**Referencias:**

- Mencionado en vision-mission.md como "terminología sin definir"

### Gap de Justificación

**Descripción:**

Decisiones técnicas, arquitectónicas o de proceso implementadas sin explicar el razonamiento o análisis de compromisos.

**Ejemplos:**

- "Usamos PostgreSQL" sin justificar por qué vs MySQL, MongoDB, etc.
- "El sistema es escalable" sin definir qué significa escalable en este contexto
- "Implementar caching" sin especificar estrategia (Redis, CDN, etc.)
- Decisión de framework sin análisis de trade-offs

**Rol Afectado:**

- Arquitecto Senior
- Desarrollador Senior
- CTO/VP Engineering

**Severidad:**

- Alta (bloquea evolución informada del sistema)

**Referencias:**

- Mencionado en vision-mission.md como "decisiones arquitectónicas sin justificar"
- Ejemplos en technical-brief.md (proceso de resolución de gaps)

### Gap de Implementación

**Descripción:**

Conceptos o arquitecturas descritos a alto nivel sin detalle técnico suficiente para implementación.

**Ejemplos:**

- "El sistema usa microservicios" sin definir límites de servicio, comunicación, orquestación
- "Implementamos autenticación" sin especificar OAuth, JWT, sesión, etc.
- "Base de datos distribuida" sin explicar estrategia de sharding, consistencia, etc.

**Rol Afectado:**

- Desarrollador Senior
- Desarrollador Junior
- DevOps/SRE

**Severidad:**

- Alta (bloquea implementación correcta)

**Referencias:**

- Mencionado en technical-brief.md como "gaps de implementación"

### Gap de Dependencia

**Descripción:**

Referencias a sistemas, APIs, componentes o recursos externos sin explicar la relación o cómo integrar.

**Ejemplos:**

- "Integración con Stripe" sin explicar qué endpoints, webhooks, etc.
- "Usamos Redis" sin explicar propósito (cache, queue, session store)
- Referencia a servicio interno sin documentar API o contrato

**Rol Afectado:**

- Desarrollador Senior
- Desarrollador Junior
- DevOps/SRE

**Severidad:**

- Media a Alta (dependiendo de criticidad de la dependencia)

**Referencias:**

- Mencionado en vision-mission.md como "dependencias no documentadas"
- Mencionado en technical-brief.md como "gaps de dependencia"

### Gap de Historia de Cambios

**Descripción:**

Modificaciones al código, arquitectura o configuración sin explicar el por qué del cambio.

**Ejemplos:**

- Commit message "fix bug" sin explicar qué bug y por qué la solución
- Cambio de configuración sin contexto de problema que resuelve
- Refactorización sin explicar motivación (performance, mantenibilidad, etc.)

**Rol Afectado:**

- Desarrollador Senior
- Arquitecto Senior
- CTO/VP Engineering

**Severidad:**

- Media (bloquea aprendizaje de evolución del sistema)

**Referencias:**

- Mencionado en vision-mission.md como "historia de cambios faltante"
- Mencionado en technical-brief.md como "gaps de historia"

### Gap de Contexto de Negocio

**Descripción:**

Funcionalidades o decisiones técnicas no conectadas con objetivos de negocio o métricas de éxito.

**Ejemplos:**

- Implementación de feature compleja sin explicar valor de negocio
- Decisión de escalado sin conectar con crecimiento esperado
- Cambio de arquitectura sin justificar ROI o costo

**Rol Afectado:**

- CTO/VP Engineering
- Product Manager
- Stakeholders de negocio

**Severidad:**

- Media (bloquea alineación técnica-negocio)

**Referencias:**

- Mencionado en vision-mission.md como "contexto de negocio ausente"

### Gap de Consistencia

**Descripción:**

Contradicciones internas o inconsistencias en el documento.

**Ejemplos:**

- Dos secciones que describen el mismo proceso de forma diferente
- Valores de configuración inconsistentes entre secciones
- Terminología usada de forma inconsistente

**Rol Afectado:**

- Todos los roles
- Especialmente crítico para documentación de referencia

**Severidad:**

- Alta (causa confusión y errores)

**Referencias:**

- Mencionado en technical-brief.md como "gaps de consistencia"

---

## 4. Criterios de Identificación

### Basado en Rol del Documento

**Documento de Arquitectura:**

- Enfoque: Decisiones de alto nivel, trade-offs, patrones
- Gaps críticos: Justificación, dependencias, contexto de negocio
- Audiencia: Arquitecto Senior, Desarrollador Senior

**Documento de Producto:**

- Enfoque: Funcionalidades, user stories, casos de uso
- Gaps críticos: Contexto de negocio, justificación de features
- Audiencia: Product Manager, Stakeholders

**Documento de Implementación:**

- Enfoque: Detalle técnico, código, configuración
- Gaps críticos: Implementación, dependencias, historia de cambios
- Audiencia: Desarrollador Senior, Desarrollador Junior

**Documento de Operaciones:**

- Enfoque: Runbooks, procedimientos, troubleshooting
- Gaps críticos: Implementación, dependencias, historia de cambios
- Audiencia: DevOps/SRE, Desarrollador Senior

### Basado en Audiencia Esperada

**Audiencia Senior:**

- Gaps esperados: Justificación de decisiones, trade-offs, contexto de negocio
- Gaps menos críticos: Definiciones de términos básicos

**Audiencia Junior:**

- Gaps esperados: Definiciones, implementación detallada, ejemplos
- Gaps menos críticos: Justificación de decisiones de alto nivel

**Audiencia Mixta:**

- Gaps esperados: Todos los tipos, con gradación de profundidad
- Estrategia: Proveer múltiples niveles de detalle

### Criterios de Procesamiento

**Criterio de Calificación:**

- El sistema revisa el campo de calificación del documento (escala 0-10)
- Documentos con calificación ≥9 NO se procesan (considerados de alta calidad)
- Solo documentos con calificación <9 son sometidos al proceso de detección
- Esto permite al sistema enfocar recursos en áreas donde hay oportunidad de mejora

**Referencia a Skills:**

- El proceso de detección se inspira en el skill document-critique como referencia para la estructura de análisis
- Debe adaptarse a las herramientas MCP disponibles y las estructuras de datos del sistema

### [PENDIENTE] Algoritmos de Detección

**Requisitos Pendientes:**

- [PENDIENTE] Patrones de texto específicos para cada tipo de gap
- [PENDIENTE] Heurísticas de detección por tipo de documento
- [PENDIENTE] Umbrales de confianza para detección
- [PENDIENTE] Estrategia de reducción de falsos positivos

---

## 5. Ejemplos por Tipo de Documento

### Documento de Arquitectura

**Gap de Justificación:**

- **Texto:** "Usamos PostgreSQL como base de datos principal."
- **Gap:** No se explica por qué PostgreSQL vs MySQL, MongoDB, etc.
- **Pregunta:** ¿Por qué se eligió PostgreSQL? ¿Qué trade-offs se consideraron?
- **Rol Afectado:** Arquitecto Senior

**Gap de Implementación:**

- **Texto:** "El sistema usa microservicios para escalabilidad."
- **Gap:** No se definen límites de servicio, estrategia de comunicación, orquestación
- **Pregunta:** ¿Cuáles son los límites de cada microservicio? ¿Cómo se comunican?
- **Rol Afectado:** Desarrollador Senior

**Gap de Dependencia:**

- **Texto:** "Integramos con Stripe para pagos."
- **Gap:** No se especifica qué endpoints, webhooks, estrategia de retry
- **Pregunta:** ¿Qué endpoints de Stripe se usan? ¿Cómo se manejan webhooks?
- **Rol Afectado:** Desarrollador Senior

### Documento de Producto

**Gap de Contexto de Negocio:**

- **Texto:** "Implementamos búsqueda avanzada de usuarios."
- **Gap:** No se conecta con métricas de negocio o objetivos
- **Pregunta:** ¿Qué problema de negocio resuelve esta feature? ¿Qué métricas de éxito se esperan?
- **Rol Afectado:** Product Manager

**Gap de Justificación:**

- **Texto:** "La plataforma soporta multi-tenant."
- **Gap:** No se explica por qué es necesario para el modelo de negocio
- **Pregunta:** ¿Por qué multi-tenant es crítico para el modelo de negocio?
- **Rol Afectado:** CTO/VP Engineering

### Documento de Operaciones

**Gap de Historia de Cambios:**

- **Texto:** "Actualizado timeout de API a 30 segundos."
- **Gap:** No se explica por qué el cambio anterior y qué problema resuelve
- **Pregunta:** ¿Por qué se cambió el timeout? ¿Qué problema de latencia se estaba experimentando?
- **Rol Afectado:** DevOps/SRE

**Gap de Implementación:**

- **Texto:** "Usamos Redis para cache."
- **Gap:** No se especifica estrategia de cache (TTL, invalidación, etc.)
- **Pregunta:** ¿Cuál es la estrategia de cache? ¿Cómo se invalidan entradas?
- **Rol Afectado:** DevOps/SRE

### Documento de Código

**Gap de Historia de Cambios:**

- **Texto:** Commit message: "fix bug in auth"
- **Gap:** No se explica qué bug y por qué la solución
- **Pregunta:** ¿Qué bug específico se corrigió? ¿Por qué esta solución?
- **Rol Afectado:** Desarrollador Senior

**Gap de Justificación:**

- **Texto:** Código implementa patrón singleton
- **Gap:** No se explica por qué singleton es apropiado aquí
- **Pregunta:** ¿Por qué singleton en lugar de otra estrategia de instanciación?
- **Rol Afectado:** Desarrollador Senior

---

## 6. Metadata de Gaps

### Metadata Requerida

**Identificación:**

- ID único del gap
- Tipo de gap (definición, justificación, implementación, etc.)
- Texto exacto del gap en el documento
- Ubicación (línea, sección)

**Contexto:**

- Tipo de documento (arquitectura, producto, implementación, operaciones)
- Rol del documento
- Audiencia esperada (senior, junior, mixta)

**Prioridad:**

- Severidad (alta, media, baja)
- Rol afectado principal
- Rol afectado secundario

**Estado:**

- Estado del gap (detectado, en sesión, resuelto, verificado)
- Fecha de detección
- Fecha de resolución

**Referencias:**

- Documentos relacionados
- Gaps similares resueltos previamente

### [PENDIENTE] Sistemas de Metadata

**Requisitos Pendientes:**

- [PENDIENTE] Esquema de base de datos para metadata de gaps
- [PENDIENTE] API para consulta y actualización de metadata
- [PENDIENTE] Sistema de búsqueda de gaps por metadata
- [PENDIENTE] Analytics de gaps por tipo, severidad, rol

---

## Referencias

- [STR-001](../../estrategia/estrategia/vision-mission.md): Vision and Mission Statement
- [FEA-001](../funcionalidades/5-phase-workflow.md): Flujo de Trabajo de 5 Fases
- [ARC-001](../../ingenieria/arquitectura/technical-brief.md): Technical Brief
- [REQ-001](requisitos-funcionales.md): Requisitos Funcionales

---

*Documento generado como catálogo de gaps de contexto del producto.*

---

## Nota de Mejora

Este documento puede mejorarse incorporando información del contexto adicional (@[docs/contexto-adicional.md]), específicamente:

- Criterio de calificación ≥9 para no procesar documentos de alta calidad
- Referencia al skill document-critique como estructura de análisis para detección de gaps
- Arqueología de código para proyectos legacy (análisis de commits, pull requests, issues)
- Detección diferenciada para proyectos nuevos (capturar decisiones arquitectónicas desde el inicio) vs legacy
- Verificación cruzada entre documentos para detectar inconsistencias y contradicciones
