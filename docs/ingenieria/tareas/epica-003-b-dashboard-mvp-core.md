---
id: EPC-0032
type: Epic Implementation
rating: 9
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
  - target: EPC-0033
    relationship_type: depends_on
    reason: EPC-0033 proporciona el diff viewer reutilizable para EPC-0032
---

## Epica 3-B: Dashboard MVP Core

**Estado**: ⏳ PENDIENTE - Técnicas por definir

**Objetivo**: Implementar funcionalidades principales del frontend para dogfooding, incluyendo dashboard completo con métricas, secciones de documentos, gaps y propuestas.

---

## Referencias

- **[../../estrategia/estrategia/technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md)**: Roadmap técnico, Hito 3
- **[../../estrategia/estrategia/frontend-strategy.md](../../estrategia/estrategia/frontend-strategy.md)**: Estrategia de frontend
- **[../arquitectura/technology-stack.md](../arquitectura/technology-stack.md)**: Stack tecnológico
- **[../arquitectura/frontend-specification.md](../arquitectura/frontend-specification.md)**: Especificación de frontend

---

## Componentes

- Dashboard General con métricas agregadas
- Sección de Documentos con filtros y búsqueda
- Sección de Gaps con agrupación por tema
- Sección de Propuestas con diff viewer integrado

---

## Recursos y Habilidades Requeridas

**Habilidades Técnicas Requeridas**:
- React + TypeScript (experiencia intermedia-senior, 2+ años)
- State Management (Zustand)
- HTTP Client (Axios)
- Routing (React Router)
- UI Components (shadcn/ui)
- Styling (TailwindCSS)
- Testing (Jest + React Testing Library)

**Asignación de Equipo**:
- 1 desarrollador (Technical Lead) según technology-stack.md

**Dependencias Externas**:
- API endpoints: Ya definidos en Hito 2 (API REST y MCP Server)
- Diseño UI/UX: Usa componentes pre-diseñados (shadcn/ui)

**Referencias**:
- [technology-stack.md](../arquitectura/technology-stack.md): Stack de frontend (líneas 95-106, 155, 206-213)
- [frontend-specification.md](../arquitectura/frontend-specification.md): Habilidades requeridas (líneas 44-52)

---

## Priorización de Features

**MVP Esenciales para Dogfooding**:
- T-033-completo: Implementar Dashboard General completo
- T-034: Implementar Sección de Documentos
- T-036: Implementar Sección de Gaps
- T-037: Implementar Sección de Propuestas

**Justificación**:
Según technical-roadmap.md, los criterios de completitud del Hito 3 incluyen "Dashboard muestra documentos y gaps". El Hito 3 se movió desde Hito 6 para facilitar dogfooding y validación temprana de UX desde el inicio del ciclo. Estas 4 tareas entregan el MVP funcional para validación temprana.

**Referencias**:
- [technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md): Hito 3 criterios y timeline (líneas 143-174)
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Requisitos de componentes (líneas 145-184, 239-241, 397-402)

---

## Valor de Negocio y Casos de Uso

**Problemas del Usuario Resueltos**:
- Falta de interfaz visual: Sin frontend, la interacción vía API REST directa requiere conocimiento técnico
- Dificultad para navegar documentos: Sin dashboard, no hay vista agregada del estado del proyecto
- Proceso manual de revisión de cambios: Sin diff viewer, la comparación manual es lenta y propensa a errores
- Falta de visibilidad de progreso: Sin dashboard de gaps/propuestas, no es fácil trackear el estado de resolución

**Casos de Usuario Habilitados**:
1. Revisar estado del proyecto via Dashboard con métricas agregadas
2. Navegar documentos via Sección de Documentos con filtros y búsqueda
3. Revisar gaps detectados via Sección de Gaps con agrupación por tema
4. Revisar y aprobar cambios via Sección de Propuestas con diff viewer integrado
5. Navegación rápida desde Dashboard a secciones específicas

**Mejora vs Situación Actual**:
- Interfaz visual intuitiva reduce barrera de entrada vs API REST directa
- Dashboard agrega métricas en un lugar vs múltiples llamadas API
- Diff viewer muestra cambios lado a lado vs comparación manual
- Filtros y búsqueda facilitan encontrar información vs navegación lineal

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

- T-033-completo: Implementar Dashboard General completo
- T-034: Implementar Sección de Documentos
- T-036: Implementar Sección de Gaps
- T-037: Implementar Sección de Propuestas

### Justificación del Orden de Tareas

El orden de tareas se basa en dependencias secuenciales y valor crítico. T-033-completo (dashboard) es el componente principal que agrega información de todas las secciones. T-034, T-036 y T-037 pueden ejecutarse en paralelo después de completar la infraestructura base (EPC-0031), ya que son secciones independientes que se integran en el dashboard.

La paralelización es posible: T-034, T-036 y T-037 pueden ejecutarse en paralelo para optimizar el tiempo total de implementación del MVP.

### T-033-completo: Implementar Dashboard General

**Descripción**: Implementar dashboard completo con resumen de documentos (total, calificación promedio), gaps pendientes por prioridad, propuestas pendientes, y métricas de progreso. Implementar navegación rápida a secciones y filtros por módulo/estado. Incluir testing de componentes.

**Criterios de Aceptación**:
- [ ] Dashboard muestra resumen de documentos (total, calificación promedio)
- [ ] Dashboard muestra gaps pendientes por prioridad
- [ ] Dashboard muestra propuestas pendientes
- [ ] Dashboard muestra métricas de progreso (porcentaje gaps resueltos, documentos healthy)
- [ ] Navegación rápida a secciones funciona
- [ ] Filtros por módulo/estado implementados
- [ ] Métricas se actualizan correctamente (polling cada 5 min)
- [ ] Unit tests para componentes del dashboard implementados
- [ ] Integration tests con mocks de API implementados
- [ ] Cobertura de tests >70%

**Dependencias**: EPC-0031 (T-030, T-031, T-032, T-040)

**Referencias**:
- [technical-specs-dashboard-general.md](../arquitectura/technical-specs-dashboard-general.md): Especificación técnica detallada
- [requisitos-dashboard-general.md](../../producto/requisitos/requisitos-dashboard-general.md): Requisitos funcionales
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Componente Dashboard (líneas 83-104)

**Estado**: PENDIENTE

---

### T-034: Implementar Sección de Documentos

**Descripción**: Implementar vista de documentos con lista paginada, filtros (tipo, calificación, fecha), búsqueda, y vista detallada de documento individual. Implementar acciones por documento (ver historial, ver gaps, marcar como healthy). Incluir testing de componentes.

**Criterios de Aceptación**:
- [ ] Lista de documentos con metadata implementada
- [ ] Filtros por tipo de documento, calificación, fecha funcionan
- [ ] Búsqueda de documentos funciona
- [ ] Vista detallada de documento individual implementada
- [ ] Acciones por documento funcionan (ver historial, ver gaps, marcar como healthy)
- [ ] Paginación o infinite scroll implementado
- [ ] Unit tests para componentes de documentos implementados
- [ ] Integration tests con mocks de API implementados
- [ ] Cobertura de tests >70%

**Dependencias**: EPC-0031 (T-030, T-031, T-032, T-040)

**Referencias**:
- [frontend-specification.md](../arquitectura/frontend-specification.md): Componente DocumentList (líneas 140-176)
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Sección de Documentos (líneas 105-124)

**Estado**: PENDIENTE

---

### T-036: Implementar Sección de Gaps

**Descripción**: Implementar dashboard de gaps detectados con filtros, agrupación de gaps por tema, metadata de tags (tema, subtema, prioridad), vista de gaps por estado, e interfaz de interacción asíncrona para resolución. Incluir testing de componentes.

**Criterios de Aceptación**:
- [ ] Dashboard de gaps con filtros implementado
- [ ] Agrupación de gaps por tema funciona
- [ ] Metadata de tags (tema, subtema, prioridad) se muestra
- [ ] Vista de gaps por estado implementada
- [ ] Interfaz de interacción asíncrona para resolución funciona
- [ ] Unit tests para componentes de gaps implementados
- [ ] Integration tests con mocks de API implementados
- [ ] Cobertura de tests >70%

**Dependencias**: EPC-0031 (T-030, T-031, T-032, T-040)

**Referencias**:
- [frontend-specification.md](../arquitectura/frontend-specification.md): Componente GapResolutionPanel (líneas 279-308)
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Sección de Gaps (líneas 145-164)

**Estado**: PENDIENTE

---

### T-037: Implementar Sección de Propuestas

**Descripción**: Implementar vista de propuestas con lista paginada, filtros por estado, vista detallada de propuesta individual, diff viewer integrado para revisar cambios, y acciones (aprobar, rechazar, aplicar). Incluir testing de componentes.

**Criterios de Aceptación**:
- [ ] Lista de propuestas con metadata implementada
- [ ] Filtros por estado funcionan
- [ ] Vista detallada de propuesta individual implementada
- [ ] Diff viewer integrado para revisar cambios funciona
- [ ] Acciones funcionan (aprobar, rechazar, aplicar)
- [ ] Unit tests para componentes de propuestas implementados
- [ ] Integration tests con mocks de API implementados
- [ ] Cobertura de tests >70%

**Dependencias**: EPC-0031 (T-030, T-031, T-032, T-040), EPC-0033 (T-039 - Diff Viewer)

**Referencias**:
- [frontend-specification.md](../arquitectura/frontend-specification.md): Componente ContextEntriesView (líneas 310-338)
- [requisitos-diff-viewer.md](../../producto/requisitos/requisitos-diff-viewer.md): Requisitos de diff viewer
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Sección de Propuestas (líneas 165-184)

**Estado**: PENDIENTE
