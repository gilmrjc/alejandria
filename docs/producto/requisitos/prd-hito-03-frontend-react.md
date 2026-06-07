---
id: PRD-003
type: PRD
rating: 9
rating-phase: document-editing
related-roadmap: STR-003
related-milestone: Hito 3
related:
  - target: STR-003
    relationship_type: implements
    reason: Implementa el roadmap técnico definiendo el Hito 3 de frontend React
  - target: STR-001
    relationship_type: implements
    reason: Implementa la visión y misión con interfaz de usuario
---

# PRD: Hito 3 - Frontend React — Alejandria

Este documento define los requisitos del producto para el Hito 3: Frontend React del MVP Bootstrapped.

---

## Índice

1. [Visión General](#1-visión-general)
2. [Objetivo del Hito](#2-objetivo-del-hito)
3. [Componentes del Hito](#3-componentes-del-hito)
4. [Requisitos Funcionales](#4-requisitos-funcionales)
5. [Requisitos No Funcionales](#5-requisitos-no-funcionales)
6. [Criterios de Aceptación](#6-criterios-de-aceptación)
7. [Dependencias](#7-dependencias)

---

## 1. Visión General

**Propósito:**

Implementar el frontend React que servirá como interfaz de usuario principal del sistema, permitiendo a los usuarios interactuar con todas las funcionalidades del sistema.

**Contexto:**

Este hito establece la capa de presentación del sistema. El frontend React se conecta a la API REST del Hito 2 y proporciona las vistas principales: Dashboard, Documentos, Preguntas, Gaps, Propuestas y Grafo.

**Casos de Usuario:**

Los workflows típicos habilitados por el frontend React son: (1) Revisar estado del proyecto via Dashboard con métricas agregadas, (2) Navegar documentos via Sección de Documentos con filtros y búsqueda, (3) Revisar gaps detectados via Sección de Gaps con agrupación por tema, (4) Revisar y aprobar cambios via Sección de Propuestas con diff viewer integrado, (5) Navegación rápida desde Dashboard a secciones específicas. Los problemas del usuario resueltos son: falta de interfaz visual, dificultad para navegar documentos, proceso manual de revisión de cambios, y falta de visibilidad de progreso.

**Referencias:**

- [STR-003](../../estrategia/estrategia/technical-roadmap.md): Technical Roadmap (Hito 3)

---

## 2. Objetivo del Hito

**Objetivo Principal:**

Implementar frontend React para interfaz de usuario, estableciendo:

- SPA React con componentes principales
- Dashboard de documentos y gaps
- Interfaz de interacción asíncrona
- Diff viewer integrado

**Valor:**

Proporcionar una interfaz de usuario funcional que permita dogfooting temprano y validación de UX desde el inicio del ciclo, mientras se construye el core del sistema en hitos posteriores.

**Nota:** Este hito se movió desde la posición original del Hito 6 para facilitar dogfooting y validación temprana de UX desde el inicio del ciclo.

**Métricas de Éxito:**

Para MVP Bootstrapped, el enfoque es funcionalidad básica sobre métricas cuantitativas. El dogfooting temprano se validará cualitativamente mediante feedback en retrospectivas de desarrollo. Métricas de éxito formales (adopción, satisfacción, KPIs) se definirán post-MVP cuando se valide problem-solution fit, similar al patrón establecido en PRD-002.

**Métricas Cualitativas de Validación:**

Las métricas cualitativas específicas para evaluar la validación durante dogfooting incluyen: tiempo promedio para encontrar información (medido en segundos/minutos), satisfacción subjetiva del fundador (escala 1-10), y fricciones percibidas (categorizadas por tipo y frecuencia). La reducción de fricción en documentación se mide mediante comparación de baseline vs tiempo actual para tareas específicas (ej. encontrar un documento, revisar gaps, aprobar una propuesta). Los umbrales de éxito para determinar que el sistema entrega valor tangible son: satisfacción ≥ 7/10 y reducción de fricciones ≥ 30% en un período de 3 meses.

**Estrategia de Dogfooting:**

La validación se enfoca en dogfooding interno intensivo por el fundador durante los primeros 6 meses: uso intensivo interno en workflow diario para identificar fricciones reales, identificación de gaps reales en documentación del proyecto que el sistema detecte, refinamiento de flujo de trabajo de interacción humano-agente basado en experiencia práctica, y validación de reducción de fricción en documentación para confirmar que el sistema entrega valor tangible. Para detalles del proceso de dogfooding y criterios de validación, ver STR-001 y POL-001.

**Mecanismo de Feedback Loop:**

El feedback del dogfooting se recopila mediante una combinación de retrospectivas semanales estructuradas y notas de desarrollo ad-hoc en un documento compartido. La priorización del feedback recibido se realiza mediante categorías predefinidas: blocker (bloquea workflow principal), friction (dificultad significativa pero no bloqueante), nice-to-have (mejora deseable), y technical debt (deuda técnica identificada). La incorporación de cambios al roadmap basados en findings de dogfooting se realiza mediante decisiones ad-hoc cuando se identifica un blocker crítico, mientras que feedback de menor prioridad se documenta para evaluación en retrospectivas posteriores.

---

## 3. Componentes del Hito

**Nota sobre Requisitos Pendientes:** Los requisitos marcados como [PENDIENTE] en esta sección siguen el patrón establecido en PRDs anteriores (PRD-001, PRD-002). Los requisitos funcionales de componentes se definen con nivel de detalle específico en este PRD. Los requisitos no funcionales se definen con valores concretos. Los detalles técnicos de implementación (librerías específicas, algoritmos, configuraciones) se delegan a las tareas técnicas de EPC-003, similar a cómo PRD-001 y PRD-002 referencian TRDs para detalles técnicos. La matriz de trazabilidad vincula cada requisito pendiente con la tarea técnica correspondiente (T-030 a T-042).

**Priorización de Implementación:**

Los componentes MVP esenciales para dogfooting son: (1) Estructura base (T-030), (2) Routing y navegación (T-031), (3) Cliente HTTP y autenticación (T-032), (4) State management global (T-040), (5) Dashboard General (T-033), (6) Sección de Documentos (T-034), (7) Sección de Gaps (T-036), (8) Sección de Propuestas (T-037), (9) Diff Viewer (T-039). Los componentes que pueden postponerse son: Sección de Grafo (T-038, nice-to-have para dogfooting inicial), Sección de Preguntas (T-035, depende de backend de Hito 4), e Interfaz de Sesión Interactiva (marcada como POST-MVP en este PRD). El orden de implementación sigue 5 fases: infraestructura base → configuración core → componentes principales → componentes avanzados → testing y deployment. Para detalles del orden específico, ver EPC-003.

**Relaciones entre Componentes:**

El flujo lógico sigue 5 fases: (1) Infraestructura base (T-030), (2) Configuración core (T-031, T-032, T-040), (3) Componentes principales (T-033, T-034, T-035), (4) Componentes avanzados (T-036, T-037, T-038, T-039), (5) Testing y deployment (T-041, T-042). Las dependencias secuenciales son: T-030 (estructura base) es prerequisito fundamental para todas las demás tareas. T-031 (routing), T-032 (cliente HTTP) y T-040 (state management) son prerequisitos para T-033 a T-038. T-039 (diff viewer) es prerequisito específico para T-037. La paralelización es posible en varias fases: T-033, T-034 y T-035 pueden ejecutarse en paralelo después de completar la infraestructura base. T-036, T-037 y T-038 pueden ejecutarse en paralelo después de la misma base. Para diagramas de arquitectura, ver ARC-001 (technical-brief.md) y ARC-011 (architecture-overview.md).

**Glosario de Términos Técnicos:**

- **SPA (Single Page Application):** Aplicación web que carga una sola página HTML y actualiza dinámicamente el contenido a medida que el usuario interactúa, sin recargar la página completa.
- **Diff Viewer:** Herramienta de comparación visual que muestra cambios propuestos antes de su aplicación, permitiendo entender el impacto completo de cambios.
- **State Management Global:** Configuración de React Context API o Zustand para manejar estado global de la aplicación (user, documents, sessions, loading, error).
- **Interfaz de Sesión Interactiva:** Marcada como POST-MVP en este PRD, se implementará en Hito 5 según STR-003. Permite interacción en tiempo real con gaps y propuestas.

### 3.1 SPA React

**Descripción:**

Single Page Application implementada con React que sirve como interfaz principal del sistema.

**Requisitos:**

- Frontend debe ser una SPA React
- Debe tener routing configurado
- Debe conectarse a API REST correctamente
- Debe tener manejo de estados global (si aplica)

### 3.2 Dashboard General

**Descripción (No Técnica):**

Vista de alto nivel que unifica el estado del proyecto, mostrando documentos, gaps y métricas clave para entender rápidamente el progreso del sistema.

**Descripción Técnica:**

Vista de alto nivel que unifica el estado del proyecto, mostrando documentos, gaps y métricas clave.

**Requisitos:**

- Dashboard debe mostrar resumen de documentos (total, calificación promedio)
- Dashboard debe mostrar gaps pendientes por prioridad
- Dashboard debe mostrar propuestas pendientes
- Dashboard debe mostrar métricas de progreso
- Debe permitir navegación rápida a secciones específicas
- Debe permitir filtrado por módulo o estado

**Requisitos Pendientes:**

- [PENDIENTE] Definición de métricas de progreso - NOTA: Definir métricas específicas (ej. % gaps resueltos, documentos healthy, tiempo promedio de resolución)
- [PENDIENTE] Agregación de métricas desde API - NOTA: Definir estrategia de polling (ej. cada 5 min) vs websockets
- [PENDIENTE] Filtros por módulo/estado - NOTA: Definir filtros específicos (por módulo: documentos/gaps/propuestas, por estado: pendiente/en progreso/resuelto)
- [PENDIENTE] Links a secciones específicas - NOTA: Definir navegación rápida (cards clickeables, breadcrumbs)

### 3.3 Sección de Documentos

**Descripción (No Técnica):**

Vista estructurada de todo el conocimiento técnico del proyecto organizada jerárquicamente como sistema de archivos, permitiendo navegación eficiente y búsqueda por intención.

**Descripción Técnica:**

Vista de documentos del proyecto.

**Requisitos:**

- Debe mostrar lista de documentos con metadata
- Debe permitir filtros por tipo de documento, calificación, fecha
- Debe permitir búsqueda de documentos
- Debe mostrar vista detallada de documento individual
- Debe permitir acciones por documento (ver historial, ver gaps, marcar como healthy)

**Requisitos Pendientes:**

- [PENDIENTE] Metadata de documentos a mostrar - NOTA: Definir campos (título, tipo, calificación, fecha última actualización, estado healthy/unhealthy, tags)
- [PENDIENTE] Tipos de filtros a implementar - NOTA: Definir filtros (por tipo: PRD/TRD/ADR, por calificación: >7/5-7/<5, por fecha: última semana/mes/año)
- [PENDIENTE] Acciones disponibles por documento - NOTA: Definir acciones (ver historial de versiones, ver gaps asociados, marcar como healthy, ver diff viewer)

### 3.4 Sección de Preguntas

**Descripción (No Técnica):**

Mecanismo donde el sistema captura conocimiento técnico inicial mediante preguntas generadas automáticamente, permitiendo transformar respuestas en vectores para búsqueda semántica.

**Descripción Técnica:**

Vista de preguntas (gaps detectados) organizadas por tema.

**Requisitos:**

- Debe mostrar lista de preguntas organizadas por tema/tags
- Debe permitir filtros por prioridad, tipo de gap, estado
- Debe mostrar vista detallada de pregunta individual
- Debe tener interfaz para responder pregunta (campo pre-rellenado)
- Debe permitir acciones (aceptar sugerencia, modificar, rechazar)

**Requisitos Pendientes:**

- [PENDIENTE] Organización de preguntas por tema - NOTA: Definir agrupación (por tags: negocio/arquitectura/seguridad, por prioridad: crítico/alto/medio/bajo)
- [PENDIENTE] Tipos de filtros a implementar - NOTA: Definir filtros (por prioridad, por estado: pendiente/respondido, por tipo de gap)
- [PENDIENTE] Interfaz de respuesta asíncrona - NOTA: Definir patrón de UX (campo de texto pre-rellenado, botones: aceptar/modificar/rechazar, feedback visual de estado)

### 3.5 Sección de Gaps

**Descripción (No Técnica):**

Interfaz para la Fase 3 de Resolución donde los usuarios responden manualmente gaps de contexto detectados, con tarjetas con caja de respuesta pre-rellenada con sugerencias del agente LLM para facilitar resolución eficiente.

**Descripción Técnica:**

Vista de gaps detectados y agrupados.

**Requisitos:**

- Debe mostrar dashboard de gaps detectados con filtros
- Debe mostrar agrupación de gaps por tema
- Debe mostrar metadata de tags (tema, subtema, prioridad)
- Debe mostrar vista de gaps por estado
- Debe tener interfaz de interacción asíncrona para resolución

**Requisitos Pendientes:**

- [PENDIENTE] Dashboard de gaps con filtros - NOTA: Definir filtros (por tema, por prioridad, por estado: pendiente/en progreso/resuelto)
- [PENDIENTE] Interfaz de interacción asíncrona - NOTA: Definir patrón de UX (similar a sección de preguntas, campo de respuesta, acciones)
- [PENDIENTE] Estados de gaps a mostrar - NOTA: Definir estados (pendiente, en progreso, resuelto, no aplica, obsoleto)

### 3.6 Sección de Propuestas

**Descripción (No Técnica):**

Interfaz para la Fase 5 de Aplicación donde el sistema presenta sugerencias de edición derivadas de gaps resueltos, transformando contexto capturado en acciones concretas.

**Descripción Técnica:**

Vista de propuestas de edición generadas.

**Requisitos:**

- Debe mostrar lista de propuestas con metadata
- Debe permitir filtros por estado
- Debe mostrar vista detallada de propuesta individual
- Debe tener diff viewer integrado para revisar cambios
- Debe permitir acciones (aprobar, rechazar, aplicar)

**Requisitos Pendientes:**

- [PENDIENTE] Metadata de propuestas a mostrar - NOTA: Definir campos (título, fecha creación, estado, documento asociado, impacto estimado)
- [PENDIENTE] Estados de propuestas - NOTA: Definir estados (pendiente, aprobada, rechazada, aplicada)
- [PENDIENTE] Integración con diff viewer - NOTA: Definir integración (modal con diff viewer lado a lado, botones: aprobar/rechazar/aplicar)

### 3.7 Sección de Grafo

**Descripción (No Técnica):**

Visualización gráfica de relaciones entre documentos, gaps y respuestas para permitir comprensión intuitiva de la estructura del conocimiento y entender impacto de cambios.

**Descripción Técnica:**

Visualización de relaciones entre documentos y código.

**Requisitos:**

- Debe mostrar visualización de grafo de relaciones
- Debe permitir filtros por tipo de relación
- Debe permitir navegación interactiva (zoom, pan, selección)
- Debe mostrar metadata de nodos
- Debe resaltar impacto de cambios

**Requisitos Pendientes:**

- [PENDIENTE] Librería de visualización de grafos - NOTA: Evaluar opciones (react-flow, vis-network, d3.js) - decisión en fase de implementación
- [PENDIENTE] Tipos de relaciones a visualizar - NOTA: Definir relaciones (referencia, implementa, depende, relacionado)
- [PENDIENTE] Metadata de nodos a mostrar - NOTA: Definir metadata (tipo de documento, calificación, estado, tags)

### 3.8 Diff Viewer

**Descripción:**

Herramienta de comparación visual que muestra cambios propuestos antes de su aplicación.

**Requisitos:**

- Debe mostrar diferencias lado a lado
- Debe resaltar adiciones, eliminaciones y modificaciones
- Debe permitir navegar por secciones específicas
- Debe permitir entender impacto completo de cambios

**Requisitos Pendientes:**

- [PENDIENTE] Motor de comparación de texto - NOTA: Evaluar librerías (react-diff-viewer, monaco-editor, diff2html) - decisión en fase de implementación
- [PENDIENTE] Algoritmo de diff - NOTA: Definir algoritmo (Myers diff algorithm es estándar) - decisión en fase de implementación
- [PENDIENTE] Esquema de colores - NOTA: Definir colores (adiciones: verde, eliminaciones: rojo, modificaciones: amarillo)
- [PENDIENTE] Sincronización de scroll - NOTA: Definir sincronización entre paneles (scroll simultáneo en ambos lados)

### 3.9 Interfaz de Sesión Interactiva

**Descripción:**

Interfaz para interacción asíncrona con gaps y propuestas.

**Requisitos:**

- Debe permitir revisar gaps en tiempo propio del usuario
- Debe ser completamente asíncrona (NO sesiones en tiempo real)
- Debe estar mediada por la plataforma

**Requisitos Pendientes:**

- [NO APLICA] Especificación de interfaz de interacción asíncrona - POST-MVP: La interfaz de sesión interactiva está fuera del alcance del Hito 3. Se implementará en hitos posteriores (Hito 5: Implementación de Fase Resolución y Verificación).
- [NO APLICA] Feedback visual de estado - POST-MVP: Parte de la interfaz de sesión interactiva, fuera del alcance del Hito 3.
- [NO APLICA] Indicadores de carga - POST-MVP: Parte de la interfaz de sesión interactiva, fuera del alcance del Hito 3.

---

## 4. Requisitos Funcionales

### 4.1 Navegación

**Requisitos Definidos:**

- Dashboard debe permitir navegación rápida a secciones específicas
- Secciones deben ser accesibles via routing

**Requisitos Pendientes:**

- [PENDIENTE] Estructura de routing - NOTA: Definir rutas (/dashboard, /documents, /questions, /gaps, /proposals, /graph)
- [PENDIENTE] Navegación entre secciones - NOTA: Definir navegación (sidebar o navbar, links a secciones)
- [PENDIENTE] Breadcrumbs o indicador de ubicación - NOTA: Definir breadcrumbs (Dashboard > Documentos > PRD-003)
- [PENDIENTE] Links directos a recursos específicos - NOTA: Definir deep linking (/documents/prd-003, /gaps/gap-123)

### 4.2 Dashboard

**Requisitos Definidos:**

- Dashboard muestra documentos y gaps
- Dashboard muestra métricas de progreso

**Requisitos Pendientes:**

- [PENDIENTE] Layout del dashboard - NOTA: Definir layout (grid de cards, widgets de métricas, lista de gaps pendientes)
- [PENDIENTE] Widgets de métricas - NOTA: Definir widgets (total documentos, calificación promedio, gaps por prioridad, propuestas pendientes)
- [PENDIENTE] Actualización en tiempo real vs polling - NOTA: Definir estrategia (polling cada 5 min para MVP, websockets post-MVP)
- [PENDIENTE] Filtros globales - NOTA: Definir filtros (por módulo, por estado, por fecha)

### 4.3 Secciones de Contenido

**Requisitos Definidos:**

- Secciones de Documentos, Preguntas, Gaps, Propuestas, Grafo deben existir
- Cada sección debe tener filtros y búsqueda

**Requisitos Pendientes:**

- [PENDIENTE] Layout consistente entre secciones - NOTA: Definir layout estándar (header, sidebar, content area, footer)
- [PENDIENTE] Componentes reutilizables (listas, filtros, cards) - NOTA: Definir componentes (DataTable, FilterBar, Card, Button, Input)
- [PENDIENTE] Estados de carga y error - NOTA: Definir estados (loading spinner, error message con retry, empty state)
- [PENDIENTE] Paginación o infinite scroll - NOTA: Definir estrategia (paginación para MVP: 20 items por página)

**Especificación de Layout:**

El layout estándar para todas las secciones consiste en: sidebar izquierda (navegación principal entre secciones), header superior (breadcrumbs, información de usuario), y content area (contenido específico de cada sección). El grid system y breakpoints se definen según TailwindCSS (desktop >1024px, tablet 768-1024px, mobile <768px). Los patrones de interacción visual incluyen hover y active states para MVP, mientras que loading y error states se definen ad-hoc según las necesidades de cada componente. Nota: no se incluyen wireframes específicos para MVP, solo especificación estructural del layout.

### 4.4 Interacción con API

**Requisitos Definidos:**

- Frontend se conecta a API REST correctamente
- Sesiones interactivas funcionan en frontend

**Requisitos Pendientes:**

- [PENDIENTE] Cliente HTTP configurado - NOTA: Usar Axios con interceptors (similar a EPC-003 T-032)
- [PENDIENTE] Manejo de errores de API - NOTA: Definir manejo (401: redirigir a login, 500: mostrar error genérico, 404: mostrar not found)
- [PENDIENTE] Autenticación con API - NOTA: Usar JWT Bearer Token (similar a EPC-003 T-032)
- [PENDIENTE] Caching de responses - NOTA: Definir estrategia (cache simple en memoria para datos frecuentes, 5 min TTL)

**Estrategia de Versioning de API:**

El frontend manejará cambios en la API REST del backend mediante versioning URL-based (/api/v1/, /api/v2/), el cual ya está implementado actualmente en el API. El contrato de estabilidad entre frontend y backend se mantiene mediante acuerdo informal por ahora, con evolución hacia un contrato formal post-MVP. La comunicación de cambios de API entre backend y frontend se realiza mediante PR reviews obligatorios para cualquier cambio que afecte endpoints utilizados por el frontend, asegurando que los desarrolladores de frontend sean notificados de breaking changes antes de su implementación.

---

## 5. Requisitos No Funcionales

**Nota sobre Requisitos Técnicos Pendientes:** Los requisitos técnicos pendientes en esta sección se delegan a las tareas técnicas de EPC-003, similar a cómo PRD-001/PRD-002 referencian TRDs para detalles técnicos. La matriz de trazabilidad vincula cada requisito pendiente con la tarea técnica correspondiente (T-030 a T-042). Los requisitos se definirán durante la implementación de cada tarea por el desarrollador responsable.

### 5.1 Performance

**Requisitos:**

- Tiempo máximo de carga inicial de SPA: < 3 segundos (en desarrollo local)
- Tiempo máximo de navegación entre secciones: < 500ms
- Tiempo máximo de renderizado de componentes: < 100ms
- Tiempo máximo de respuesta a acciones de usuario: < 200ms
- **NOTA**: Para MVP Bootstrapped, el enfoque es funcionalidad básica sobre optimización prematura. Performance específica se medirá post-MVP cuando se valide problem-solution fit.

### 5.2 Usabilidad

**Requisitos Definidos:**

- Baja fricción: Usuarios solo interactúan cuando es necesario
- Sistema trabaja proactivamente en el fondo
- Balance entre automatización con control humano

**Requisitos:**

- Tiempo de aprendizaje de la interfaz: < 30 minutos para desarrollador familiarizado con el stack
- Número de clicks para completar tareas comunes: < 3 clicks para acciones frecuentes (ver documento, ver gaps)
- Feedback visual de estado del sistema: Indicadores de carga (spinners), mensajes de error claros, confirmaciones de acciones
- Consistencia de diseño: Componentes reutilizables, paleta de colores consistente, patrones de UX uniformes
- **NOTA**: Usabilidad específica se validará mediante dogfooting durante MVP. Métricas cuantitativas post-MVP.

**Sistema de Diseño y Biblioteca de Componentes:**

La biblioteca de componentes UI seleccionada es shadcn/ui (componentes copiados al proyecto, full control, moderno, integración con TailwindCSS). Los tokens de diseño incluyen: paleta de colores, tipografía, y espaciado (scale de 4px). El enfoque de consistencia visual se basa en convenciones de código sin herramientas adicionales para MVP. Para patrones de componentes específicos, referenciar documentación de shadcn/ui.

### 5.3 Responsividad

**Requisitos:**

- Soporte para desktop: > 1024px (prioridad para MVP)
- Soporte para tablet: 768px - 1024px (nice-to-have para MVP)
- Soporte para mobile: < 768px (NO APLICA para MVP Bootstrapped - POST-MVP)
- Breakpoints de diseño: desktop (>1024px), tablet (768-1024px), mobile (<768px)
- **NOTA**: Para MVP Bootstrapped, el foco es desktop para desarrollo local. Responsividad completa se implementará post-MVP.

### 5.4 Accesibilidad

**Requisitos:**

- Compliance WCAG: Nivel AA (objetivo para MVP Bootstrapped)
- Soporte para navegación por teclado: Tab navigation entre elementos interactivos
- Contraste de colores: Mínimo 4.5:1 para texto normal, 3:1 para texto grande (WCAG AA)
- Texto alternativo para imágenes: Alt text descriptivo para imágenes informativas
- **NOTA**: Accesibilidad completa se validará post-MVP. Para MVP, seguir mejores prácticas básicas.

### 5.5 Mantenibilidad

**Requisitos:**

- Arquitectura de componentes: Estructura de carpetas organizada (components/, pages/, hooks/, utils/, services/)
- Estado global: Zustand para MVP (justificado por investigación: ideal para startups/MVPs, overhead mínimo, optimización automática de performance, bundle size ~1KB)
- Estado global específico: user (auth), documents (lista), sessions (activas), loading/error globales
- Estado local: componentes específicos (filtros, modales, forms)
- Patrones de state management: Zustand stores separados por dominio (authStore, documentsStore, sessionsStore)
- Estándar de código: ESLint configurado, Prettier para formatting, convenciones de nombres consistentes
- Testing de componentes: Cobertura objetivo >70% (similar a PRD-002), unit tests con Vitest + React Testing Library
- **NOTA**: Testing básico para MVP, testing completo post-MVP.

---

## 6. Criterios de Aceptación

**Criterios de Completitud (del roadmap):**

- [ ] Frontend se conecta a API REST correctamente
- [ ] Dashboard muestra documentos y gaps
- [ ] **NO APLICA**: Sesiones interactivas funcionan en frontend - POST-MVP (Hito 5)
- [ ] Diff viewer muestra cambios correctamente

**Criterios Adicionales:**

- [ ] Todas las secciones (Documentos, Preguntas, Gaps, Propuestas, Grafo) son accesibles
- [ ] Navegación entre secciones funciona correctamente
- [ ] Filtros y búsqueda funcionan en todas las secciones
- [ ] Interfaz es responsiva en desktop
- [ ] Manejo de errores de API es claro para el usuario
- [ ] Estados de carga son visibles durante operaciones asíncronas

---

## 7. Dependencias

**Dependencias Externas:**

- API REST del Hito 2 debe estar funcionando
- React y dependencias de frontend deben estar instaladas

**Dependencias Internas:**

- Hito 1: Infraestructura Base (para desarrollo local)
- Hito 2: API REST y MCP Server (endpoints de backend)

**Hitos Posteriores que Dependen de Este Hito:**

- Hito 4: Implementación de Fases Detección y Agrupación (frontend de gaps)
- Hito 5: Implementación de Fases Resolución y Verificación (frontend de resolución)
- Hito 6: Implementación de Fase Aplicación (frontend de propuestas)

**Nota:** Hito 3 y Hito 4 pueden desarrollarse en paralelo después de Hito 2, permitiendo dogfooting temprano de UX mientras se construye el core del sistema.

---

## Referencias

- [STR-003](../../estrategia/estrategia/technical-roadmap.md): Technical Roadmap (Hito 3)
- [FEAT-009](../funcionalidades/dashboard-general.md): Dashboard General
- [FEAT-008](../funcionalidades/diff-viewer.md): Diff Viewer
- [FEAT-004](../funcionalidades/seccion-grafo.md): Sección de Grafo
- [Sección de Documentos](../funcionalidades/seccion-documentos.md)
- [Sección de Preguntas](../funcionalidades/seccion-preguntas.md)
- [Sección de Gaps](../funcionalidades/seccion-gaps.md)
- [Sección de Propuestas](../funcionalidades/seccion-propuestas.md)
