---
id: FEA-001
type: Feature
rating:
rating-phase:
related:
  - target: STR-001
    relationship_type: implements
    reason: Implementa la visión y misión definiendo el workflow de 5 fases
  - target: STR-002
    relationship_type: implements
    reason: Implementa la estrategia tecnológica mediante el workflow de 5 fases
---

# Flujo de Trabajo de 5 Fases

Descripción del proceso automatizado que transforma documentación técnica degradada en un activo estratégico mediante detección y resolución iterativa de gaps de contexto.

---

## Visión General

El flujo de trabajo de 5 fases es el mecanismo mediante el cual Alejandria mantiene automáticamente la calidad de la documentación técnica. A diferencia de enfoques tradicionales que requieren mantenimiento manual continuo, este sistema detecta proactivamente información faltante, facilita su resolución mediante interacción asíncrona, y aplica mejoras de forma continua.

**Valor para el usuario:** Transforma la documentación de pasivo costoso en activo estratégico sin requerir dedicación manual significativa.

---

## Las 5 Fases

### Fase 1: Detección

**Objetivo:** Identificar sistemáticamente información faltante en la documentación.

**Qué sucede:**

- El sistema analiza documentos existentes
- Genera preguntas sobre información que parece faltar (terminología sin definir, decisiones sin justificar, referencias no explicadas)
- Cada pregunta representa un "gap de contexto" que impide comprensión completa

**Valor:** Automatiza el proceso de identificación de problemas que normalmente requeriría revisión manual exhaustiva.

---

### Fase 2: Agrupación

**Objetivo:** Organizar las preguntas detectadas mediante tags para facilitar navegación coherente.

**Qué sucede:**

- Las preguntas individuales se agrupan por tema o contexto relacionado
- Cada grupo forma un conjunto de gaps relacionados por tags
- Esto evita sobrecarga cognitiva al resolver muchos gaps dispersos

**Valor:** Permite resolución eficiente de gaps en bloques coherentes en lugar de preguntas aisladas.

---

### Fase 3: Resolución

**Objetivo:** Llenar los gaps de contexto mediante interacción humana.

**Qué sucede:**

- El usuario ve grupos de preguntas listos para resolver
- Interactúa con gaps en su propio tiempo de forma asíncrona
- Responde preguntas proporcionando el contexto faltante
- El sistema captura las respuestas como "context entries"

**Valor:** Combina automatización con juicio humano—el sistema identifica qué falta, el humano decide qué es correcto.

---

### Fase 4: Verificación

**Objetivo:** Validar que las respuestas no revelan nuevos gaps.

**Qué sucede:**

- El sistema evalúa las respuestas proporcionadas
- Si una respuesta revela nueva información faltante, genera nuevas preguntas automáticamente
- Si no hay nuevos gaps, procede a la siguiente fase
- Este ciclo puede repetirse automáticamente múltiples veces via triggers

**Nota:** Los rounds/iteraciones se generan automáticamente vía triggers en respuesta a cambios en documentos o respuestas de gaps. No hay tracking explícito de rounds en la base de datos - el sistema detecta y genera nuevos gaps de forma autónoma cuando es necesario.

**Valor:** Asegura profundidad en lugar de superficialidad—previene respuestas incompletas que crean ilusión de completitud.

---

### Fase 5: Aplicación

**Objetivo:** Integrar el contexto enriquecido en la documentación.

**Qué sucede:**

- El sistema aplica sugerencias de mejora a los documentos
- Las respuestas capturadas se integran como contenido estructurado
- La documentación se actualiza con el nuevo contexto
- El documento se marca como "healthy" (completo)

**Valor:** Automatiza la actualización de documentación—no requiere edición manual post-resolución.

---

## Ciclo Continuo

El flujo no es un evento único sino un ciclo continuo:

```text
Documento creado → Detección → Agrupación → Resolución → Verificación → Aplicación → Documento healthy
                                                                             ↓
                                                Documento editado → Re-detección (ciclo)
```

**Mantenimiento continuo:** Cuando un documento se edita manualmente, el sistema re-ejecuta la detección para identificar si los cambios introdujeron nuevos gaps. Esto asegura que la documentación se mantenga actualizada automáticamente.

---

## Valor por Fase

| Fase         | Problema que Resuelve                                    | Valor Generado                             |
|--------------|----------------------------------------------------------|--------------------------------------------|
| Detección    | Revisión manual costosa para identificar problemas       | Identificación automatizada de gaps        |
| Agrupación   | Preguntas dispersas difíciles de resolver eficientemente | Tags coherentes y enfocados            |
| Resolución   | Falta de proceso estructurado para llenar gaps           | Interacción guiada con captura de contexto |
| Verificación | Respuestas superficiales que dejan gaps ocultos          | Validación de profundidad y completitud    |
| Aplicación   | Edición manual post-resolución                           | Integración automática de mejoras          |

---

## Diferenciación vs Enfoques Tradicionales

| Aspecto                     | Enfoque Tradicional                  | Alejandria (5 Fases)                  |
|-----------------------------|--------------------------------------|---------------------------------------|
| Identificación de problemas | Revisión manual periódica            | Detección automatizada continua       |
| Resolución de gaps          | Ad-hoc, cuando alguien nota problema | Resolución estructurada proactiva     |
| Actualización               | Edición manual post-identificación   | Aplicación automática post-resolución |
| Mantenimiento               | Requiere dedicación continua         | Sistema trabaja en segundo plano      |
| Profundidad                 | Superficial (problemas visibles)     | Iterativo (detecta gaps ocultos)      |

---

## Referencias Técnicas

Para detalles de implementación técnica de las 5 fases, ver:

- [ARC-001](../../ingenieria/arquitectura/technical-brief.md): Technical Brief - Arquitectura general
- [ARC-002](../../ingenieria/arquitectura/end-to-end-flow.md): End-to-End Flow - Flujo técnico detallado
- [ADR-002](../../ingenieria/decisiones/adr-002-5-phase-architecture.md): Justificación de la arquitectura de 5 fases

---

*Documento generado como especificación de funcionalidad del producto.*

---

## Nota de Mejora

Este documento puede mejorarse incorporando información del contexto adicional (@[docs/contexto-adicional.md]), específicamente:

- El modelo de interacción es asíncrono mediado por la plataforma, con agrupación mediante tags
- Criterio de calificación ≥9 para no procesar documentos de alta calidad
- Descripción detallada de la interfaz de usuario (secciones de documentos, preguntas, gaps, propuestas, grafo)
- Onboarding de proyectos (nuevo vs legacy) con análisis de salud y arqueología de código
- Onboarding de equipo con rutas de aprendizaje personalizadas, quizzes automáticos y mentoría asistida por IA
- Referencia a skills de agentes como base para implementación de las fases
