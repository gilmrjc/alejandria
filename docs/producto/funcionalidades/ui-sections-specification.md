---
id: FEA-003
type: Feature Document
related:
  - target: FEA-001
    relationship_type: implements
    reason: Implementa el workflow de 5 fases especificando secciones de UI
  - target: PRD-003
    relationship_type: implements
    reason: Implementa el PRD de Hito 3 con especificaciones de UI
  - target: FEAT-007
    relationship_type: implements
    reason: Implementa el feature de búsqueda semántica en UI
  - target: REQ-013
    relationship_type: references
    reason: Referencia los requisitos de secciones de UI
---

# UI Sections Specification

Especificación de las secciones principales de la interfaz de usuario de Alejandria.

**Nota**: Para definiciones de conceptos técnicos clave (SPA, Diff Viewer, State Management, etc.), consulte [PRD-003](../requisitos/prd-hito-03-frontend-react.md) (sección 3, subsección Glosario de Términos Técnicos).

---

## Sección de Documentos

### Descripción

Vista estructurada de todo el conocimiento técnico del proyecto organizada jerárquicamente como sistema de archivos.

### Propósito

Permitir navegación eficiente de documentación con capacidades de búsqueda semántica y múltiples modos de vista.

### User Personas

- Todos los roles

### Cómo Funciona

Los usuarios navegan carpetas y archivos en vista de árbol. Incluye búsqueda semántica en lenguaje natural, versiones históricas, y modos de vista (aprendizaje, referencia, auditoría, contribución, grafo).

### Casos de Uso

- Encontrar documento específico
- Buscar información por intención en lenguaje natural
- Comparar versiones de un documento
- Ver evolución del contenido

### Componentes y Referencias

- Vista jerárquica de documentos → [ARC-008](../../ingenieria/arquitectura/technology-stack.md)
- Búsqueda semántica → [PENDIENTE]
- Versioning de documentos → [PENDIENTE]

### Decisiones Relacionadas

- Metadata a mostrar: Título, tipo, calificación, fecha última actualización, estado healthy/unhealthy, tags (según PRD-003)
- Filtros: Por tipo (PRD/TRD/ADR), por calificación (>7/5-7/<5), por fecha (última semana/mes/año) (según PRD-003)
- Acciones: Ver historial de versiones, ver gaps asociados, marcar como healthy, ver diff viewer (según PRD-003)
- Paginación: 20 items por página para MVP (según PRD-003)

---

## Sección de Preguntas

### Descripción

Mecanismo donde el sistema captura conocimiento técnico inicial mediante preguntas generadas automáticamente.

### Propósito

Transformar respuestas en vectores para búsqueda semántica posterior y mantener traza clara entre respuestas y referencias originales.

### User Personas

- CTO/VP Engineering
- Senior Developer/Tech Lead

### Cómo Funciona

El sistema genera preguntas automáticamente al crear el primer documento. Las respuestas son generadas internamente por agentes LLM y transformadas en vectores para Qdrant. Los usuarios pueden regenerar respuestas si no están satisfechos.

### Casos de Uso

- Capturar conocimiento inicial del proyecto
- Responder preguntas sobre el proyecto
- Buscar información similar posteriormente

### Componentes y Referencias

- Generación de preguntas → [PENDIENTE]
- Respuestas por agentes LLM → [PENDIENTE]
- Almacenamiento en Qdrant → [PENDIENTE]

### Decisiones Relacionadas

- Organización: Por tags (negocio/arquitectura/seguridad), por prioridad (crítico/alto/medio/bajo) (según PRD-003)
- Filtros: Por prioridad, por estado (pendiente/respondido), por tipo de gap (según PRD-003)
- Interfaz de respuesta: Campo de texto pre-rellenado, botones (aceptar/modificar/rechazar), feedback visual de estado (según PRD-003)

---

## Sección de Gaps

### Descripción

Interfaz para la Fase 3 de Resolución donde los usuarios responden manualmente gaps de contexto detectados.

### Propósito

Facilitar resolución eficiente de gaps mediante sugerencias pre-rellenadas y referencias al contexto original.

### User Personas

- CTO/VP Engineering
- Senior Developer/Tech Lead
- DevOps/SRE

### Cómo Funciona

Los gaps se presentan como tarjetas con caja de respuesta pre-rellenada con sugerencias del agente LLM. El usuario puede aceptar, modificar o rechazar sugerencias. Cada gap incluye referencia al documento que lo generó.

### Casos de Uso

- Resolver gaps de contexto
- Revisar sugerencias del sistema
- Navegar al documento original para contexto

### Componentes y Referencias

- Presentación de gaps → [FEA-001](../5-phase-workflow.md)
- Sugerencias pre-rellenadas → [PENDIENTE]

### Decisiones Relacionadas

- Dashboard de gaps: Filtros por tema, prioridad, estado (pendiente/en progreso/resuelto) (según PRD-003)
- Estados de gaps: Pendiente, en progreso, resuelto, no aplica, obsoleto (según PRD-003)
- Interfaz de interacción asíncrona: Similar a sección de preguntas, campo de respuesta, acciones (según PRD-003)

---

## Sección de Propuestas

### Descripción

Interfaz para la Fase 5 de Aplicación donde el sistema presenta sugerencias de edición derivadas de gaps resueltos.

### Propósito

Transformar contexto capturado en acciones específicas que pueden implementarse en los documentos.

### User Personas

- CTO/VP Engineering
- Senior Developer/Tech Lead
- DevOps/SRE

### Cómo Funciona

Las propuestas se presentan como tarjetas con nombre descriptivo, archivos a editar, referencias a gaps resueltos, y texto detallado de acciones. El usuario aprueba o rechaza propuestas para implementación automática.

### Casos de Uso

- Revisar propuestas de edición
- Aprobar cambios automáticos
- Rechazar propuestas no deseadas

### Componentes y Referencias

- Generación de propuestas → [FEA-001](../5-phase-workflow.md)
- Implementación automática → [PENDIENTE]

### Decisiones Relacionadas

- Metadata a mostrar: Título, fecha creación, estado, documento asociado, impacto estimado (según PRD-003)
- Estados de propuestas: Pendiente, aprobada, rechazada, aplicada (según PRD-003)
- Integración con diff viewer: Modal con diff viewer lado a lado, botones (aprobar/rechazar/aplicar) (según PRD-003)

---

## Sección de Grafo

### Descripción

Visualización gráfica de relaciones entre documentos, gaps y respuestas para entender estructura del conocimiento.

### Propósito

Permitir comprensión intuitiva de cómo se construye y conecta el conocimiento institucional.

### User Personas

- CTO/VP Engineering
- Senior Developer/Tech Lead
- Arquitecto Senior

### Cómo Funciona

El grafo muestra conexiones entre elementos con capacidades de filtrado por tipo, categoría, y nivel de detalle. Incluye grafo temporal (evolución en tiempo), grafo de impacto (dependencias), y grafo de autoría (mapa de expertise).

### Casos de Uso

- Visualizar relaciones entre documentos
- Entender impacto de cambios antes de aplicarlos
- Identificar knowledge silos
- Ver evolución del conocimiento en tiempo

### Componentes y Referencias

- Visualización de grafo → [PENDIENTE]
- Filtrado multidimensional → [PENDIENTE]
- Grafo temporal/impacto/autoría → [PENDIENTE]

### Decisiones Relacionadas

- Librería de visualización: Evaluar opciones (react-flow, vis-network, d3.js) - decisión en fase de implementación (según PRD-003)
- Tipos de relaciones: Referencia, implementa, depende, relacionado (según PRD-003)
- Metadata de nodos: Tipo de documento, calificación, estado, tags (según PRD-003)
