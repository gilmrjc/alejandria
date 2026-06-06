---
id: FEAT-009
type: Feature Document
related:
  - target: REQ-011
    relationship_type: implements
    reason: Implementa los requisitos de dashboard general
  - target: TS-004
    relationship_type: references
    reason: Referencia el technical-specs-dashboard-general para especificación técnica detallada
---

# Dashboard General

## Descripción
Vista de alto nivel que unifica el estado del proyecto, mostrando documentos, gaps y métricas clave.

## Propósito
Proporcionar punto de entrada claro para navegar el sistema y visibilidad del progreso general del proyecto.

## User Personas
- CTO/VP Engineering
- Senior Developer/Tech Lead
- Todos los usuarios

## Cómo Funciona
El dashboard muestra resumen de documentos (total, calificación promedio), gaps pendientes por prioridad, propuestas pendientes, y métricas de progreso. Permite navegación rápida a secciones específicas y filtrado por módulo o estado.

## Casos de Uso
- Ver estado general del proyecto
- Navegar a secciones específicas
- Priorizar trabajo basado en gaps pendientes
- Entender progreso de mejoras documentales

## Componentes y Referencias
- Agregación de métricas → NOTA: Definir métricas específicas (ej. % gaps resueltos, documentos healthy, tiempo promedio de resolución)
- Navegación a secciones → NOTA: Definir navegación rápida (cards clickeables, breadcrumbs)
- Filtrado por módulo/estado → NOTA: Definir filtros específicos (por módulo: documentos/gaps/propuestas, por estado: pendiente/en progreso/resuelto)

## Decisiones Relacionadas
- Estrategia de actualización: Polling cada 5 min para MVP, websockets post-MVP (según PRD-003)
- Widgets de métricas: Total documentos, calificación promedio, gaps por prioridad, propuestas pendientes (según PRD-003)
- Layout: Sidebar izquierda (navegación) + header superior (breadcrumbs, user) + content area, grid system y breakpoints según TailwindCSS (según PRD-003)
- Patrones de interacción: Hover y active states para MVP, loading/error states definidos ad-hoc (según PRD-003)
