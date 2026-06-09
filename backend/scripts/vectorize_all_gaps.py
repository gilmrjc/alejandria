#!/usr/bin/env python3
"""
Script para vectorizar todos los gaps existentes en Qdrant con búsqueda híbrida.

Este script:
1. Lista todos los gaps en la base de datos
2. Genera embeddings densos (semánticos) para cada gap
3. Genera vectores sparse (BM25-like) para búsqueda por palabras clave
4. Inserta los vectores híbridos en Qdrant
5. Muestra el progreso de la vectorización

Uso:
    python scripts/vectorize_all_gaps.py
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from shared.db.models import Gap
from shared.db.session import get_db_session
from shared.vector.qdrant import QdrantClient, generate_embedding


def list_all_gaps():
    """Lista todos los gaps en la base de datos."""
    session = get_db_session()
    try:
        gaps = session.query(Gap).all()
        return [
            {
                "id": str(gap.id),
                "question": gap.question,
                "context_missing": gap.context_missing,
                "priority": gap.priority,
                "status": gap.status,
                "document_id": str(gap.document_id),
            }
            for gap in gaps
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


async def vectorize_gap(gap_data: dict, qdrant_client: QdrantClient, collection_name: str):
    """
    Vectoriza un gap individual y lo inserta en Qdrant.

    Args:
        gap_data: Datos del gap
        qdrant_client: Cliente de Qdrant
        collection_name: Nombre de la colección
    """
    # Combinar question y context_missing para el embedding
    text_to_embed = gap_data["question"]
    if gap_data["context_missing"]:
        text_to_embed += f"\n\nContexto: {gap_data['context_missing']}"

    # Generar embedding denso (semántico)
    from shared.config.settings import settings
    print(f"  → Usando Ollama URL: {settings.ollama_url}")
    dense_vector = await generate_embedding(text_to_embed)

    # Generar vector sparse (BM25-like)
    sparse_vector = generate_sparse_vector(text_to_embed)

    # Preparar payload
    payload = {
        "gap_id": gap_data["id"],
        "document_id": gap_data["document_id"],
        "question": gap_data["question"],
        "context_missing": gap_data["context_missing"] or "",
        "priority": gap_data["priority"],
        "status": gap_data["status"],
    }

    # Generar point ID - Qdrant requires unsigned integers or UUIDs
    import hashlib
    point_id = int(hashlib.md5(gap_data["id"].encode()).hexdigest(), 16) % (2**63)

    # Insertar en Qdrant
    qdrant_client.insert_hybrid_vectors(
        collection_name=collection_name,
        dense_vectors=[dense_vector],
        sparse_vectors=[sparse_vector],
        payloads=[payload],
        ids=[point_id],
    )


async def main():
    """Función principal."""
    print("=" * 80)
    print("Vectorización de Gaps con Búsqueda Híbrida (Dense + Sparse)")
    print("=" * 80)
    print()

    # Listar gaps
    print("Obteniendo gaps de la base de datos...")
    gaps = list_all_gaps()

    if not gaps:
        print("⚠ No se encontraron gaps en la base de datos.")
        return

    print(f"✓ Encontrados {len(gaps)} gaps")
    print()

    # Mostrar gaps
    print("Gaps encontrados:")
    print("-" * 80)
    for i, gap in enumerate(gaps, 1):
        print(f"{i}. {gap['question'][:60]}...")
        print(f"   ID: {gap['id']}")
        print(f"   Prioridad: {gap['priority']}, Estado: {gap['status']}")
    print()

    # Inicializar cliente Qdrant
    print("Inicializando cliente Qdrant...")
    qdrant_client = QdrantClient()

    # Crear colección híbrida
    collection_name = "gaps_hybrid"
    print(f"Creando colección híbrida: {collection_name}")
    qdrant_client.create_hybrid_collection(
        collection_name=collection_name,
        vector_size=1024,  # BGE-M3
        distance="cosine",
        force_recreate=True,  # Recreate with correct config
    )
    print("✓ Colección creada o recreada")
    print()

    # Vectorizar gaps
    print("Vectorizando gaps...")
    print("-" * 80)

    success_count = 0
    error_count = 0

    for i, gap in enumerate(gaps, 1):
        try:
            await vectorize_gap(gap, qdrant_client, collection_name)
            print(f"✓ [{i}/{len(gaps)}] Vectorizado: {gap['question'][:50]}...")
            success_count += 1
        except Exception as e:
            print(f"✗ [{i}/{len(gaps)}] Error vectorizando {gap['id']}: {e}")
            error_count += 1

    print()
    print(f"✓ Total de gaps vectorizados: {success_count}")
    if error_count > 0:
        print(f"✗ Errores: {error_count}")
    print()

    print("=" * 80)
    print("Vectorización completada")
    print(f"Colección: {collection_name}")
    print(f"Total gaps: {len(gaps)}")
    print(f"Exitosos: {success_count}")
    print(f"Errores: {error_count}")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
