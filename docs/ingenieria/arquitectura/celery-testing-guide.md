---
id: ARC-018
type: Testing Guide
rating: 9.0
rating-phase: document-editing
related:
  - target: EPC-004
    relationship_type: implements
    reason: Implementa la guía de testing para jobs de Celery en Épica 4
  - target: ARC-015
    relationship_type: references
    reason: Referencia celery-implementation-guide para contexto de implementación
  - target: ARC-040
    relationship_type: extends
    reason: Extiende api-testing-logging con estrategias específicas de Celery
---

# Celery Testing Guide - Alejandria

Este documento proporciona una guía completa para testing de jobs de Celery en Alejandria. Para la guía de implementación, ver [celery-implementation-guide.md](./celery-implementation-guide.md). Para testing general de API, ver [api-testing-logging.md](./api-testing-logging.md).

---

## 1. Testing Unitario de Tasks

### 1.1 Estrategia General

**Objetivos:**
- Validar lógica de business de cada task
- Verificar manejo de errores y retries
- Testear idempotencia con locks
- Mockear dependencias externas (Ollama, Qdrant, Database)

**Herramientas:**
- pytest para testing framework
- unittest.mock para mocking
- pytest-asyncio para tests asíncronos
- faker para datos de prueba

### 1.2 Test de gap_detection Task

**Archivo:** `backend/tests/test_jobs/test_gap_detection.py`

```python
import pytest
from unittest.mock import Mock, patch, MagicMock
from jobs.tasks.gap_detection import gap_detection_task
from shared.services.document_service import DocumentService
from shared.services.gap_service import GapService
from shared.llm.ollama_client import OllamaClient

@pytest.fixture
def mock_document():
    return Mock(
        id="doc-1",
        title="Test Document",
        content="Test content for gap detection"
    )

@pytest.fixture
def mock_ollama_response():
    return [
        {
            "question": "How is authentication implemented?",
            "context_missing": "Missing authentication details",
            "type": "implementation",
            "severity": "high",
            "role_affected": "developer"
        }
    ]

class TestGapDetectionTask:
    
    @patch('jobs.tasks.gap_detection.DocumentService')
    @patch('jobs.tasks.gap_detection.GapService')
    @patch('jobs.tasks.gap_detection.OllamaClient')
    def test_gap_detection_success(self, mock_ollama, mock_gap_service, mock_doc_service, mock_document):
        """Test successful gap detection."""
        # Setup mocks
        mock_doc_service.return_value.get_document.return_value = mock_document
        mock_gap_service.return_value.list_gaps.return_value = []
        mock_ollama.return_value.detect_gaps.return_value = mock_ollama_response
        mock_gap_service.return_value.create_gap.return_value = Mock(id="gap-1")
        
        # Execute task
        result = gap_detection_task("doc-1")
        
        # Assert
        assert result["gaps_created"] == 1
        mock_doc_service.return_value.get_document.assert_called_once_with("doc-1")
        mock_gap_service.return_value.list_gaps.assert_called_once_with("doc-1", status='pending')
        mock_ollama.return_value.detect_gaps.assert_called_once()
        mock_gap_service.return_value.create_gap.assert_called_once()
    
    @patch('jobs.tasks.gap_detection.DocumentService')
    @patch('jobs.tasks.gap_detection.GapService')
    @patch('jobs.tasks.gap_detection.OllamaClient')
    def test_gap_detection_document_not_found(self, mock_ollama, mock_gap_service, mock_doc_service):
        """Test gap detection with non-existent document."""
        # Setup mock
        mock_doc_service.return_value.get_document.return_value = None
        
        # Execute task
        result = gap_detection_task("doc-1")
        
        # Assert
        assert "error" in result
        assert result["error"] == "Document not found"
        mock_ollama.return_value.detect_gaps.assert_not_called()
    
    @patch('jobs.tasks.gap_detection.DocumentService')
    @patch('jobs.tasks.gap_detection.GapService')
    @patch('jobs.tasks.gap_detection.OllamaClient')
    def test_gap_detection_filters_duplicates(self, mock_ollama, mock_gap_service, mock_doc_service, mock_document):
        """Test that duplicate gaps are filtered out."""
        # Setup mocks
        mock_doc_service.return_value.get_document.return_value = mock_document
        mock_gap_service.return_value.list_gaps.return_value = [
            Mock(question="How is authentication implemented?")
        ]
        mock_ollama.return_value.detect_gaps.return_value = [
            {
                "question": "How is authentication implemented?",
                "context_missing": "Missing authentication details",
                "type": "implementation",
                "severity": "high",
                "role_affected": "developer"
            }
        ]
        
        # Execute task
        result = gap_detection_task("doc-1")
        
        # Assert - duplicate should be filtered
        assert result["gaps_created"] == 0
        mock_gap_service.return_value.create_gap.assert_not_called()
    
    @patch('jobs.tasks.gap_detection.DocumentService')
    @patch('jobs.tasks.gap_detection.GapService')
    @patch('jobs.tasks.gap_detection.OllamaClient')
    def test_gap_detection_llm_error_triggers_retry(self, mock_ollama, mock_gap_service, mock_doc_service, mock_document):
        """Test that LLM errors trigger retry."""
        # Setup mock to raise error
        mock_doc_service.return_value.get_document.return_value = mock_document
        mock_gap_service.return_value.list_gaps.return_value = []
        mock_ollama.return_value.detect_gaps.side_effect = Exception("LLM error")
        
        # Execute task - should raise retry exception
        with pytest.raises(Exception) as exc_info:
            gap_detection_task("doc-1")
        
        assert "LLM error" in str(exc_info.value)
```

### 1.3 Test de vector_sync Task

**Archivo:** `backend/tests/test_jobs/test_vector_sync.py`

```python
import pytest
from unittest.mock import Mock, patch
from jobs.tasks.vector_sync import vector_sync_task, chunk_document

class TestVectorSyncTask:
    
    @patch('jobs.tasks.vector_sync.DocumentService')
    @patch('jobs.tasks.vector_sync.QdrantService')
    @patch('jobs.tasks.vector_sync.OllamaClient')
    def test_vector_sync_success(self, mock_ollama, mock_qdrant, mock_doc_service):
        """Test successful vector sync."""
        # Setup mocks
        mock_doc_service.return_value.get_document.return_value = Mock(
            id="doc-1",
            content="Test content for vector sync"
        )
        mock_ollama.return_value.generate_embedding.return_value = [0.1, 0.2, 0.3]
        
        # Execute task
        result = vector_sync_task("doc-1")
        
        # Assert
        assert "vectors_synced" in result
        assert result["vectors_synced"] > 0
        mock_qdrant.return_value.upsert_vectors.assert_called_once()
    
    @patch('jobs.tasks.vector_sync.chunk_document')
    def test_chunking_preserves_structure(self, mock_chunk):
        """Test that chunking preserves document structure."""
        mock_chunk.return_value = [
            {
                "text": "# Section 1\n\nContent 1",
                "metadata": {
                    "section_title": "Section 1",
                    "section_level": "h1",
                    "chunk_index": 0,
                    "total_chunks": 2
                }
            }
        ]
        
        chunks = chunk_document("# Section 1\n\nContent 1\n\n## Section 2\n\nContent 2")
        
        assert len(chunks) > 0
        assert chunks[0]["metadata"]["section_title"] == "Section 1"
```

---

## 2. Testing de Idempotencia

### 2.1 Test de Locks Distribuidos

```python
import pytest
from unittest.mock import patch
from jobs.tasks.gap_detection import gap_detection_task
from celery_once import AlreadyQueued

class TestIdempotency:
    
    @patch('jobs.tasks.gap_detection.DocumentService')
    @patch('jobs.tasks.gap_detection.GapService')
    @patch('jobs.tasks.gap_detection.OllamaClient')
    def test_gap_detection_idempotent_with_lock(self, mock_ollama, mock_gap_service, mock_doc_service):
        """Test that task is idempotent with distributed lock."""
        # Setup mocks
        mock_doc_service.return_value.get_document.return_value = Mock(
            id="doc-1",
            title="Test Document",
            content="Test content"
        )
        mock_gap_service.return_value.list_gaps.return_value = []
        mock_ollama.return_value.detect_gaps.return_value = []
        
        # Execute task twice with same document_id
        result1 = gap_detection_task("doc-1")
        result2 = gap_detection_task("doc-1")
        
        # Assert both executions return same result
        assert result1 == result2
        
        # If using celery_once, second execution should be skipped
        # This depends on celery_once configuration
    
    @patch('jobs.tasks.gap_detection.DocumentService')
    @patch('jobs.tasks.gap_detection.GapService')
    @patch('jobs.tasks.gap_detection.OllamaClient')
    def test_gap_detection_no_duplicate_gaps(self, mock_ollama, mock_gap_service, mock_doc_service):
        """Test that running task twice doesn't create duplicate gaps."""
        # Setup mocks
        mock_doc_service.return_value.get_document.return_value = Mock(
            id="doc-1",
            title="Test Document",
            content="Test content"
        )
        mock_gap_service.return_value.list_gaps.return_value = []
        mock_ollama.return_value.detect_gaps.return_value = [
            {"question": "Test question", "context_missing": "Test context", "type": "implementation", "severity": "high", "role_affected": "developer"}
        ]
        mock_gap_service.return_value.create_gap.return_value = Mock(id="gap-1")
        
        # Execute task twice
        result1 = gap_detection_task("doc-1")
        
        # Second execution should see existing gap
        mock_gap_service.return_value.list_gaps.return_value = [
            Mock(question="Test question")
        ]
        result2 = gap_detection_task("doc-1")
        
        # Assert second execution creates no new gaps
        assert result1["gaps_created"] == 1
        assert result2["gaps_created"] == 0
```

---

## 3. Testing de Retry Strategy

### 3.1 Test de Backoff Exponencial

```python
import pytest
from unittest.mock import patch
from jobs.tasks.gap_detection import gap_detection_task

class TestRetryStrategy:
    
    @patch('jobs.tasks.gap_detection.DocumentService')
    @patch('jobs.tasks.gap_detection.GapService')
    @patch('jobs.tasks.gap_detection.OllamaClient')
    def test_gap_detection_retry_on_llm_failure(self, mock_ollama, mock_gap_service, mock_doc_service):
        """Test that task retries on LLM failure with exponential backoff."""
        # Setup mock to fail twice, then succeed
        mock_doc_service.return_value.get_document.return_value = Mock(
            id="doc-1",
            title="Test Document",
            content="Test content"
        )
        mock_gap_service.return_value.list_gaps.return_value = []
        mock_ollama.return_value.detect_gaps.side_effect = [
            Exception("LLM error 1"),
            Exception("LLM error 2"),
            [{"question": "Test question", "context_missing": "Test context", "type": "implementation", "severity": "high", "role_affected": "developer"}]
        ]
        
        # Execute task with retry logic
        # In real scenario, Celery handles retry automatically
        # For testing, we simulate retry logic
        
        attempt = 0
        max_retries = 3
        result = None
        
        while attempt < max_retries:
            try:
                result = gap_detection_task("doc-1")
                break
            except Exception as e:
                attempt += 1
                if attempt >= max_retries:
                    raise
                # Simulate backoff
                import time
                time.sleep(2 ** attempt)
        
        # Assert task eventually succeeded
        assert result is not None
        assert result["gaps_created"] == 1
        assert mock_ollama.return_value.detect_gaps.call_count == 3
```

---

## 4. Integration Tests con Bases de Datos Reales

### 4.1 Configuración de Test Database

**Archivo:** `backend/tests/conftest.py`

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from shared.database.base import Base
from shared.config.settings import settings

# Test database URL
TEST_DATABASE_URL = "postgresql://test_user:test_pass@localhost:5433/alejandria_test"

@pytest.fixture(scope="function")
def test_db():
    """Create a fresh database for each test."""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(engine)
```

### 4.2 Integration Test de gap_detection

```python
def test_gap_detection_integration(test_db):
    """Test gap detection with real database."""
    # Create test document
    document = Document(
        id="doc-1",
        title="Test Document",
        content="Test content for gap detection"
    )
    test_db.add(document)
    test_db.commit()
    
    # Execute task
    result = gap_detection_task("doc-1")
    
    # Verify gaps were created in database
    gaps = test_db.query(Gap).filter(Gap.document_id == "doc-1").all()
    assert len(gaps) == result["gaps_created"]
    assert all(gap.status == "pending" for gap in gaps)
```

---

## 5. Testing de Performance

### 5.1 Test de Performance de Chunking

```python
import time
import pytest

class TestPerformance:
    
    def test_chunking_performance_large_document():
        """Test chunking performance with large document."""
        # Create large document (10,000 tokens)
        large_content = "Test content. " * 10000
        
        start_time = time.time()
        chunks = chunk_document(large_content, max_tokens=512, overlap=50)
        end_time = time.time()
        
        # Assert chunking completes in reasonable time (< 5 seconds)
        assert end_time - start_time < 5
        assert len(chunks) > 10
    
    def test_embedding_generation_performance():
        """Test embedding generation performance."""
        test_text = "Test content for embedding generation"
        
        start_time = time.time()
        embedding = ollama_client.generate_embedding(test_text)
        end_time = time.time()
        
        # Assert embedding generation completes in reasonable time (< 10 seconds)
        assert end_time - start_time < 10
        assert len(embedding) > 0
```

---

## 6. Coverage Targets

### 6.1 Configuración de Coverage

**Archivo:** `backend/pyproject.toml`

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--cov=jobs --cov=shared --cov-report=html --cov-report=term-missing --cov-fail-under=70"
```

### 6.2 Comandos de Coverage

```bash
# Ejecutar tests con coverage
pytest --cov=jobs --cov=shared --cov-report=html

# Ver reporte de coverage
open htmlcov/index.html

# Ver coverage por módulo
pytest --cov=jobs.tasks.gap_detection --cov-report=term-missing
```

### 6.3 Targets de Coverage

- **Jobs tasks**: > 80% coverage
- **Services**: > 75% coverage
- **LLM client**: > 70% coverage (harder to test due to external dependencies)
- **Overall**: > 70% coverage

---

## 7. Mocking de Dependencias Externas

### 7.1 Mocking de Ollama

```python
from unittest.mock import Mock, patch

@pytest.fixture
def mock_ollama_client():
    with patch('shared.llm.ollama_client.OllamaClient') as mock:
        mock.return_value.generate_embedding.return_value = [0.1, 0.2, 0.3]
        mock.return_value.detect_gaps.return_value = [
            {"question": "Test", "context_missing": "Test", "type": "implementation", "severity": "high", "role_affected": "developer"}
        ]
        yield mock
```

### 7.2 Mocking de Qdrant

```python
@pytest.fixture
def mock_qdrant_service():
    with patch('shared.services.qdrant_service.QdrantService') as mock:
        mock.return_value.upsert_vectors.return_value = None
        mock.return_value.delete_vectors.return_value = None
        mock.return_value.search.return_value = []
        yield mock
```

### 7.3 Mocking de Redis

```python
@pytest.fixture
def mock_redis():
    with patch('redis.Redis') as mock:
        mock.return_value.get.return_value = None
        mock.return_value.set.return_value = True
        yield mock
```

---

## 8. Estrategia de Testing Continuo

### 8.1 Pre-commit Hooks

**Archivo:** `.pre-commit-config.yaml`

```yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
```

### 8.2 CI/CD Integration

**Archivo:** `.github/workflows/test.yml`

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:18
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: alejandria_test
        ports:
          - 5433:5432
      redis:
        image: redis:7
        ports:
          - 6380:6379
    
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install uv
          uv sync
      - name: Run tests
        run: pytest --cov=jobs --cov=shared --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## 9. Troubleshooting de Tests

### 9.1 Tests Fallan con Database Errors

**Síntoma:** `sqlalchemy.exc.OperationalError: no such table`

**Solución:**
- Verificar que test database está configurada correctamente
- Asegurar que migrations se ejecutan antes de tests
- Usar fixture que crea/drop tablas para cada test

### 9.2 Tests Fallan con Timeout

**Síntoma:** Tests timeout después de 30 segundos

**Solución:**
- Aumentar timeout en pytest config: `timeout=60`
- Mockear llamadas externas lentas (Ollama, Qdrant)
- Optimizar código de test para ser más rápido

### 9.3 Tests Fallan con Import Errors

**Síntoma:** `ModuleNotFoundError: No module named 'jobs'`

**Solución:**
- Verificar que PYTHONPATH incluye directorio `backend`
- Usar `pytest.ini` para configurar paths
- Ejecutar tests desde directorio `backend`

---

## 10. Referencias

- [celery-implementation-guide.md](./celery-implementation-guide.md): Guía de implementación
- [api-testing-logging.md](./api-testing-logging.md): Testing general de API
- [llm-prompts-gap-detection.md](./llm-prompts-gap-detection.md): Prompts de LLM
- [epica-04-deteccion-agrupacion.md](../tareas/epica-04-deteccion-agrupacion.md): Épica 4

---

*Fin del documento de guía de testing para jobs de Celery.*
