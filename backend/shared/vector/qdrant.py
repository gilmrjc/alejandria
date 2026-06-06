"""Qdrant vector database integration for semantic search."""

import re
from typing import Any

import httpx
from qdrant_client import QdrantClient as QdrantSDKClient
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
            # BM25 text search - use scroll for now as placeholder
            # Full BM25 implementation requires proper sparse vector setup
            # For now, return empty results
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
                    "model": "bge-m3",
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
                    "model": "bge-m3",
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
