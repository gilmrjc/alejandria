---
id: ARC-015
type: Implementation Guide
rating: 9.0
rating-phase: document-editing
related:
  - target: EPC-004
    relationship_type: implements
    reason: Implementa la guía de configuración de Celery para Épica 4
  - target: ADR-004
    relationship_type: references
    reason: Referencia ADR-004 para estrategia de retry con backoff exponencial
  - target: ADR-005
    relationship_type: references
    reason: Referencia ADR-005 para estrategia de idempotencia con locks distribuidos
  - target: ARC-007
    relationship_type: extends
    reason: Extiende job-implementation-guide con detalles específicos de Celery
---

# Celery Implementation Guide - Alejandria

Este documento proporciona una guía completa para implementar y configurar Celery workers en Alejandria. Para la guía general de implementación de jobs, ver [job-implementation-guide.md](./job-implementation-guide.md). Para ADRs relacionados, ver [ADR-004](../decisiones/adr-004-celery-retry-strategy.md) y [ADR-005](../decisiones/adr-005-celery-idempotency.md).

---

## 1. Configuración de celery_app.py

### 1.1 Configuración Base (Actual)

El archivo `backend/jobs/celery_app.py` ya tiene la configuración base:

```python
from celery import Celery
from shared.config.settings import settings

celery_app = Celery(
    "alejandria",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["jobs.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutos
    task_soft_time_limit=25 * 60,  # 25 minutos
)
```

### 1.2 Configuración Adicional Requerida

Agregar configuración de retry strategy según ADR-004:

```python
celery_app.conf.update(
    # ... configuración existente ...
    
    # Retry strategy con backoff exponencial
    task_default_retry_delay=60,  # 1 minuto inicial
    task_max_retries=5,
    task_acks_late=True,  # Ack solo después de completar exitosamente
    
    # Worker configuration
    worker_prefetch_multiplier=1,  # Procesar una tarea a la vez
    worker_disable_rate_limits=True,
)
```

---

## 2. Definición de Job Types

### 2.1 Estructura de Tasks

Crear directorio `backend/jobs/tasks/` con los siguientes módulos:

```
backend/jobs/tasks/
├── __init__.py
├── gap_detection.py
├── vector_sync.py
└── question_generation.py
```

### 2.2 Job Type: gap_detection

**Archivo:** `backend/jobs/tasks/gap_detection.py`

```python
from celery import current_task
from celery.utils.log import get_task_logger

from jobs.celery_app import celery_app
from shared.services.document_service import DocumentService
from shared.services.gap_service import GapService
from shared.llm.ollama_client import OllamaClient

logger = get_task_logger(__name__)

@celery_app.task(
    bind=True,
    name='gap_detection',
    max_retries=5,
    default_retry_delay=60,
)
def gap_detection_task(self, document_id: str):
    """
    Detect gaps in a document using LLM analysis.
    
    Args:
        document_id: UUID of the document to analyze
    
    Returns:
        Dict with gaps created count
    """
    try:
        logger.info(f"Starting gap detection for document {document_id}")
        
        # 1. Leer documento
        document_service = DocumentService()
        document = document_service.get_document(document_id)
        
        if not document:
            logger.error(f"Document {document_id} not found")
            return {"error": "Document not found"}
        
        # 2. Leer gaps existentes
        gap_service = GapService()
        existing_gaps = gap_service.list_gaps(document_id, status='pending')
        
        # 3. Ejecutar análisis LLM
        ollama_client = OllamaClient()
        gaps = ollama_client.detect_gaps(
            document_content=document.content,
            document_title=document.title,
            existing_gaps=existing_gaps
        )
        
        # 4. Crear gaps nuevos
        gaps_created = 0
        for gap_data in gaps:
            try:
                gap_service.create_gap(document_id, gap_data)
                gaps_created += 1
            except Exception as e:
                logger.error(f"Error creating gap: {e}")
        
        logger.info(f"Gap detection completed for document {document_id}: {gaps_created} gaps created")
        return {"gaps_created": gaps_created}
        
    except Exception as exc:
        logger.error(f"Gap detection failed for document {document_id}: {exc}")
        # Retry con backoff exponencial
        raise self.retry(exc=exc, countdown=2 ** self.request.retries * 60)
```

### 2.3 Job Type: vector_sync

**Archivo:** `backend/jobs/tasks/vector_sync.py`

```python
from celery import current_task
from celery.utils.log import get_task_logger

from jobs.celery_app import celery_app
from shared.services.document_service import DocumentService
from shared.services.qdrant_service import QdrantService
from shared.llm.ollama_client import OllamaClient

logger = get_task_logger(__name__)

@celery_app.task(
    bind=True,
    name='vector_sync',
    max_retries=5,
    default_retry_delay=60,
)
def vector_sync_task(self, document_id: str):
    """
    Synchronize document embeddings with Qdrant vector database.
    
    Args:
        document_id: UUID of the document to sync
    
    Returns:
        Dict with vectors synced count
    """
    try:
        logger.info(f"Starting vector sync for document {document_id}")
        
        # 1. Leer documento
        document_service = DocumentService()
        document = document_service.get_document(document_id)
        
        if not document:
            logger.error(f"Document {document_id} not found")
            return {"error": "Document not found"}
        
        # 2. Chunking del contenido
        chunks = chunk_document(document.content, max_tokens=512, overlap=50)
        
        # 3. Generar embeddings
        ollama_client = OllamaClient()
        embeddings = []
        for chunk in chunks:
            embedding = ollama_client.generate_embedding(chunk.text)
            embeddings.append({
                "text": chunk.text,
                "embedding": embedding,
                "metadata": chunk.metadata
            })
        
        # 4. Sincronizar con Qdrant
        qdrant_service = QdrantService()
        qdrant_service.upsert_vectors(
            collection_name="documents",
            vectors=embeddings,
            document_id=document_id
        )
        
        logger.info(f"Vector sync completed for document {document_id}: {len(embeddings)} vectors synced")
        return {"vectors_synced": len(embeddings)}
        
    except Exception as exc:
        logger.error(f"Vector sync failed for document {document_id}: {exc}")
        raise self.retry(exc=exc, countdown=2 ** self.request.retries * 60)

def chunk_document(content: str, max_tokens: int = 512, overlap: int = 50):
    """
    Chunk document content for vector embedding.
    
    Strategy:
    - Split by paragraphs
    - Group paragraphs until ~max_tokens
    - Maintain overlap between chunks
    - Preserve section structure in metadata
    """
    # Implementación de chunking (ver vector-chunking-strategy.md)
    pass
```

### 2.4 Job Type: question_generation

**Archivo:** `backend/jobs/tasks/question_generation.py`

```python
from celery import current_task
from celery.utils.log import get_task_logger

from jobs.celery_app import celery_app
from shared.services.gap_service import GapService
from shared.services.qdrant_service import QdrantService
from shared.llm.ollama_client import OllamaClient

logger = get_task_logger(__name__)

@celery_app.task(
    bind=True,
    name='question_generation',
    max_retries=5,
    default_retry_delay=60,
)
def question_generation_task(self, gap_id: str, answer: str):
    """
    Generate response to a gap question using LLM and vectorize the answer.
    
    Args:
        gap_id: UUID of the gap to answer
        answer: The answer provided by the user
    
    Returns:
        Dict with answer vectorized status
    """
    try:
        logger.info(f"Starting question generation for gap {gap_id}")
        
        # 1. Leer gap
        gap_service = GapService()
        gap = gap_service.get_gap(gap_id)
        
        if not gap:
            logger.error(f"Gap {gap_id} not found")
            return {"error": "Gap not found"}
        
        # 2. Generar embedding de la respuesta
        ollama_client = OllamaClient()
        answer_embedding = ollama_client.generate_embedding(answer)
        
        # 3. Sincronizar con Qdrant
        qdrant_service = QdrantService()
        qdrant_service.upsert_vectors(
            collection_name="answers",
            vectors=[{
                "text": answer,
                "embedding": answer_embedding,
                "metadata": {"gap_id": gap_id}
            }]
        )
        
        logger.info(f"Question generation completed for gap {gap_id}")
        return {"answer_vectorized": True}
        
    except Exception as exc:
        logger.error(f"Question generation failed for gap {gap_id}: {exc}")
        raise self.retry(exc=exc, countdown=2 ** self.request.retries * 60)
```

---

## 3. Configuración de Workers en docker-compose.yml

### 3.1 Agregar Servicio de Celery Worker

Agregar al archivo `docker-compose.yml`:

```yaml
services:
  # ... servicios existentes ...
  
  celery-worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A jobs.celery_app worker --loglevel=info --concurrency=2
    volumes:
      - ./backend:/app
    environment:
      - REDIS_URL=redis://redis:6379/0
      - DATABASE_URL=postgresql://user:password@postgresql:5432/alejandria
      - QDRANT_URL=http://qdrant:6333
      - OLLAMA_URL=http://host.docker.internal:11434
    depends_on:
      - redis
      - postgresql
      - qdrant
    networks:
      - alejandria-network
```

### 3.2 Configuración de Beat (Opcional - para tareas programadas)

Si se requieren tareas programadas, agregar servicio de Celery Beat:

```yaml
  celery-beat:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A jobs.celery_app beat --loglevel=info
    volumes:
      - ./backend:/app
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    networks:
      - alejandria-network
```

---

## 4. Implementación de Locks Distribuidos (ADR-005)

### 4.1 Instalación de celery_once

```bash
uv add celery-once
```

### 4.2 Configuración de celery_once

Agregar a `celery_app.py`:

```python
from celery_once import QueueOnce

celery_app.conf.update(
    # ... configuración existente ...
    
    # celery_once configuration
    once={
        'backend': 'celery_once.backends.redis.Redis',
        'settings': {
            'url': settings.redis_url,
        }
    }
)
```

### 4.3 Uso de Locks en Tasks

Modificar tasks para usar locks:

```python
@celery_app.task(
    bind=True,
    base=QueueOnce,
    once={'graceful': True},  # Permitir que expire el lock
    name='gap_detection',
)
def gap_detection_task(self, document_id: str):
    # Si el task ya está ejecutándose, celery_once lo evitará
    pass
```

---

## 5. Monitoreo y Logging

### 5.1 Configuración de Logging

Configurar logging estructurado en `celery_app.py`:

```python
import logging
from celery.signals import task_prerun, task_postrun, task_failure

@task_prerun.connect
def task_prerun_handler(sender=None, task_id=None, task=None, **kwargs):
    logger.info(f"Task started: {task.name}[{task_id}]")

@task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, task=None, retval=None, **kwargs):
    logger.info(f"Task completed: {task.name}[{task_id}]")

@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, **kwargs):
    logger.error(f"Task failed: {task.name}[{task_id}] - {exception}")
```

### 5.2 Monitoreo con Flower (Opcional)

Instalar Flower para monitoreo web:

```bash
uv add flower
```

Agregar a `docker-compose.yml`:

```yaml
  flower:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A jobs.celery_app flower --port=5555
    ports:
      - "5555:5555"
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    networks:
      - alejandria-network
```

---

## 6. Testing de Jobs

### 6.1 Testing Unitario

**Archivo:** `backend/tests/test_jobs/test_gap_detection.py`

```python
import pytest
from jobs.tasks.gap_detection import gap_detection_task
from unittest.mock import Mock, patch

@pytest.mark.asyncio
async def test_gap_detection_task_success():
    # Mock dependencies
    with patch('jobs.tasks.gap_detection.DocumentService') as mock_doc_service, \
         patch('jobs.tasks.gap_detection.GapService') as mock_gap_service, \
         patch('jobs.tasks.gap_detection.OllamaClient') as mock_ollama:
        
        # Setup mocks
        mock_doc_service.return_value.get_document.return_value = Mock(
            id="doc-1",
            title="Test Doc",
            content="Test content"
        )
        mock_gap_service.return_value.list_gaps.return_value = []
        mock_ollama.return_value.detect_gaps.return_value = [
            {"question": "Test question", "context_missing": "Test context"}
        ]
        
        # Execute task
        result = gap_detection_task("doc-1")
        
        # Assert
        assert result["gaps_created"] == 1
        mock_gap_service.return_value.create_gap.assert_called_once()
```

### 6.2 Testing de Idempotencia

```python
def test_gap_detection_idempotent():
    # Ejecutar el mismo task dos veces
    result1 = gap_detection_task("doc-1")
    result2 = gap_detection_task("doc-1")
    
    # La segunda ejecución no debe crear gaps duplicados
    assert result1["gaps_created"] == result2["gaps_created"]
```

### 6.3 Testing de Retry Strategy

```python
def test_gap_detection_retry_on_failure():
    with patch('jobs.tasks.gap_detection.OllamaClient') as mock_ollama:
        # Simular fallo en primera llamada
        mock_ollama.return_value.detect_gaps.side_effect = [Exception("LLM error"), [{"question": "Test"}]]
        
        # Ejecutar task (debería reintentar)
        result = gap_detection_task("doc-1")
        
        # Assert que eventualmente tuvo éxito
        assert result["gaps_created"] == 1
```

---

## 7. Troubleshooting Común

### 7.1 Worker no procesa tasks

**Síntoma:** Tasks en estado PENDING en Flower

**Soluciones:**
1. Verificar que worker está conectado: `celery -A jobs.celery_app inspect active`
2. Verificar que el nombre del task coincide: `celery -A jobs.celery_app inspect registered`
3. Revisar logs del worker: `docker-compose logs celery-worker`

### 7.2 Tasks fallan con timeout

**Síntoma:** TaskSoftTimeLimitExceeded

**Soluciones:**
1. Aumentar `task_soft_time_limit` en `celery_app.py`
2. Optimizar el task para que sea más rápido
3. Dividir tasks largos en sub-tasks más pequeños

### 7.3 Locks no funcionan

**Síntoma:** Tasks duplicados se ejecutan simultáneamente

**Soluciones:**
1. Verificar que celery_once está configurado correctamente
2. Verificar que Redis está accesible
3. Aumentar el tiempo de expiración del lock en configuración

### 7.4 Memory leaks en workers

**Síntoma:** Worker consume memoria crecientemente

**Soluciones:**
1. Usar `worker_max_tasks_per_child` para reiniciar workers periódicamente
2. Verificar que no se estén acumulando objetos en memoria global
3. Usar `--max-tasks-per-child=1000` al iniciar worker

---

## 8. Referencias

- [ADR-004: Celery Retry Strategy](../decisiones/adr-004-celery-retry-strategy.md)
- [ADR-005: Celery Idempotency](../decisiones/adr-005-celery-idempotency.md)
- [job-implementation-guide.md](./job-implementation-guide.md)
- [llm-prompts-gap-detection.md](./llm-prompts-gap-detection.md)
- [vector-chunking-strategy.md](./vector-chunking-strategy.md)
- [epica-04-deteccion-agrupacion.md](../tareas/epica-04-deteccion-agrupacion.md)

---

*Fin del documento de guía de implementación de Celery.*
