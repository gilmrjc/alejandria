---
id: REQ-011
type: Requirements
rating:
rating-phase:
related:
  - target: FEAT-009
    relationship_type: implements
    reason: Implementa el feature de dashboard general
  - target: STR-003
    relationship_type: implements
    reason: Implementa el roadmap técnico definiendo dashboard en Hito 3
---

# Requisitos: Dashboard General — Alejandria

Este documento define los requisitos para el dashboard general.

---

## Índice

1. [Visión General](#1-visión-general)
2. [Requisitos Funcionales](#2-requisitos-funcionales)
3. [Requisitos No Funcionales](#3-requisitos-no-funcionales)

---

## 1. Visión General

**Propósito:**

Proporcionar punto de entrada claro para navegar el sistema y visibilidad del progreso general del proyecto.

**Contexto:**

Vista de alto nivel que unifica el estado del proyecto, mostrando documentos, gaps y métricas clave.

**Referencias:**

- [FEAT-009](../funcionalidades/dashboard-general.md): Dashboard General
- [STR-003](../../estrategia/estrategia/technical-roadmap.md): Technical Roadmap (Hito 3)

---

## 2. Requisitos Funcionales

### Resumen de Documentos

**Requisitos Definidos:**

- El dashboard debe mostrar resumen de documentos (total, calificación promedio)

**Requisitos Pendientes:**

- [PENDIENTE] Cálculo de calificación promedio de documentos
- [PENDIENTE] Desglose de documentos por estado (healthy, needs improvement)
- [PENDIENTE] Desglose de documentos por tipo
- [PENDIENTE] Lista de documentos recientemente actualizados

### Resumen de Gaps

**Requisitos Definidos:**

- El dashboard debe mostrar gaps pendientes por prioridad

**Requisitos Pendientes:**

- [PENDIENTE] Conteo de gaps por prioridad (alta, media, baja)
- [PENDIENTE] Conteo de gaps por estado (detectado, en sesión, resuelto)
- [PENDIENTE] Lista de gaps de alta prioridad
- [PENDIENTE] Tendencia de gaps resueltos en el tiempo

### Resumen de Propuestas

**Requisitos Definidos:**

- El dashboard debe mostrar propuestas pendientes

**Requisitos Pendientes:**

- [PENDIENTE] Conteo de propuestas por estado (pendiente, aprobada, rechazada)
- [PENDIENTE] Lista de propuestas pendientes
- [PENDIENTE] Tendencia de propuestas aplicadas en el tiempo

### Métricas de Progreso

**Requisitos Definidos:**

- El dashboard debe mostrar métricas de progreso

**Requisitos Pendientes:**

- [PENDIENTE] Definición de métricas de progreso
- [PENDIENTE] Porcentaje de gaps resueltos
- [PENDIENTE] Porcentaje de documentos marcados como healthy
- [PENDIENTE] Tiempo promedio de resolución de gaps

### Navegación

**Requisitos Definidos:**

- El dashboard debe permitir navegación rápida a secciones específicas
- El dashboard debe permitir filtrado por módulo o estado

**Requisitos Pendientes:**

- [PENDIENTE] Links a secciones de documentos, preguntas, gaps, propuestas, grafo
- [PENDIENTE] Filtro por módulo o componente
- [PENDIENTE] Filtro por estado de documento
- [PENDIENTE] Búsqueda dentro del dashboard

---

## 3. Requisitos No Funcionales

### Performance

**Requisitos Pendientes:**

- [PENDIENTE] Tiempo máximo de carga del dashboard
- [PENDIENTE] Tiempo máximo de actualización de métricas
- [PENDIENTE] Tiempo máximo de aplicación de filtros

### Usabilidad

**Requisitos Pendientes:**

- [PENDIENTE] Claridad de presentación de métricas
- [PENDIENTE] Facilidad de navegación a secciones
- [PENDIENTE] Intuitividad de filtros
- [PENDIENTE] Responsividad (mobile, tablet, desktop)

### Actualización

**Requisitos Pendientes:**

- [PENDIENTE] Frecuencia de actualización de métricas
- [PENDIENTE] Estrategia de actualización en tiempo real vs polling
- [PENDIENTE] Notificaciones de cambios significativos

---

## Referencias

- [FEAT-009](../funcionalidades/dashboard-general.md): Dashboard General
- [STR-003](../../estrategia/estrategia/technical-roadmap.md): Technical Roadmap (Hito 3)
- [REQ-001](requisitos-funcionales.md): Requisitos Funcionales

---

*Documento generado como especificación de requisitos para el dashboard general.*
