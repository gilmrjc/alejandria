---
id: FEA-002
type: Feature Document
related:
  - target: REQ-006
    relationship_type: implements
    reason: Implementa los requisitos de onboarding de proyecto nuevo
  - target: REQ-007
    relationship_type: implements
    reason: Implementa los requisitos de onboarding de proyecto legacy
  - target: TS-006
    relationship_type: references
    reason: Referencia el technical-specs-onboarding-proyecto-legacy para especificación técnica detallada
  - target: TS-007
    relationship_type: references
    reason: Referencia el technical-specs-onboarding-proyecto-nuevo para especificación técnica detallada
---

# Onboarding Strategy

Estrategia de onboarding de proyectos para Alejandria, adaptada según el tipo de proyecto (nuevo vs legacy).

---

## Onboarding de Proyecto Nuevo

### Descripción

Proceso guiado para incorporar proyectos que comienzan desde cero a Alejandría.

### Propósito

Establecer expectativas claras sobre documentación desde el inicio, evitando acumulación de deuda documental.

### User Personas

- CTO/VP Engineering
- Senior Developer/Tech Lead

### Cómo Funciona

El usuario conecta el repositorio de GitHub o crea el primer documento descriptivo del proyecto. El sistema proporciona plantillas de documentación mínima requerida y establece expectativas sobre documentación de decisiones arquitectónicas.

### Casos de Uso

- Crear un nuevo proyecto en Alejandría
- Conectar repositorio GitHub
- Establecer baseline de documentación para proyecto nuevo

### Componentes y Referencias

- Integración con GitHub → [PENDIENTE]
- Plantillas de documentación → [PENDIENTE]

### Decisiones Relacionadas

- [PENDIENTE]

---

## Onboarding de Proyecto Legacy

### Descripción

Proceso de migración gradual para proyectos con historia acumulada y documentación existente.

### Propósito

Generar baseline del estado actual de documentación y priorizar áreas que deben abordarse primero.

### User Personas

- CTO/VP Engineering
- Senior Developer/Tech Lead

### Cómo Funciona

Al conectar un repositorio con historia, el sistema ejecuta análisis de salud completo generando calificación global, mapa de calor de módulos, y priorización inteligente basada en frecuencia de cambios y complejidad. Realiza arqueología de código analizando commits, pull requests e issues.

### Casos de Uso

- Migrar proyecto existente a Alejandría
- Evaluar salud de documentación actual
- Priorizar áreas de mejora documental
- Recuperar contexto perdido mediante arqueología de código

### Componentes y Referencias

- Análisis de salud inicial → [PENDIENTE]
- Arqueología de código → [PENDIENTE]
- Mapa de calor de documentación → [PENDIENTE]

### Decisiones Relacionadas

- [PENDIENTE]
