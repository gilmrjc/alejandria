#!/usr/bin/env python3
"""
One-time script to index existing documents in Qdrant with BM25.

This script:
1. Fetches all existing documents from the database
2. Creates Qdrant collections for each project with BM25 enabled
3. Indexes document chunks using BM25 text search
4. Reports progress and errors
"""

import sys
from pathlib import Path

# Add current directory to path (running from backend/scripts)
current_path = Path(__file__).parent.parent
sys.path.insert(0, str(current_path))

from qdrant_client.models import PointStruct  # noqa: E402
from sqlalchemy import select  # noqa: E402

from shared.db.models import Document, Project  # noqa: E402
from shared.db.session import get_db_session  # noqa: E402
from shared.vector.qdrant import QdrantClient  # noqa: E402


def index_document_for_bm25(
    qdrant_client: QdrantClient,
    document: Document,
    collection_name: str,
) -> bool:
    """
    Index a document for BM25 search by inserting text chunks.

    Args:
        qdrant_client: Qdrant client instance
        document: Document to index
        collection_name: Collection name (project_{project_id})

    Returns:
        True if successful, False otherwise
    """
    try:
        # Chunk the document content
        chunks = []
        chunk_size = 500
        overlap = 50

        paragraphs = document.content.split("\n\n")
        current_chunk = ""

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            if len(current_chunk) + len(paragraph) > chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                if overlap > 0 and len(current_chunk) > overlap:
                    current_chunk = current_chunk[-overlap:]
                else:
                    current_chunk = ""

            if current_chunk:
                current_chunk += "\n\n" + paragraph
            else:
                current_chunk = paragraph

        if current_chunk:
            chunks.append(current_chunk.strip())

        if not chunks:
            print(f"  Warning: No chunks generated for document {document.id}")
            return True

        # Create payloads with chunk content
        payloads = [
            {
                "document_id": str(document.id),
                "chunk_index": i,
                "content": chunk,
                "title": document.title,
            }
            for i, chunk in enumerate(chunks)
        ]

        # Generate point IDs
        ids = [f"{document.id}_chunk_{i}" for i in range(len(chunks))]

        # Insert into Qdrant with dummy vectors
        # Qdrant requires vectors even for BM25, so we use zero vectors
        # BM25 will use the text in the payload for search
        points = []
        for i, chunk_id in enumerate(ids):
            # Use a dummy vector (all zeros) since Qdrant requires vectors
            # BM25 will use the text in the payload for search
            dummy_vector = [0.0] * 1024
            points.append(
                PointStruct(
                    id=chunk_id,
                    vector=dummy_vector,
                    payload=payloads[i],
                )
            )

        qdrant_client.client.upsert(
            collection_name=collection_name,
            points=points,
        )

        print(f"  Indexed {len(chunks)} chunks for document {document.slug}")
        return True

    except Exception as e:
        print(f"  Error indexing document {document.id}: {e}")
        return False


def main():
    """Main function to index all existing documents."""
    print("Starting document indexing for BM25...")
    print("=" * 60)

    session = get_db_session()
    try:
        # Get all projects
        projects = session.execute(select(Project)).scalars().all()
        print(f"Found {len(projects)} projects")

        qdrant_client = QdrantClient()

        total_documents = 0
        total_indexed = 0
        total_failed = 0

        for project in projects:
            print(f"\nProcessing project: {project.name} (ID: {project.id})")
            collection_name = f"project_{project.id}"

            # Create collection with BM25 enabled
            print(f"  Creating collection '{collection_name}' with BM25...")
            try:
                qdrant_client.create_collection(
                    collection_name=collection_name,
                    vector_size=1024,
                    distance="cosine",
                    enable_bm25=True,
                )
                print("  Collection created/verified")
            except Exception as e:
                print(f"  Error creating collection: {e}")
                continue

            # Get all documents for this project
            documents = (
                session.execute(
                    select(Document).where(Document.project_id == project.id)
                )
                .scalars()
                .all()
            )

            print(f"  Found {len(documents)} documents")

            for document in documents:
                total_documents += 1
                print(f"  Indexing: {document.slug}")

                if index_document_for_bm25(qdrant_client, document, collection_name):
                    total_indexed += 1
                else:
                    total_failed += 1

        print("\n" + "=" * 60)
        print("Indexing complete!")
        print(f"Total documents: {total_documents}")
        print(f"Successfully indexed: {total_indexed}")
        print(f"Failed: {total_failed}")

        if total_failed > 0:
            print("\n⚠️  Some documents failed to index. Check the errors above.")
            sys.exit(1)
        else:
            print("\n✅ All documents indexed successfully!")
            sys.exit(0)

    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
    finally:
        session.close()


if __name__ == "__main__":
    main()
