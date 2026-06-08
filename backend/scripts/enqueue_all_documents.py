#!/usr/bin/env python3
"""
Script para encolar todos los documentos existentes para detección de gaps.

Este script:
1. Lista todos los documentos en la base de datos
2. Encola una tarea de gap_detection para cada uno
3. Muestra el estado de la cola de Celery

Uso:
    python scripts/enqueue_all_documents.py
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from jobs.celery_app import celery_app
from jobs.tasks.gap_detection import gap_detection_task
from shared.db.models import Document
from shared.db.session import get_db_session


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
            }
            for doc in documents
        ]
    finally:
        session.close()


def enqueue_gap_detection(document_id: str):
    """Encola una tarea de gap detection para un documento."""
    result = gap_detection_task.delay(document_id)
    return result.id


def get_queue_status():
    """Obtiene el estado de la cola de Celery."""
    inspector = celery_app.control.inspect()

    # Información de workers
    active = inspector.active()
    scheduled = inspector.scheduled()
    reserved = inspector.reserved()

    return {
        "active": active,
        "scheduled": scheduled,
        "reserved": reserved,
    }


def main():
    """Función principal."""
    print("=" * 80)
    print("Encolado de Documentos para Detección de Gaps")
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
        print(f"{i}. {doc['title']} (slug: {doc['slug']})")
        print(f"   ID: {doc['id']}")
        print(f"   Tamaño: {doc['content_length']} caracteres")
    print()

    # Encolar tareas
    print("Encolando tareas de gap_detection...")
    print("-" * 80)

    task_ids = []
    for doc in documents:
        try:
            task_id = enqueue_gap_detection(doc["id"])
            task_ids.append(
                {
                    "document_id": doc["id"],
                    "document_title": doc["title"],
                    "task_id": task_id,
                }
            )
            print(f"✓ Encolado: {doc['title']} -> Task ID: {task_id}")
        except Exception as e:
            print(f"✗ Error encolando {doc['title']}: {e}")

    print()
    print(f"✓ Total de tareas encoladas: {len(task_ids)}")
    print()

    # Mostrar estado de la cola
    print("Estado de la cola de Celery:")
    print("-" * 80)

    try:
        status = get_queue_status()

        if status["active"]:
            print("Tareas activas:")
            for worker, tasks in status["active"].items():
                print(f"  {worker}: {len(tasks)} tareas")
        else:
            print("Tareas activas: 0")

        if status["scheduled"]:
            print("Tareas programadas:")
            for worker, tasks in status["scheduled"].items():
                print(f"  {worker}: {len(tasks)} tareas")
        else:
            print("Tareas programadas: 0")

        if status["reserved"]:
            print("Tareas reservadas:")
            for worker, tasks in status["reserved"].items():
                print(f"  {worker}: {len(tasks)} tareas")
        else:
            print("Tareas reservadas: 0")

    except Exception as e:
        print(f"⚠ No se pudo obtener estado de la cola: {e}")
        print("  (Asegúrate de que el worker de Celery esté corriendo)")

    print()
    print("=" * 80)
    print("Para ver el progreso, revisa los logs del worker:")
    print("  docker compose logs -f celery-worker")
    print("=" * 80)


if __name__ == "__main__":
    main()
