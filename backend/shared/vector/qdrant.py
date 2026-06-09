"""Qdrant vector database integration for semantic search."""

import logging
import re
from typing import Any

import httpx
from qdrant_client import QdrantClient as QdrantSDKClient

logger = logging.getLogger(__name__)
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    FilterSelector,
    MatchValue,
    PayloadSchemaType,
    PointStruct,
    TextIndexParams,
    VectorParams,
    SparseVectorParams,
    NamedVector,
    NamedSparseVector,
    SearchRequest,
    Prefetch,
)

from shared.config.settings import settings
from shared.utils.retry import retry_with_backoff


class QdrantClient:
    """HTTP client for Qdrant vector database operations."""

    def __init__(self, url: str = None):
        """
        Initialize Qdrant client.

        Args:
            url: Qdrant server URL (defaults to settings.qdrant_url)
        """
        self.url = url or settings.qdrant_url
        self.client = QdrantSDKClient(url=self.url)

    def create_collection(
        self,
        collection_name: str,
        vector_size: int = 1024,
        distance: str = "cosine",
        enable_bm25: bool = True,
    ) -> bool:
        """
        Create a new collection in Qdrant.

        Args:
            collection_name: Name of the collection
            vector_size: Dimension of vectors (BGE-M3 uses 1024)
            distance: Distance metric (cosine, euclidean, dot)
            enable_bm25: Enable BM25 text index for full-text search

        Returns:
            True if collection created successfully
        """
        try:
            vectors_config = VectorParams(
                size=vector_size, distance=Distance[distance.upper()]
            )

            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=vectors_config,
            )

            # Create text index for BM25 if enabled
            if enable_bm25:
                self.client.create_payload_index(
                    collection_name=collection_name,
                    field_name="content",
                    field_schema=PayloadSchemaType.TEXT,
                    field_params=TextIndexParams(
                        type="text",
                        tokenizer="whitespace",
                        lowercase=True,
                    ),
                )

            return True
        except Exception as e:
            # Collection might already exist
            if "already exists" in str(e):
                # Try to create the text index if collection exists but index doesn't
                try:
                    if enable_bm25:
                        self.client.create_payload_index(
                            collection_name=collection_name,
                            field_name="content",
                            field_schema=PayloadSchemaType.TEXT,
                            field_params=TextIndexParams(
                                type="text",
                                tokenizer="whitespace",
                                lowercase=True,
                            ),
                        )
                except Exception:
                    # Index might already exist, ignore
                    pass
                return True
            raise

    def create_hybrid_collection(
        self,
        collection_name: str,
        vector_size: int = 1024,
        distance: str = "cosine",
        force_recreate: bool = False,
    ) -> bool:
        """
        Create a hybrid collection with both dense (semantic) and sparse (BM25) vectors.

        Args:
            collection_name: Name of the collection
            vector_size: Dimension of dense vectors (BGE-M3 uses 1024)
            distance: Distance metric for dense vectors (cosine, euclidean, dot)
            force_recreate: If True, delete and recreate collection if it exists

        Returns:
            True if collection created successfully
        """
        try:
            # Delete collection if it exists and force_recreate is True
            if force_recreate:
                try:
                    self.client.delete_collection(collection_name=collection_name)
                except Exception:
                    pass  # Collection might not exist

            # Configure named dense vectors
            vectors_config = {
                "dense": VectorParams(
                    size=vector_size, distance=Distance[distance.upper()]
                )
            }

            # Configure named sparse vectors separately
            sparse_vectors_config = {
                "sparse": SparseVectorParams()
            }

            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=vectors_config,
                sparse_vectors_config=sparse_vectors_config,
            )

            return True
        except Exception as e:
            # Collection might already exist
            if "already exists" in str(e):
                return True
            raise

    def insert_vectors(
        self,
        collection_name: str,
        vectors: list[list[float]],
        payloads: list[dict[str, Any]],
        ids: list[str] | None = None,
    ) -> bool:
        """
        Insert vectors into a collection.

        Args:
            collection_name: Name of the collection
            vectors: List of vector embeddings
            payloads: List of payload dictionaries
            ids: Optional list of point IDs

        Returns:
            True if vectors inserted successfully
        """
        if ids is None:
            ids = [str(i) for i in range(len(vectors))]

        points = [
            PointStruct(
                id=ids[i],
                vector=vectors[i],
                payload=payloads[i],
            )
            for i in range(len(vectors))
        ]

        self.client.upsert(
            collection_name=collection_name,
            points=points,
        )
        return True

    def insert_hybrid_vectors(
        self,
        collection_name: str,
        dense_vectors: list[list[float]],
        sparse_vectors: list[dict[str, int]] | None = None,
        payloads: list[dict[str, Any]] | None = None,
        ids: list[str] | None = None,
    ) -> bool:
        """
        Insert hybrid vectors (dense + sparse) into a collection.

        Args:
            collection_name: Name of the collection
            dense_vectors: List of dense vector embeddings
            sparse_vectors: Optional list of sparse vectors (BM25-like)
            payloads: List of payload dictionaries
            ids: Optional list of point IDs

        Returns:
            True if vectors inserted successfully
        """
        if ids is None:
            ids = [str(i) for i in range(len(dense_vectors))]

        if payloads is None:
            payloads = [{} for _ in range(len(dense_vectors))]

        points = []
        for i in range(len(dense_vectors)):
            # Build vector dict with named vectors
            vector_dict = {
                "dense": dense_vectors[i],
            }

            # Add sparse vector if provided using NamedSparseVector
            if sparse_vectors and i < len(sparse_vectors):
                sparse_vec = sparse_vectors[i]
                # Convert dict to SparseVector format
                # Use hash to convert string keys to integer indices
                from qdrant_client.models import SparseVector
                sparse_vector = SparseVector(
                    indices=[hash(term) % 2**31 for term in sparse_vec.keys()],  # Convert to positive int
                    values=list(sparse_vec.values()),
                )
                vector_dict["sparse"] = sparse_vector

            points.append(
                PointStruct(
                    id=ids[i],
                    vector=vector_dict,
                    payload=payloads[i],
                )
            )

        self.client.upsert(
            collection_name=collection_name,
            points=points,
        )
        return True

    def search_similar(
        self,
        collection_name: str,
        query_vector: list[float] = None,
        query_text: str = None,
        limit: int = 5,
        score_threshold: float = 0.7,
        filter_condition: Filter | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search for similar vectors or text in a collection.

        Args:
            collection_name: Name of the collection
            query_vector: Query vector embedding (for semantic search)
            query_text: Query text (for BM25 search)
            limit: Maximum number of results
            score_threshold: Minimum similarity score
            filter_condition: Optional filter for search

        Returns:
            List of search results with scores and payloads
        """
        if query_text:
            # BM25 text search using sparse vectors
            try:
                from qdrant_client.models import (
                    Filter,
                    FieldCondition,
                    MatchValue,
                    SearchRequest,
                    SparseVector,
                )
                
                # Use search with sparse vector
                # First, we need to generate a sparse vector from the query text
                # For now, use a simple approach: search the collection and filter by text content
                # This is a simplified BM25-like search

                # Get all points from the collection (inefficient but works for now)
                scroll_result = self.client.scroll(
                    collection_name=collection_name,
                    limit=limit * 10,  # Get more points to filter
                    with_payload=True,
                    with_vectors=False,
                )
                
                # Simple text matching (not true BM25, but functional)
                scored_results = []
                query_lower = query_text.lower()
                
                for point in scroll_result[0]:
                    payload = point.payload or {}
                    # Search in content field (actual field name from vectorize_all_documents.py)
                    text_content = ""
                    if "content" in payload:
                        text_content += payload["content"] + " "
                    if "section_title" in payload:
                        text_content += payload["section_title"] + " "
                    
                    # Simple relevance scoring based on word overlap
                    text_lower = text_content.lower()
                    score = 0.0
                    query_words = set(query_lower.split())
                    text_words = set(text_lower.split())
                    
                    if query_words:
                        # Jaccard similarity
                        intersection = len(query_words & text_words)
                        union = len(query_words | text_words)
                        if union > 0:
                            score = intersection / union
                    
                    # Accept any match (even very low scores) to avoid empty results
                    if score > 0.0 or intersection > 0:
                        # If intersection > 0 but score is 0 (due to union being 0), give minimal score
                        if score == 0.0 and intersection > 0:
                            score = 0.01
                        scored_results.append({
                            "id": str(point.id),
                            "score": score,
                            "payload": payload,
                        })
                
                # Sort by score and return top results
                scored_results.sort(key=lambda x: x["score"], reverse=True)
                return scored_results[:limit]
                
            except Exception as e:
                logger.error(f"BM25 search failed: {e}")
                return []
        elif query_vector:
            # Semantic vector search
            results = self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold,
                query_filter=filter_condition,
            )
        else:
            raise ValueError("Either query_vector or query_text must be provided")

        return [
            {
                "id": result.id,
                "score": result.score,
                "payload": result.payload,
            }
            for result in results
        ]

    def search_hybrid(
        self,
        collection_name: str,
        query_vector: list[float],
        query_text: str,
        limit: int = 5,
        rrf_k: int = 60,
        filter_condition: Filter | None = None,
    ) -> list[dict[str, Any]]:
        """
        Hybrid search using Qdrant's Query API with RRF to combine dense and sparse results.

        Uses the modern Qdrant Query API with prefetch and RRF fusion.

        Args:
            collection_name: Name of the collection (must be hybrid with dense + sparse)
            query_vector: Query dense vector for semantic search
            query_text: Query text for BM25 search
            limit: Maximum number of results
            rrf_k: RRF constant (higher = more emphasis on top results)
            filter_condition: Optional filter for search

        Returns:
            List of search results with combined RRF scores and payloads
        """
        from collections import Counter
        import re
        from qdrant_client.models import Prefetch, SparseVector, RrfQuery, Rrf
        
        # Convert text to sparse vector using the same method as indexing
        words = re.findall(r"\b\w+\b", query_text.lower())
        term_freq = Counter(words)
        
        # Filter stop words (same as in vectorize_all_documents.py)
        stop_words = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "must", "what", "how", "why", "when", "where",
            "who", "which", "that", "this", "these", "those", "with", "from", "for",
            "and", "or", "but", "in", "on", "at", "to", "by", "of", "as", "it",
        }
        
        sparse_vector_dict = {
            term: freq for term, freq in term_freq.items()
            if term not in stop_words and len(term) > 2
        }
        
        # Convert to SparseVector format
        sparse_vector = SparseVector(
            indices=[hash(term) % 2**31 for term in sparse_vector_dict.keys()],
            values=list(sparse_vector_dict.values()),
        )
        
        # Use Qdrant's Query API with prefetch for hybrid search
        search_result = self.client.query_points(
            collection_name=collection_name,
            prefetch=[
                Prefetch(
                    query=sparse_vector,
                    using="sparse",
                    limit=limit * 2,
                ),
                Prefetch(
                    query=query_vector,
                    using="dense",
                    limit=limit * 2,
                ),
            ],
            query=RrfQuery(rrf=Rrf()),
            limit=limit,
        )
        
        # Format results - query_points returns a QueryResponse object with points attribute
        results = []
        for point in search_result:
            results.append({
                "id": str(point.id),
                "score": point.score,
                "payload": point.payload,
            })
        
        return results

    def delete_vectors(
        self,
        collection_name: str,
        ids: list[str],
    ) -> bool:
        """
        Delete vectors from a collection.

        Args:
            collection_name: Name of the collection
            ids: List of point IDs to delete

        Returns:
            True if vectors deleted successfully
        """
        self.client.delete(
            collection_name=collection_name,
            points_selector=ids,
        )
        return True

    def delete_collection(self, collection_name: str) -> bool:
        """
        Delete a collection.

        Args:
            collection_name: Name of the collection

        Returns:
            True if collection deleted successfully
        """
        self.client.delete_collection(collection_name=collection_name)
        return True


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split text into chunks for embedding generation.

    Args:
        text: Input text to chunk
        chunk_size: Maximum size of each chunk in characters
        overlap: Number of characters to overlap between chunks

    Returns:
        List of text chunks
    """
    if not text:
        return []

    # Split by paragraphs first
    paragraphs = re.split(r"\n\n+", text)
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        # If adding this paragraph would exceed chunk size, save current chunk
        if len(current_chunk) + len(paragraph) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # Keep overlap from previous chunk
            if overlap > 0 and len(current_chunk) > overlap:
                current_chunk = current_chunk[-overlap:]
            else:
                current_chunk = ""

        # Add paragraph to current chunk
        if current_chunk:
            current_chunk += "\n\n" + paragraph
        else:
            current_chunk = paragraph

    # Add final chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def chunk_document(
    content: str, max_tokens: int = 512, overlap: int = 50
) -> list[dict[str, Any]]:
    """
    Chunk document content for vector embedding with metadata.

    Strategy:
    - Split by paragraphs
    - Group paragraphs until ~max_tokens
    - Maintain overlap between chunks
    - Preserve section structure in metadata

    Args:
        content: Document content (markdown or plain text)
        max_tokens: Maximum tokens per chunk
        overlap: Token overlap between chunks

    Returns:
        List of chunks with metadata
    """
    if not content:
        return []

    # Split into paragraphs
    paragraphs = split_into_paragraphs(content)

    # Group paragraphs into chunks
    chunks = []
    current_chunk = []
    current_tokens = 0

    for paragraph in paragraphs:
        paragraph_tokens = estimate_tokens(paragraph)

        # If paragraph is very long, split it
        if paragraph_tokens > max_tokens:
            if current_chunk:
                chunks.append(create_chunk(current_chunk))
                current_chunk = []
                current_tokens = 0

            # Split long paragraph
            sub_chunks = split_long_paragraph(paragraph, max_tokens, overlap)
            chunks.extend(sub_chunks)
            continue

        # If adding paragraph exceeds limit, create chunk
        if current_tokens + paragraph_tokens > max_tokens and current_chunk:
            chunks.append(create_chunk(current_chunk))
            current_chunk = []
            current_tokens = 0

        # Add paragraph to current chunk
        current_chunk.append(paragraph)
        current_tokens += paragraph_tokens

    # Add final chunk
    if current_chunk:
        chunks.append(create_chunk(current_chunk))

    # Add overlap between chunks
    chunks_with_overlap = add_overlap(chunks, overlap)

    # Add section metadata
    chunks_with_metadata = add_section_metadata(chunks_with_overlap, content)

    return chunks_with_metadata


def split_into_paragraphs(content: str) -> list[str]:
    """
    Split content into paragraphs based on markdown structure.

    Args:
        content: Document content

    Returns:
        List of paragraphs
    """
    lines = content.split("\n")
    paragraphs = []
    current_paragraph = []

    for line in lines:
        # Headers mark new sections
        if line.startswith("#"):
            if current_paragraph:
                paragraphs.append("\n".join(current_paragraph))
                current_paragraph = []
            current_paragraph.append(line)
        # Empty lines mark end of paragraph
        elif line.strip() == "":
            if current_paragraph:
                paragraphs.append("\n".join(current_paragraph))
                current_paragraph = []
        # Lists stay together
        elif line.strip().startswith(("-", "*", "+")):
            current_paragraph.append(line)
        # Normal text
        else:
            current_paragraph.append(line)

    # Add last paragraph
    if current_paragraph:
        paragraphs.append("\n".join(current_paragraph))

    return paragraphs


def estimate_tokens(text: str) -> int:
    """
    Estimate token count (rough approximation: 1 token ≈ 4 characters).

    Args:
        text: Text to estimate

    Returns:
        Estimated token count
    """
    return len(text) // 4


def create_chunk(paragraphs: list[str]) -> dict[str, Any]:
    """
    Create a chunk from paragraphs.

    Args:
        paragraphs: List of paragraphs

    Returns:
        Chunk dictionary
    """
    return {"text": "\n\n".join(paragraphs)}


def split_long_paragraph(
    paragraph: str, max_tokens: int, overlap: int
) -> list[dict[str, Any]]:
    """
    Split a long paragraph into smaller chunks.

    Args:
        paragraph: Long paragraph to split
        max_tokens: Maximum tokens per chunk
        overlap: Token overlap

    Returns:
        List of chunks
    """
    words = paragraph.split()
    chunks = []
    current_words = []
    current_tokens = 0

    for word in words:
        word_tokens = estimate_tokens(word)

        if current_tokens + word_tokens > max_tokens and current_words:
            chunks.append(create_chunk(current_words))
            # Keep overlap
            overlap_words = current_words[-overlap:] if overlap > 0 else []
            current_words = overlap_words
            current_tokens = sum(estimate_tokens(w) for w in current_words)

        current_words.append(word)
        current_tokens += word_tokens

    if current_words:
        chunks.append(create_chunk(current_words))

    return chunks


def add_overlap(
    chunks: list[dict[str, Any]], overlap_tokens: int
) -> list[dict[str, Any]]:
    """
    Add token overlap between adjacent chunks.

    Args:
        chunks: List of chunks
        overlap_tokens: Number of tokens to overlap

    Returns:
        Chunks with overlap
    """
    if not chunks:
        return []

    chunks_with_overlap = [chunks[0]]

    for i in range(1, len(chunks)):
        prev_chunk = chunks[i - 1]["text"]
        current_chunk = chunks[i]["text"]

        # Get last N tokens from previous chunk
        prev_words = prev_chunk.split()
        overlap_text = (
            " ".join(prev_words[-overlap_tokens:]) if overlap_tokens > 0 else ""
        )

        # Add overlap to current chunk
        if overlap_text:
            chunk_with_overlap = f"{overlap_text}\n\n{current_chunk}"
        else:
            chunk_with_overlap = current_chunk

        chunks_with_overlap.append({"text": chunk_with_overlap})

    return chunks_with_overlap


def add_section_metadata(
    chunks: list[dict[str, Any]], content: str
) -> list[dict[str, Any]]:
    """
    Add section metadata to chunks.

    Args:
        chunks: List of chunks
        content: Original document content

    Returns:
        Chunks with metadata
    """
    # Extract sections from content
    sections = extract_sections(content)

    chunks_with_metadata = []
    current_section = None

    for i, chunk in enumerate(chunks):
        # Determine current section based on chunk content
        for section in sections:
            if section["title"] in chunk["text"]:
                current_section = section
                break

        chunks_with_metadata.append(
            {
                "text": chunk["text"],
                "metadata": {
                    "section_title": current_section["title"]
                    if current_section
                    else None,
                    "section_level": current_section["level"]
                    if current_section
                    else None,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "token_count": estimate_tokens(chunk["text"]),
                },
            }
        )

    return chunks_with_metadata


def extract_sections(content: str) -> list[dict[str, str]]:
    """
    Extract section headers from markdown content.

    Args:
        content: Document content

    Returns:
        List of sections with title and level
    """
    sections = []
    lines = content.split("\n")

    for line in lines:
        if line.startswith("#"):
            level = line.count("#")
            title = line.lstrip("#").strip()
            sections.append({"title": title, "level": f"h{level}"})

    return sections


async def generate_embedding(text: str, ollama_url: str = None) -> list[float]:
    """
    Generate embedding using BGE-M3 model via Ollama with retry logic.

    Args:
        text: Text to embed
        ollama_url: Ollama API URL (defaults to settings.ollama_url)

    Returns:
        Vector embedding as list of floats
    """
    if ollama_url is None:
        ollama_url = settings.ollama_url

    async def _call_ollama():
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{ollama_url}/api/embeddings",
                json={
                    "model": "BGE-M3:latest",
                    "prompt": text,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data.get("embedding", [])

    return await retry_with_backoff(
        _call_ollama,
        max_retries=3,
        base_delay=0.5,
        max_delay=5.0,
        retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException),
    )


async def generate_embeddings_batch(
    texts: list[str], ollama_url: str = None
) -> list[list[float]]:
    """
    Generate embeddings for multiple texts using batched Ollama requests.

    Args:
        texts: List of texts to embed
        ollama_url: Ollama API URL (defaults to settings.ollama_url)

    Returns:
        List of vector embeddings as lists of floats
    """
    if ollama_url is None:
        ollama_url = settings.ollama_url

    async def _call_ollama_batch():
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{ollama_url}/api/embed",
                json={
                    "model": "BGE-M3:latest",
                    "input": texts,
                },
            )
            response.raise_for_status()
            data = response.json()
            # Ollama returns embeddings in "embeddings" array
            return data.get("embeddings", [])

    return await retry_with_backoff(
        _call_ollama_batch,
        max_retries=3,
        base_delay=0.5,
        max_delay=5.0,
        retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException),
    )


async def index_document(
    qdrant_client: QdrantClient,
    collection_name: str,
    document_id: str,
    content: str,
    metadata: dict[str, Any],
) -> bool:
    """
    Index a document in Qdrant with chunking and embeddings.

    Args:
        qdrant_client: Qdrant client instance
        collection_name: Name of the collection
        document_id: Document ID
        content: Document content
        metadata: Additional metadata to store

    Returns:
        True if document indexed successfully
    """
    # Chunk the text
    chunks = chunk_text(content)

    # Generate embeddings for each chunk
    embeddings = []
    for chunk in chunks:
        embedding = await generate_embedding(chunk)
        embeddings.append(embedding)

    # Create payloads with chunk content and metadata
    payloads = [
        {
            "document_id": document_id,
            "chunk_index": i,
            "content": chunk,
            **metadata,
        }
        for i, chunk in enumerate(chunks)
    ]

    # Generate point IDs
    ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]

    # Insert vectors
    qdrant_client.insert_vectors(
        collection_name=collection_name,
        vectors=embeddings,
        payloads=payloads,
        ids=ids,
    )

    return True


async def reindex_document(
    qdrant_client: QdrantClient,
    collection_name: str,
    document_id: str,
    new_content: str,
    metadata: dict[str, Any],
) -> bool:
    """
    Re-index a document by deleting old vectors and inserting new ones.

    Args:
        qdrant_client: Qdrant client instance
        collection_name: Name of the collection
        document_id: Document ID
        new_content: New document content
        metadata: Additional metadata to store

    Returns:
        True if document re-indexed successfully
    """
    # Delete existing vectors for this document using Qdrant's filter deletion
    qdrant_client.client.delete(
        collection_name=collection_name,
        points_selector=FilterSelector(
            filter=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=str(document_id)),
                    )
                ]
            )
        ),
    )

    # Re-index with new content
    return await index_document(
        qdrant_client=qdrant_client,
        collection_name=collection_name,
        document_id=document_id,
        content=new_content,
        metadata=metadata,
    )
