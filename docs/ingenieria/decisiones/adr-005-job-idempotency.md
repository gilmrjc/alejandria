---
id: ADR-005
type: Architecture Decision Record
rating: 10
rating-phase: document-editing
related:
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del schema de base de datos para campos de locks en tabla documents
  - target: ADR-002
    relationship_type: extends
    reason: Extiende el stack unificado Python con estrategia de idempotencia de jobs
  - target: ADR-004
    relationship_type: extends
    reason: Extiende las decisiones de jobs efímeros con locks de idempotencia
  - target: ADR-006
    relationship_type: reinforces
    reason: Refuerza el versioning al prevenir duplicación de trabajo en reintentos
---

# ADR-005: Idempotencia de Jobs

## Contexto y Problema

Alejandria ejecuta jobs asíncronos para detección, agrupación, resolución, verificación y aplicación de cambios. Sin idempotencia, el sistema tendría:

- **Duplicación de trabajo**: Un job podría ejecutarse múltiples veces para la misma tarea
- **Inconsistencia de estados**: Reintentos de jobs fallidos podrían causar efectos secundarios duplicados
- **Corrupción de datos**: Aplicaciones repetidas de cambios podrían corromper la documentación
- **Dificultad de debugging**: Incapacidad de distinguir entre ejecuciones únicas y duplicadas

El problema es crítico porque jobs pueden fallar por razones transitorias (network issues, timeouts temporales) y el sistema necesita reintentar automáticamente. Sin idempotencia, los reintentos causarían efectos secundarios no deseados.

## Decisiones

**Decisión**: Implementar idempotencia usando Redis distributed locks con celery_once.

**Implementación específica**:

- Usar librería `celery_once` con backend Redis para distributed locks
- Redis ya está en el stack como broker de Celery (ADR-002)
- Tasks de Celery heredan de `QueueOnce` para prevenir ejecución duplicada
- Lock keys basadas en `document_id` como parámetro de identificación
- Timeout configurable por task (default: 60 minutos, override por job type). celery_once permite timeout configurable por task usando el parámetro `once={'timeout': X}` en la definición de la task. Esto permite que jobs largos tengan timeouts más largos y jobs cortos tengan timeouts más cortos, optimizando la recuperación de failures sin riesgo de ejecución duplicada por timeout prematuro.
- Auto-release de lock cuando task completa o falla
- Opción `graceful=True` para no lanzar excepción si lock existe
- Sistema de reintentos con backoff exponencial (configurado en ADR-002). Backoff exponencial es una estrategia de reintentos donde el tiempo de espera entre reintentos crece exponencialmente (ej: 1s, 2s, 4s, 8s, 16s). Esto reduce presión en sistemas externos porque si un job falla por razones transitorias (ej: API LLM temporalmente sobrecargada), no se bombardea con reintentos inmediatos. En Alejandria, el backoff exponencial está configurado en ADR-002 con jitter aleatorio (±20%) para evitar thundering herd problem.

## Justificación

### Beneficios de la Idempotencia con Redis Distributed Locks

**Prevenir duplicación de trabajo**:

- Un job no se ejecuta dos veces para la misma tarea (celery_once previene encolamiento duplicado)
- Si un job falla y se reintentra, no causa efectos secundarios duplicados
- Ahorro de recursos computacionales y costos de API LLM

**Consistencia en estados**:

- El estado del sistema permanece consistente incluso con reintentos
- No hay efectos secundarios no deseados por ejecuciones duplicadas
- Estados de documentos son predecibles

**Manejo de reintentos robusto**:

- Si un job falla por razones transitorias, puede reintentarse sin riesgo
- Backoff exponencial reduce presión en sistemas externos (configurado en ADR-002)
- Facilita debugging de problemas específicos sin efectos secundarios

**Simplicidad de implementación**:

- Redis ya está en el stack como broker de Celery (ADR-002)
- celery_once es una librería probada y estable (versión 3.0.1)
- Menos código custom que locks en base de datos
- Timeout configurable por job type (no fijo como en locks en base de datos)

**Escalabilidad distribuida**:

- Redis distributed locks son nativamente escalables para sistemas distribuidos
- Eliminan el problema de escalabilidad que tendrían locks en base de datos
- Redis está diseñado para alta concurrencia y baja latencia
- Múltiples workers en diferentes hosts pueden adquirir y liberar locks eficientemente

**Performance**:

- Redis locks son significativamente más rápidos que locks en base de datos
- Redis es un store en memoria optimizado para operaciones de locks con latencia <1ms en condiciones normales
- Locks en PostgreSQL requieren queries a disco con latencia típicamente 5-10ms
- El overhead de celery_once es mínimo porque usa redis-py's distributed Lock nativo
- Para MVP Bootstrapped con <100 jobs/día, el overhead es despreciable
- Si el sistema escala a miles de jobs/día, Redis puede manejar >100,000 ops/segundo

### Alineación con Valores Organizacionales

Idempotencia de jobs implementa el valor de "Calidad Automática" al prevenir duplicación de trabajo y asegurar consistencia. Esto mantiene la calidad sin supervisión manual.

También implementa "Baja Fricción" al permitir reintentos automáticos sin intervención manual del usuario.

## Trade-offs

### Desventajas

- **Dependencia de Redis**: Redis es un punto de failure adicional (ya presente en el stack)
- **Overhead de lock**: Adquirir y liberar locks en Redis añade overhead a cada job (menor que PostgreSQL)
- **Complejidad de configuración**: Requiere configuración de celery_once con backend Redis
- **Timeout de locks**: Si un job excede el timeout configurado, el lock expira y puede permitir ejecución duplicada

### Mitigación

- **Timeout de locks**: Locks expiran automáticamente después de timeout configurable (default 60 minutos)
- **Implementación simple**: Usar celery_once con backend Redis, librería probada y estable
- **Monitoreo de locks**: Alertas si locks permanecen activos por tiempo inusual
- **Testing exhaustivo**: Validar comportamiento de locks en escenarios de fallo
- **Rollback automático**: Si job falla, celery_once libera lock automáticamente
- **Redis ya en stack**: Redis ya es parte del stack como broker de Celery (ADR-002), no es una dependencia nueva
- **Configuración por job type**: Timeout configurable por task para jobs largos o cortos
- **Prevención de deadlocks**: celery_once con Redis distributed locks maneja deadlocks automáticamente usando el mecanismo de locks de Redis (redis-py's shared, distributed Lock) con timeout automático que previene deadlocks permanentes. Además, celery_once previene encolamiento duplicado de tasks, eliminando escenarios donde deadlocks podrían ocurrir por múltiples workers intentando procesar el mismo documento simultáneamente.

## Alternativas Consideradas

### Sin Idempotencia (Ejecución Directa)

**Ventaja**: Menor complejidad, menor overhead, implementación más simple

**Desventaja**: Duplicación de trabajo en reintentos, inconsistencia de estados, corrupción de datos

**Decisión**: Rechazada porque el riesgo de efectos secundarios duplicados es inaceptable para integridad de documentación.

### Idempotencia a Nivel de Aplicación (Deduplication en Memoria)

**Ventaja**: Menor overhead de base de datos, implementación más simple

**Desventaja**: No funciona en sistemas distribuidos, estado no persistente, vulnerable a crashes

**Decisión**: Rechazada porque el sistema usa jobs distribuidos y necesita persistencia de locks across workers.

### Idempotencia con Locks en Base de Datos

**Ventaja**: PostgreSQL ya está en el stack, locks son persistentes

**Desventaja**: Mayor overhead de queries, requiere campos adicionales en schema, timeout fijo no configurable por job type, locks en base de datos son más lentos que Redis

**Decisión**: Rechazada porque Redis distributed locks con celery_once son más simples (menos código custom), Redis ya está en el stack como broker de Celery (ADR-002), y permiten timeout configurable por job type. Locks en base de datos añadirían complejidad innecesaria y overhead adicional.

## Consecuencias

### Impacto Positivo

- **Consistencia**: Estados del sistema permanecen consistentes con reintentos
- **Eficiencia**: No hay duplicación de trabajo, ahorro de recursos
- **Robustez**: Reintentos automáticos sin efectos secundarios
- **Debugging**: Facilita identificación de problemas sin efectos secundarios
- **Simplicidad**: Menos código custom que locks en base de datos
- **Performance**: Redis locks son más rápidos que locks en base de datos
- **Flexibilidad**: Timeout configurable por job type

### Impacto Negativo

- **Complejidad**: Configuración de celery_once añade complejidad a implementación
- **Overhead**: Adquirir y liberar locks en Redis añade overhead a cada job (menor que PostgreSQL)
- **Dependencia**: Redis es un punto de failure (ya presente en el stack)
- **Timeout**: Si job excede timeout configurado, lock expira y puede permitir ejecución duplicada

### Requerimientos de Implementación

- Instalación de librería `celery_once` (versión 3.0.1)
- Configuración de Celery con backend `celery_once.backends.Redis`
- Configuración de timeout default (60 minutos) y por job type
- Tasks de Celery heredan de `QueueOnce` con keys basadas en `document_id`
- Opción `graceful=True` para manejo silencioso de locks existentes
- Sistema de reintentos con backoff exponencial (configurado en ADR-002)
- Monitoreo de locks activos y alertas por locks expirados
- Testing de comportamiento de locks en escenarios de fallo

## Referencias

- architecture-overview.md: Sección "Idempotencia de Jobs"
- technology-strategy.md: Sección "Componentes Principales" (Job Queue)
- adr-002-python-unified-stack.md: Stack Python con Celery y Redis como broker
- adr-004-ephemeral-jobs.md: Jobs efímeros vs persistentes
- celery_once documentation: <https://pypi.org/project/celery_once/>
