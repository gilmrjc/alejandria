"""Proposal generation Celery task for creating proposals from resolved gaps."""

import asyncio
import uuid

from celery.utils.log import get_task_logger
from celery_once import QueueOnce

from jobs.celery_app import celery_app
from shared.services.document_service import DocumentService
from shared.services.proposal_generation_service import ProposalGenerationService

logger = get_task_logger(__name__)


@celery_app.task(
    bind=True,
    base=QueueOnce,
    once={"graceful": True},
    name="proposal_generation",
    max_retries=5,
    default_retry_delay=60,
)
def proposal_generation_task(self):
    """
    Generate proposals from gaps resolved in the last 30 minutes.

    This task runs periodically (via Celery Beat) to:
    1. Find gaps with status=responded in the last 30 minutes
    2. Group gaps by document
    3. Generate proposals for each document with new resolved gaps
    4. Create Proposal, ProposalDocument, and ProposalGap relationships

    Returns:
        Dict with proposals created count
    """
    async def _async_proposal_generation():
        try:
            from datetime import UTC, datetime, timedelta

            from shared.db.session import get_db_session
            from shared.llm.ollama_client import OllamaClient

            logger.info("Starting proposal generation task")

            # Create DB session
            session = get_db_session()

            try:
                # Calculate timestamp for 30 minutes ago
                thirty_minutes_ago = datetime.now(UTC) - timedelta(minutes=30)

                # Initialize services
                proposal_service = ProposalGenerationService(session=session)
                document_service = DocumentService(session=session)

                # Get resolved gaps in last 30 minutes
                resolved_gaps = proposal_service.get_resolved_gaps_since(
                    thirty_minutes_ago
                )

                if not resolved_gaps:
                    logger.info("No resolved gaps found in last 30 minutes")
                    return {"proposals_created": 0, "gaps_processed": 0}

                logger.info(f"Found {len(resolved_gaps)} resolved gaps")

                # Group gaps by document
                gaps_by_document = proposal_service.group_gaps_by_document(resolved_gaps)

                logger.info(f"Gaps grouped into {len(gaps_by_document)} documents")

                # Process each document
                proposals_created = 0
                total_gaps_processed = 0

                for document_id, gaps in gaps_by_document.items():
                    try:
                        # Check which gaps are already in existing proposals
                        gap_ids = [gap.id for gap in gaps]
                        existing_gap_ids = proposal_service.check_existing_proposals(
                            document_id, gap_ids
                        )

                        # Filter out gaps already in proposals
                        new_gap_ids = [gid for gid in gap_ids if gid not in existing_gap_ids]
                        new_gaps = [gap for gap in gaps if gap.id in new_gap_ids]

                        if not new_gaps:
                            logger.info(
                                f"All gaps for document {document_id} already in proposals, skipping"
                            )
                            continue

                        logger.info(
                            f"Processing document {document_id} with {len(new_gaps)} new gaps"
                        )

                        # Get document
                        document = document_service.get_document(document_id)

                        if not document:
                            logger.error(f"Document {document_id} not found")
                            continue

                        # Generate proposal prompt using LLM
                        ollama_client = OllamaClient()

                        # Build context for LLM
                        gaps_context = [
                            {
                                "question": gap.question,
                                "answer": gap.answer,
                                "priority": gap.priority,
                                "context_missing": gap.context_missing,
                                "role_affected": gap.role_affected,
                            }
                            for gap in new_gaps
                        ]

                        # Calculate adaptive timeout based on document size
                        # Estimate tokens: ~4 characters per token
                        estimated_tokens = len(document.content) // 4
                        tokens_per_second = 2.0
                        safety_margin = 2.0
                        max_timeout = 600.0
                        estimated_time = estimated_tokens / tokens_per_second
                        timeout = min(estimated_time * safety_margin, max_timeout)

                        logger.info(f"Adaptive timeout for proposal generation: {timeout:.1f}s")

                        # Generate prompt
                        prompt = await ollama_client.generate_proposal_prompt(
                            document_title=document.title,
                            document_content=document.content,
                            gaps=gaps_context,
                        )

                        if not prompt:
                            logger.error(f"Failed to generate prompt for document {document_id}")
                            continue

                        # Create proposal
                        proposal = proposal_service.create_proposal(
                            document_id=document_id,
                            gap_ids=new_gap_ids,
                            prompt=prompt,
                        )

                        proposals_created += 1
                        total_gaps_processed += len(new_gaps)

                        logger.info(
                            f"Created proposal {proposal.id} for document {document_id} with {len(new_gaps)} gaps"
                        )

                    except Exception as e:
                        logger.error(f"Error processing document {document_id}: {e}")
                        continue

                logger.info(
                    f"Proposal generation completed: {proposals_created} proposals created, {total_gaps_processed} gaps processed"
                )
                return {
                    "proposals_created": proposals_created,
                    "gaps_processed": total_gaps_processed,
                }

            finally:
                session.close()

        except Exception as exc:
            logger.error(f"Proposal generation failed: {exc}")
            # Retry with exponential backoff
            raise self.retry(exc=exc, countdown=2**self.request.retries * 60)

    # Run async function
    return asyncio.run(_async_proposal_generation())
