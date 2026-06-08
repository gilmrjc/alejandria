---
id: ARC-017
type: Technical Specification
rating: 9.0
rating-phase: document-editing
related:
  - target: EPC-004
    relationship_type: implements
    reason: Implementa la especificación de chunking para vector_sync en Épica 4
  - target: ARC-015
    relationship_type: references
    reason: Referencia celery-implementation-guide para implementación en jobs
  - target: ARC-004
    relationship_type: depends_on
    reason: Depende del schema de base de datos para metadata de chunks
---

# Vector Chunking Strategy - Alejandria

Este documento define la estrategia de chunking para sincronización de vectores con Qdrant. Para la guía de implementación de jobs, ver [celery-implementation-guide.md](./celery-implementation-guide.md).

---

## 1. Estrategia de Chunking

### 1.1 Parámetros de Chunking

- **Tamaño máximo de chunk**: 512 tokens
- **Superposición entre chunks**: 50 tokens (10%)
- **Algoritmo**: División por párrafos con agrupación inteligente
- **Preservación de estructura**: Metadata de secciones mantenida

### 1.2 Justificación de Parámetros

**512 tokens por chunk:**
- Balance entre granularidad y contexto
- Compatible con límites de contexto de la mayoría de LLMs
- Optimizado para embeddings BGE-M3

**50 tokens de superposición:**
- Mantiene continuidad semántica entre chunks
- Permite recuperación de información que cruza límites de chunks
- 10% de superposición es un estándar en RAG systems

---

## 2. Algoritmo de Chunking

### 2.1 Pseudocódigo

```python
def chunk_document(content: str, max_tokens: int = 512, overlap: int = 50):
    """
    Chunk document content for vector embedding.
    
    Args:
        content: Document content (markdown or plain text)
        max_tokens: Maximum tokens per chunk
        overlap: Token overlap between chunks
    
    Returns:
        List of chunks with metadata
    """
    # Paso 1: Dividir texto en párrafos
    paragraphs = split_into_paragraphs(content)
    
    # Paso 2: Agrupar párrafos hasta alcanzar ~max_tokens
    chunks = []
    current_chunk = []
    current_tokens = 0
    
    for paragraph in paragraphs:
        paragraph_tokens = count_tokens(paragraph)
        
        # Si el párrafo es muy largo, dividirlo
        if paragraph_tokens > max_tokens:
            if current_chunk:
                chunks.append(create_chunk(current_chunk))
                current_chunk = []
                current_tokens = 0
            
            # Dividir párrafo largo
            sub_chunks = split_long_paragraph(paragraph, max_tokens, overlap)
            chunks.extend(sub_chunks)
            continue
        
        # Si agregar el párrafo excede el límite, crear chunk actual
        if current_tokens + paragraph_tokens > max_tokens:
            chunks.append(create_chunk(current_chunk))
            current_chunk = []
            current_tokens = 0
        
        # Agregar párrafo al chunk actual
        current_chunk.append(paragraph)
        current_tokens += paragraph_tokens
    
    # Agregar último chunk si existe
    if current_chunk:
        chunks.append(create_chunk(current_chunk))
    
    # Paso 3: Agregar superposición entre chunks
    chunks_with_overlap = add_overlap(chunks, overlap)
    
    # Paso 4: Preservar estructura de secciones en metadata
    chunks_with_metadata = add_section_metadata(chunks_with_overlap, content)
    
    return chunks_with_metadata
```

### 2.2 División por Párrafos

```python
def split_into_paragraphs(content: str) -> List[str]:
    """
    Split content into paragraphs based on markdown structure.
    
    Markdown structure:
    - Headers (#, ##, ###) separan secciones
    - Líneas vacías separan párrafos
    - Listas se mantienen juntas
    """
    lines = content.split('\n')
    paragraphs = []
    current_paragraph = []
    
    for line in lines:
        # Headers marcan nueva sección
        if line.startswith('#'):
            if current_paragraph:
                paragraphs.append('\n'.join(current_paragraph))
                current_paragraph = []
            current_paragraph.append(line)
        # Líneas vacías marcan fin de párrafo
        elif line.strip() == '':
            if current_paragraph:
                paragraphs.append('\n'.join(current_paragraph))
                current_paragraph = []
        # Listas se mantienen juntas
        elif line.strip().startswith(('-', '*', '+')):
            current_paragraph.append(line)
        # Texto normal
        else:
            current_paragraph.append(line)
    
    # Agregar último párrafo
    if current_paragraph:
        paragraphs.append('\n'.join(current_paragraph))
    
    return paragraphs
```

### 2.3 Agregar Superposición

```python
def add_overlap(chunks: List[str], overlap_tokens: int) -> List[str]:
    """
    Add token overlap between adjacent chunks.
    
    Strategy:
    - Take last N tokens from previous chunk
    - Add to beginning of next chunk
    """
    if not chunks:
        return []
    
    chunks_with_overlap = [chunks[0]]
    
    for i in range(1, len(chunks)):
        prev_chunk = chunks[i - 1]
        current_chunk = chunks[i]
        
        # Obtener últimos N tokens del chunk anterior
        prev_tokens = tokenize(prev_chunk)
        overlap_text = ' '.join(prev_tokens[-overlap_tokens:])
        
        # Agregar superposición al chunk actual
        chunk_with_overlap = f"{overlap_text}\n\n{current_chunk}"
        chunks_with_overlap.append(chunk_with_overlap)
    
    return chunks_with_overlap
```

### 2.4 Metadata de Secciones

```python
def add_section_metadata(chunks: List[str], content: str) -> List[Dict]:
    """
    Add section metadata to chunks.
    
    Metadata includes:
    - section_title: Title of the section
    - section_level: Header level (h1, h2, h3)
    - chunk_index: Index of chunk in document
    - total_chunks: Total number of chunks
    """
    # Extraer estructura de secciones del documento
    sections = extract_sections(content)
    
    chunks_with_metadata = []
    current_section = None
    
    for i, chunk in enumerate(chunks):
        # Determinar sección actual basado en contenido del chunk
        for section in sections:
            if section['title'] in chunk:
                current_section = section
                break
        
        chunks_with_metadata.append({
            'text': chunk,
            'metadata': {
                'section_title': current_section['title'] if current_section else None,
                'section_level': current_section['level'] if current_section else None,
                'chunk_index': i,
                'total_chunks': len(chunks),
                'token_count': count_tokens(chunk)
            }
        })
    
    return chunks_with_metadata
```

---

## 3. Ejemplos de Chunking

### 3.1 Ejemplo Simple

**Input:**
```markdown
# Authentication System

The system uses JWT tokens for authentication. Tokens expire after 8 hours.

## Token Generation

Tokens are generated using the HS256 algorithm with a secret key.
```

**Output (chunks):**
```json
[
  {
    "text": "# Authentication System\n\nThe system uses JWT tokens for authentication. Tokens expire after 8 hours.",
    "metadata": {
      "section_title": "Authentication System",
      "section_level": "h1",
      "chunk_index": 0,
      "total_chunks": 2,
      "token_count": 25
    }
  },
  {
    "text": "Tokens expire after 8 hours.\n\n## Token Generation\n\nTokens are generated using the HS256 algorithm with a secret key.",
    "metadata": {
      "section_title": "Token Generation",
      "section_level": "h2",
      "chunk_index": 1,
      "total_chunks": 2,
      "token_count": 28
    }
  }
]
```

### 3.2 Ejemplo con Documento Largo

**Input:** Documento técnico de 2000 tokens

**Output:**
- Chunk 1: Tokens 0-512 (sin overlap)
- Chunk 2: Tokens 462-974 (overlap de 50 tokens)
- Chunk 3: Tokens 924-1436 (overlap de 50 tokens)
- Chunk 4: Tokens 1386-1898 (overlap de 50 tokens)
- Chunk 5: Tokens 1848-2000 (último chunk, menos de 512 tokens)

---

## 4. Estrategia de Actualización Incremental

### 4.1 Trigger de Actualización

Actualización de vectores se dispara cuando:
- Documento es actualizado (evento `document.updated`)
- Nuevo documento es creado (evento `document.created`)
- Documento es eliminado (evento `document.deleted`)

### 4.2 Proceso de Actualización

```python
def update_document_vectors(document_id: str):
    """
    Update vectors for a document incrementally.
    
    Strategy:
    1. Eliminar vectores existentes del documento
    2. Aplicar chunking al contenido actualizado
    3. Generar embeddings para cada chunk
    4. Insertar vectores con metadata en Qdrant
    5. Actualizar vector_sync_log
    """
    # 1. Eliminar vectores existentes
    qdrant_service = QdrantService()
    qdrant_service.delete_vectors(collection_name="documents", filter={"document_id": document_id})
    
    # 2. Leer documento actualizado
    document_service = DocumentService()
    document = document_service.get_document(document_id)
    
    # 3. Aplicar chunking
    chunks = chunk_document(document.content, max_tokens=512, overlap=50)
    
    # 4. Generar embeddings
    ollama_client = OllamaClient()
    vectors = []
    for chunk in chunks:
        embedding = ollama_client.generate_embedding(chunk['text'])
        vectors.append({
            "id": f"{document_id}_{chunk['metadata']['chunk_index']}",
            "vector": embedding,
            "payload": {
                "document_id": document_id,
                "text": chunk['text'],
                "metadata": chunk['metadata']
            }
        })
    
    # 5. Insertar vectores en Qdrant
    qdrant_service.upsert_vectors(collection_name="documents", vectors=vectors)
    
    # 6. Actualizar log
    update_vector_sync_log(document_id, status="completed", chunks_count=len(chunks))
```

### 4.3 Manejo de Errores

```python
def update_document_vectors_with_retry(document_id: str, max_retries: int = 3):
    """
    Update vectors with retry logic.
    """
    for attempt in range(max_retries):
        try:
            update_document_vectors(document_id)
            return
        except QdrantError as e:
            logger.error(f"Qdrant error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Backoff exponencial
        except OllamaError as e:
            logger.error(f"Ollama error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
```

---

## 5. Testing de Chunking

### 5.1 Test Unitario

```python
def test_chunking_simple_document():
    content = "# Title\n\nParagraph 1.\n\nParagraph 2."
    chunks = chunk_document(content, max_tokens=512, overlap=50)
    
    assert len(chunks) == 1
    assert chunks[0]['metadata']['section_title'] == "Title"
    assert chunks[0]['metadata']['chunk_index'] == 0
```

### 5.2 Test de Superposición

```python
def test_chunking_overlap():
    content = "A " * 600  # 600 tokens
    chunks = chunk_document(content, max_tokens=512, overlap=50)
    
    assert len(chunks) == 2
    # Verificar que el segundo chunk tiene superposición
    assert chunks[0]['text'][-50:] in chunks[1]['text'][:100]
```

### 5.3 Test de Preservación de Estructura

```python
def test_chunking_preserves_structure():
    content = "# Section 1\n\nContent 1.\n\n## Section 2\n\nContent 2."
    chunks = chunk_document(content, max_tokens=512, overlap=50)
    
    # Verificar metadata de secciones
    assert chunks[0]['metadata']['section_title'] == "Section 1"
    assert chunks[1]['metadata']['section_title'] == "Section 2"
    assert chunks[0]['metadata']['section_level'] == "h1"
    assert chunks[1]['metadata']['section_level'] == "h2"
```

---

## 6. Optimizaciones

### 6.1 Caching de Embeddings

```python
def chunk_document_with_cache(content: str, cache: Dict[str, np.ndarray]):
    """
    Chunk document with embedding cache.
    
    If a chunk text is already in cache, reuse the embedding.
    """
    chunks = chunk_document(content)
    chunks_with_embeddings = []
    
    for chunk in chunks:
        chunk_hash = hashlib.md5(chunk['text'].encode()).hexdigest()
        
        if chunk_hash in cache:
            embedding = cache[chunk_hash]
        else:
            embedding = ollama_client.generate_embedding(chunk['text'])
            cache[chunk_hash] = embedding
        
        chunks_with_embeddings.append({
            'text': chunk['text'],
            'embedding': embedding,
            'metadata': chunk['metadata']
        })
    
    return chunks_with_embeddings
```

### 6.2 Chunking Paralelo

```python
from concurrent.futures import ThreadPoolExecutor

def generate_embeddings_parallel(chunks: List[str], max_workers: int = 4):
    """
    Generate embeddings for chunks in parallel.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        embeddings = list(executor.map(
            ollama_client.generate_embedding,
            [chunk['text'] for chunk in chunks]
        ))
    
    return embeddings
```

---

## 7. Referencias

- [celery-implementation-guide.md](./celery-implementation-guide.md): Guía de implementación de jobs
- [llm-prompts-gap-detection.md](./llm-prompts-gap-detection.md): Prompts de LLM
- [api-specification-gaps-metadata.md](./api-specification-gaps-metadata.md): Especificación de API
- [epica-04-deteccion-agrupacion.md](../tareas/epica-04-deteccion-agrupacion.md): Épica 4 - T-042

---

*Fin del documento de especificación de chunking para vector sync.*
