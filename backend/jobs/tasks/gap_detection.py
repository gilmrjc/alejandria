"""Gap detection Celery task for LLM-based document analysis."""

import uuid

from celery.utils.log import get_task_logger

from jobs.celery_app import celery_app
from shared.services.document_service import DocumentService
from shared.services.gap_service import GapService
from shared.services.gap_detection_service import GapDetectionService

logger = get_task_logger(__name__)


@celery_app.task(
    bind=True,
    name="gap_detection",
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
    import asyncio

    async def _async_gap_detection():
        try:
            logger.info(f"Starting gap detection for document {document_id}")

            # Create DB session
            from shared.db.session import get_db_session

            session = get_db_session()

            try:
                # Parse document_id
                doc_uuid = uuid.UUID(document_id)

                # 1. Read document using DocumentService
                document_service = DocumentService(session=session)
                document = document_service.get_document(doc_uuid)

                if not document:
                    logger.error(f"Document {document_id} not found")
                    return {"error": "Document not found", "gaps_created": 0}

                # 2. Read existing gaps to avoid duplicates
                gap_service = GapService(session=session)
                existing_gaps = gap_service.list_gaps_as_dict(
                    document_id=doc_uuid, status="pending"
                )

                logger.info(
                    f"Found {len(existing_gaps)} existing gaps for document {document_id}"
                )

                # 3. Execute LLM analysis using GapDetectionService
                gap_detection_service = GapDetectionService(session=session)
                gaps = await gap_detection_service.detect_gaps(
                    document_title=document.title,
                    document_content=document.content,
                    document_type="technical",  # TODO: make configurable
                    existing_gaps=existing_gaps,
                    role_affected="developer",  # TODO: make configurable
                    project_id=str(document.project_id),
                    use_tools=True,
                )

                if not gaps:
                    logger.info(f"No new gaps detected for document {document_id}")
                    return {"gaps_created": 0}

                # 4. Create new gaps using GapService
                gaps_created = 0
                for gap_data in gaps:
                    try:
                        gap = gap_service.create_gap(doc_uuid, gap_data)
                        if gap:
                            gaps_created += 1
                    except Exception as e:
                        logger.error(f"Error creating gap: {e}")

                logger.info(
                    f"Gap detection completed for document {document_id}: {gaps_created} gaps created"
                )
                return {"gaps_created": gaps_created}
            finally:
                session.close()

        except Exception as exc:
            logger.error(f"Gap detection failed for document {document_id}: {exc}")
            # Retry with exponential backoff
            raise self.retry(exc=exc, countdown=2**self.request.retries * 60)

    # Run async function
    return asyncio.run(_async_gap_detection())
