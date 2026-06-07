---
id: EPC-0033
type: Epic Implementation
rating: 8
rating-phase: document-editing
related:
  - target: STR-003
    relationship_type: implements
    reason: Implementa la estrategia técnica de frontend React
  - target: STR-005
    relationship_type: implements
    reason: Implementa la estrategia de frontend
  - target: PRD-003
    relationship_type: implements
    reason: Implementa el PRD de Hito 3 con requisitos de frontend
  - target: ARC-008
    relationship_type: references
    reason: Referencia el frontend-specification para especificación técnica
  - target: EPC-0031
    relationship_type: depends_on
    reason: Depende de la infraestructura base configurada en EPC-0031
  - target: EPC-0032
    relationship_type: extends
    reason: Proporciona componentes reutilizables (diff viewer) para el Dashboard MVP
---

## Epica 3-C: Componentes Adicionales

**Estado**: ⏳ PENDIENTE - Técnicas por definir

**Objetivo**: Implementar features POST-MVP y componentes reutilizables como sección de preguntas, grafo de relaciones y diff viewer.

---

## Referencias

- **[../../estrategia/estrategia/technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md)**: Roadmap técnico, Hito 3
- **[../../estrategia/estrategia/frontend-strategy.md](../../estrategia/estrategia/frontend-strategy.md)**: Estrategia de frontend
- **[../arquitectura/technology-stack.md](../arquitectura/technology-stack.md)**: Stack tecnológico
- **[../arquitectura/frontend-specification.md](../arquitectura/frontend-specification.md)**: Especificación de frontend

---

## Componentes

- Sección de Preguntas (gaps detectados)
- Sección de Grafo (visualización de relaciones)
- Diff Viewer (componente reutilizable para comparación de cambios)

---

## Recursos y Habilidades Requeridas

**Habilidades Técnicas Requeridas**:
- React + TypeScript (experiencia intermedia-senior, 2+ años)
- State Management (Zustand)
- HTTP Client (Axios)
- Routing (React Router)
- UI Components (shadcn/ui)
- Styling (TailwindCSS)
- Testing (Vitest + React Testing Library)
- Graph Visualization (librería específica)

**Asignación de Equipo**:
- 1 desarrollador (Technical Lead) según technology-stack.md

**Dependencias Externas**:
- API endpoints: Ya definidos en Hito 2 (API REST y MCP Server)
- Diseño UI/UX: Usa componentes pre-diseñados (shadcn/ui)
- Graph Visualization Library: Por definir (ej. D3.js, React Flow, Cytoscape.js)

**Referencias**:
- [technology-stack.md](../arquitectura/technology-stack.md): Stack de frontend (líneas 95-106, 155, 206-213)
- [frontend-specification.md](../arquitectura/frontend-specification.md): Habilidades requeridas (líneas 44-52)

---

## Priorización de Features

**Features POST-MVP / Nice-to-have**:
- T-039: Implementar Diff Viewer (componente reutilizable, usado por EPC-0032)
- T-035: Implementar Sección de Preguntas (depende de backend de Hito 4)
- T-038: Implementar Sección de Grafo (nice-to-have para dogfooding inicial)

**Justificación**:
T-039 (Diff Viewer) tiene prioridad alta porque es componente reutilizable requerido por EPC-0032 (Sección de Propuestas). T-035 y T-038 son features POST-MVP que pueden desarrollarse en paralelo después de completar el MVP core. T-035 depende de backend de Hito 4 según PRD-003.

**Referencias**:
- [technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md): Hito 3 criterios y timeline (líneas 143-174)
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Requisitos de componentes (líneas 125-144, 185-204, 205-224)

---

## Valor de Negocio y Casos de Uso

**Problemas del Usuario Resueltos**:
- Sin diff viewer, la revisión de cambios es manual y propensa a errores
- Sin sección de preguntas, no hay interfaz para interactuar con gaps detectados
- Sin grafo de relaciones, es difícil entender el impacto de cambios entre documentos

**Casos de Usuario Habilitados**:
1. Revisar y responder preguntas (gaps detectados) con interfaz interactiva
2. Visualizar relaciones entre documentos y código en un grafo interactivo
3. Comparar cambios lado a lado con diff viewer integrado
4. Entender el impacto completo de cambios antes de aplicarlos

**Mejora vs Situación Actual**:
- Diff viewer muestra cambios lado a lado vs comparación manual
- Interfaz de preguntas facilita resolución de gaps vs proceso manual
- Grafo visualiza relaciones vs navegación lineal entre documentos
- Componentes reutilizables reducen duplicación de código

**Referencias**:
- [technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md): Valor de Hito 3 (líneas 143-174)
- [frontend-strategy.md](../../estrategia/estrategia/frontend-strategy.md): Objetivos de frontend (líneas 25-28)
- [frontend-specification.md](../arquitectura/frontend-specification.md): Componentes de UI (líneas 104-176)
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Casos de Usuario (sección 1, subsección Casos de Usuario)

---

## Técnicas Individuales

### Estimación de Esfuerzo Total

**PENDIENTE**: Estimación total por definir en fase de implementación

Desglose por tarea:

- T-039: Implementar Diff Viewer
- T-035: Implementar Sección de Preguntas
- T-038: Implementar Sección de Grafo

### Justificación del Orden de Tareas

T-039 (Diff Viewer) tiene prioridad alta porque es componente reutilizable requerido por EPC-0032 (T-037: Sección de Propuestas). T-035 y T-038 pueden ejecutarse en paralelo después de completar la infraestructura base (EPC-0031), ya que son componentes independientes. T-035 depende de backend de Hito 4 según PRD-003, por lo que puede postponerse si el backend no está listo.

### T-039: Implementar Diff Viewer

**Descripción**: Implementar componente de diff viewer para comparación visual de cambios. Mostrar diferencias lado a lado, resaltar adiciones/eliminaciones/modificaciones, permitir navegación por secciones específicas, y entender impacto completo de cambios. Incluir testing de componentes.

**Criterios de Aceptación**:
- [ ] Diff viewer muestra diferencias lado a lado
- [ ] Adiciones, eliminaciones y modificaciones están resaltadas
- [ ] Navegación por secciones específicas funciona
- [ ] Impacto completo de cambios es entendible
- [ ] Motor de comparación de texto funciona
- [ ] Sincronización de scroll entre paneles funciona
- [ ] Componente es reutilizable en múltiples contextos
- [ ] Unit tests para diff viewer implementados
- [ ] Integration tests con mocks de datos implementados
- [ ] Cobertura de tests >70%

**Dependencias**: EPC-0031 (T-030)

**Referencias**:
- [requisitos-diff-viewer.md](../../producto/requisitos/requisitos-diff-viewer.md): Requisitos funcionales detallados
- [technical-specs-diff-viewer.md](../arquitectura/technical-specs-diff-viewer.md): Especificación técnica
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Diff Viewer (líneas 205-224)

**Estado**: PENDIENTE

---

### T-035: Implementar Sección de Preguntas

**Descripción**: Implementar vista de preguntas (gaps detectados) organizadas por tema/tags. Implementar filtros por prioridad, tipo de gap, estado. Implementar vista detallada de pregunta individual con interfaz para responder (campo pre-rellenado) y acciones (aceptar sugerencia, modificar, rechazar). Incluir testing de componentes.

**Criterios de Aceptación**:
- [ ] Lista de preguntas organizadas por tema/tags implementada
- [ ] Filtros por prioridad, tipo de gap, estado funcionan
- [ ] Vista detallada de pregunta individual implementada
- [ ] Interfaz para responder pregunta (campo pre-rellenado) funciona
- [ ] Acciones funcionan (aceptar sugerencia, modificar, rechazar)
- [ ] Unit tests para componentes de preguntas implementados
- [ ] Integration tests con mocks de API implementados
- [ ] Cobertura de tests >70%

**Dependencias**: EPC-0031 (T-030, T-031, T-032, T-040), Backend Hito 4

**Referencias**:
- [frontend-specification.md](../arquitectura/frontend-specification.md): Componente SessionView (líneas 241-277)
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Sección de Preguntas (líneas 125-144)

**Estado**: PENDIENTE

---

### T-038: Implementar Sección de Grafo

**Descripción**: Implementar visualización de grafo de relaciones entre documentos y código. Implementar filtros por tipo de relación, navegación interactiva (zoom, pan, selección), metadata de nodos, y resaltado de impacto de cambios. Incluir testing de componentes.

**Criterios de Aceptación**:
- [ ] Visualización de grafo de relaciones implementada
- [ ] Filtros por tipo de relación funcionan
- [ ] Navegación interactiva (zoom, pan, selección) funciona
- [ ] Metadata de nodos se muestra
- [ ] Resaltado de impacto de cambios funciona
- [ ] Performance de renderizado de grafo es aceptable
- [ ] Unit tests para componentes de grafo implementados
- [ ] Integration tests con mocks de datos implementados
- [ ] Cobertura de tests >70%

**Dependencias**: EPC-0031 (T-030, T-031, T-032, T-040)

**Referencias**:
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Sección de Grafo (líneas 185-204)

**Estado**: PENDIENTE
