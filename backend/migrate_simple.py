#!/usr/bin/env python3
"""
Script simple para migrar documentos desde los archivos JSON preparados.
"""

import glob
import json
import sys
import uuid

sys.path.insert(0, "/workspace")

try:
    from sqlalchemy import select

    from shared.db.models import Document
    from shared.db.session import get_db_session

    ORGANIZATION_ID = uuid.UUID("72f77226-bfc0-427f-9915-e56de5caa588")
    PROJECT_ID = uuid.UUID("6081c2e6-9fe7-4d1f-907a-7a0f8681e1ef")
    MIGRATED_SLUGS = {"vision-mission", "organizational-culture"}

    json_files = sorted(glob.glob("/tmp/migration_*.json"))
    json_files = [
        f for f in json_files if not any(slug in f for slug in MIGRATED_SLUGS)
    ]

    print(f"Migrando {len(json_files)} documentos a la base de datos...")

    session = get_db_session()
    success_count = 0
    error_count = 0
    skipped_count = 0

    try:
        for json_file in json_files:
            try:
                with open(json_file) as f:
                    doc_data = json.load(f)

                slug = doc_data["slug"]

                existing = session.execute(
                    select(Document).where(Document.slug == slug)
                ).scalar_one_or_none()

                if existing:
                    print(f"⊘ Saltado (ya existe): {doc_data['filename']} -> {slug}")
                    skipped_count += 1
                    continue

                doc = Document(
                    project_id=PROJECT_ID,
                    organization_id=ORGANIZATION_ID,
                    title=doc_data["title"],
                    slug=slug,
                    content=doc_data["content"],
                    filename=doc_data["filename"],
                    rating=doc_data.get("rating"),
                )

                session.add(doc)
                session.commit()
                session.refresh(doc)

                print(f"✓ Creado: {doc_data['filename']} -> {slug} (ID: {doc.id})")
                success_count += 1

            except Exception as e:
                print(f"✗ Error procesando {json_file}: {e}")
                session.rollback()
                error_count += 1

        print("\nMigración completada:")
        print(f"  ✓ Exitosos: {success_count}")
        print(f"  ⊘ Saltados (ya existían): {skipped_count}")
        print(f"  ✗ Errores: {error_count}")
        print(f"  Total procesados: {len(json_files)}")

    finally:
        session.close()

except Exception as e:
    print(f"Error general: {e}")
    import traceback

    traceback.print_exc()
