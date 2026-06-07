---
id: EPC-003
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
    relationship_type: extends
    reason: Esta epica se divide en 3 epicas atómicas para mejor gestión
  - target: EPC-0032
    relationship_type: extends
    reason: Esta epica se divide en 3 epicas atómicas para mejor gestión
  - target: EPC-0033
    relationship_type: extends
    reason: Esta epica se divide en 3 epicas atómicas para mejor gestión
---

## Epica 3: Frontend React (Overview)

**Estado**: ⏳ DIVIDIDA - Ver epicas hijas para detalles

**Objetivo**: Implementar el frontend SPA con React que incluye el dashboard de documentos, interfaz de sesión interactiva y diff viewer integrado.

**Nota**: Esta epica se ha dividido en 3 epicas atómicas para mejor gestión y paralelización. Ver las epicas hijas para detalles de implementación.

---

## Epicas Hijas

Esta epica se ha dividido en las siguientes epicas atómicas:

1. **[EPC-0031: Infraestructura Frontend Base](./epica-003-a-infraestructura-frontend-base.md)**
   - Configurar estructura base de proyecto React
   - Implementar routing y navegación
   - Implementar cliente HTTP y autenticación
   - Implementar state management global
   - Configurar build y deployment
   - Implementar Dashboard base (validación visual)
   - Configurar Storybook

2. **[EPC-0032: Dashboard MVP Core](./epica-003-b-dashboard-mvp-core.md)**
   - Implementar Dashboard General completo
   - Implementar Sección de Documentos
   - Implementar Sección de Gaps
   - Implementar Sección de Propuestas
   - Testing integrado en cada componente

3. **[EPC-0033: Componentes Adicionales](./epica-003-c-componentes-adicionales.md)**
   - Implementar Diff Viewer (componente reutilizable)
   - Implementar Sección de Preguntas
   - Implementar Sección de Grafo
   - Testing integrado en cada componente

---

## Referencias

- **[../../estrategia/estrategia/technical-roadmap.md](../../estrategia/estrategia/technical-roadmap.md)**: Roadmap técnico, Hito 3
- **[../../estrategia/estrategia/frontend-strategy.md](../../estrategia/estrategia/frontend-strategy.md)**: Estrategia de frontend
- **[../arquitectura/technology-stack.md](../arquitectura/technology-stack.md)**: Stack tecnológico
- **[../arquitectura/frontend-specification.md](../arquitectura/frontend-specification.md)**: Especificación de frontend

---

## Componentes

- SPA React con componentes principales
- Dashboard de documentos y gaps
- Interfaz de sesión interactiva
- Diff viewer integrado

---

## Recursos y Habilidades Requeridas

**Habilidades Técnicas Requeridas**:
- React + TypeScript (experiencia intermedia-senior, 2+ años)
- State Management (Zustand para MVP)
- HTTP Client (Axios con interceptors JWT)
- Routing (React Router)
- UI Components (shadcn/ui)
- Styling (TailwindCSS)
- Testing (Jest + React Testing Library)
- Build Tool (Vite)

**Asignación de Equipo**:
- 1 desarrollador (Technical Lead) según technology-stack.md que define monorepo con un desarrollador para MVP Bootstrapped

**Dependencias Externas**:
- API endpoints: Ya definidos en Hito 2 (API REST y MCP Server)
- Diseño UI/UX: Usa componentes pre-diseñados (shadcn/ui, no requiere diseñador dedicado)
- LLM Provider: Ollama local (Qwen 3.5, no requiere configuración externa)

**Referencias**:
- [technology-stack.md](../arquitectura/technology-stack.md): Stack de frontend (líneas 95-106, 155, 206-213)
- [frontend-specification.md](../arquitectura/frontend-specification.md): Habilidades requeridas (líneas 44-52)

---

## Priorización de Features

**MVP Esenciales para Dogfooding**:
- T-030: Configurar Estructura Base de Proyecto React
- T-031: Implementar Routing y Navegación
- T-032: Implementar Cliente HTTP y Autenticación
- T-040: Implementar State Management Global
- T-033: Implementar Dashboard General
- T-034: Implementar Sección de Documentos
- T-036: Implementar Sección de Gaps
- T-037: Implementar Sección de Propuestas
- T-039: Implementar Diff Viewer

**Features que pueden Postponerse**:
- T-038: Sección de Grafo - nice-to-have para dogfooding inicial
- T-035: Sección de Preguntas - depende de backend de Hito 4
- Interfaz de Sesión Interactiva - marcada como POST-MVP en PRD-003

**Justificación**:
Según technical-roadmap.md, los criterios de completitud del Hito 3 incluyen "Dashboard muestra documentos y gaps". El Hito 3 se movió desde Hito 6 para facilitar dogfooding y validación temprana de UX desde el inicio del ciclo. El orden de tareas en EPC-003 permite paralelización de T-036 y T-037, optimizando el tiempo de implementación del MVP.

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

- T-030: Configurar estructura base de proyecto React
- T-031: Implementar routing y navegación
- T-032: Implementar cliente HTTP y autenticación
- T-033: Implementar Dashboard General
- T-034: Implementar Sección de Documentos
- T-035: Implementar Sección de Preguntas
- T-036: Implementar Sección de Gaps
- T-037: Implementar Sección de Propuestas
- T-038: Implementar Sección de Grafo
- T-039: Implementar Diff Viewer
- T-040: Implementar state management global
- T-041: Implementar testing de componentes
- T-042: Configurar build y deployment

### Justificación del Orden de Tareas

El orden de tareas se basa en dependencias secuenciales y valor crítico. T-030 (estructura base) es prerequisito fundamental para todas las demás tareas. T-031 (routing), T-032 (cliente HTTP) y T-040 (state management) son prerequisitos para T-033 a T-038, ya que estos componentes requieren navegación, llamadas a API y estado global. T-039 (diff viewer) es prerequisito específico para T-037, ya que la sección de propuestas utiliza el diff viewer para revisar cambios.

La paralelización es posible en varias fases: T-033, T-034 y T-035 pueden ejecutarse en paralelo después de completar la infraestructura base (T-030, T-031, T-032, T-040). De manera similar, T-036, T-037 y T-038 pueden ejecutarse en paralelo después de la misma base. T-041 (testing) puede ejecutarse en paralelo con el desarrollo de componentes para optimizar el tiempo total.

El flujo lógico sigue cinco fases: (1) Infraestructura base (T-030), (2) Configuración core (T-031, T-032, T-040), (3) Componentes principales (T-033, T-034, T-035), (4) Componentes avanzados (T-036, T-037, T-038, T-039), y (5) Testing y deployment (T-041, T-042).

### T-030: Configurar Estructura Base de Proyecto React

**Descripción**: Crear estructura base del proyecto React con Vite, configurar dependencias (React, React Router, Axios, shadcn/ui/Material-UI, TailwindCSS), y establecer convenciones de código. Configurar TypeScript y ESLint.

**Criterios de Aceptación**:
- [ ] Estructura de directorios configurada según frontend-specification.md (líneas 619-668)
- [ ] package.json configurado con dependencias (React, React Router, Axios, UI library)
- [ ] Vite configurado para desarrollo local (puerto 3000, proxy a API)
- [ ] TypeScript configurado con strict mode
- [ ] ESLint y Prettier configurados
- [ ] TailwindCSS configurado (si se usa shadcn/ui)
- [ ] README con instrucciones de setup

**Dependencias**: Ninguna

**Referencias**:
- [frontend-specification.md](../arquitectura/frontend-specification.md): Estructura de proyecto (líneas 619-668)
- [technology-stack.md](../arquitectura/technology-stack.md): Stack de frontend (líneas 95-106)

**Estado**: PENDIENTE

---

### T-031: Implementar Routing y Navegación

**Descripción**: Configurar React Router para navegación entre secciones. Implementar rutas principales: / (dashboard), /documents, /questions, /gaps, /proposals, /graph. Implementar breadcrumbs o indicador de ubicación.

**Criterios de Aceptación**:
- [ ] React Router configurado con rutas principales
- [ ] Navegación entre secciones funciona correctamente
- [ ] Breadcrumbs o indicador de ubicación implementado
- [ ] Links directos a recursos específicos funcionan
- [ ] 404 page implementada para rutas inexistentes

**Dependencias**: T-030

**Referencias**:
- [frontend-specification.md](../arquitectura/frontend-specification.md): Flujo de navegación (líneas 88-98)
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Requisitos de navegación (líneas 247-260)

**Estado**: PENDIENTE

---

### T-032: Implementar Cliente HTTP y Autenticación

**Descripción**: Configurar Axios como cliente HTTP con interceptors para autenticación (JWT) y manejo de errores. Implementar servicios de API para documents, sessions, gaps, proposals. Configurar base URL y timeout.

**Criterios de Aceptación**:
- [ ] Axios configurado con base URL y timeout
- [ ] Interceptor para agregar token JWT en headers
- [ ] Interceptor para manejar errores 401 (redirigir a login)
- [ ] Servicios de API implementados (documents, sessions, gaps, proposals)
- [ ] Manejo de errores de API claro para el usuario
- [ ] Autenticación con API funciona correctamente

**Dependencias**: T-030

**Referencias**:
- [frontend-specification.md](../arquitectura/frontend-specification.md): Integración con API (líneas 398-529)
- [api-specification.md](../arquitectura/api-specification.md): Endpoints de API REST
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Interacción con API (líneas 289-302)

**Estado**: PENDIENTE

---

### T-033: Implementar Dashboard General

**Descripción**: Implementar dashboard con resumen de documentos (total, calificación promedio), gaps pendientes por prioridad, propuestas pendientes, y métricas de progreso. Implementar navegación rápida a secciones y filtros por módulo/estado.

**Criterios de Aceptación**:
- [ ] Dashboard muestra resumen de documentos (total, calificación promedio)
- [ ] Dashboard muestra gaps pendientes por prioridad
- [ ] Dashboard muestra propuestas pendientes
- [ ] Dashboard muestra métricas de progreso (porcentaje gaps resueltos, documentos healthy)
- [ ] Navegación rápida a secciones funciona
- [ ] Filtros por módulo/estado implementados
- [ ] Métricas se actualizan correctamente (polling cada 5 min)

**PENDIENTE**: Definición exacta de métricas de progreso (ver PRD-003 líneas 100-103)

**Dependencias**: T-030, T-031, T-032, T-040

**Referencias**:
- [technical-specs-dashboard-general.md](../arquitectura/technical-specs-dashboard-general.md): Especificación técnica detallada
- [requisitos-dashboard-general.md](../../producto/requisitos/requisitos-dashboard-general.md): Requisitos funcionales
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Componente Dashboard (líneas 83-104)

**Estado**: PENDIENTE

---

### T-034: Implementar Sección de Documentos

**Descripción**: Implementar vista de documentos con lista paginada, filtros (tipo, calificación, fecha), búsqueda, y vista detallada de documento individual. Implementar acciones por documento (ver historial, ver gaps, marcar como healthy).

**Criterios de Aceptación**:
- [ ] Lista de documentos con metadata implementada
- [ ] Filtros por tipo de documento, calificación, fecha funcionan
- [ ] Búsqueda de documentos funciona
- [ ] Vista detallada de documento individual implementada
- [ ] Acciones por documento funcionan (ver historial, ver gaps, marcar como healthy)
- [ ] Paginación o infinite scroll implementado

**PENDIENTE**: Metadata de documentos a mostrar (ver PRD-003 líneas 121-123), tipos de filtros específicos (líneas 122), acciones disponibles (líneas 123)

**Dependencias**: T-030, T-031, T-032, T-040

**Referencias**:
- [frontend-specification.md](../arquitectura/frontend-specification.md): Componente DocumentList (líneas 140-176)
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Sección de Documentos (líneas 105-124)

**Estado**: PENDIENTE

---

### T-035: Implementar Sección de Preguntas

**Descripción**: Implementar vista de preguntas (gaps detectados) organizadas por tema/tags. Implementar filtros por prioridad, tipo de gap, estado. Implementar vista detallada de pregunta individual con interfaz para responder (campo pre-rellenado) y acciones (aceptar sugerencia, modificar, rechazar).

**Criterios de Aceptación**:
- [ ] Lista de preguntas organizadas por tema/tags implementada
- [ ] Filtros por prioridad, tipo de gap, estado funcionan
- [ ] Vista detallada de pregunta individual implementada
- [ ] Interfaz para responder pregunta (campo pre-rellenado) funciona
- [ ] Acciones funcionan (aceptar sugerencia, modificar, rechazar)

**PENDIENTE**: Organización de preguntas por tema (ver PRD-003 líneas 141), tipos de filtros específicos (líneas 142), interfaz de respuesta asíncrona (líneas 143)

**Dependencias**: T-030, T-031, T-032, T-040

**Referencias**:
- [frontend-specification.md](../arquitectura/frontend-specification.md): Componente SessionView (líneas 241-277)
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Sección de Preguntas (líneas 125-144)

**Estado**: PENDIENTE

---

### T-036: Implementar Sección de Gaps

**Descripción**: Implementar dashboard de gaps detectados con filtros, agrupación de gaps por tema, metadata de tags (tema, subtema, prioridad), vista de gaps por estado, e interfaz de interacción asíncrona para resolución.

**Criterios de Aceptación**:
- [ ] Dashboard de gaps con filtros implementado
- [ ] Agrupación de gaps por tema funciona
- [ ] Metadata de tags (tema, subtema, prioridad) se muestra
- [ ] Vista de gaps por estado implementada
- [ ] Interfaz de interacción asíncrona para resolución funciona

**PENDIENTE**: Dashboard de gaps con filtros específicos (ver PRD-003 líneas 161), interfaz de interacción asíncrona (líneas 162), estados de gaps a mostrar (líneas 163)

**Dependencias**: T-030, T-031, T-032, T-040

**Referencias**:
- [frontend-specification.md](../arquitectura/frontend-specification.md): Componente GapResolutionPanel (líneas 279-308)
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Sección de Gaps (líneas 145-164)

**Estado**: PENDIENTE

---

### T-037: Implementar Sección de Propuestas

**Descripción**: Implementar vista de propuestas con lista paginada, filtros por estado, vista detallada de propuesta individual, diff viewer integrado para revisar cambios, y acciones (aprobar, rechazar, aplicar).

**Criterios de Aceptación**:
- [ ] Lista de propuestas con metadata implementada
- [ ] Filtros por estado funcionan
- [ ] Vista detallada de propuesta individual implementada
- [ ] Diff viewer integrado para revisar cambios funciona
- [ ] Acciones funcionan (aprobar, rechazar, aplicar)

**PENDIENTE**: Metadata de propuestas a mostrar (ver PRD-003 líneas 181), estados de propuestas (líneas 182), integración con diff viewer (líneas 183)

**Dependencias**: T-030, T-031, T-032, T-039, T-040

**Referencias**:
- [frontend-specification.md](../arquitectura/frontend-specification.md): Componente ContextEntriesView (líneas 310-338)
- [requisitos-diff-viewer.md](../../producto/requisitos/requisitos-diff-viewer.md): Requisitos de diff viewer
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Sección de Propuestas (líneas 165-184)

**Estado**: PENDIENTE

---

### T-038: Implementar Sección de Grafo

**Descripción**: Implementar visualización de grafo de relaciones entre documentos y código. Implementar filtros por tipo de relación, navegación interactiva (zoom, pan, selección), metadata de nodos, y resaltado de impacto de cambios.

**Criterios de Aceptación**:
- [ ] Visualización de grafo de relaciones implementada
- [ ] Filtros por tipo de relación funcionan
- [ ] Navegación interactiva (zoom, pan, selección) funciona
- [ ] Metadata de nodos se muestra
- [ ] Resaltado de impacto de cambios funciona

**PENDIENTE**: Librería de visualización de grafos (ver PRD-003 líneas 201), tipos de relaciones a visualizar (líneas 202), metadata de nodos a mostrar (líneas 203)

**Dependencias**: T-030, T-031, T-032, T-040

**Referencias**:
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Sección de Grafo (líneas 185-204)

**Estado**: PENDIENTE

---

### T-039: Implementar Diff Viewer

**Descripción**: Implementar componente de diff viewer para comparación visual de cambios. Mostrar diferencias lado a lado, resaltar adiciones/eliminaciones/modificaciones, permitir navegación por secciones específicas, y entender impacto completo de cambios.

**Criterios de Aceptación**:
- [ ] Diff viewer muestra diferencias lado a lado
- [ ] Adiciones, eliminaciones y modificaciones están resaltadas
- [ ] Navegación por secciones específicas funciona
- [ ] Impacto completo de cambios es entendible
- [ ] Motor de comparación de texto funciona
- [ ] Sincronización de scroll entre paneles funciona

**PENDIENTE**: Motor de comparación de texto específico (ver PRD-003 líneas 220), algoritmo de diff (líneas 221), esquema de colores (líneas 222), sincronización de scroll (líneas 223)

**Dependencias**: T-030

**Referencias**:
- [requisitos-diff-viewer.md](../../producto/requisitos/requisitos-diff-viewer.md): Requisitos funcionales detallados
- [technical-specs-diff-viewer.md](../arquitectura/technical-specs-diff-viewer.md): Especificación técnica
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Diff Viewer (líneas 205-224)

**Estado**: PENDIENTE

---

### T-040: Implementar State Management Global

**Descripción**: Configurar state management global con Zustand. Implementar estado global para user (auth), documents (lista), sessions (activas), loading/error globales. Definir Zustand stores separados por dominio (authStore, documentsStore, sessionsStore). Estado local para componentes específicos (filtros, modales, forms).

**Criterios de Aceptación**:
- [ ] Zustand configurado como state management global
- [ ] Estado global implementado (user, documents, sessions, loading, error)
- [ ] Zustand stores separados por dominio implementados (authStore, documentsStore, sessionsStore)
- [ ] Actions para actualizar estado implementadas
- [ ] Integración con componentes funciona correctamente
- [ ] Performance de state management es aceptable

**Dependencias**: T-030

**Referencias**:
- [frontend-specification.md](../arquitectura/frontend-specification.md): State Management (líneas 340-395)
- [PRD-003](../../producto/requisitos/prd-hito-03-frontend-react.md): Mantenibilidad - estado global (líneas 427-430)

**Estado**: PENDIENTE

---

### T-041: Implementar Testing de Componentes

**Descripción**: Implementar unit tests e integration tests para componentes principales usando Vitest y React Testing Library. Configurar coverage >70%. Implementar tests para servicios de API y state management.

**Criterios de Aceptación**:
- [ ] Vitest y React Testing Library configurados
- [ ] Unit tests para componentes principales implementados
- [ ] Unit tests para servicios de API implementados
- [ ] Unit tests para state management implementados
- [ ] Integration tests con mocks de API implementados
- [ ] Cobertura >70% objetivo inicial

**Dependencias**: T-030, T-033, T-034, T-035, T-036, T-037, T-038, T-039, T-040

**Referencias**:
- [technology-stack.md](../arquitectura/technology-stack.md): Estrategia de testing (líneas 206-213)
- [frontend-specification.md](../arquitectura/frontend-specification.md): Testing (mencionado en línea 52)

**Estado**: PENDIENTE

---

### T-042: Configurar Build y Deployment

**Descripción**: Configurar build de producción con Vite. Configurar optimización de bundle, code splitting, y assets. Configurar deployment local (Docker) y preparación para deployment futuro.

**Criterios de Aceptación**:
- [ ] Build de producción funciona sin errores
- [ ] Bundle optimizado (code splitting, lazy loading)
- [ ] Assets optimizados (imágenes, fonts)
- [ ] Dockerfile para frontend configurado
- [ ] Integración con docker-compose funciona
- [ ] Variables de entorno configuradas

**PENDIENTE**: Estrategia de performance y lazy loading (ver gaps identificados en análisis)

**Dependencias**: T-030, T-033, T-034, T-035, T-036, T-037, T-038, T-039, T-040, T-041

**Referencias**:
- [frontend-specification.md](../arquitectura/frontend-specification.md): Configuración de Vite (líneas 670-689)
- [technology-stack.md](../arquitectura/technology-stack.md): Stack de frontend

**Estado**: PENDIENTE
