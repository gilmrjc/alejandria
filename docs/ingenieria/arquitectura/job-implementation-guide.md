---
id: ARC-007
type: Implementation Guide
rating:
rating-phase:
dependency: [ADR-004, ADR-005, ARC-002, ARC-004]
related:
  - target: ADR-004
    relationship_type: implements
    reason: Implementa la decisión de jobs efímeros con guía de implementación
  - target: ADR-005
    relationship_type: implements
    reason: Implementa la decisión de idempotencia de jobs con guía de implementación
  - target: ARC-004
    relationship_type: implements
    reason: Implementa el schema de base de datos con guía de implementación de jobs
---

# Job Implementation Guide — Alejandria

Este documento proporciona una guía paso a paso para implementar jobs de Celery en Alejandria. Los jobs orchestran el pipeline de 5 fases (detección → agrupación → resolución → verificación → aplicación) con retry strategy, idempotencia, y manejo de errores.

---

## Índice

1. [Visión General](#1-visión-general)
2. [Arquitectura de Jobs](#2-arquitectura-de-jobs)
3. [Implementación de Jobs](#3-implementación-de-jobs)
4. [Retry Strategy](#4-retry-strategy)
5. [Idempotencia](#5-idempotencia)
6. [Chains de Celery](#6-chains-de-celery)
7. [Testing de Jobs](#7-testing-de-jobs)
8. [Debugging en Desarrollo](#8-debugging-en-desarrollo)

---

## 1. Visión General

### Stack de Jobs

- **Framework**: Celery o RQ (decisión pendiente para MVP)
- **Broker**: Redis
- **Backend**: PostgreSQL (para persistencia de resultados)
- **Workers**: Efímeros, escalables según demanda (ver ADR-004)

### Tipos de Jobs

| Job | Fase | Agente | Descripción |
|-----|------|--------|-------------|
| gap_detection | Detección | Agente 1 | Detecta gaps en documento |
| question_grouping | Agrupación | Agente 2 | Agrupa gaps por tema |
| gap_verification | Verificación | Agente 1 | Verifica respuestas |
| suggestion_application | Aplicación | Agente 4 | Aplica cambios al documento |
| snapshot_cleanup | Mantenimiento | Sistema | Limpia snapshots antiguos |

### Referencias

- **[ADR-004: Jobs Efímeros vs Persistentes](../decisiones/adr-004-ephemeral-jobs.md)**: Justificación de jobs efímeros
- **[ADR-005: Idempotencia de Jobs](../decisiones/adr-005-job-idempotency.md)**: Locks y estrategia de idempotencia
- **[end-to-end-flow.md](end-to-end-flow.md)**: Flujo detallado del pipeline
- **[database-schema-design.md](database-schema-design.md)**: Diseño conceptual de esquema de base de datos

---

## 2. Arquitectura de Jobs

### Estructura de Proyecto

```
alejandria/
├── alejandria/
│   ├── jobs/
│   │   ├── __init__.py
│   │   ├── base.py          # Job base con retry y logging
│   │   ├── gap_detection.py
│   │   ├── question_grouping.py
│   │   ├── gap_verification.py
│   │   ├── suggestion_application.py
│   │   └── snapshot_cleanup.py
│   ├── celery_app.py        # Configuración de Celery
│   └── mcp_server.py         # MCP Server para agentes
├── tests/
│   └── jobs/
│       ├── test_gap_detection.py
│       └── ...
└── docker-compose.yml        # Orquestación local
```

### Configuración de Celery

```python
# alejandria/celery_app.py
from celery import Celery
from alejandria.config import settings

celery_app = Celery(
    "alejandria",
    broker=settings.redis_url,
    backend=settings.postgres_url,
    include=[
        "alejandria.jobs.gap_detection",
        "alejandria.jobs.question_grouping",
        "alejandria.jobs.gap_verification",
        "alejandria.jobs.suggestion_application",
        "alejandria.jobs.snapshot_cleanup",
    ]
)

# Configuración de retry
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutos timeout
    task_soft_time_limit=280,  # 4:40 minutos soft limit
    task_acks_late=True,  # ACK solo si task completa
    worker_prefetch_multiplier=1,  # Un task a la vez por worker
)
```

---

## 3. Implementación de Jobs

### Job Base

```python
# alejandria/jobs/base.py
from celery import Task
from alejandria.database import db
from alejandria.models import Job
import logging

logger = logging.getLogger(__name__)

class BaseJob(Task):
    """Base class for all jobs with retry and logging."""
    
    def __call__(self, *args, **kwargs):
        job_id = self.request.id
        logger.info(f"Starting job {self.name} with id {job_id}")
        
        # Actualizar estado en base de datos
        job = db.query(Job).filter(Job.id == job_id).first()
        if job:
            job.status = "running"
            job.started_at = datetime.now()
            db.commit()
        
        try:
            result = super().__call__(*args, **kwargs)
            
            # Actualizar estado a completed
            if job:
                job.status = "completed"
                job.completed_at = datetime.now()
                db.commit()
            
            logger.info(f"Job {self.name} completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Job {self.name} failed: {str(e)}")
            
            # Actualizar estado a failed
            if job:
                job.status = "failed"
                job.error_message = str(e)
                job.retry_count += 1
                db.commit()
            
            raise
```

### gap_detection Job

```python
# alejandria/jobs/gap_detection.py
from celery import shared_task
from alejandria.jobs.base import BaseJob
from alejandria.mcp_server import mcp
from alejandria.database import db
from alejandria.models import Session, Gap, Document
import logging

logger = logging.getLogger(__name__)

@shared_task(
    base=BaseJob,
    bind=True,
    max_retries=5,
    default_retry_delay=60,  # 1 minuto inicial
)
def gap_detection(self, session_id: str):
    """
    Detecta gaps en un documento usando Agente 1.
    
    Args:
        session_id: ID de la sesión
    """
    logger.info(f"Starting gap detection for session {session_id}")
    
    # Adquirir lock en sesión (idempotencia)
    if not acquire_session_lock(session_id, self.request.id):
        logger.warning(f"Session {session_id} is locked, skipping")
        return
    
    try:
        # Obtener sesión y documento
        session = db.query(Session).filter(Session.id == session_id).first()
        document = db.query(Document).filter(Document.id == session.document_id).first()
        
        # Llamar tool MCP para leer documento
        doc_content = mcp.call_tool("read_document", {
            "document_id": str(document.id)
        })
        
        # Llamar prompt MCP para detección
        gaps = mcp.call_prompt("gap_detection_prompt", {
            "document_type": "architecture",
            "document_content": doc_content["content"],
            "target_audience": "senior",
            "perspective": "technical"
        })
        
        # Guardar gaps en base de datos
        for gap_data in gaps:
            gap = Gap(
                session_id=session_id,
                question=gap_data["question"],
                context_missing=gap_data["context_missing"],
                priority=gap_data["priority"],
                role_affected=gap_data["role_affected"],
                status="pending"
            )
            db.add(gap)
        
        # Actualizar estado de sesión
        session.status = "grouping"
        db.commit()
        
        # Encolar siguiente job
        from alejandria.jobs.question_grouping import question_grouping
        question_grouping.delay(session_id)
        
        logger.info(f"Gap detection completed for session {session_id}")
        
    finally:
        # Liberar lock
        release_session_lock(session_id, self.request.id)
```

### question_grouping Job

```python
# alejandria/jobs/question_grouping.py
from celery import shared_task
from alejandria.jobs.base import BaseJob
from alejandria.mcp_server import mcp
from alejandria.database import db
from alejandria.models import Session, Gap, GapGroup, GapGroupItem
import logging

logger = logging.getLogger(__name__)

@shared_task(
    base=BaseJob,
    bind=True,
    max_retries=5,
    default_retry_delay=60,
)
def question_grouping(self, session_id: str):
    """
    Agrupa gaps por tema usando Agente 2.
    
    Args:
        session_id: ID de la sesión
    """
    logger.info(f"Starting question grouping for session {session_id}")
    
    if not acquire_session_lock(session_id, self.request.id):
        logger.warning(f"Session {session_id} is locked, skipping")
        return
    
    try:
        # Obtener gaps de la sesión
        gaps = db.query(Gap).filter(
            Gap.session_id == session_id,
            Gap.status == "pending"
        ).all()
        
        gaps_json = [gap.to_dict() for gap in gaps]
        
        # Llamar prompt MCP para agrupación
        groups = mcp.call_prompt("grouping_prompt", {
            "gaps_json": gaps_json
        })
        
        # Guardar grupos en base de datos
        for group_data in groups:
            group = GapGroup(
                session_id=session_id,
                name=group_data["name"],
                description=group_data["description"]
            )
            db.add(group)
            db.flush()
            
            # Asociar gaps al grupo
            for gap_id in group_data["gap_ids"]:
                item = GapGroupItem(
                    gap_group_id=group.id,
                    gap_id=gap_id
                )
                db.add(item)
        
        # Actualizar estado de sesión
        session = db.query(Session).filter(Session.id == session_id).first()
        session.status = "awaiting_resolution"
        db.commit()
        
        logger.info(f"Question grouping completed for session {session_id}")
        
    finally:
        release_session_lock(session_id, self.request.id)
```

### gap_verification Job

```python
# alejandria/jobs/gap_verification.py
from celery import shared_task
from alejandria.jobs.base import BaseJob
from alejandria.mcp_server import mcp
from alejandria.database import db
from alejandria.models import Session, Gap
import logging

logger = logging.getLogger(__name__)

@shared_task(
    base=BaseJob,
    bind=True,
    max_retries=5,
    default_retry_delay=60,
)
def gap_verification(self, session_id: str):
    """
    Verifica respuestas usando Agente 1.
    
    Args:
        session_id: ID de la sesión
    """
    logger.info(f"Starting gap verification for session {session_id}")
    
    if not acquire_session_lock(session_id, self.request.id):
        logger.warning(f"Session {session_id} is locked, skipping")
        return
    
    try:
        # Obtener gaps respondidos
        gaps = db.query(Gap).filter(
            Gap.session_id == session_id,
            Gap.status == "responded"
        ).all()
        
        gaps_json = [gap.to_dict() for gap in gaps]
        responses_json = [{"gap_id": g.id, "answer": g.answer} for g in gaps]
        
        # Llamar prompt MCP para verificación
        verification = mcp.call_prompt("verification_prompt", {
            "gaps_json": gaps_json,
            "responses_json": responses_json
        })
        
        session = db.query(Session).filter(Session.id == session_id).first()
        
        if verification["new_gaps"]:
            # Hay nuevos gaps, incrementar round y volver a grouping
            session.round += 1
            session.status = "grouping"
            
            # Guardar nuevos gaps
            for gap_data in verification["new_gaps"]:
                gap = Gap(
                    session_id=session_id,
                    question=gap_data["question"],
                    context_missing=gap_data["context_missing"],
                    priority=gap_data["priority"],
                    role_affected=gap_data["role_affected"],
                    status="pending"
                )
                db.add(gap)
            
            db.commit()
            
            # Reencolar question_grouping
            from alejandria.jobs.question_grouping import question_grouping
            question_grouping.delay(session_id)
            
            logger.info(f"New gaps detected, round {session.round}")
            
        else:
            # No hay nuevos gaps, pasar a aplicación
            session.status = "applying"
            db.commit()
            
            # Encolar suggestion_application
            from alejandria.jobs.suggestion_application import suggestion_application
            suggestion_application.delay(session_id)
            
            logger.info(f"Verification passed, proceeding to application")
        
    finally:
        release_session_lock(session_id, self.request.id)
```

### suggestion_application Job

```python
# alejandria/jobs/suggestion_application.py
from celery import shared_task
from alejandria.jobs.base import BaseJob
from alejandria.mcp_server import mcp
from alejandria.database import db
from alejandria.models import Session, Document, ContextEntry
import logging

logger = logging.getLogger(__name__)

@shared_task(
    base=BaseJob,
    bind=True,
    max_retries=5,
    default_retry_delay=60,
)
def suggestion_application(self, session_id: str):
    """
    Aplica cambios sugeridos usando Agente 4.
    
    Args:
        session_id: ID de la sesión
    """
    logger.info(f"Starting suggestion application for session {session_id}")
    
    if not acquire_session_lock(session_id, self.request.id):
        logger.warning(f"Session {session_id} is locked, skipping")
        return
    
    try:
        # Obtener contexto de cambios
        session = db.query(Session).filter(Session.id == session_id).first()
        document = db.query(Document).filter(Document.id == session.document_id).first()
        
        context_entries = db.query(ContextEntry).filter(
            ContextEntry.session_id == session_id,
            ContextEntry.applied == False
        ).all()
        
        context_entries_json = [ce.to_dict() for ce in context_entries]
        
        # Llamar tool MCP para aplicar cambios
        result = mcp.call_tool("apply_changes", {
            "session_id": session_id,
            "context_entry_ids": [ce.id for ce in context_entries]
        })
        
        # Actualizar documento
        document.healthy = True
        document.updated_by = self.request.id
        
        # Actualizar estado de sesión
        session.status = "done"
        db.commit()
        
        logger.info(f"Suggestion application completed for session {session_id}")
        
    finally:
        release_session_lock(session_id, self.request.id)
```

### snapshot_cleanup Job

```python
# alejandria/jobs/snapshot_cleanup.py
from celery import shared_task
from alejandria.jobs.base import BaseJob
from alejandria.database import db
from alejandria.models import DocumentSnapshot
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@shared_task(
    base=BaseJob,
    bind=True,
    max_retries=3,
    default_retry_delay=300,  # 5 minutos
)
def snapshot_cleanup(self):
    """
    Limpia snapshots antiguos (>90 días).
    """
    logger.info("Starting snapshot cleanup")
    
    # Calcular fecha de corte
    cutoff_date = datetime.now() - timedelta(days=90)
    
    # Eliminar snapshots antiguos
    deleted_count = db.query(DocumentSnapshot).filter(
        DocumentSnapshot.created_at < cutoff_date
    ).delete()
    
    db.commit()
    
    logger.info(f"Snapshot cleanup completed, deleted {deleted_count} snapshots")
```

---

## 4. Retry Strategy

### Backoff Exponencial con Jitter

```python
import random
import time

def exponential_backoff(retry_count: int, base_delay: int = 60) -> int:
    """
    Calcula delay con backoff exponencial y jitter aleatorio.
    
    Args:
        retry_count: Número de reintentos actuales
        base_delay: Delay base en segundos
    
    Returns:
        Delay en segundos
    """
    # Backoff exponencial: base * 2^retry_count
    exponential_delay = base_delay * (2 ** retry_count)
    
    # Jitter aleatorio: ±20% del delay
    jitter = random.uniform(0.8, 1.2)
    
    delay = int(exponential_delay * jitter)
    
    # Limitar a máximo 1 hora
    return min(delay, 3600)
```

### Ejemplo de Reintentos

| Retry | Delay (seg) | Jitter | Delay Final |
|-------|-------------|--------|-------------|
| 1 | 60 | 0.9-1.1 | 54-66 |
| 2 | 120 | 0.9-1.1 | 108-132 |
| 3 | 240 | 0.9-1.1 | 216-264 |
| 4 | 480 | 0.9-1.1 | 432-528 |
| 5 | 960 | 0.9-1.1 | 864-1056 (limitado a 3600) |

### Configuración en Celery

```python
@shared_task(
    bind=True,
    max_retries=5,
    default_retry_delay=60,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    retry_backoff_max=3600,
    retry_jitter=True,
)
def my_job(self, *args, **kwargs):
    # Implementación del job
    pass
```

---

## 5. Idempotencia

### Funciones de Lock

```python
# alejandria/jobs/locks.py
from datetime import datetime, timedelta
from alejandria.database import db
from alejandria.models import Session

def acquire_session_lock(session_id: str, job_id: str, timeout: int = 30) -> bool:
    """
    Adquiere lock en una sesión para idempotencia.
    
    Args:
        session_id: ID de la sesión
        job_id: ID del job
        timeout: Timeout del lock en minutos
    
    Returns:
        True si el lock fue adquirido, False si ya está locked
    """
    lock_expiry = datetime.now() + timedelta(minutes=timeout)
    
    result = db.execute("""
        UPDATE sessions
        SET job_locked_at = %s,
            locked_by_job_id = %s
        WHERE id = %s
        AND (job_locked_at IS NULL OR job_locked_at < NOW())
        RETURNING id
    """, (lock_expiry, job_id, session_id))
    
    return result.rowcount > 0


def release_session_lock(session_id: str, job_id: str) -> None:
    """
    Libera lock en una sesión.
    
    Args:
        session_id: ID de la sesión
        job_id: ID del job
    """
    db.execute("""
        UPDATE sessions
        SET job_locked_at = NULL,
            locked_by_job_id = NULL
        WHERE id = %s
        AND locked_by_job_id = %s
    """, (session_id, job_id))
```

### Uso en Jobs

```python
@shared_task(bind=True)
def my_job(self, session_id: str):
    # Adquirir lock
    if not acquire_session_lock(session_id, self.request.id):
        logger.warning(f"Session {session_id} is locked, skipping")
        return
    
    try:
        # Lógica del job
        pass
    finally:
        # Liberar lock
        release_session_lock(session_id, self.request.id)
```

---

## 6. Chains de Celery

### Chain Simple

```python
from celery import chain

# Encadenar jobs secuencialmente
workflow = chain(
    gap_detection.s(session_id),
    question_grouping.s(session_id),
    gap_verification.s(session_id),
    suggestion_application.s(session_id)
)

workflow.delay()
```

### Chain con Callbacks

```python
from celery import chain, group

# Ejecutar jobs en paralelo y luego unir resultados
workflow = chain(
    gap_detection.s(session_id),
    group(
        question_grouping.s(session_id),
        search_similar_documents.s(session_id)
    ),
    gap_verification.s(session_id)
)

workflow.delay()
```

### Chain Condicional

```python
from celery import chain

def on_verification_success(result):
    if result["new_gaps"]:
        return question_grouping.s(session_id)
    else:
        return suggestion_application.s(session_id)

workflow = chain(
    gap_detection.s(session_id),
    question_grouping.s(session_id),
    gap_verification.s(session_id).apply_async(
        link=on_verification_success
    )
)
```

---

## 7. Testing de Jobs

### Test de gap_detection

```python
# tests/jobs/test_gap_detection.py
import pytest
from alejandria.jobs.gap_detection import gap_detection
from alejandria.database import db
from alejandria.models import Session, Document, Gap
from unittest.mock import patch

@pytest.fixture
def session_with_document():
    document = Document(
        title="Test Document",
        content="# Test\n\nContent",
        file_path="/test.md"
    )
    db.add(document)
    db.flush()
    
    session = Session(
        document_id=document.id,
        status="gap_detection"
    )
    db.add(session)
    db.commit()
    
    return session

def test_gap_detection_creates_gaps(session_with_document):
    """Test que gap_detection crea gaps correctamente."""
    
    # Mock MCP call
    with patch('alejandria.mcp_server.mcp.call_tool') as mock_read:
        with patch('alejandria.mcp_server.mcp.call_prompt') as mock_detect:
            mock_read.return_value = {
                "content": "# Test\n\nContent"
            }
            mock_detect.return_value = [
                {
                    "question": "Test question",
                    "context_missing": "Missing context",
                    "priority": "high",
                    "role_affected": "Senior"
                }
            ]
            
            # Ejecutar job
            gap_detection(str(session_with_document.id))
            
            # Verificar que se creó el gap
            gaps = db.query(Gap).filter(
                Gap.session_id == session_with_document.id
            ).all()
            
            assert len(gaps) == 1
            assert gaps[0].question == "Test question"
            assert gaps[0].status == "pending"

def test_gap_detection_idempotent(session_with_document):
    """Test que gap_detection es idempotente."""
    
    # Adquirir lock manualmente
    from alejandria.jobs.locks import acquire_session_lock
    acquire_session_lock(str(session_with_document.id), "test_job_id")
    
    # Intentar ejecutar job
    gap_detection(str(session_with_document.id))
    
    # Verificar que no se crearon gaps (por lock)
    gaps = db.query(Gap).filter(
        Gap.session_id == session_with_document.id
    ).all()
    
    assert len(gaps) == 0
```

### Test de Retry Strategy

```python
def test_gap_detection_retry_on_failure(session_with_document):
    """Test que gap_detection reintenta en fallo."""
    
    with patch('alejandria.mcp_server.mcp.call_tool') as mock_read:
        # Simular fallo transitorio
        mock_read.side_effect = [
            ConnectionError("Network error"),
            {"content": "# Test\n\nContent"}  # Segundo intento exitoso
        ]
        
        with patch('alejandria.mcp_server.mcp.call_prompt') as mock_detect:
            mock_detect.return_value = []
            
            # Ejecutar job con retry
            task = gap_detection.apply_async(
                args=[str(session_with_document.id)],
                retry=True
            )
            
            # Verificar que se reintentó
            assert task.retry_count == 1
```

---

## 8. Debugging en Desarrollo

### Ejecutar Jobs Manualmente

```python
# En shell de Python
from alejandria.jobs.gap_detection import gap_detection

# Ejecutar job sincrónicamente para debugging
result = gap_detection.apply(args=["session_uuid"], throw=True)
```

### Ver Logs de Celery

```bash
# Ver logs de worker
celery -A alejandria.celery_app worker --loglevel=info

# Ver logs de tareas específicas
celery -A alejandria.celery_app worker --loglevel=debug -Q gap_detection
```

### Monitorear Jobs con Flower

```bash
# Instalar flower
pip install flower

# Iniciar flower
celery -A alejandria.celery_app flower

# Acceder a http://localhost:5555
```

### Debuggear con pdb

```python
# Agregar breakpoint en job
@shared_task(bind=True)
def my_job(self, session_id: str):
    import pdb; pdb.set_trace()
    
    # Lógica del job
    pass
```

### Inspeccionar Estado de Jobs

```python
from alejandria.database import db
from alejandria.models import Job

# Ver jobs fallidos
failed_jobs = db.query(Job).filter(Job.status == "failed").all()

for job in failed_jobs:
    print(f"Job {job.id}: {job.error_message}")
    print(f"Retry count: {job.retry_count}")
```

---

## Análisis de Documento

**ESTADO DEL ANÁLISIS**
- Análisis previo: NO
- Fecha de análisis: 2026-05-22
- Versión del análisis: 1

**CLASIFICACIÓN DEL DOCUMENTO**
- Tipo: Documento de Implementación Técnica
- Rol Principal: Desarrollador
- Roles a Revisar: Desarrollador + DevOps/SRE (+ QA/Tester)
- Enfoque: Guía de implementación de jobs Celery para pipeline de 5 fases
- Perspectiva: Senior + Junior
- Fecha de análisis: 2026-05-22
- Versión del análisis: 1

### Revisión por Rol: Desarrollador (Senior)

**Validación de Respuestas Existentes**
El documento proporciona código Python completo para implementación de jobs (gap_detection, question_grouping, gap_verification, suggestion_application, snapshot_cleanup), configuración de Celery, retry strategy con backoff exponencial, funciones de locks para idempotencia, y ejemplos de testing. Las referencias a ADRs justifican decisiones arquitectónicas.

**Gaps Identificados**

**IMPLEMENTACIÓN TÉCNICA**

**GAP: Decisión entre Celery y RQ** [PRIORIDAD: Alto] [ESTADO: PENDIENTE]
- **Pregunta**: ¿Por qué la decisión entre Celery y RQ está pendiente? ¿Qué criterios se usarán para decidir? ¿Cuáles son los trade-offs entre ambos frameworks?
- **Contexto faltante**: El documento menciona "decisión pendiente para MVP" pero no proporciona análisis comparativo de Celery vs RQ ni criterios para la decisión.
- **Rol afectado**: Desarrollador Senior
- **Fecha de identificación**: 2026-05-22

**GAP: Estrategia de manejo de dead letter queues** [PRIORIDAD: Alto] [ESTADO: PENDIENTE]
- **Pregunta**: ¿Cómo se manejan jobs que fallan permanentemente después de max_retries? ¿Hay dead letter queue? ¿Cómo se monitorean y procesan estos jobs fallidos?
- **Contexto faltante**: El documento define retry strategy pero no menciona dead letter queues o manejo de jobs que exceden max_retries permanentemente.
- **Rol afectado**: Desarrollador Senior
- **Fecha de identificación**: 2026-05-22

**GAP: Estrategia de rollback de jobs fallidos** [PRIORIDAD: Medio] [ESTADO: PENDIENTE]
- **Pregunta**: ¿Qué sucede si un job falla a mitad de ejecución después de haber modificado estado? ¿Hay mecanismo de rollback o compensating transactions?
- **Contexto faltante**: Los jobs modifican estado de base de datos pero no hay información sobre rollback o compensating transactions si un job falla parcialmente.
- **Rol afectado**: Desarrollador Senior
- **Fecha de identificación**: 2026-05-22

### Revisión por Rol: Desarrollador (Junior)

**Gaps Identificados**

**IMPLEMENTACIÓN TÉCNICA**

**GAP: Explicación de Celery** [PRIORIDAD: Medio] [ESTADO: PENDIENTE]
- **Pregunta**: ¿Qué es Celery y cómo funciona como task queue? ¿Por qué se necesita un task queue en este sistema?
- **Contexto faltante**: El documento asume conocimiento de task queues pero no explica qué son Celery/RQ, por qué se necesitan, o cómo funcionan en el contexto de Alejandria.
- **Rol afectado**: Desarrollador Junior
- **Fecha de identificación**: 2026-05-22

**GAP: Explicación de backoff exponencial** [PRIORIDAD: Bajo] [ESTADO: PENDIENTE]
- **Pregunta**: ¿Qué es backoff exponencial y por qué se usa? ¿Por qué se agrega jitter aleatorio? ¿Cuáles son los beneficios de este enfoque?
- **Contexto faltante**: El documento muestra código de backoff exponencial pero no explica el concepto, por qué se usa, o los beneficios del jitter.
- **Rol afectado**: Desarrollador Junior
- **Fecha de identificación**: 2026-05-22

### Revisión por Rol: DevOps/SRE (Senior)

**Validación de Respuestas Existentes**
El documento incluye configuración de Celery, timeouts de jobs (5 minutos), y menciona workers efímeros escalables. Hay información sobre debugging con Flower y pdb.

**Gaps Identificados**

**OPERACIONES Y DESPLIEGUE**

**GAP: Estrategia de escalado de workers** [PRIORIDAD: Alto] [ESTADO: PENDIENTE]
- **Pregunta**: ¿Cómo se escalan los workers de Celery? ¿Qué métricas se usan para decidir cuándo escalar? ¿Es autoscaling o manual? ¿Cuál es la configuración de autoscaling?
- **Contexto faltante**: El documento menciona "workers efímeros, escalables según demanda" pero no detalla la estrategia de escalado, métricas, o configuración de autoscaling.
- **Rol afectado**: DevOps/SRE Senior
- **Fecha de identificación**: 2026-05-22

**GAP: Monitoreo de jobs y workers** [PRIORIDAD: Alto] [ESTADO: PENDIENTE]
- **Pregunta**: ¿Qué métricas se monitorean de jobs y workers? ¿Qué alertas se configuran? ¿Cuáles son los SLOs para ejecución de jobs? ¿Cómo se monitorea queue depth?
- **Contexto faltante**: No hay información sobre monitoreo de jobs, métricas clave, alertas, o SLOs para el sistema de task queue.
- **Rol afectado**: DevOps/SRE Senior
- **Fecha de identificación**: 2026-05-22

**GAP: Estrategia de despliegue de workers** [PRIORIDAD: Medio] [ESTADO: PENDIENTE]
- **Pregunta**: ¿Cómo se despliegan los workers en producción? ¿Se ejecutan como contenedores, servicios systemd, o serverless? ¿Qué configuración de infraestructura se necesita?
- **Contexto faltante**: No hay información sobre estrategia de despliegue de workers, tipo de infraestructura, o configuración necesaria.
- **Rol afectado**: DevOps/SRE Senior
- **Fecha de identificación**: 2026-05-22

### Revisión por Rol: DevOps/SRE (Junior)

**Gaps Identificados**

**OPERACIONES Y DESPLIEGUE**

**GAP: Configuración de Redis para producción** [PRIORIDAD: Alto] [ESTADO: PENDIENTE]
- **Pregunta**: ¿Qué configuración específica de Redis se necesita para Celery en producción? ¿Qué parámetros de persistencia se configuran? ¿Cómo se escala Redis?
- **Contexto faltante**: Redis se menciona como broker pero no hay detalles de configuración para producción, persistencia, o escalabilidad para task queues.
- **Rol afectado**: DevOps/SRE Junior
- **Fecha de identificación**: 2026-05-22

**GAP: Proceso de restart de workers** [PRIORIDAD: Medio] [ESTADO: PENDIENTE]
- **Pregunta**: ¿Cómo se reinician los workers sin perder jobs en ejecución? ¿Qué proceso se sigue para graceful shutdown? ¿Cómo se maneja jobs en progreso durante deploy?
- **Contexto faltante**: No hay información sobre proceso de restart, graceful shutdown, o manejo de jobs en progreso durante despliegues.
- **Rol afectado**: DevOps/SRE Junior
- **Fecha de identificación**: 2026-05-22

### Revisión por Rol: QA/Tester (Senior)

**Validación de Respuestas Existentes**
El documento incluye ejemplos de tests unitarios para gap_detection con mocking de MCP calls. Hay información sobre debugging con pdb y Flower.

**Gaps Identificados**

**OPERACIONES Y DESPLIEGUE**

**GAP: Estrategia de testing de integración de jobs** [PRIORIDAD: Alto] [ESTADO: PENDIENTE]
- **Pregunta**: ¿Cómo se testean jobs en un entorno de integración con Redis y PostgreSQL reales? ¿Qué estrategia se usa para limpiar estado entre tests? ¿Hay fixtures de datos?
- **Contexto faltante**: Los ejemplos de tests son unitarios con mocks. No hay información sobre testing de integración con dependencias reales o estrategia de limpieza de estado.
- **Rol afectado**: QA/Tester Senior
- **Fecha de identificación**: 2026-05-22

**GAP: Testing de retry strategy y locks** [PRIORIDAD: Alto] [ESTADO: PENDIENTE]
- **Pregunta**: ¿Cómo se testea la retry strategy? ¿Cómo se simulan fallos transitorios? ¿Cómo se testea la adquisición y liberación de locks?
- **Contexto faltante**: No hay información sobre testing de retry strategy, simulación de fallos, o testing de locks de idempotencia.
- **Rol afectado**: QA/Tester Senior
- **Fecha de identificación**: 2026-05-22

**GAP: Testing de chains de Celery** [PRIORIDAD: Medio] [ESTADO: PENDIENTE]
- **Pregunta**: ¿Cómo se testean chains de Celery? ¿Se testean jobs individualmente o como chains completas? ¿Cómo se mockean dependencias entre jobs?
- **Contexto faltante**: El documento muestra ejemplos de chains pero no detalla cómo se testean, si se testean individualmente o como chains completas.
- **Rol afectado**: QA/Tester Senior
- **Fecha de identificación**: 2026-05-22

### Revisión por Rol: QA/Tester (Junior)

**Gaps Identificados**

**OPERACIONES Y DESPLIEGUE**

**GAP: Proceso de manual testing de jobs** [PRIORIDAD: Medio] [ESTADO: PENDIENTE]
- **Pregunta**: ¿Cómo se puede ejecutar un job manualmente para testing? ¿Qué comandos se usan? ¿Cómo se verifica el resultado de un job manual?
- **Contexto faltante**: El documento menciona ejecución manual con `apply()` pero no detalla el proceso paso a paso para manual testing de jobs.
- **Rol afectado**: QA/Tester Junior
- **Fecha de identificación**: 2026-05-22

**GAP: Casos de prueba de ejemplo para jobs** [PRIORIDAD: Bajo] [ESTADO: PENDIENTE]
- **Pregunta**: ¿Cuáles son algunos casos de prueba de ejemplo para cada tipo de job? ¿Qué escenarios happy path y edge cases deberían probarse?
- **Contexto faltante**: Solo hay un ejemplo de test para gap_detection. No hay ejemplos para otros jobs ni escenarios de edge cases.
- **Rol afectado**: QA/Tester Junior
- **Fecha de identificación**: 2026-05-22

### CALIFICACIÓN DEL DOCUMENTO: 8/10

**Desglose**:
- Completitud de Respuestas: 8/10 - Cubre implementación de jobs, configuración de Celery, retry strategy, locks, y ejemplos de testing. Falta contexto sobre decisión Celery vs RQ, dead letter queues, y monitoreo.
- Contexto Multi-Rol: 8/10 - Proporciona contexto técnico sólido para desarrolladores. Falta contexto para DevOps/SRE (estrategia de escalado y monitoreo) y QA/Tester (testing de integración).
- Calidad de Referencias: 8/10 - Referencias a ADRs son relevantes. Faltan referencias a documentación de Celery, best practices de task queues, o patrones de retry.
- Estructura y Organización: 9/10 - Estructura excelente con índice, secciones bien organizadas, código bien formateado y comentado.
- Consistencia: 9/10 - No se detectaron contradicciones, la implementación es consistente con el pipeline descrito y ADRs.

**Resumen**: Guía de implementación de jobs completa con código Python detallado, configuración de Celery, retry strategy, locks de idempotencia, y ejemplos de testing. Falta contexto estratégico para decisiones técnicas (Celery vs RQ) y aspectos operacionales (escalado de workers, monitoreo, dead letter queues). El documento es muy útil para implementación pero requiere complemento con documentos de operaciones y decisión de framework de task queue.

---

## Referencias

- **[ADR-004: Jobs Efímeros vs Persistentes](../decisiones/adr-004-ephemeral-jobs.md)**: Justificación de jobs efímeros
- **[ADR-005: Idempotencia de Jobs](../decisiones/adr-005-job-idempotency.md)**: Locks y estrategia de idempotencia
- **[end-to-end-flow.md](end-to-end-flow.md)**: Flujo detallado del pipeline
- **[database-schema-design.md](database-schema-design.md)**: Diseño conceptual de esquema de base de datos
- **[api-specification.md](api-specification.md)**: Endpoints de API para jobs

---

*Documento generado como parte de [ARC-004](database-schema-design.md).*
*Fecha de creación: 2026-05-22.*
