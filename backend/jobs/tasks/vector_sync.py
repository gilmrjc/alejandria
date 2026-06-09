"""Vector sync Celery task for Qdrant synchronization."""

import uuid

from celery.utils.log import get_task_logger
from celery_once import QueueOnce
from qdrant_client.models import FieldCondition, Filter, FilterSelector, MatchValue

from jobs.celery_app import celery_app
from shared.services.document_service import DocumentService
from shared.vector.qdrant import QdrantClient, chunk_document, generate_embedding

logger = get_task_logger(__name__)


@celery_app.task(
    bind=True,
    base=QueueOnce,
    once={"graceful": True},
    name="vector_sync",
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
    import asyncio

    try:
        logger.info(f"Starting vector sync for document {document_id}")

        # Parse document_id
        doc_uuid = uuid.UUID(document_id)

        # 1. Read document using DocumentService
        with DocumentService() as document_service:
            document = document_service.get_document(doc_uuid)

        if not document:
            logger.error(f"Document {document_id} not found")
            return {"error": "Document not found", "vectors_synced": 0}

        # 2. Apply chunking strategy (512 tokens, 50 overlap)
        chunks = chunk_document(document.content, max_tokens=512, overlap=50)

        if not chunks:
            logger.warning(f"No chunks generated for document {document_id}")
            return {"vectors_synced": 0}

        logger.info(f"Generated {len(chunks)} chunks for document {document_id}")

        # 3. Generate embeddings for each chunk
        async def generate_embeddings():
            embeddings = []
            for chunk in chunks:
                embedding = await generate_embedding(chunk["text"])
                embeddings.append(embedding)
            return embeddings

        embeddings = asyncio.run(generate_embeddings())

        # 4. Sync with Qdrant using QdrantClient
        qdrant_client = QdrantClient()

        # Collection name based on project_id
        collection_name = f"project_{document.project_id}"

        # Create collection if it doesn't exist
        qdrant_client.create_collection(collection_name)

        # Delete existing vectors for this document
        qdrant_client.client.delete(
            collection_name=collection_name,
            points_selector=FilterSelector(
                filter=Filter(
                    must=[
                        FieldCondition(
                            key="document_id", match=MatchValue(value=str(doc_uuid))
                        )
                    ]
                )
            ),
        )

        # Prepare payloads
        payloads = [
            {
                "document_id": str(doc_uuid),
                "chunk_index": chunk["metadata"]["chunk_index"],
                "content": chunk["text"],
                "section_title": chunk["metadata"].get("section_title"),
                "section_level": chunk["metadata"].get("section_level"),
                "total_chunks": chunk["metadata"]["total_chunks"],
                "token_count": chunk["metadata"]["token_count"],
            }
            for chunk in chunks
        ]

        # Generate point IDs
        ids = [f"{doc_uuid}_chunk_{i}" for i in range(len(chunks))]

        # Insert vectors
        qdrant_client.insert_vectors(
            collection_name=collection_name,
            vectors=embeddings,
            payloads=payloads,
            ids=ids,
        )

        # 5. Update document with vector_id (use first chunk ID)
        # TODO: Update VectorSyncLog if needed

        logger.info(
            f"Vector sync completed for document {document_id}: {len(embeddings)} vectors synced"
        )
        return {"vectors_synced": len(embeddings)}

    except Exception as exc:
        logger.error(f"Vector sync failed for document {document_id}: {exc}")
        raise self.retry(exc=exc, countdown=2**self.request.retries * 60)
