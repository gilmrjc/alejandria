"""Question generation Celery task for vectorizing gap answers."""

import asyncio
import uuid

from celery.utils.log import get_task_logger
from celery_once import QueueOnce

from jobs.celery_app import celery_app
from shared.services.gap_service import GapService
from shared.vector.qdrant import QdrantClient, generate_embedding

logger = get_task_logger(__name__)


@celery_app.task(
    bind=True,
    base=QueueOnce,
    once={"graceful": True},
    name="question_generation",
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

        # Parse gap_id
        gap_uuid = uuid.UUID(gap_id)

        # 1. Read gap using GapService
        from shared.db.session import get_db_session, get_db_session_context

        with get_db_session_context() as session:
            gap_service = GapService(session=session)
            gap = gap_service.get_gap(gap_uuid)

        if not gap:
            logger.error(f"Gap {gap_id} not found")
            return {"error": "Gap not found", "answer_vectorized": False}

        # 2. Generate embedding of the answer using OllamaClient
        async def generate_answer_embedding():
            return await generate_embedding(answer)

        embedding = asyncio.run(generate_answer_embedding())

        if not embedding:
            logger.error(f"Failed to generate embedding for gap {gap_id}")
            return {"error": "Embedding generation failed", "answer_vectorized": False}

        # 3. Sync with Qdrant for semantic search
        qdrant_client = QdrantClient()

        # Collection name for answers (could be project-specific)
        collection_name = "gap_answers"

        # Create collection if it doesn't exist
        qdrant_client.create_collection(collection_name)

        # Prepare payload
        payload = {
            "gap_id": str(gap_uuid),
            "document_id": str(gap.document_id),
            "question": gap.question,
            "answer": answer,
            "priority": gap.priority,
            "status": gap.status,
        }

        # Insert vector
        qdrant_client.insert_vectors(
            collection_name=collection_name,
            vectors=[embedding],
            payloads=[payload],
            ids=[str(gap_uuid)],
        )

        # 4. Update gap with vector_id (if needed)
        # TODO: Add vector_id field to Gap model if needed

        logger.info(f"Question generation completed for gap {gap_id}")
        return {"answer_vectorized": True}

    except Exception as exc:
        logger.error(f"Question generation failed for gap {gap_id}: {exc}")
        raise self.retry(exc=exc, countdown=2**self.request.retries * 60)
