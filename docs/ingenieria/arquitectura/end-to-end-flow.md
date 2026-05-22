---
id: ARC-002
type: Flow
rating:
rating-phase:
related:
  - target: ARC-001
    relationship_type: depends_on
    reason: Depende del technical brief para contexto de arquitectura general
  - target: ADR-002
    relationship_type: implements
    reason: Implementa la arquitectura de 5 fases descrita en ADR-002
  - target: ADR-004
    relationship_type: references
    reason: Referencia la estrategia de jobs efímeros para manejo de jobs del pipeline
  - target: ADR-005
    relationship_type: references
    reason: Referencia la idempotencia de jobs para manejo de locks y reintentos
---

# End-to-End Flow — Alejandria

Flujo completo del sistema desde la creación de un documento hasta su actualización.

---

## Flujo principal

```text
1. Usuario crea documento vía frontend o MCP
   → API crea documento con healthy: false, rating: 0
   → API encola job gap_detection (Fase 1: Detección)

2. gap_detection corre en background (Fase 1: Detección)
   → Sistema revisa campo de calificación del documento
   → Si rating >= 9: no se procesa (documento suficientemente completo)
   → Si rating < 9: Agente LLM analiza documento buscando gaps contextuales
   → Genera gaps específicos y accionables con estado: pending
   → Gaps se almacenan en base de datos
   → API encola job gap_grouping (Fase 2: Agrupación)

3. gap_grouping corre en background (Fase 2: Agrupación)
   → Sistema agrupa gaps por similitud semántica
   → Agrupación multidimensional: tema, impacto, audiencia, módulo, temporalidad
   → Gaps organizados visualmente en interfaz para navegación eficiente
   → Usuario notificado: "Gaps listos para resolver"
   → Espera interacción asíncrona del usuario (Fase 3: Resolución)

4. Usuario revisa gaps en su propio tiempo (Fase 3: Resolución)
   → Usuario navega a sección de Gaps en interfaz
   → Cada gap presentado con caja de respuesta pre-rellenada (sugerencia de agente)
   → Usuario tiene 3 opciones:
     * Aceptar sugerencia tal como está → gap estado: responded
     * Modificar sugerencia → gap estado: responded
     * Rechazar con motivo (obsoleto, no aplica, no es gap) → gap estado: rejected
   → Interacción completamente asíncrona, mediada por plataforma
   → No hay sesión interactiva en tiempo real con agente

5. Cron job corre cada 30 minutos (Fase 4: Plan de Acción)
   → Sistema verifica gaps resueltos en últimos 30 minutos
   → Si no hubo gaps resueltos: no se ejecuta (ejecución condicional)
   → Si hubo gaps resueltos: Agente LLM genera propuestas de edición
   → Propuestas incluyen: nombre descriptivo, archivos a editar, referencias a gaps, texto detallado
   → Propuestas disponibles en sección de Propuestas de interfaz
   → Usuario puede revisar, aceptar o rechazar propuestas

6. Usuario aprueba propuesta
   → Usuario navega a sección de Propuestas
   → Revisa propuesta con diff viewer integrado
   → Puede editar propuesta antes de aprobar (botón "validar" en lugar de "aceptar")
   → Al aprobar: API encola job suggestion_application (Fase 5: Aplicación)

7. suggestion_application corre en background (Fase 5: Aplicación)
   → Trabajo de cola implementa propuestas aceptadas
   → Aplica ediciones sugeridas a documentos correspondientes
   → Documento actualizado con nuevo contexto
   → Documento marcado con healthy: true, rating actualizado
   → Historial de versiones mantenido con snapshot previo

8. Ciclo continuo
   → Cuando documento se edita manualmente: sistema re-ejecuta gap_detection
   → Ciclo se reinicia: detección → agrupación → resolución → plan de acción → aplicación
   → Asegura mantenimiento continuo de calidad de documentación
```

---

## Análisis de Crítica de Documentación

### Estado del Análisis

- Análisis previo: SÍ (versión 1, fecha 2026-05-20)
- Fecha del análisis actual: 2026-05-22
- Versión del análisis: 2
- Gaps pendientes previos: 4
- Gaps respondidos en este análisis: 1
- Gaps pendientes actualizados: 3
- Nuevos gaps identificados: 4
- Total gaps pendientes: 7

### Clasificación del Documento

- Tipo: Documento de Arquitectura (Flow)
- Rol Principal: Arquitecto
- Roles a Revisar: Arquitecto + Desarrollador + DevOps/SRE
- Enfoque: Validación de flujo end-to-end del sistema
- Perspectiva: Senior + Junior
- Fecha de análisis: 2026-05-22
- Versión del análisis: 2

### Calificación del Documento: 7.2/10

**Desglose**:

- Completitud de Respuestas: 7/10 - El flujo principal está bien definido con transiciones de estado claras. Se respondió 1 gap previo (justificación de arquitectura de 5 fases) mediante ADR-002. Faltan respuestas a preguntas de implementación (manejo de fallos, timeouts, rollback) y operaciones.
- Contexto Multi-Rol: 6/10 - Contexto razonable para arquitectos (senior) a través de referencias. Contexto limitado para desarrolladores junior (falta explicación de cómo funciona cada agente) y DevOps (falta estrategia de operaciones).
- Calidad de Referencias: 8/10 - Buena referencia a ADR-002 que responde gap sobre arquitectura de 5 fases. Faltan referencias a documentos de diseño-decisions para detalles de implementación.
- Estructura y Organización: 9/10 - Estructura clara y apropiada para un documento de flujo. Buen uso de diagrama de flujo textual y secciones temáticas.
- Consistencia: 9/10 - Sin contradicciones detectadas. Alineación consistente con ADR-002 y technology-strategy.

### Resumen

El documento proporciona un flujo end-to-end claro con transiciones de estado bien definidas. Se validó y respondió un gap previo mediante ADR-002. Faltan respuestas a preguntas de implementación técnica (manejo de fallos, timeouts, rollback) y operaciones (estrategia de retry, alerting).

---

## Gaps Identificados

### Gaps Previos Actualizados

**GAP: Justificación de la arquitectura de 5 fases** [PRIORIDAD: Alta] [ESTADO: RESPONDIDO]

- **Pregunta**: ¿Por qué se eligió este flujo específico (detección → agrupación → resolución → verificación → aplicación)?
- **Respuesta encontrada**: ADR-002 justifica cada fase del flujo: Agrupación es necesaria para eficiencia cognitiva, Verificación previene propagación de errores, Ciclo iterativo permite mejoras progresivas. Alternativas consideradas (3 fases, sin verificación, sin agrupación) fueron rechazadas por comprometer calidad o eficiencia.
- **Rol afectado**: Arquitecto
- **Referencia**: `/Users/gil/projects/alejandria/docs/ingenieria/decisiones/adr-002-5-phase-architecture.md`
- **Fecha de respuesta**: 2026-05-22

**GAP: Ciclo de verificación detallado** [PRIORIDAD: Media] [ESTADO: PENDIENTE]

- **Pregunta**: ¿Cómo funciona en detalle el ciclo de verificación?
- **Contexto faltante**: No hay explicación de cómo el Agente 1 determina si hay nuevos gaps, ejemplo de un ciclo que genera nuevas preguntas, límites máximos de rounds para evitar loops infinitos
- **Rol afectado**: Arquitecto Junior, Desarrollador Junior
- **Referencia**: No disponible
- **Fecha de identificación**: 2026-05-20

**GAP: Integración de context_entries en aplicación** [PRIORIDAD: Media] [ESTADO: PENDIENTE]

- **Pregunta**: ¿Cómo el Agente 4 usa los context_entries para aplicar cambios?
- **Contexto faltante**: No hay ejemplo de cómo se mapean context_entries a ediciones específicas, estrategia para conflictos cuando múltiples context_entries sugieren cambios contradictorios
- **Rol afectado**: Arquitecto Junior, Desarrollador Junior
- **Referencia**: No disponible
- **Fecha de identificación**: 2026-05-20

**GAP: Estrategia de rollback en aplicación** [PRIORIDAD: Alta] [ESTADO: PENDIENTE]

- **Pregunta**: ¿Qué pasa si el Agente 4 aplica cambios incorrectos?
- **Contexto faltante**: No hay estrategia de rollback, mecanismo de reversión automática o manual, criterios para detectar cambios problemáticos
- **Rol afectado**: Arquitecto Senior, DevOps/SRE
- **Referencia**: architecture-overview.md menciona versioning de documentos pero no detalla estrategia de rollback
- **Fecha de identificación**: 2026-05-20

**GAP: Manejo de fallos en jobs** [PRIORIDAD: Alta] [ESTADO: PENDIENTE]

- **Pregunta**: ¿Qué pasa si un job falla (gap_detection, question_grouping, etc.)?
- **Contexto faltante**: No hay estrategia de retry, manejo de errores transitorios vs permanentes, alerting para jobs fallidos
- **Rol afectado**: Arquitecto Junior, Desarrollador Junior, DevOps/SRE
- **Referencia**: No disponible
- **Fecha de identificación**: 2026-05-20

**GAP: Timeout de jobs** [PRIORIDAD: Media] [ESTADO: PENDIENTE]

- **Pregunta**: ¿Cuáles son los timeouts para cada tipo de job?
- **Contexto faltante**: No hay especificación de timeouts máximos, estrategia para jobs que exceden timeout, impacto en estado del documento
- **Rol afectado**: Desarrollador Junior, DevOps/SRE Junior
- **Referencia**: No disponible
- **Fecha de identificación**: 2026-05-20

### Nuevos Gaps Identificados

**GAP: Estrategia de retry con backoff** [PRIORIDAD: Alta] [ESTADO: PENDIENTE]

- **Pregunta**: ¿Cuál es la estrategia de retry con backoff para jobs fallidos? ¿Cuántos reintentos antes de marcar como fallido permanente?
- **Contexto faltante**: Política de retry con backoff exponencial para manejar errores transitorios de LLM providers o servicios externos
- **Rol afectado**: Arquitecto Senior, Desarrollador Senior, DevOps/SRE
- **Referencia**: No disponible
- **Fecha de identificación**: 2026-05-22

**GAP: Detección de deadlocks en ciclo iterativo** [PRIORIDAD: Alta] [ESTADO: PENDIENTE]

- **Pregunta**: ¿Cómo se detecta y previene un loop infinito en el ciclo de verificación? ¿Cuál es el límite máximo de rounds?
- **Contexto faltante**: Mecanismo para detectar cuando el ciclo de verificación no converge (por ejemplo, si siempre se detectan nuevos gaps sin progreso)
- **Rol afectado**: Arquitecto Senior, Desarrollador Senior
- **Referencia**: No disponible
- **Fecha de identificación**: 2026-05-22

**GAP: Correlación de logs across jobs distribuidos** [PRIORIDAD: Media] [ESTADO: PENDIENTE]

- **Pregunta**: ¿Cómo se correlacionan logs entre jobs distribuidos (gap_detection, question_grouping, etc.) para debugging?
- **Contexto faltante**: Estrategia de logging con trace ID para seguir el flujo end-to-end de un documento a través de múltiples jobs
- **Rol afectado**: Desarrollador Senior, DevOps/SRE
- **Referencia**: No disponible
- **Fecha de identificación**: 2026-05-22

**GAP: Estrategia de alerting para jobs fallidos** [PRIORIDAD: Media] [ESTADO: PENDIENTE]

- **Pregunta**: ¿Qué alertas se generan cuando un job falla? ¿Quién recibe notificaciones? ¿Cuál es el SLA de respuesta?
- **Contexto faltante**: Configuración de alerting y notificaciones para monitoreo de jobs fallidos
- **Rol afectado**: DevOps/SRE, Arquitecto Senior
- **Referencia**: No disponible
- **Fecha de identificación**: 2026-05-22

---

## Respuestas Encontradas en Referencias

### ADR-002: Arquitectura de 5 Fases

- **Pregunta**: ¿Por qué este flujo específico?
- **Respuesta**: ADR-002 justifica cada fase del flujo y por qué el ciclo iterativo es necesario para mejoras progresivas. Agrupación es necesaria para eficiencia cognitiva, Verificación previene propagación de errores, Ciclo iterativo permite mejoras progresivas. Alternativas consideradas (3 fases, sin verificación, sin agrupación) fueron rechazadas.
- **Referencia**: `/Users/gil/projects/alejandria/docs/ingenieria/decisiones/adr-002-5-phase-architecture.md`
- **Fecha de validación**: 2026-05-22

---

*Documento generado como parte de [ARC-001](technical-brief.md).*

*Análisis de gaps actualizado el 2026-05-22.*
