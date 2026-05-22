---
id: FEA-005
type: Product Definition
rating: 9
rating-phase: document-editing
related:
  - target: STR-001
    relationship_type: implements
    reason: Implementa la visión y misión definiendo el ciclo de vida de documentación
  - target: STR-002
    relationship_type: implements
    reason: Implementa la estrategia tecnológica mediante el workflow de 5 fases
---

# Arquitectura de 5 Fases para Ciclo de Detección-Resolución

## Contexto y Problema

Alejandria necesita automatizar el ciclo de vida de la documentación técnica mediante detección de gaps de contexto y resolución colaborativa. Un enfoque simple de "detectar y resolver" sería insuficiente porque:

- **Ineficiencia cognitiva**: Responder preguntas dispersas sin agrupación sería agotador para el usuario
- **Propagación de errores**: Sin verificación, respuestas incorrectas se aplicarían a la documentación
- **Falta de iteración automática**: Sin ciclo continuo autónomo, la documentación no mejoraría progresivamente sin intervención manual

## Decisiones

**Decisión**: Implementar un pipeline secuencial de 5 fases: Detección → Agrupación → Resolución → Verificación → Aplicación, con capacidad de ciclo iterativo (Aplicación → Detección).

**Las 5 fases del sistema**:

1. **Detección**: Agentes LLM analizan documentos para identificar información faltante (gaps de contexto)
2. **Agrupación**: Las preguntas detectadas se agrupan por tema mediante tags para facilitar navegación coherente
3. **Resolución**: Proceso asíncrono mediado por la plataforma donde los usuarios interactúan con gaps pre-rellenados en su propio tiempo, aceptando, modificando o rechazando sugerencias. La plataforma actúa como intermediario, no hay conversación directa en tiempo real entre agente y usuario.
4. **Verificación**: Las respuestas se verifican automáticamente para detectar nuevos gaps o inconsistencias
5. **Aplicación**: Los cambios validados se aplican automáticamente a la documentación

## Justificación

### Alineación con la Misión

La arquitectura de 5 fases implementa directamente la misión de "automatizar el ciclo de vida de la documentación técnica". Cada fase corresponde a un componente específico de la misión:

| Fase | Componente de la misión | Propósito |
| --- | --- | --- |
| **Detección** | "detectar gaps de contexto" | Agentes LLM identifican sistemáticamente información faltante en los documentos |
| **Agrupación** | Optimización para eficiencia | Agrupar gaps por tema mediante tags permite resolución gradual donde el usuario mantiene contexto mental |
| **Resolución** | "facilitar resolución mediante interacción asíncrona" | Usuarios interactúan con gaps pre-rellenados en su propio tiempo, aceptando/modificando sugerencias |
| **Verificación** | Aseguramiento de calidad | Respuestas se validan antes de aplicar cambios para evitar propagación de errores |
| **Aplicación** | "aplicar mejoras de forma continua" | Cambios se aplican automáticamente sin intervención manual repetitiva |

### Por Qué Estas Fases Son Necesarias

**Agrupación**: Sin agrupación, responder preguntas dispersas sería cognitivamente agotador. Agrupar por tema mediante tags permite resolución gradual donde el usuario mantiene contexto mental entre preguntas relacionadas.

**Verificación**: Las respuestas de los usuarios pueden contener nuevos gaps o ser incompletas. Verificar antes de aplicar evita propagar errores a la documentación. Además, la verificación puede revelar gaps que el usuario no notó (por ejemplo, contradicciones entre respuestas).

**Ciclo iterativo**: La verificación puede detectar nuevos gaps, lo que reinicia el ciclo (Detección → Agrupación → Resolución → Verificación). Esto crea el ciclo de vida continuo mencionado en la misión, permitiendo mejoras progresivas de la documentación.

### Onboarding de Proyectos

El workflow de 5 fases se adapta según el tipo de proyecto:

**Proyectos nuevos**:

- Onboarding guiado y proactivo
- Plantillas de documentación mínima
- Enfoque en documentar decisiones arquitectónicas desde el inicio
- Integración con flujo de commits

**Proyectos legacy**:

- Ejecuta análisis de salud completo inicial
- Genera baseline y calificación global (0-10)
- Crea mapa de calor de gaps
- Priorización inteligente de módulos
- Arqueología de código para entender contexto existente
- Migración gradual comenzando con módulos críticos

**Criterio de optimización**: Documentos con calificación ≥9 no se procesan para optimizar recursos, enfocándose en áreas que requieren mayor atención.

### Flujo Integrado de las 5 Fases

Cada fase depende de la salida de la fase anterior, creando un sistema integrado:

1. **Detección → Agrupación**: Los gaps detectados se agrupan por tema y similitud semántica mediante tags para facilitar navegación
2. **Agrupación → Resolución**: Los tags organizados permiten que el usuario mantenga contexto mental entre preguntas relacionadas, haciendo la resolución eficiente
3. **Resolución → Verificación**: Las respuestas se analizan para detectar inconsistencias, contradicciones o nuevos gaps antes de aplicar cambios
4. **Verificación → Aplicación**: Solo respuestas validadas se aplican automáticamente a la documentación, protegiendo su integridad
5. **Aplicación → Detección (ciclo iterativo)**: La documentación actualizada se re-analiza para detectar nuevos gaps, creando mejoras progresivas

### Alineación con Valores Organizacionales

La arquitectura de 5 fases implementa directamente los valores organizacionales establecidos en vision-mission.md:

| Fase | Valor Organizacional | Implementación |
| --- | --- | --- |
| **Detección** | Calidad Automática | Los agentes LLM identifican sistemáticamente gaps sin intervención manual, asegurando calidad automática de la documentación |
| **Agrupación** | Baja Fricción | Agrupar gaps por tema mediante tags reduce la fricción cognitiva para el usuario, permitiendo resolución gradual donde mantiene contexto mental |
| **Resolución** | Contexto Acumulativo | La interacción asíncrona acumula contexto y respuestas que pueden reutilizarse, construyendo conocimiento institucional |
| **Verificación** | Verificación Iterativa | Las respuestas se validan automáticamente antes de aplicar cambios, asegurando mejoras iterativas sin riesgo de degradación |
| **Aplicación** | Integración Continua | Los cambios se aplican automáticamente sin intervención manual repetitiva, integrándose continuamente con el workflow de documentación |

## Trade-offs

### Desventajas

- **Complejidad arquitectónica**: 5 fases añaden más componentes que un flujo simple de 3 fases
- **Latencia adicional**: Cada fase añade tiempo al proceso total
- **Superficie de errores mayor**: Más componentes = más puntos potenciales de failure

### Mitigación

- **Simplicidad en implementación inicial**: Comenzar con MVP que implemente las 5 fases de manera básica
- **Idempotencia de jobs**: Prevenir duplicación de trabajo y efectos secundarios
- **Versioning de documentos**: Permitir rollback si se detectan errores
- **Testing exhaustivo**: Validar cada fase independientemente y en integración

## Alternativas Consideradas

### Flujo de 3 Fases (Detección → Resolución → Aplicación)

**Ventaja**: Menor complejidad arquitectónica, setup más simple

**Desventaja**: Sin agrupación la resolución es ineficiente cognitivamente, y sin verificación se propagan errores

**Decisión**: Rechazada porque compromete calidad y eficiencia del usuario

### Flujo Sin Verificación

**Ventaja**: Menor latencia, menor complejidad

**Desventaja**: Las respuestas pueden contener nuevos gaps o contradicciones que se propagarían a la documentación

**Decisión**: Rechazada porque compromete la calidad de la documentación y puede causar degradación

### Flujo Sin Agrupación

**Ventaja**: Simplicidad, menor latencia

**Desventaja**: Responder preguntas dispersas sería cognitivamente agotador para el usuario

**Decisión**: Rechazada porque compromete la experiencia del usuario y eficiencia de resolución

## Consecuencias

### Impacto Positivo

- **Eficiencia cognitiva**: Agrupación mediante tags permite resolución gradual donde el usuario mantiene contexto mental
- **Calidad de documentación**: Verificación previene propagación de errores
- **Mejoras progresivas**: Ciclo iterativo permite mejoras continuas de la documentación
- **Alineación con misión**: Implementación directa del propósito de automatizar el ciclo de vida

### Impacto Negativo

- **Complejidad inicial**: Más componentes que implementar y mantener
- **Latencia**: Cada fase añade tiempo al proceso
- **Superficie de errores**: Más componentes = más puntos potenciales de failure

### Requerimientos de Implementación

- Sistema de agrupación por tema y similitud semántica
- Sistema de verificación automática de consistencia
- Sistema de versioning de documentos con rollback
- Sistema de idempotencia de jobs para prevenir duplicación
- Dashboard para seguimiento del estado de documentos en cada fase

## Referencias

- vision-mission.md: Misión de "automatizar el ciclo de vida de la documentación técnica"
- vision-mission.md: Valores organizacionales (Calidad Automática, Baja Fricción, Contexto Acumulativo, Verificación Iterativa, Integración Continua)
- technology-strategy.md: Sección "Arquitectura General"
- @[docs/estrategia/estrategia/vision-mission.md]: User personas y journeys detallados para CTO/VP Engineering, Senior Developer/Tech Lead, y DevOps/SRE (sección User Personas)
