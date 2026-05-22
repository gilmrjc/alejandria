#!/usr/bin/env python3
"""
Script para detectar y validar relaciones entre documentos.
Utilizado por el skill document-critique en el paso de investigación.
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Relationship:
    """Representa una relación entre documentos."""
    target: str
    relationship_type: str
    reason: str


@dataclass
class DocumentRelations:
    """Representa un documento con sus relaciones."""
    path: str
    id: str
    related: List[Relationship]
    related_targets_exist: bool
    missing_targets: List[str]


class RelationDetector:
    """Detecta y valida relaciones entre documentos."""
    
    def __init__(self, docs_dir: str):
        self.docs_dir = Path(docs_dir)
        self.id_to_path: Dict[str, str] = {}
        self._load_document_ids()
    
    def _load_document_ids(self):
        """Carga todos los IDs de documentos del directorio."""
        for md_file in self.docs_dir.rglob('*.md'):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
                if match:
                    front_matter = yaml.safe_load(match.group(1)) or {}
                    if 'id' in front_matter:
                        doc_id = front_matter['id']
                        rel_path = str(md_file.relative_to(self.docs_dir))
                        if doc_id in self.id_to_path and self.id_to_path[doc_id] != rel_path:
                            print(f"WARNING: Duplicate ID '{doc_id}' found in {rel_path}")
                        self.id_to_path[doc_id] = rel_path
            except Exception as e:
                print(f"Error parsing {md_file}: {e}")
    
    def parse_relations(self, file_path: str) -> Optional[DocumentRelations]:
        """
        Parsea las relaciones de un documento específico.
        
        Args:
            file_path: Ruta al archivo markdown (absoluta o relativa a docs/)
        
        Returns:
            DocumentRelations con las relaciones encontradas y validación
        """
        # Convertir a path absoluto si es relativo
        path = Path(file_path)
        if not path.is_absolute():
            # Si el path ya incluye el directorio base (ej: "docs/..."), usarlo directamente
            if file_path.startswith(str(self.docs_dir.name) + '/') or file_path.startswith(str(self.docs_dir.name) + '\\'):
                path = self.docs_dir.parent / file_path
            else:
                path = self.docs_dir / file_path
        
        if not path.exists():
            print(f"Error: File not found: {path}")
            return None
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if not match:
                return None
            
            front_matter = yaml.safe_load(match.group(1)) or {}
            if 'id' not in front_matter:
                return None
            
            doc_id = front_matter['id']
            rel_path = str(path.relative_to(self.docs_dir))
            
            # Parse related field
            related_raw = front_matter.get('related', [])
            related = []
            for rel in related_raw:
                if isinstance(rel, dict):
                    related.append(Relationship(
                        target=rel.get('target', ''),
                        relationship_type=rel.get('relationship_type', ''),
                        reason=rel.get('reason', '')
                    ))
            
            # Validar que los targets existan
            missing_targets = []
            for rel in related:
                if rel.target not in self.id_to_path:
                    missing_targets.append(rel.target)
            
            return DocumentRelations(
                path=rel_path,
                id=doc_id,
                related=related,
                related_targets_exist=len(missing_targets) == 0,
                missing_targets=missing_targets
            )
        except Exception as e:
            print(f"Error parsing {path}: {e}")
            return None
    
    def format_relations(self, relations: DocumentRelations) -> str:
        """Formatea las relaciones para uso en el skill."""
        if not relations.related:
            return f"Documento '{relations.id}' no tiene relaciones (campo 'related' vacío o ausente)."
        
        output = [f"Relaciones del documento '{relations.id}':"]
        output.append(f"Path: {relations.path}")
        output.append(f"Total relaciones: {len(relations.related)}")
        
        if relations.missing_targets:
            output.append(f"\n⚠️  ADVERTENCIA: {len(relations.missing_targets)} targets no existen:")
            for target in relations.missing_targets:
                output.append(f"  - {target}")
        
        output.append("\nRelaciones encontradas:")
        for rel in relations.related:
            exists = "✓" if rel.target in self.id_to_path else "✗"
            target_path = self.id_to_path.get(rel.target, "NO ENCONTRADO")
            output.append(f"\n  {exists} Target: {rel.target}")
            output.append(f"     Path: {target_path}")
            output.append(f"     Tipo: {rel.relationship_type}")
            output.append(f"     Razón: {rel.reason}")
        
        return "\n".join(output)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Detectar y validar relaciones entre documentos'
    )
    parser.add_argument('file_path', help='Ruta al archivo markdown a analizar')
    parser.add_argument('--docs-dir', default='docs', help='Directorio base de documentos (default: docs)')
    
    args = parser.parse_args()
    
    # Determinar docs_dir
    script_dir = Path(__file__).parent.parent.parent.parent.parent
    docs_dir = script_dir / args.docs_dir
    
    if not docs_dir.exists():
        print(f"Error: Directorio docs no encontrado en {docs_dir}")
        return
    
    detector = RelationDetector(str(docs_dir))
    relations = detector.parse_relations(args.file_path)
    
    if relations:
        print(detector.format_relations(relations))
    else:
        print("No se encontraron relaciones o el archivo no tiene frontmatter válido.")


if __name__ == '__main__':
    main()
