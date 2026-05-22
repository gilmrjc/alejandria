---
id: ARC-020
type: Implementation Specification
rating: 9.2
rating-phase: document-editing
related:
  - target: ADR-004
    relationship_type: implements
    reason: Implementa la estrategia de retry con backoff exponencial definida en ADR-004
  - target: TRD-023
    relationship_type: references
    reason: Referencia el TRD de Hito 2 para requisitos de integraciones y jobs
  - target: EPC-002
    relationship_type: implements
    reason: Implementa la configuración de Celery para la épica de API y MCP
---

# Celery Retry Implementation — Alejandria

Este documento define la implementación específica de la estrategia de retry con backoff exponencial para jobs de Celery según ADR-004.

## Índice

1. [Visión General](#1-visión-general)
2. [Configuración de Backoff Exponencial](#2-configuración-de-backoff-exponencial)
3. [Implementación de Jitter](#3-implementación-de-jitter)
4. [Máximo de Reintentos](#4-máximo-de-reintentos)
5. [Timeout de Jobs](#5-timeout-de-jobs)
6. [Clasificación de Excepciones](#6-clasificación-de-excepciones)
7. [Dead Letter Queue](#7-dead-letter-queue)
8. [Monitoreo de Retries](#8-monitoreo-de-retries)

---

## 1. Visión General

### Propósito

Especificar la implementación de retry strategy con backoff exponencial y jitter para jobs de Celery, asegurando resiliencia ante fallos transitorios.

### Referencia

Para la estrategia conceptual de jobs efímeros, ver [ADR-004: Jobs Efímeros vs Persistentes](../decisiones/adr-004-ephemeral-jobs.md).

---

## 2. Configuración de Backoff Exponencial

### Secuencia de Retries

Según ADR-004, la secuencia de backoff es: 1s, 2s, 4s, 8s, 16s

### Implementación en Celery

La configuración de backoff exponencial en Celery se realiza mediante parámetros específicos en el decorador `@app.task`. El siguiente ejemplo muestra la configuración básica:

```python
@app.task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=16,
    retry_jitter=True
)
def my_task():
    pass
```

En esta configuración, `autoretry_for=(Exception,)` especifica que el job debe reintentarse ante cualquier excepción, `retry_backoff=True` habilita el backoff exponencial en lugar de reintentos inmediatos, `retry_backoff_max=16` establece el tiempo máximo de espera entre reintentos (16 segundos), y `retry_jitter=True` añade variabilidad aleatoria para prevenir thundering herd. Según ADR-004 y ADR-005, la configuración completa también incluye `max_retries=5` como máximo de reintentos por defecto y `time_limit=300` para un timeout de 5 minutos (300 segundos), aunque estos parámetros pueden sobrescribirse por job type según necesidades específicas.

---

## 3. Implementación de Jitter

### Propósito del Jitter

El jitter (±20%) previene thundering herd problem cuando múltiples jobs fallan simultáneamente y reintentan al mismo tiempo.

### Algoritmo de Jitter

Según ADR-004 y ADR-005, el jitter es de ±20% aplicado al backoff exponencial. Celery implementa jitter usando distribución uniforme cuando `retry_jitter=True`. El cálculo es: `retry_delay = base_delay * (1 + random.uniform(-0.2, 0.2))`. Esto previene el thundering herd problem cuando múltiples jobs fallan simultáneamente.

### Implementación

Celery implementa jitter automáticamente cuando `retry_jitter=True`, utilizando una distribución uniforme. El siguiente ejemplo muestra el cálculo manual equivalente:

```python
# Ejemplo con jitter
retry_delay = base_delay * (1 + random.uniform(-0.2, 0.2))
```

En este cálculo, `base_delay` es el tiempo de backoff exponencial calculado (1s, 2s, 4s, 8s, 16s), y `random.uniform(-0.2, 0.2)` genera un valor aleatorio entre -0.2 y 0.2, resultando en un factor de jitter entre 0.8 y 1.2. Esto significa que un backoff de 8 segundos podría resultar en un delay entre 6.4 y 9.6 segundos, distribuyendo los reintentos en el tiempo y previniendo que múltiples jobs fallen simultáneamente.

---

## 4. Máximo de Reintentos

### Configuración por Defecto de Reintentos

La configuración por defecto establece un máximo de 5 reintentos para todos los jobs, aunque este valor es configurable por job type según las necesidades específicas de cada tipo de tarea.

### Implementación de Máximo de Reintentos

El parámetro `max_retries` controla el número máximo de reintentos antes de que el job sea marcado como fallido:

```python
@app.task(max_retries=5)
def my_task():
    pass
```

Con `max_retries=5`, el job se ejecutará hasta 6 veces en total (1 ejecución inicial + 5 reintentos). Si el job falla en todos los intentos, será enviado a la dead letter queue según la configuración descrita en la sección 7. Este valor puede ajustarse por job type; por ejemplo, jobs I/O bound como vector_sync podrían beneficiarse de un valor más alto (ej: 10 reintentos) debido a la naturaleza transitoria de los errores de red.

### Excepciones

Según ADR-004 y TRD-002, los job types identificados son gap_detection, suggestion_application, vector_sync y question_generation. Para el MVP bootstrapped, se utiliza la configuración por defecto (max_retries=5) para todos los job types. Sin embargo, excepciones específicas por job type pueden definirse durante la implementación según necesidades particulares; por ejemplo, vector_sync podría requerir más reintentos debido a su naturaleza I/O bound.

---

## 5. Timeout de Jobs

### Configuración por Defecto de Timeout

Se establece un timeout de 5 minutos para todos los jobs, aunque este valor es configurable por job type según las características específicas de cada tarea.

### Implementación de Timeout

El parámetro `time_limit` establece el tiempo máximo de ejecución del job en segundos:

```python
@app.task(time_limit=300)  # 5 minutos
def my_task():
    pass
```

Con `time_limit=300`, el job será terminado forzosamente después de 5 minutos si no ha completado su ejecución. Este es un hard timeout que no permite cleanup controlado. Para implementar cleanup controlado, se debe usar `soft_time_limit` en conjunto con `time_limit` como se muestra en la siguiente sección. El timeout previene jobs que se cuelguen indefinidamente debido a bugs o condiciones inesperadas.

### Tipos de Timeout

Celery implementa dos tipos de timeout: **soft_timeout**, que permite al job manejar cleanup de forma controlada antes de ser terminado, y **hard_timeout**, que fuerza la terminación inmediata del job sin oportunidad de cleanup. El uso de soft_timeout es recomendado cuando el job necesita liberar recursos o guardar estado antes de terminar.

### Implementación de Cleanup en Soft Timeout

Para implementar cleanup controlado, se utiliza el parámetro `soft_time_limit` junto con el decorador `@app.task(bind=True)` para acceder a la excepción de timeout:

```python
@app.task(bind=True, soft_time_limit=300, time_limit=360)
def my_task(self):
    try:
        # Lógica del job
        process_data()
    except SoftTimeLimitExceeded:
        # Cleanup controlado antes de terminar
        cleanup_resources()
        save_partial_state()
        raise  # Re-raise para marcar el job como timeout
```

En este ejemplo, `soft_time_limit=300` permite 5 minutos para cleanup controlado, mientras `time_limit=360` establece un hard timeout de 6 minutos como medida de seguridad final.

### Consideraciones por Job Type

Diferentes job types pueden requerir configuraciones de timeout específicas según su naturaleza:

- **gap_detection**: Timeout estándar de 5 minutos es adecuado para análisis de documentos de tamaño moderado
- **suggestion_application**: Puede requerir timeout extendido (ej: 10 minutos) para documentos con muchas sugerencias
- **vector_sync**: Timeout estándar es suficiente, pero soft_timeout es crítico para liberar conexiones a base de datos
- **question_generation**: Timeout extendido puede ser necesario para generación compleja con LLMs

Para MVP bootstrapped, se utiliza la configuración por defecto (5 minutos) para todos los job types, pero estas consideraciones guiarán ajustes post-MVP.

---

## 6. Clasificación de Excepciones

### Excepciones Retryables

Las excepciones que deberían reintentarse incluyen errores de red como ConnectionError y TimeoutError, fallos temporales como 503 Service Unavailable, y situaciones de rate limiting como 429 Too Many Requests. Estos errores son típicamente transitorios y pueden resolverse con reintentos.

### Excepciones No Retryables

Las excepciones que NO deberían reintentarse incluyen errores de validación como ValueError y TypeError, errores de autenticación como 401 Unauthorized, errores de recurso no encontrado como 404 Not Found, y errores de permisos como 403 Forbidden. Estos errores indican problemas estructurales o de configuración que no se resolverán con reintentos.

### Implementación de Clasificación de Excepciones

La clasificación de excepciones se implementa mediante tuplas de tipos de excepción que se utilizan para configurar el comportamiento de retry:

```python
RETRYABLE_EXCEPTIONS = (ConnectionError, TimeoutError, HTTPError)
NON_RETRYABLE_EXCEPTIONS = (ValueError, AuthenticationError)
```

Estas tuplas se utilizan con el parámetro `autoretry_for` para especificar qué excepciones deben reintentarse. Por ejemplo, `autoretry_for=RETRYABLE_EXCEPTIONS` configurará el job para reintentar solo ante errores de red y HTTP, mientras que excepciones en `NON_RETRYABLE_EXCEPTIONS` causarán falla inmediata sin reintentos. Esta clasificación permite un manejo más granular de errores, evitando reintentos inútiles en errores estructurales mientras se mantiene resiliencia ante fallos transitorios.

---

## 7. Dead Letter Queue

### Propósito de Dead Letter Queue

Almacenar jobs que fallaron después de max_retries para análisis manual y reintentos manuales.

### Configuración

Según ADR-004 y TRD-002, la dead letter queue se implementa marcando jobs como `failed` en la tabla `jobs` de PostgreSQL después de max_retries (5), con `error_message` detallado. No se usa DLQ separada en Redis/RabbitMQ para MVP bootstrapped. Jobs fallidos pueden reintentarse manualmente vía API endpoint `POST /api/v1/jobs/{id}/retry`. El backend es PostgreSQL (no Redis/RabbitMQ) para persistencia de estado.

### Implementación de Dead Letter Queue

La implementación de dead letter queue requiere el uso de `bind=True` para acceder al contexto del job y verificar el número de reintentos:

```python
@app.task(bind=True)
def my_task(self):
    try:
        # Lógica del job
        pass
    except Exception as exc:
        if self.request.retries >= self.max_retries:
            # Enviar a dead letter queue
            send_to_dlq(self.request.id, exc)
        raise
```

En este ejemplo, `bind=True` permite acceder a `self.request.retries` (número actual de reintentos) y `self.max_retries` (máximo configurado). Cuando se alcanza el máximo de reintentos, la función `send_to_dlq` marca el job como fallido en la tabla `jobs` de PostgreSQL con el error detallado. El `raise` final es necesario para que Celery registre el fallo correctamente. Esta implementación permite análisis manual de jobs fallidos y reintentos manuales vía API endpoint `POST /api/v1/jobs/{id}/retry`.

---

## 8. Monitoreo de Retries

### Métricas a Recolectar

Las métricas clave para monitorear la efectividad de la estrategia de retry incluyen el retry rate por job type para identificar jobs problemáticos, el tiempo promedio entre retries para validar el backoff exponencial, la cantidad de jobs en dead letter queue para medir la tasa de fallos permanentes, y el success rate después de retries para evaluar la efectividad global de la estrategia.

### Implementación de Monitoreo

Según ADR-002, para MVP Bootstrapped NO se implementan métricas con Prometheus/StatsD ni dashboards. La estrategia de observabilidad para MVP es logging estructurado JSON con request IDs para correlación manual, log aggregation vía Docker Compose logs (`docker-compose logs`), health checks básicos para verificar disponibilidad, sin metrics, sin distributed tracing, sin alerting automático. Métricas avanzadas (Prometheus/Grafana) se implementarán post-MVP según ADR-002.
