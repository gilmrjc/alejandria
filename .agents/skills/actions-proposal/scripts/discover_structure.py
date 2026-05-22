#!/usr/bin/env python3
"""
Script para determinar la estructura del proyecto con depth 2.
Utiliza el campo 'related' del frontmatter para descubrir relaciones y archivos hermanos.
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class DocumentInfo:
    """Información de un documento."""
    path: str
    id: str
    type: Optional[str]
    title: Optional[str]
    related: List[str]
    siblings: Set[str]


class StructureDiscoverer:
    """Descubre la estructura del proyecto con depth 2."""
    
    def __init__(self, docs_dir: str, depth: int = 2):
        self.docs_dir = Path(docs_dir)
        self.depth = depth
        self.id_to_path: Dict[str, str] = {}
        self.path_to_info: Dict[str, DocumentInfo] = {}
        self._load_documents()
    
    def _load_documents(self):
        """Carga todos los documentos del directorio."""
        for md_file in self.docs_dir.rglob('*.md'):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
                if match:
                    front_matter = yaml.safe_load(match.group(1)) or {}
                    doc_id = front_matter.get('id', '')
                    rel_path = str(md_file.relative_to(self.docs_dir))
                    
                    # Extraer relaciones
                    related_raw = front_matter.get('related', [])
                    related_ids = []
                    for rel in related_raw:
                        if isinstance(rel, dict):
                            related_ids.append(rel.get('target', ''))
                    
                    self.id_to_path[doc_id] = rel_path
                    self.path_to_info[rel_path] = DocumentInfo(
                        path=rel_path,
                        id=doc_id,
                        type=front_matter.get('type'),
                        title=front_matter.get('title'),
                        related=related_ids,
                        siblings=set()
                    )
            except Exception as e:
                print(f"Error parsing {md_file}: {e}")
    
    def _discover_siblings(self):
        """Descubre archivos hermanos basándose en directorios y relaciones."""
        # Agrupar por directorio padre (depth 1)
        dir_to_docs: Dict[str, List[str]] = defaultdict(list)
        for path in self.path_to_info.keys():
            parent_dir = str(Path(path).parent)
            dir_to_docs[parent_dir].append(path)
        
        # Marcar hermanos por directorio
        for docs in dir_to_docs.values():
            for path1 in docs:
                for path2 in docs:
                    if path1 != path2:
                        self.path_to_info[path1].siblings.add(path2)
        
        # Agregar hermanos por relaciones (depth 2)
        for path, info in self.path_to_info.items():
            for related_id in info.related:
                if related_id in self.id_to_path:
                    related_path = self.id_to_path[related_id]
                    # Los hermanos del relacionado también son hermanos (depth 2)
                    if related_path in self.path_to_info:
                        for sibling in self.path_to_info[related_path].siblings:
                            info.siblings.add(sibling)
    
    def get_structure(self, file_path: str) -> Dict:
        """
        Obtiene la estructura del proyecto desde la perspectiva de un archivo específico.
        
        Args:
            file_path: Ruta al archivo de referencia
        
        Returns:
            Diccionario con la estructura del proyecto
        """
        self._discover_siblings()
        
        # Normalizar path
        path = Path(file_path)
        if not path.is_absolute():
            path = self.docs_dir / file_path
        
        rel_path = str(path.relative_to(self.docs_dir))
        
        if rel_path not in self.path_to_info:
            return {"error": f"Archivo no encontrado: {rel_path}"}
        
        current_info = self.path_to_info[rel_path]
        
        # Obtener directorio actual y directorios cercanos (depth 2)
        current_dir = Path(rel_path).parent
        parent_dir = current_dir.parent if current_dir != Path('.') else None
        
        # Estructura del directorio actual
        current_dir_structure = self._get_directory_structure(current_dir)
        
        # Estructura del directorio padre (depth 2)
        parent_dir_structure = None
        if parent_dir and parent_dir != Path('.'):
            parent_dir_structure = self._get_directory_structure(parent_dir)
        
        # Archivos hermanos (depth 1 y 2)
        siblings = sorted(list(current_info.siblings))
        
        return {
            "current_file": {
                "path": rel_path,
                "id": current_info.id,
                "type": current_info.type,
                "title": current_info.title
            },
            "current_directory": str(current_dir),
            "current_directory_structure": current_dir_structure,
            "parent_directory": str(parent_dir) if parent_dir else None,
            "parent_directory_structure": parent_dir_structure,
            "siblings": siblings,
            "related_files": [self.id_to_path.get(r, r) for r in current_info.related]
        }
    
    def _get_directory_structure(self, directory: Path) -> Dict:
        """Obtiene la estructura de un directorio específico."""
        structure = {
            "subdirectories": [],
            "files": []
        }
        
        dir_path = self.docs_dir / directory
        if not dir_path.exists():
            return structure
        
        for item in sorted(dir_path.iterdir()):
            if item.is_dir() and not item.name.startswith('.'):
                structure["subdirectories"].append(item.name)
            elif item.is_file() and item.suffix == '.md':
                rel_path = str(item.relative_to(self.docs_dir))
                if rel_path in self.path_to_info:
                    info = self.path_to_info[rel_path]
                    structure["files"].append({
                        "name": item.name,
                        "path": rel_path,
                        "id": info.id,
                        "type": info.type,
                        "title": info.title
                    })
        
        return structure
    
    def format_structure(self, structure: Dict) -> str:
        """Formatea la estructura para uso en el skill."""
        if "error" in structure:
            return structure["error"]
        
        output = []
        
        # Archivo actual
        current = structure["current_file"]
        output.append(f"**Archivo actual**: {current['path']}")
        output.append(f"  - ID: {current['id']}")
        output.append(f"  - Tipo: {current['type'] or 'No especificado'}")
        output.append(f"  - Título: {current['title'] or 'No especificado'}")
        output.append("")
        
        # Directorio actual
        output.append(f"**Directorio actual**: {structure['current_directory']}")
        current_dir = structure["current_directory_structure"]
        if current_dir["subdirectories"]:
            output.append(f"  - Subdirectorios: {', '.join(current_dir['subdirectories'])}")
        if current_dir["files"]:
            output.append(f"  - Archivos ({len(current_dir['files'])}):")
            for file in current_dir["files"]:
                output.append(f"    - {file['name']} ({file['type'] or 'sin tipo'})")
        output.append("")
        
        # Directorio padre (depth 2)
        if structure["parent_directory"]:
            output.append(f"**Directorio padre (depth 2)**: {structure['parent_directory']}")
            parent_dir = structure["parent_directory_structure"]
            if parent_dir["subdirectories"]:
                output.append(f"  - Subdirectorios: {', '.join(parent_dir['subdirectories'])}")
            if parent_dir["files"]:
                output.append(f"  - Archivos ({len(parent_dir['files'])}):")
                for file in parent_dir["files"]:
                    output.append(f"    - {file['name']} ({file['type'] or 'sin tipo'})")
            output.append("")
        
        # Archivos hermanos
        if structure["siblings"]:
            output.append(f"**Archivos hermanos (depth 1-2)**: {len(structure['siblings'])}")
            for sibling in structure["siblings"][:10]:  # Limitar a 10 para no saturar
                if sibling in self.path_to_info:
                    info = self.path_to_info[sibling]
                    output.append(f"  - {sibling} ({info.type or 'sin tipo'})")
            if len(structure["siblings"]) > 10:
                output.append(f"  ... y {len(structure['siblings']) - 10} más")
            output.append("")
        
        # Archivos relacionados
        if structure["related_files"]:
            output.append(f"**Archivos relacionados (campo 'related')**: {len(structure['related_files'])}")
            for related in structure["related_files"]:
                output.append(f"  - {related}")
        
        return "\n".join(output)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Descubrir estructura del proyecto con depth 2'
    )
    parser.add_argument('--file-path', required=True, help='Ruta al archivo markdown de referencia')
    parser.add_argument('--docs-dir', default='docs', help='Directorio base de documentos (default: docs)')
    parser.add_argument('--depth', type=int, default=2, help='Profundidad de análisis (default: 2)')
    
    args = parser.parse_args()
    
    # Determinar docs_dir
    script_dir = Path(__file__).parent.parent.parent.parent.parent
    docs_dir = script_dir / args.docs_dir
    
    if not docs_dir.exists():
        print(f"Error: Directorio docs no encontrado en {docs_dir}")
        return
    
    discoverer = StructureDiscoverer(str(docs_dir), depth=args.depth)
    structure = discoverer.get_structure(args.file_path)
    
    print(discoverer.format_structure(structure))


if __name__ == '__main__':
    main()
