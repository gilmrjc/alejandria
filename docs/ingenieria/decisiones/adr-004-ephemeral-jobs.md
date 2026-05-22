---
id: ADR-004
type: Architecture Decision Record
rating:
rating-phase:
related:
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del schema de base de datos para persistencia de jobs y locks
---

# ADR-004: Jobs Efímeros vs Persistentes

## Contexto y Problema

Alejandria requiere un sistema de cola de trabajos para ejecutar tareas asíncronas como detección de gaps, agrupación, verificación y aplicación de cambios. La decisión clave es entre jobs efímeros (que se crean y destruyen según demanda) vs jobs persistentes (workers que permanecen activos continuamente).

Sin un sistema de colas apropiado, el sistema tendría:

- **Bloqueo de recursos**: Tareas largas bloquearían el API principal
- **Falta de escalabilidad**: Incapacidad de distribuir carga across múltiples workers
- **Fallo en cascada**: Si un job falla, podría afectar otros procesos
- **Ineficiencia de recursos**: Workers idle consumiendo recursos sin trabajo

## Decisiones

**Decisión**: Usar jobs efímeros con Celery para mejor utilización de recursos y fault tolerance.

**Implementación específica**:

- Celery para sistema de colas nativo de Python (decisión tomada: usar Celery desde el inicio)
- Redis como broker de mensajes
- Workers efímeros que se escalan según demanda
- Sistema de reintentos con backoff exponencial
- Redis distributed locks (celery_once) para idempotencia

## Justificación

### Ventajas de Jobs Efímeros

**Escalabilidad horizontal**:

- Los jobs efímeros pueden distribuirse across múltiples workers según demanda
- Permite agregar o remover workers dinámicamente
- Ideal para workload variable de detección y procesamiento de documentos

**Aislamiento de failures**:

- Si un job falla, no afecta otros jobs ni el sistema principal
- Fallos en un worker no causan degradación del sistema completo
- Facilita debugging de problemas específicos

**Mejor resource utilization**:

- Los recursos se asignan solo cuando se necesitan
- No se mantienen workers idle consumiendo recursos
- Costo operativo más bajo para fase bootstrapped

**Integración nativa con stack Python**:

- Celery está mejor acoplado con el stack de Python
- Mayor control durante la programación y debugging
- Ecosistema maduro de herramientas de monitoreo y administración

### Alineación con Valores Organizacionales

Jobs efímeros implementan el valor de "Baja Fricción" al permitir escalabilidad horizontal sin configuración manual compleja. El sistema escala automáticamente según demanda, reduciendo la fricción operacional.

También implementa "Calidad Automática" al prevenir que fallos en un job afecten el sistema completo, asegurando calidad sin supervisión manual.

## Trade-offs

### Desventajas

- **Latencia de startup**: Workers efímeros pueden tener latencia inicial al iniciar
- **Complejidad de orquestación**: Requiere sistema de gestión de colas y workers
- **Overhead de Redis**: Necesidad de mantener Redis como broker adicional

### Mitigación

- **Workers pre-calentados**: Mantener pool de workers activos para reducir latencia
- **Simplicidad en fase bootstrapped**: Comenzar con configuración básica de Celery
- **Redis como servicio gestionado**: Usar Redis simple para fase bootstrapped, evaluar servicios gestionados post-MVP

## Alternativas Consideradas

### Jobs Persistentes (Workers Siempre Activos)

**Ventaja**: Menor latencia de ejecución, workers siempre listos

**Desventaja**: Mayor consumo de recursos (workers idle), menor flexibilidad de escalabilidad, costo operativo más alto

**Decisión**: Rechazada porque para fase bootstrapped con workload variable, jobs efímeros proporcionan mejor utilización de recursos y costo operativo más bajo.

### Integración Directa en API (Sin Colas)

**Ventaja**: Menor complejidad arquitectónica, setup más simple

**Desventaja**: Bloqueo de recursos en tareas largas, falta de escalabilidad, fallo en cascada

**Decisión**: Rechazada porque tareas como detección de gaps y verificación pueden tomar tiempo significativo y bloquearían el API principal.

### Nomad para Orquestación de Jobs

**Ventaja**: Cloud-native, escalabilidad horizontal robusta, soporte para jobs efímeros

**Desventaja**: Mayor complejidad operacional, curva de aprendizaje más alta, overhead para fase bootstrapped

**Decisión**: Rechazada para fase bootstrapped porque Celery proporciona integración nativa con stack Python y menor complejidad operacional. Nomad puede considerarse en fase post-inversión si se requiere escalabilidad masiva.

## Consecuencias

### Impacto Positivo

- **Escalabilidad**: Capacidad de distribuir carga across múltiples workers
- **Fault tolerance**: Aislamiento de failures previene degradación del sistema
- **Eficiencia**: Mejor utilización de recursos con workers on-demand
- **Integración nativa**: Celery se integra directamente con stack Python

### Impacto Negativo

- **Complejidad**: Sistema de colas añade componentes adicionales a la arquitectura
- **Latencia**: Workers efímeros pueden tener latencia inicial
- **Overhead**: Redis como broker añade infraestructura adicional

### Requerimientos de Implementación

- Celery para sistema de colas
- Redis como broker de mensajes
- Sistema de reintentos con backoff exponencial
- Redis distributed locks (celery_once) para idempotencia (ver ADR-005)
- Monitoreo de jobs y workers
- Estrategia de escalado de workers según demanda

## Referencias

- architecture-overview.md: Sección "Jobs Efímeros vs Persistentes"
- technology-strategy.md: Sección "Componentes Principales" (Job Queue)

---

## Análisis de Document-Critique

### Estado del Análisis

- Análisis previo: NO
- Fecha del último análisis: 2026-05-26
- Versión anterior: N/A
- Gaps pendientes: 0
- Gaps respondidos: 0

### Clasificación del Documento

- Tipo: Architecture Decision Record (ADR)
- Rol Principal: Arquitecto
- Roles a Revisar: Arquitecto + Desarrollador
- Enfoque: Decisiones arquitectónicas, trade-offs técnicos, justificación de diseño, alternativas consideradas
- Perspectiva: Senior + Junior
- Fecha de análisis: 2026-05-26
- Versión del análisis: 1

### Respuestas Encontradas en Referencias para Arquitecto

architecture-overview.md:

- ¿Cuál es la decisión específica entre Celery y RQ? Respuesta: Elegir Celery desde el inicio porque aunque es más complejo, el ecosistema es más maduro, tiene mejor documentación, y la curva de aprendizaje adicional vale la pena por la flexibilidad futura. RQ podría ser un cuello de botella si el sistema escala.
- ¿Cómo se alinea esta decisión con el stack unificado en Python? Respuesta: Celery está mejor acoplado con el stack de Python y ofrece mayor control durante la programación y debugging.
- Referencia: docs/ingenieria/arquitectura/architecture-overview.md (líneas 42-46)

database-schema-design.md:

- ¿Cómo se implementa el retry strategy en el schema? Respuesta: Backoff exponencial con jitter aleatorio, máximo 5 reintentos por defecto, timeout de 5 minutos para todos los jobs.
- Referencia: docs/ingenieria/arquitectura/database-schema-design.md (líneas 458-462)

### Respuestas Encontradas en Referencias para Desarrollador

architecture-overview.md:

- ¿Qué significa "jobs efímeros" en la práctica? Respuesta: Jobs efímeros son procesos que se inician para ejecutar una tarea específica y terminan cuando la tarea completa. Jobs persistentes son procesos que quedan corriendo continuamente, esperando tareas en una cola. La diferencia es el ciclo de vida: efímeros = ciclo corto, persistentes = ciclo largo.
- Referencia: docs/ingenieria/arquitectura/architecture-overview.md (líneas 172)

adr-005-job-idempotency.md:

- ¿Cómo se implementa la idempotencia en relación con jobs efímeros? Respuesta: Locks en base de datos a nivel de documento con campo `job_locked_at` y `locked_by_job_id`, timeout configurable (default: 30 minutos), release automático cuando job completa o falla.
- Referencia: docs/ingenieria/decisiones/adr-005-job-idempotency.md (líneas 38-45)

### Gaps Identificados

No se identificaron gaps críticos. El documento proporciona contexto claro y completo para ambos roles.

### Correcciones Aplicadas

**Corrección de consistencia**: Se actualizó el ADR para reflejar la decisión específica de usar Celery (no "Celery o RQ") en las secciones de implementación específica y requerimientos de implementación, alineándolo con la decisión documentada en architecture-overview.md.

### Calificación del Documento: 9/10

**Desglose**:

- Completitud de Respuestas: 9/10 - El documento responde todas las preguntas clave para Arquitecto y Desarrollador tras la corrección de consistencia
- Contexto Multi-Rol: 9/10 - Excelente contexto para ambos roles. Senior tiene contexto estratégico y trade-offs. Junior tiene explicaciones claras de conceptos como "jobs efímeros" y la implementación práctica
- Calidad de Referencias: 9/10 - Referencias específicas a documentos relacionados con información relevante encontrada
- Estructura y Organización: 9/10 - Estructura clara con secciones bien definidas (Contexto, Decisiones, Justificación, Trade-offs, Alternativas, Consecuencias)
- Consistencia: 9/10 - Consistencia excelente tras la corrección aplicada

**Resumen**: El documento es excelente y bien estructurado, con fuerte contexto técnico y justificación clara de la decisión. No se identificaron gaps críticos durante el análisis. La calificación de 9/10 indica que el documento cumple con los estándares de calidad y no requiere gaps adicionales.
