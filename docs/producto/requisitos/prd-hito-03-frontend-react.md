---
id: PRD-003
type: PRD
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

---

## 3. Componentes del Hito

### 3.1 SPA React

**Descripción:**

Single Page Application implementada con React que sirve como interfaz principal del sistema.

**Requisitos:**

- Frontend debe ser una SPA React
- Debe tener routing configurado
- Debe conectarse a API REST correctamente
- Debe tener manejo de estados global (si aplica)

### 3.2 Dashboard General

**Descripción:**

Vista de alto nivel que unifica el estado del proyecto, mostrando documentos, gaps y métricas clave.

**Requisitos:**

- Dashboard debe mostrar resumen de documentos (total, calificación promedio)
- Dashboard debe mostrar gaps pendientes por prioridad
- Dashboard debe mostrar propuestas pendientes
- Dashboard debe mostrar métricas de progreso
- Debe permitir navegación rápida a secciones específicas
- Debe permitir filtrado por módulo o estado

**Requisitos Pendientes:**

- [PENDIENTE] Definición de métricas de progreso
- [PENDIENTE] Agregación de métricas desde API
- [PENDIENTE] Filtros por módulo/estado
- [PENDIENTE] Links a secciones específicas

### 3.3 Sección de Documentos

**Descripción:**

Vista de documentos del proyecto.

**Requisitos:**

- Debe mostrar lista de documentos con metadata
- Debe permitir filtros por tipo de documento, calificación, fecha
- Debe permitir búsqueda de documentos
- Debe mostrar vista detallada de documento individual
- Debe permitir acciones por documento (ver historial, ver gaps, marcar como healthy)

**Requisitos Pendientes:**

- [PENDIENTE] Metadata de documentos a mostrar
- [PENDIENTE] Tipos de filtros a implementar
- [PENDIENTE] Acciones disponibles por documento

### 3.4 Sección de Preguntas

**Descripción:**

Vista de preguntas (gaps detectados) organizadas por tema.

**Requisitos:**

- Debe mostrar lista de preguntas organizadas por tema/tags
- Debe permitir filtros por prioridad, tipo de gap, estado
- Debe mostrar vista detallada de pregunta individual
- Debe tener interfaz para responder pregunta (campo pre-rellenado)
- Debe permitir acciones (aceptar sugerencia, modificar, rechazar)

**Requisitos Pendientes:**

- [PENDIENTE] Organización de preguntas por tema
- [PENDIENTE] Tipos de filtros a implementar
- [PENDIENTE] Interfaz de respuesta asíncrona

### 3.5 Sección de Gaps

**Descripción:**

Vista de gaps detectados y agrupados.

**Requisitos:**

- Debe mostrar dashboard de gaps detectados con filtros
- Debe mostrar agrupación de gaps por tema
- Debe mostrar metadata de tags (tema, subtema, prioridad)
- Debe mostrar vista de gaps por estado
- Debe tener interfaz de interacción asíncrona para resolución

**Requisitos Pendientes:**

- [PENDIENTE] Dashboard de gaps con filtros
- [PENDIENTE] Interfaz de interacción asíncrona
- [PENDIENTE] Estados de gaps a mostrar

### 3.6 Sección de Propuestas

**Descripción:**

Vista de propuestas de edición generadas.

**Requisitos:**

- Debe mostrar lista de propuestas con metadata
- Debe permitir filtros por estado
- Debe mostrar vista detallada de propuesta individual
- Debe tener diff viewer integrado para revisar cambios
- Debe permitir acciones (aprobar, rechazar, aplicar)

**Requisitos Pendientes:**

- [PENDIENTE] Metadata de propuestas a mostrar
- [PENDIENTE] Estados de propuestas
- [PENDIENTE] Integración con diff viewer

### 3.7 Sección de Grafo

**Descripción:**

Visualización de relaciones entre documentos y código.

**Requisitos:**

- Debe mostrar visualización de grafo de relaciones
- Debe permitir filtros por tipo de relación
- Debe permitir navegación interactiva (zoom, pan, selección)
- Debe mostrar metadata de nodos
- Debe resaltar impacto de cambios

**Requisitos Pendientes:**

- [PENDIENTE] Librería de visualización de grafos
- [PENDIENTE] Tipos de relaciones a visualizar
- [PENDIENTE] Metadata de nodos a mostrar

### 3.8 Diff Viewer

**Descripción:**

Herramienta de comparación visual que muestra cambios propuestos antes de su aplicación.

**Requisitos:**

- Debe mostrar diferencias lado a lado
- Debe resaltar adiciones, eliminaciones y modificaciones
- Debe permitir navegar por secciones específicas
- Debe permitir entender impacto completo de cambios

**Requisitos Pendientes:**

- [PENDIENTE] Motor de comparación de texto
- [PENDIENTE] Algoritmo de diff
- [PENDIENTE] Esquema de colores
- [PENDIENTE] Sincronización de scroll

### 3.9 Interfaz de Sesión Interactiva

**Descripción:**

Interfaz para interacción asíncrona con gaps y propuestas.

**Requisitos:**

- Debe permitir revisar gaps en tiempo propio del usuario
- Debe ser completamente asíncrona (NO sesiones en tiempo real)
- Debe estar mediada por la plataforma

**Requisitos Pendientes:**

- [PENDIENTE] Especificación de interfaz de interacción asíncrona
- [PENDIENTE] Feedback visual de estado
- [PENDIENTE] Indicadores de carga

---

## 4. Requisitos Funcionales

### 4.1 Navegación

**Requisitos Definidos:**

- Dashboard debe permitir navegación rápida a secciones específicas
- Secciones deben ser accesibles via routing

**Requisitos Pendientes:**

- [PENDIENTE] Estructura de routing
- [PENDIENTE] Navegación entre secciones
- [PENDIENTE] Breadcrumbs o indicador de ubicación
- [PENDIENTE] Links directos a recursos específicos

### 4.2 Dashboard

**Requisitos Definidos:**

- Dashboard muestra documentos y gaps
- Dashboard muestra métricas de progreso

**Requisitos Pendientes:**

- [PENDIENTE] Layout del dashboard
- [PENDIENTE] Widgets de métricas
- [PENDIENTE] Actualización en tiempo real vs polling
- [PENDIENTE] Filtros globales

### 4.3 Secciones de Contenido

**Requisitos Definidos:**

- Secciones de Documentos, Preguntas, Gaps, Propuestas, Grafo deben existir
- Cada sección debe tener filtros y búsqueda

**Requisitos Pendientes:**

- [PENDIENTE] Layout consistente entre secciones
- [PENDIENTE] Componentes reutilizables (listas, filtros, cards)
- [PENDIENTE] Estados de carga y error
- [PENDIENTE] Paginación o infinite scroll

### 4.4 Interacción con API

**Requisitos Definidos:**

- Frontend se conecta a API REST correctamente
- Sesiones interactivas funcionan en frontend

**Requisitos Pendientes:**

- [PENDIENTE] Cliente HTTP configurado
- [PENDIENTE] Manejo de errores de API
- [PENDIENTE] Autenticación con API
- [PENDIENTE] Caching de responses

---

## 5. Requisitos No Funcionales

### 5.1 Performance

**Requisitos Pendientes:**

- [PENDIENTE] Tiempo máximo de carga inicial de SPA
- [PENDIENTE] Tiempo máximo de navegación entre secciones
- [PENDIENTE] Tiempo máximo de renderizado de componentes
- [PENDIENTE] Tiempo máximo de respuesta a acciones de usuario

### 5.2 Usabilidad

**Requisitos Definidos:**

- Baja fricción: Usuarios solo interactúan cuando es necesario
- Sistema trabaja proactivamente en el fondo
- Balance entre automatización con control humano

**Requisitos Pendientes:**

- [PENDIENTE] Tiempo de aprendizaje de la interfaz
- [PENDIENTE] Número de clicks para completar tareas comunes
- [PENDIENTE] Feedback visual de estado del sistema
- [PENDIENTE] Consistencia de diseño

### 5.3 Responsividad

**Requisitos Pendientes:**

- [PENDIENTE] Soporte para desktop
- [PENDIENTE] Soporte para tablet
- [PENDIENTE] Soporte para mobile (si aplica para MVP)
- [PENDIENTE] Breakpoints de diseño

### 5.4 Accesibilidad

**Requisitos Pendientes:**

- [PENDIENTE] Compliance WCAG (nivel a definir)
- [PENDIENTE] Soporte para navegación por teclado
- [PENDIENTE] Contraste de colores
- [PENDIENTE] Texto alternativo para imágenes

### 5.5 Mantenibilidad

**Requisitos Pendientes:**

- [PENDIENTE] Arquitectura de componentes
- [PENDIENTE] Estado global (Redux, Context, etc.)
- [PENDIENTE] Estándar de código
- [PENDIENTE] Testing de componentes

---

## 6. Criterios de Aceptación

**Criterios de Completitud (del roadmap):**

- [ ] Frontend se conecta a API REST correctamente
- [ ] Dashboard muestra documentos y gaps
- [ ] Sesiones interactivas funcionan en frontend
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

---

*Documento generado como PRD para el Hito 3: Frontend React.*
