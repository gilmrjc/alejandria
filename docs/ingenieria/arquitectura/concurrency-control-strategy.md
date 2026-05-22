---
id: ARC-019
type: Implementation Specification
rating: 9
rating-phase: document-editing
related:
  - target: ARC-005
    relationship_type: implements
    reason: Implementa la estrategia de manejo de concurrencia para endpoints de documentos
  - target: ADR-005
    relationship_type: contradicts
    reason: ADR-005 rechaza locks en base de datos en favor de Redis distributed locks; este documento evalúa ambas estrategias para contexto de edición de usuarios (distinto de jobs asíncronos)
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del schema de base de datos para implementación de control de concurrencia
  - target: ADR-006
    relationship_type: references
    reason: ADR-006 menciona uso de SELECT FOR UPDATE para versioning de documentos; este documento alinea la estrategia de concurrencia con esa decisión
---

# Concurrency Control Strategy — Alejandria

Este documento define la estrategia de manejo de concurrencia para ediciones simultáneas de documentos por múltiples usuarios.

## Índice

1. [Visión General](#1-visión-general)
2. [Análisis de Estrategias](#2-análisis-de-estrategias)
3. [Implementación Seleccionada](#3-implementación-seleccionada)
4. [Manejo de Conflictos](#4-manejo-de-conflictos)
5. [API Endpoints Modificados](#5-api-endpoints-modificados)
6. [Edge Cases](#6-edge-cases)
7. [Testing](#7-testing)

---

## 1. Visión General

### Propósito

Definir la estrategia para manejar ediciones concurrentes del mismo documento por múltiples usuarios, previniendo sobrescritura de cambios y conflictos de datos.

### Problema

Cuando múltiples usuarios editan el mismo documento simultáneamente, pueden ocurrir:

- Sobrescritura de cambios (last-write-wins)
- Pérdida de trabajo no guardado
- Conflicto de versiones

---

## 2. Análisis de Estrategias

Para manejar ediciones concurrentes de documentos, evaluamos tres estrategias principales con diferentes compensaciones entre prevención de conflictos, experiencia de usuario y complejidad de implementación.

### Optimistic Locking

El optimistic locking utiliza verificación de versiones para detectar conflictos en el momento de guardar cambios. Esta estrategia permite que múltiples usuarios editen simultáneamente el mismo documento, pero valida que la versión que se está guardando coincide con la versión actual en la base de datos. Si hay una discrepancia, indica que otro usuario modificó el documento y se rechaza el cambio.

La principal ventaja de esta estrategia es que no requiere locks persistentes en la base de datos, lo que resulta en mejor performance en escenarios de baja contención donde los conflictos son poco frecuentes. Además, permite ediciones concurrentes con detección de conflictos, lo que puede ser útil en ciertos contextos de colaboración.

Sin embargo, el optimistic locking tiene desventajas significativas. Requiere reintentos manuales cuando ocurren conflictos, lo que puede resultar en una experiencia de usuario frustrante si hay alta contención. Los usuarios pueden perder trabajo si no implementan mecanismos de guardado automático o merge de cambios.

### Pessimistic Locking

El pessimistic locking adquiere locks explícitos antes de permitir que un usuario edite un documento. Esta estrategia previene conflictos proactivamente al bloquear el recurso para otros usuarios mientras uno está editando, proporcionando una experiencia de usuario clara donde el documento aparece como "bloqueado" para otros.

La ventaja principal de esta estrategia es la prevención completa de conflictos. Los usuarios saben inmediatamente si un documento está siendo editado por otro, evitando que pierdan trabajo en ediciones que luego serían rechazadas. Esta claridad en la experiencia de usuario es especialmente valiosa en sistemas donde la colaboración síncrona no es un requisito crítico.

Las desventajas incluyen la necesidad de locks persistentes en la base de datos, lo que aumenta la complejidad del sistema. También puede causar deadlocks si no se implementa correctamente, y tiene menor performance en escenarios de alta contención donde muchos usuarios intentan editar los mismos documentos simultáneamente.

### ETags / HTTP Caching

Los ETags HTTP utilizan el mecanismo estándar de caché de HTTP para detectar cambios en documentos. Esta estrategia aprovecha la infraestructura existente de HTTP para implementar control de concurrencia, usando identificadores de versión que el cliente puede enviar para validar si el recurso ha cambiado.

Como ventaja, esta estrategia sigue el estándar HTTP y se integra naturalmente con APIs REST existentes, lo que puede simplificar la implementación en sistemas que ya utilizan ETags para otros propósitos de caché.

Sin embargo, los ETags requieren implementación específica en la capa HTTP y no previenen conflictos, solo los detecta. Similar al optimistic locking, los usuarios pueden encontrar frustrante la experiencia si hay alta contención, ya que sus cambios serían rechazados después de haberlos realizado.

---

## 3. Implementación Seleccionada

**Estrategia Seleccionada**: Pessimistic Locking con SELECT FOR UPDATE

**Justificación**:

- Previene conflictos completamente al bloquear el documento durante la edición
- Experiencia de usuario clara (documento bloqueado)
- Adecuado para MVP bootstrapped con baja contención esperada
- Implementación simple con PostgreSQL nativo
- Alineado con ADR-006 que menciona SELECT FOR UPDATE para versioning de documentos

**Nota sobre contradicción con ADR-005**:

ADR-005 rechaza locks en base de datos en favor de Redis distributed locks para **jobs asíncronos** (idempotencia de Celery tasks). Esta decisión es diferente del contexto de **edición síncrona de usuarios** por las siguientes razones:

- **Jobs asíncronos**: Requieren locks distribuidos para prevenir ejecución duplicada en múltiples workers, Redis es óptimo para este caso (latencia <1ms, escalabilidad distribuida)
- **Edición síncrona de usuarios**: Operación síncrona en transacción de base de datos, SELECT FOR UPDATE es más simple y mantiene integridad ACID
- **Contexto diferente**: ADR-005 previene duplicación de trabajo en background; este documento previene sobrescritura de ediciones concurrentes en tiempo real
- **Performance aceptable**: Para MVP bootstrapped con baja contención, la latencia de SELECT FOR UPDATE (5-10ms) es aceptable comparado con la complejidad de integrar Redis locks en el flujo síncrono de API

**Referencia**: ADR-006 (líneas 174-177), epica-02-api-rest-mcp-server.md (sección T-017)

### Componentes

- **Database Lock**: SELECT FOR UPDATE en PostgreSQL para adquirir lock exclusivo

- **Lock Acquisition**: Adquisición de lock al inicio de la transacción

- **Lock Release**: Liberación automática al commit o rollback

- **Retry Strategy**: Re-intento con backoff exponencial si el lock falla

- **Timeout**: Timeout configurable para evitar deadlocks indefinidos

---

## 4. Manejo de Conflictos

### Detección de Conflictos

**Algoritmo de Detección**:

1. Al iniciar una edición de documento, iniciar transacción PostgreSQL
2. Ejecutar `SELECT FOR UPDATE` sobre el registro del documento
3. Si el lock se adquiere exitosamente, proceder con la edición
4. Si el lock falla (otro usuario tiene el lock), retornar error 409 Conflict
5. Implementar retry con backoff exponencial: 1s, 2s, 4s, 8s, 16s con ±20% jitter
6. Máximo 5 reintentos antes de retornar error definitivo

**Ventajas de SELECT FOR UPDATE**:

- Lock exclusivo a nivel de fila en PostgreSQL
- Bloquea otros SELECT FOR UPDATE pero permite lecturas normales
- Liberación automática al commit/rollback de la transacción
- Deadlock detection automático de PostgreSQL

### Estrategias de Resolución

**Estrategia Principal**: Reject con Retry

- Rechazar cambios inmediatamente si el lock no puede adquirirse
- Retornar error 409 Conflict con mensaje claro
- Cliente puede reintentar automáticamente con backoff
- Usuario recibe notificación de que el documento está siendo editado

**No se implementa**:

- Merge automático (complejidad excesiva para MVP)
- Resolución manual (requiere UI compleja)

---

## 5. API Endpoints Modificados

### PUT /api/v1/documents/{id}

**Request**:

```json
{
  "title": "Updated Title",
  "content": "Updated content",
  "file_path": "/docs/doc.md"
}
```

**Response en Conflicto (409)**:

```json
{
  "error": "document_locked",
  "message": "Document is currently being edited by another user",
  "retry_after": 2
}
```

**Implementación en Código**:

```python
async def update_document(document_id: int, update_data: DocumentUpdate):
    max_retries = 5
    base_delay = 1  # segundo
    
    for attempt in range(max_retries):
        async with get_db_session() as session:
            try:
                # Adquirir lock con SELECT FOR UPDATE
                result = await session.execute(
                    select(Document).where(Document.id == document_id).with_for_update()
                )
                document = result.scalar_one()

                # Actualizar documento
                document.title = update_data.title
                document.content = update_data.content

                # Commit libera el lock automáticamente
                await session.commit()
                return document

            except OperationalError as e:
                await session.rollback()
                if "could not obtain lock" in str(e):
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)
                        delay = delay * (0.8 + random.random() * 0.4)  # ±20% jitter
                        await asyncio.sleep(delay)
                        continue
                    else:
                        raise HTTPException(
                            status_code=409,
                            detail={
                                "error": "document_locked",
                                "message": "Document is currently being edited by another user"
                            }
                        )
                else:
                    raise
```

---

## 6. Edge Cases

### Escenarios Identificados y Manejo

#### Usuario A edita mientras Usuario B edita

Cuando dos usuarios intentan editar el mismo documento simultáneamente, el primero en iniciar la transacción adquiere el lock mediante SELECT FOR UPDATE. El segundo usuario recibe un error 409 Conflict indicando que el documento está bloqueado. Este manejo es directo y proporciona feedback inmediato al usuario, quien puede reintentar automáticamente con el mecanismo de backoff implementado. La estrategia de retry con backoff exponencial (1s, 2s, 4s, 8s, 16s con jitter) evita que el usuario tenga que reintentar manualmente y reduce la carga en el sistema durante períodos de alta contención.

#### Usuario A guarda, Usuario B intenta guardar versión antigua

Este escenario no es aplicable con pessimistic locking porque Usuario B no puede adquirir el lock mientras Usuario A tiene la transacción abierta. A diferencia del optimistic locking donde un usuario podría editar basándose en una versión antigua y luego intentar guardar, con pessimistic locking el lock se adquiere al inicio de la transacción, previniendo que Usuario B incluso inicie una edición basada en datos obsoletos. Usuario B recibe un error 409 inmediatamente al intentar adquirir el lock, lo que simplifica el manejo de errores y evita situaciones donde el usuario pierde trabajo después de haber realizado ediciones extensas.

#### Ediciones en diferentes secciones del mismo documento

El pessimistic locking bloquea el documento completo, lo que significa que no se permite edición concurrente de diferentes secciones del mismo documento. Esta es una simplificación deliberada para el MVP bootstrapped: aunque sería posible implementar locks a nivel de sección o campo, esto aumentaría significativamente la complejidad del sistema. El trade-off es aceptable porque en un MVP con baja contención esperada, la probabilidad de que dos usuarios necesiten editar diferentes secciones del mismo documento simultáneamente es baja. Si este escenario se vuelve frecuente en el futuro, se puede evolucionar hacia una estrategia más granular.

#### Ediciones simultáneas en campos diferentes (title vs content)

Similar al caso anterior, el lock se aplica a nivel de documento completo, no a nivel de campo individual. Esto significa que no se permite edición concurrente de campos diferentes como title y content. Esta simplificación es aceptable para el MVP porque mantiene la implementación simple y predecible. La complejidad de implementar locks a nivel de campo (requiriendo múltiples locks por transacción, manejo de deadlocks más complejo, y mayor overhead en la base de datos) no se justifica para el caso de uso actual del sistema.

#### Deadlocks

PostgreSQL tiene detección automática de deadlocks, lo que significa que si dos transacciones están esperando locks que la otra tiene, PostgreSQL detecta esta condición y falla una de las transacciones con un error específico. El cliente debe reintentar la operación cuando recibe este error de deadlock. Aunque el pessimistic locking reduce la probabilidad de deadlocks comparado con estrategias más complejas de locking múltiple, no las elimina completamente. La implementación incluye manejo de errores de deadlock en el bloque de retry, permitiendo que el sistema se recupere automáticamente de estas situaciones.

#### Timeout de locks

Si una transacción queda abierta indefinidamente (por ejemplo, debido a un error en la aplicación que no hace rollback, o un problema de conectividad), el lock persistiría indefinidamente bloqueando el documento. Para prevenir esto, implementamos un timeout en la capa de aplicación (configurado a 5 minutos por defecto). Después de este timeout, se fuerza un rollback de la transacción y se libera el lock. Este mecanismo es un safeguard que asegura que los locks no persistan indefinidamente debido a errores de aplicación o problemas de infraestructura. El timeout debe ser configurado según los requisitos del negocio: demasiado corto puede interrumpir ediciones legítimas, demasiado largo puede bloquear documentos por períodos inaceptables.

---

## 7. Testing

### Unit Tests

```python
async def test_select_for_update_lock_acquisition():
    """Test que el lock se adquiere correctamente"""
    # Crear documento de prueba
    document = await create_test_document()

    # Iniciar transacción y adquirir lock
    async with get_db_session() as session:
        result = await session.execute(
            select(Document).where(Document.id == document.id).with_for_update()
        )
        locked_doc = result.scalar_one()

        # Verificar que el documento está bloqueado
        assert locked_doc.id == document.id

        # Intentar adquirir lock en otra sesión debe fallar
        async with get_db_session() as session2:
            try:
                await session2.execute(
                    select(Document).where(Document.id == document.id).with_for_update(nowait=True)
                )
                assert False, "Lock no debería ser adquirible"
            except OperationalError as e:
                assert "could not obtain lock" in str(e)

async def test_lock_release_on_commit():
    """Test que el lock se libera al commit"""
    document = await create_test_document()

    # Adquirir lock y hacer commit
    async with get_db_session() as session:
        await session.execute(
            select(Document).where(Document.id == document.id).with_for_update()
        )
        await session.commit()

    # Verificar que el lock se liberó
    async with get_db_session() as session2:
        result = await session2.execute(
            select(Document).where(Document.id == document.id).with_for_update(nowait=True)
        )
        doc = result.scalar_one()
        assert doc.id == document.id

async def test_lock_release_on_rollback():
    """Test que el lock se libera al rollback"""
    document = await create_test_document()

    # Adquirir lock y hacer rollback
    async with get_db_session() as session:
        await session.execute(
            select(Document).where(Document.id == document.id).with_for_update()
        )
        await session.rollback()

    # Verificar que el lock se liberó
    async with get_db_session() as session2:
        result = await session2.execute(
            select(Document).where(Document.id == document.id).with_for_update(nowait=True)
        )
        doc = result.scalar_one()
        assert doc.id == document.id

async def test_retry_with_backoff():
    """Test que el retry con backoff funciona"""
    document = await create_test_document()

    # Simular lock fallido con reintentos
    retry_count = 0
    max_retries = 3
    base_delay = 0.1  # 100ms para test rápido

    for attempt in range(max_retries):
        try:
            async with get_db_session() as session:
                await session.execute(
                    select(Document).where(Document.id == document.id).with_for_update(nowait=True)
                )
                break
        except OperationalError:
            retry_count += 1
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                await asyncio.sleep(delay)

    assert retry_count >= 0  # Verificar que se intentó retry
```

### Integration Tests

```python
async def test_concurrent_document_editions():
    """Test ediciones concurrentes del mismo documento"""
    document = await create_test_document()

    # Crear dos tareas concurrentes
    async def edit_document(user_id: int):
        async with get_db_session() as session:
            try:
                result = await session.execute(
                    select(Document).where(Document.id == document.id).with_for_update(nowait=True)
                )
                doc = result.scalar_one()
                doc.title = f"Edited by user {user_id}"
                await asyncio.sleep(0.1)  # Simular edición
                await session.commit()
                return True
            except OperationalError:
                await session.rollback()
                return False

    # Ejecutar concurrentemente
    results = await asyncio.gather(
        edit_document(1),
        edit_document(2),
        return_exceptions=True
    )

    # Verificar que solo una tuvo éxito
    successes = sum(1 for r in results if r is True)
    failures = sum(1 for r in results if r is False)
    assert successes == 1
    assert failures == 1

async def test_deadlock_detection():
    """Test detección de deadlocks de PostgreSQL"""
    doc1 = await create_test_document()
    doc2 = await create_test_document()

    # Crear escenario de deadlock potencial
    async def lock_order_1():
        async with get_db_session() as session1:
            await session1.execute(
                select(Document).where(Document.id == doc1.id).with_for_update()
            )
            await asyncio.sleep(0.1)
            try:
                await session1.execute(
                    select(Document).where(Document.id == doc2.id).with_for_update(nowait=True)
                )
                await session1.commit()
            except OperationalError as e:
                if "deadlock" in str(e).lower():
                    await session1.rollback()
                    return "deadlock_detected"
                raise

    async def lock_order_2():
        async with get_db_session() as session2:
            await session2.execute(
                select(Document).where(Document.id == doc2.id).with_for_update()
            )
            await asyncio.sleep(0.1)
            try:
                await session2.execute(
                    select(Document).where(Document.id == doc1.id).with_for_update(nowait=True)
                )
                await session2.commit()
            except OperationalError as e:
                if "deadlock" in str(e).lower():
                    await session2.rollback()
                    return "deadlock_detected"
                raise

    results = await asyncio.gather(lock_order_1(), lock_order_2(), return_exceptions=True)
    # Al menos una debería detectar deadlock o completar exitosamente
    assert len(results) == 2

async def test_lock_timeout():
    """Test timeout de locks largos"""
    document = await create_test_document()

    # Adquirir lock y mantenerlo
    async with get_db_session() as session1:
        await session1.execute(
            select(Document).where(Document.id == document.id).with_for_update()
        )
        # No hacer commit, mantener lock

        # Intentar adquirir lock con timeout corto
        async with get_db_session() as session2:
            try:
                await session2.execute(
                    select(Document).where(Document.id == document.id).with_for_update(nowait=True)
                )
                assert False, "No debería adquirir lock"
            except OperationalError as e:
                assert "could not obtain lock" in str(e)
```
