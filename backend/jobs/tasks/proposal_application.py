"""Proposal application Celery task for applying approved proposals to documents."""

import asyncio
import uuid

from celery.utils.log import get_task_logger
from celery_once import QueueOnce

from jobs.celery_app import celery_app
from shared.services.document_service import DocumentService
from shared.services.proposal_application_service import ProposalApplicationService
from shared.services.rollback_service import RollbackService

logger = get_task_logger(__name__)


@celery_app.task(
    bind=True,
    base=QueueOnce,
    once={"graceful": True},
    name="proposal_application",
    max_retries=5,
    default_retry_delay=60,
)
def proposal_application_task(self, proposal_id: str):
    """
    Apply an approved proposal to its associated documents.

    This task:
    1. Gets the proposal with status=accepted
    2. Gets all documents from ProposalDocument relationships
    3. For each document:
       - Applies proposal instructions using LLM
       - Updates document content
       - Versioning middleware automatically creates snapshot
    4. Updates proposal status to implemented
    5. On failure: triggers automatic rollback

    Args:
        proposal_id: UUID of the proposal to apply

    Returns:
        Dict with application results
    """
    async def _async_proposal_application():
        try:
            from shared.db.session import get_db_session
            from shared.llm.ollama_client import OllamaClient

            logger.info(f"Starting proposal application for proposal {proposal_id}")

            # Create DB session
            session = get_db_session()

            try:
                # Parse proposal_id
                proposal_uuid = uuid.UUID(proposal_id)

                # Initialize services
                proposal_service = ProposalApplicationService(session=session)
                document_service = DocumentService(session=session)
                rollback_service = RollbackService(session=session)

                # Get proposal
                proposal = proposal_service.get_proposal(proposal_uuid)

                if not proposal:
                    logger.error(f"Proposal {proposal_id} not found")
                    return {"error": "Proposal not found", "documents_updated": 0}

                # Validate proposal is in accepted status
                if proposal.status != "accepted":
                    logger.warning(
                        f"Proposal {proposal_id} is not in accepted status, current status: {proposal.status}"
                    )
                    return {
                        "error": f"Proposal not in accepted status: {proposal.status}",
                        "documents_updated": 0,
                    }

                # Get associated documents
                documents = proposal_service.get_proposal_documents(proposal_uuid)

                if not documents:
                    logger.warning(f"No documents found for proposal {proposal_id}")
                    return {"documents_updated": 0, "message": "No documents to update"}

                logger.info(f"Found {len(documents)} documents for proposal {proposal_id}")

                # Store document IDs for rollback on failure
                affected_document_ids = [doc.id for doc in documents]

                # Apply instructions to each document
                documents_updated = 0
                ollama_client = OllamaClient()

                for document in documents:
                    try:
                        logger.info(f"Applying proposal to document {document.id}")

                        # Calculate adaptive timeout based on document size
                        estimated_tokens = len(document.content) // 4
                        tokens_per_second = 2.0
                        safety_margin = 2.0
                        max_timeout = 600.0
                        estimated_time = estimated_tokens / tokens_per_second
                        timeout = min(estimated_time * safety_margin, max_timeout)

                        logger.info(f"Adaptive timeout for proposal application: {timeout:.1f}s")

                        # Apply instructions using LLM
                        updated_content = await ollama_client.apply_proposal_instructions(
                            document_title=document.title,
                            document_content=document.content,
                            instructions=proposal.description,
                        )

                        if not updated_content:
                            logger.error(
                                f"Failed to apply instructions to document {document.id}"
                            )
                            raise Exception("LLM failed to apply instructions")

                        # Update document content
                        document.content = updated_content
                        session.commit()
                        session.refresh(document)

                        documents_updated += 1
                        logger.info(f"Successfully updated document {document.id}")

                    except Exception as e:
                        logger.error(f"Error applying proposal to document {document.id}: {e}")
                        # Trigger rollback for all affected documents
                        logger.info(f"Triggering rollback for {len(affected_document_ids)} documents")
                        for doc_id in affected_document_ids:
                            try:
                                rollback_service.rollback_to_latest(doc_id)
                                logger.info(f"Rolled back document {doc_id}")
                            except Exception as rollback_error:
                                logger.error(
                                    f"Failed to rollback document {doc_id}: {rollback_error}"
                                )

                        # Mark proposal as failed
                        proposal_service.mark_proposal_failed(
                            proposal_uuid, str(e)
                        )

                        raise

                # Mark proposal as implemented
                proposal_service.mark_proposal_implemented(proposal_uuid)

                logger.info(
                    f"Proposal application completed: {documents_updated} documents updated"
                )
                return {"documents_updated": documents_updated}

            finally:
                session.close()

        except Exception as exc:
            logger.error(f"Proposal application failed for proposal {proposal_id}: {exc}")
            # Retry with exponential backoff
            raise self.retry(exc=exc, countdown=2**self.request.retries * 60)

    # Run async function
    return asyncio.run(_async_proposal_application())
