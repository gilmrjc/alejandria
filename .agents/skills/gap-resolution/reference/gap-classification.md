# Clasificación de Gaps

Este documento describe los tipos de gaps que se resuelven en sesiones colaborativas, los roles involucrados y los enfoques específicos según el tipo de gap.

## Tipos de Gaps

### Gaps de Definición

**Descripción**: Gaps que requieren clarificar términos, conceptos o terminología.

**Ejemplos**:

- "¿Qué significa [término] en este contexto?"
- "¿Cuál es la definición precisa de [concepto]?"
- "¿Cómo se define [rol] en este proyecto?"

**Enfoque de Resolución**:

- Proveer definiciones iniciales como punto de partida
- Solicitar ejemplos concretos del contexto del proyecto
- Validar que la definición sea aplicable al dominio
- Documentar contexto de uso y casos de aplicación

**Roles Involucrados**:

- Usuario final (para usabilidad)
- Desarrollador/Ingeniero (para implementación)
- Product Manager (para requisitos)
- Stakeholders de negocio (para alineación)

**Preguntas Clave**:

- ¿Qué significa este término en este contexto específico?
- ¿Hay definiciones alternativas que debamos considerar?
- ¿Cómo se relaciona este concepto con otros en el dominio?
- ¿Qué ejemplos concretos ilustran este concepto?

### Gaps de Razonamiento

**Descripción**: Gaps que requieren establecer la lógica detrás de decisiones o el "por qué" de ciertos enfoques.

**Ejemplos**:

- "¿Por qué se tomó esta decisión?"
- "¿Qué razonamiento justifica este enfoque?"
- "¿Por qué no se consideraron alternativas?"

**Enfoque de Resolución**:

- Proveer marcos de razonamiento posibles
- Explorar trade-offs y alternativas consideradas
- Documentar el proceso de toma de decisiones
- Usar frameworks estructurados (First Principles, Trade-off Analysis)

**Roles Involucrados**:

- Ejecutivo/Liderazgo (para contexto estratégico)
- Arquitecto (para decisiones técnicas)
- Product Manager (para decisiones de producto)
- Stakeholders de negocio (para alineación)

**Preguntas Clave**:

- ¿Cuáles fueron las razones fundamentales para esta decisión?
- ¿Qué alternativas se consideraron y por qué se rechazaron?
- ¿Qué criterios se usaron para evaluar las opciones?
- ¿Cuáles son los trade-offs de esta decisión?

### Gaps de Estrategia

**Descripción**: Gaps que requieren definir enfoques estratégicos, planeamiento o roadmap.

**Ejemplos**:

- "¿Cuál es la estrategia para [iniciativa]?"
- "¿Cómo se priorizarán estas features?"
- "¿Qué dirección estratégica debe seguir el proyecto?"

**Enfoque de Resolución**:

- Proveer opciones con pros y contras
- Considerar dependencias y riesgos
- Validar alineación con objetivos de negocio
- Documentar suposiciones y planes de contingencia

**Roles Involucrados**:

- Ejecutivo/Liderazgo (para visión estratégica)
- Product Manager (para roadmap y priorización)
- Business Analyst (para análisis de viabilidad)
- Stakeholders de negocio (para alineación)

**Preguntas Clave**:

- ¿Qué objetivos estratégicos guían esta dirección?
- ¿Qué recursos y capacidades se requieren?
- ¿Cuáles son los riesgos y mitigaciones?
- ¿Cómo se medirá el éxito de esta estrategia?

### Gaps de Implementación

**Descripción**: Gaps que requieren detalles de cómo implementar algo técnicamente u operacionalmente.

**Ejemplos**:

- "¿Cómo se implementa esta funcionalidad?"
- "¿Qué patrones o enfoques técnicos se usarán?"
- "¿Cuál es el procedimiento operativo para este proceso?"

**Enfoque de Resolución**:

- Sugerir patrones o enfoques técnicos
- Considerar restricciones y dependencias
- Validar factibilidad técnica
- Documentar trade-offs técnicos explícitamente

**Roles Involucrados**:

- Desarrollador/Ingeniero (para implementación técnica)
- Arquitecto (para diseño de alto nivel)
- DevOps/SRE (para operaciones y despliegue)
- QA/Tester (para criterios de aceptación)

**Preguntas Clave**:

- ¿Qué tecnologías o herramientas se usarán?
- ¿Cuáles son las dependencias y restricciones?
- ¿Cómo se integrará con sistemas existentes?
- ¿Qué criterios de aceptación se aplicarán?

## Perspectivas de Nivel de Experiencia

Aplicar ambas perspectivas a cada tipo de gap:

### Perspectiva Senior

Enfocarse en decisiones y contexto estratégico:

- Entender las razones fundamentales detrás de las decisiones
- Identificar el impacto en el negocio y consideraciones de largo plazo
- Evaluar trade-offs y alternativas consideradas
- Validar que el contexto estratégico esté documentado
- Enfocarse en gaps que impidan la toma de decisiones informadas

### Perspectiva Junior

Enfocarse en entendimiento fundamental y onboarding:

- Entender las razones desde un punto más fundamental: pros y contras
- Obtener explicaciones claras de conceptos de dominio y terminología
- Tener un paso a paso de los procesos a implementar
- Validar que haya suficiente contexto para entender sin investigación adicional
- Enfocarse en gaps que dificulten el aprendizaje y el entendimiento

## Modos de Resolución

Según el tipo y complejidad del gap, aplicar diferentes modos:

### Modo Rápido

**Para**: Gaps simples, definiciones claras, respuestas directas.

**Enfoque**:

- 1-2 rondas de preguntas
- Respuestas directas sin mucho brainstorming
- Validación rápida y documentación inmediata

**Ejemplos**: Definiciones de términos, decisiones técnicas menores, procedimientos estándar.

### Modo Profundo

**Para**: Gaps complejos, decisiones estratégicas, razonamientos complejos.

**Enfoque**:

- Múltiples rondas con investigación
- Brainstorming extenso
- Validación iterativa de alternativas
- Documentación detallada de razonamiento

**Ejemplos**: Decisiones arquitectónicas, estrategias de producto, trade-offs significativos.

### Modo Diferido

**Para**: Gaps que el usuario no puede resolver ahora, requieren investigación adicional.

**Enfoque**:

- Documentar como gap persistente
- Crear plan de acción específico
- Sugerir responsables o fuentes a consultar
- Programar para sesión futura

**Ejemplos**: Decisiones que requieren aprobación ejecutiva, investigación de mercado, validación con stakeholders externos.

## Formato de Declaración de Clasificación

Al iniciar la resolución de un gap, declarar:

```text
**CLASIFICACIÓN DEL GAP**
- Tipo: [Definición/Razonamiento/Estrategia/Implementación]
- Modo: [Rápido/Profundo/Diferido]
- Roles involucrados: [Rol 1] + [Rol 2]
- Enfoque: [Descripción del enfoque de resolución]
- Perspectiva: Senior + Junior
```
