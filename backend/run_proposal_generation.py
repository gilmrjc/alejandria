"""Script para ejecutar proposal_generation de forma síncrona."""

import sys
from pathlib import Path

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent))

from shared.db.session import get_db_session
from shared.services.proposal_generation_service import ProposalGenerationService
from shared.services.document_service import DocumentService
from shared.llm.ollama_client import OllamaClient
from datetime import UTC, datetime, timedelta


def main():
    """Ejecutar proposal_generation de forma síncrona."""
    print("Ejecutando proposal_generation de forma síncrona...")

    # Create DB session
    session = get_db_session()

    try:
        # Calculate timestamp for 30 minutes ago
        thirty_minutes_ago = datetime.now(UTC) - timedelta(minutes=30)

        # Initialize services
        proposal_service = ProposalGenerationService(session=session)
        document_service = DocumentService(session=session)

        # Get resolved gaps in last 30 minutes
        resolved_gaps = proposal_service.get_resolved_gaps_since(thirty_minutes_ago)

        if not resolved_gaps:
            print("No resolved gaps found in last 30 minutes")
            return {"proposals_created": 0, "gaps_processed": 0}

        print(f"Found {len(resolved_gaps)} resolved gaps")

        # Group gaps by document
        gaps_by_document = proposal_service.group_gaps_by_document(resolved_gaps)

        print(f"Gaps grouped into {len(gaps_by_document)} documents")

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
                    print(f"All gaps for document {document_id} already in proposals, skipping")
                    continue

                print(f"Processing document {document_id} with {len(new_gaps)} new gaps")

                # Get document
                document = document_service.get_document(document_id)

                if not document:
                    print(f"Document {document_id} not found")
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

                # Generate prompt (synchronous wrapper)
                import asyncio

                prompt = asyncio.run(
                    ollama_client.generate_proposal_prompt(
                        document_title=document.title,
                        document_content=document.content,
                        gaps=gaps_context,
                    )
                )

                if not prompt:
                    print(f"Failed to generate prompt for document {document_id}")
                    continue

                # Create proposal
                proposal = proposal_service.create_proposal(
                    document_id=document_id,
                    gap_ids=new_gap_ids,
                    prompt=prompt,
                )

                proposals_created += 1
                total_gaps_processed += len(new_gaps)

                print(f"Created proposal {proposal.id} for document {document_id} with {len(new_gaps)} gaps")

            except Exception as e:
                print(f"Error processing document {document_id}: {e}")
                import traceback

                traceback.print_exc()
                continue

        print(f"Proposal generation completed: {proposals_created} proposals created, {total_gaps_processed} gaps processed")
        return {
            "proposals_created": proposals_created,
            "gaps_processed": total_gaps_processed,
        }

    finally:
        session.close()


if __name__ == "__main__":
    result = main()
    print(f"Resultado: {result}")
