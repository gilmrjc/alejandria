#!/usr/bin/env python3
"""
Script para vectorizar todos los documentos existentes en Qdrant con búsqueda híbrida.

Este script:
1. Lista todos los documentos en la base de datos
2. Genera embeddings densos (semánticos) para cada chunk de documento
3. Genera vectores sparse (BM25-like) para búsqueda por palabras clave
4. Inserta los vectores híbridos en Qdrant
5. Muestra el progreso de la vectorización

Uso:
    python scripts/vectorize_all_documents.py
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from sqlalchemy import select
from shared.db.models import Document
from shared.db.session import get_db_session
from shared.vector.qdrant import QdrantClient, generate_embedding, chunk_document


def list_all_documents():
    """Lista todos los documentos en la base de datos."""
    session = get_db_session()
    try:
        documents = session.query(Document).all()
        return [
            {
                "id": str(doc.id),
                "title": doc.title,
                "slug": doc.slug,
                "content_length": len(doc.content) if doc.content else 0,
                "project_id": str(doc.project_id),
            }
            for doc in documents
        ]
    finally:
        session.close()


def generate_sparse_vector(text: str) -> dict[str, int]:
    """
    Genera un vector sparse simple basado en frecuencia de términos (BM25-like).

    Args:
        text: Texto a procesar

    Returns:
        Diccionario con términos y sus frecuencias
    """
    from collections import Counter
    import re

    # Tokenizar: convertir a minúsculas, eliminar puntuación
    words = re.findall(r"\b\w+\b", text.lower())

    # Contar frecuencia de términos
    term_freq = Counter(words)

    # Filtrar stop words comunes
    stop_words = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "must", "what", "how", "why", "when", "where",
        "who", "which", "that", "this", "these", "those", "with", "from", "for",
        "and", "or", "but", "in", "on", "at", "to", "by", "of", "as", "it",
    }

    sparse_vector = {
        term: freq for term, freq in term_freq.items()
        if term not in stop_words and len(term) > 2
    }

    return sparse_vector


async def vectorize_document(doc_data: dict, qdrant_client: QdrantClient):
    """
    Vectoriza un documento individual y lo inserta en Qdrant.

    Args:
        doc_data: Datos del documento
        qdrant_client: Cliente de Qdrant
    """
    session = get_db_session()
    try:
        # Obtener documento completo
        doc = session.execute(
            select(Document).where(Document.id == doc_data["id"])
        ).scalar_one_or_none()

        if not doc:
            print(f"✗ Documento {doc_data['id']} no encontrado")
            return

        # Chunk del documento
        chunks = chunk_document(doc.content, max_tokens=512, overlap=50)

        if not chunks:
            print(f"✗ No se generaron chunks para {doc.title}")
            return

        # Generar embeddings densos para cada chunk
        dense_vectors = []
        for chunk in chunks:
            embedding = await generate_embedding(chunk["text"])
            dense_vectors.append(embedding)

        # Generar vectores sparse para cada chunk
        sparse_vectors = []
        for chunk in chunks:
            sparse_vector = generate_sparse_vector(chunk["text"])
            sparse_vectors.append(sparse_vector)

        # Preparar payloads
        payloads = [
            {
                "document_id": str(doc.id),
                "chunk_index": chunk["metadata"]["chunk_index"],
                "content": chunk["text"],
                "section_title": chunk["metadata"].get("section_title"),
                "section_level": chunk["metadata"].get("section_level"),
                "total_chunks": chunk["metadata"]["total_chunks"],
                "token_count": chunk["metadata"]["token_count"],
            }
            for chunk in chunks
        ]

        # Generar point IDs - Qdrant requires unsigned integers or UUIDs
        # Use hash of the string to generate a unique integer ID
        import hashlib
        ids = [int(hashlib.md5(f"{doc.id}_chunk_{i}".encode()).hexdigest(), 16) % (2**63) for i in range(len(chunks))]

        # Nombre de colección basado en project_id
        collection_name = f"project_{doc.project_id}_hybrid"

        # Crear colección híbrida si no existe
        try:
            qdrant_client.create_hybrid_collection(
                collection_name=collection_name,
                vector_size=1024,  # BGE-M3
                distance="cosine",
            )
        except Exception as e:
            if "already exists" not in str(e):
                raise

        # Eliminar vectores existentes para este documento
        from qdrant_client.models import FieldCondition, Filter, FilterSelector, MatchValue
        qdrant_client.client.delete(
            collection_name=collection_name,
            points_selector=FilterSelector(
                filter=Filter(
                    must=[
                        FieldCondition(
                            key="document_id", match=MatchValue(value=str(doc.id))
                        )
                    ]
                )
            ),
        )

        # Insertar vectores híbridos
        qdrant_client.insert_hybrid_vectors(
            collection_name=collection_name,
            dense_vectors=dense_vectors,
            sparse_vectors=sparse_vectors,
            payloads=payloads,
            ids=ids,
        )

        return len(chunks)

    finally:
        session.close()


async def main():
    """Función principal."""
    print("=" * 80)
    print("Vectorización de Documentos con Búsqueda Híbrida (Dense + Sparse)")
    print("=" * 80)
    print()

    # Listar documentos
    print("Obteniendo documentos de la base de datos...")
    documents = list_all_documents()

    if not documents:
        print("⚠ No se encontraron documentos en la base de datos.")
        return

    print(f"✓ Encontrados {len(documents)} documentos")
    print()

    # Mostrar documentos
    print("Documentos encontrados:")
    print("-" * 80)
    for i, doc in enumerate(documents, 1):
        print(f"{i}. {doc['title']}")
        print(f"   ID: {doc['id']}")
        print(f"   Slug: {doc['slug']}")
        print(f"   Tamaño: {doc['content_length']} caracteres")
    print()

    # Inicializar cliente Qdrant
    print("Inicializando cliente Qdrant...")
    qdrant_client = QdrantClient()
    print("✓ Cliente inicializado")
    print()

    # Vectorizar documentos
    print("Vectorizando documentos...")
    print("-" * 80)

    success_count = 0
    error_count = 0
    total_chunks = 0

    for i, doc in enumerate(documents, 1):
        try:
            chunks_count = await vectorize_document(doc, qdrant_client)
            if chunks_count:
                print(f"✓ [{i}/{len(documents)}] Vectorizado: {doc['title']} ({chunks_count} chunks)")
                success_count += 1
                total_chunks += chunks_count
            else:
                print(f"⚠ [{i}/{len(documents)}] Sin chunks: {doc['title']}")
        except Exception as e:
            print(f"✗ [{i}/{len(documents)}] Error vectorizando {doc['id']}: {e}")
            error_count += 1

    print()
    print(f"✓ Total de documentos vectorizados: {success_count}")
    print(f"✓ Total de chunks procesados: {total_chunks}")
    if error_count > 0:
        print(f"✗ Errores: {error_count}")
    print()

    print("=" * 80)
    print("Vectorización completada")
    print(f"Documentos: {len(documents)}")
    print(f"Exitosos: {success_count}")
    print(f"Errores: {error_count}")
    print(f"Chunks totales: {total_chunks}")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
