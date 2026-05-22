#!/usr/bin/env python3
"""
Script para descubrir archivos relevantes usando grafo de referencias y grep.
Utilizado por el skill actions-proposal al proponer ediciones a archivos existentes.
"""

import os
import re
import yaml
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass


@dataclass
class RelevantFile:
    """Representa un archivo relevante para un gap."""
    path: str
    source: str  # 'related' o 'grep'
    terms_found: List[str]
    context: Optional[str] = None


class RelevantFileDiscoverer:
    """Descubre archivos relevantes usando grafo de referencias y grep."""
    
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
    
    def discover_from_related(self, file_path: str) -> List[RelevantFile]:
        """
        Descubre archivos relevantes desde el campo 'related' del frontmatter.
        
        Args:
            file_path: Ruta al archivo markdown actual
        
        Returns:
            Lista de archivos relevantes desde el campo 'related'
        """
        path = Path(file_path)
        if not path.is_absolute():
            if file_path.startswith(str(self.docs_dir.name) + '/') or file_path.startswith(str(self.docs_dir.name) + '\\'):
                path = self.docs_dir.parent / file_path
            else:
                path = self.docs_dir / file_path
        
        if not path.exists():
            print(f"Error: File not found: {path}")
            return []
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if not match:
                return []
            
            front_matter = yaml.safe_load(match.group(1)) or {}
            related_raw = front_matter.get('related', [])
            
            relevant_files = []
            for rel in related_raw:
                if isinstance(rel, dict):
                    target = rel.get('target', '')
                    if target in self.id_to_path:
                        relevant_files.append(RelevantFile(
                            path=self.id_to_path[target],
                            source='related',
                            terms_found=[],
                            context=f"Relación declarada: {rel.get('relationship_type', '')}"
                        ))
            
            return relevant_files
        except Exception as e:
            print(f"Error parsing {path}: {e}")
            return []
    
    def discover_from_grep(self, terms: List[str], exclude_file: Optional[str] = None) -> List[RelevantFile]:
        """
        Descubre archivos relevantes usando grep para buscar términos.
        
        Args:
            terms: Lista de términos a buscar
            exclude_file: Ruta del archivo actual a excluir de resultados
        
        Returns:
            Lista de archivos relevantes desde grep
        """
        if not terms:
            return []
        
        relevant_files = []
        exclude_path = str(Path(exclude_file).relative_to(self.docs_dir)) if exclude_file else None
        
        for term in terms:
            try:
                # Ejecutar grep en el directorio docs
                result = subprocess.run(
                    ['grep', '-r', '-i', '-n', term, str(self.docs_dir)],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        # Parsear salida de grep: archivo:linea:contenido
                        parts = line.split(':', 2)
                        if len(parts) >= 3:
                            file_rel = parts[0]
                            line_num = parts[1]
                            content = parts[2]
                            
                            # Excluir el archivo actual
                            if exclude_path and file_rel == exclude_path:
                                continue
                            
                            # Verificar si ya existe en resultados
                            existing = next((f for f in relevant_files if f.path == file_rel), None)
                            if existing:
                                if term not in existing.terms_found:
                                    existing.terms_found.append(term)
                            else:
                                relevant_files.append(RelevantFile(
                                    path=file_rel,
                                    source='grep',
                                    terms_found=[term],
                                    context=f"Línea {line_num}: {content[:100]}..."
                                ))
            except subprocess.TimeoutExpired:
                print(f"Timeout searching for term: {term}")
            except Exception as e:
                print(f"Error searching for term '{term}': {e}")
        
        return relevant_files
    
    def discover(self, file_path: str, gap_terms: List[str]) -> List[RelevantFile]:
        """
        Descubre archivos relevantes combinando related y grep.
        
        Args:
            file_path: Ruta al archivo markdown actual
            gap_terms: Lista de términos clave del gap
        
        Returns:
            Lista combinada de archivos relevantes
        """
        # Obtener archivos desde related
        related_files = self.discover_from_related(file_path)
        
        # Obtener archivos desde grep
        grep_files = self.discover_from_grep(gap_terms, exclude_file=file_path)
        
        # Combinar resultados, priorizando related
        all_files: List[RelevantFile] = []
        seen_paths: Set[str] = set()
        
        # Agregar archivos de related primero
        for file in related_files:
            if file.path not in seen_paths:
                all_files.append(file)
                seen_paths.add(file.path)
        
        # Agregar archivos de grep que no estén duplicados
        for file in grep_files:
            if file.path not in seen_paths:
                all_files.append(file)
                seen_paths.add(file.path)
        
        return all_files
    
    def format_results(self, files: List[RelevantFile]) -> str:
        """Formatea los resultados para uso en el skill."""
        if not files:
            return "No se encontraron archivos relevantes."
        
        output = ["Archivos relevantes para el gap:\n"]
        
        # Separar por fuente
        related_files = [f for f in files if f.source == 'related']
        grep_files = [f for f in files if f.source == 'grep']
        
        if related_files:
            output.append("Desde campo 'related':")
            for i, file in enumerate(related_files, 1):
                output.append(f"{i}. {file.path}")
                output.append(f"   - Fuente: related (relación declarada)")
                if file.context:
                    output.append(f"   - {file.context}")
            output.append("")
        
        if grep_files:
            output.append("Desde búsqueda grep:")
            for i, file in enumerate(grep_files, 1):
                output.append(f"{i}. {file.path}")
                output.append(f"   - Fuente: grep")
                output.append(f"   - Términos encontrados: {', '.join(file.terms_found)}")
                if file.context:
                    output.append(f"   - Contexto: {file.context}")
        
        return "\n".join(output)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Descubrir archivos relevantes usando grafo de referencias y grep'
    )
    parser.add_argument('--file-path', required=True, help='Ruta al archivo markdown actual')
    parser.add_argument('--gap-terminos', required=True, help='Términos clave del gap (separados por coma)')
    parser.add_argument('--docs-dir', default='docs', help='Directorio base de documentos (default: docs)')
    
    args = parser.parse_args()
    
    # Determinar docs_dir
    script_dir = Path(__file__).parent.parent.parent.parent.parent
    docs_dir = script_dir / args.docs_dir
    
    if not docs_dir.exists():
        print(f"Error: Directorio docs no encontrado en {docs_dir}")
        return
    
    # Parsear términos
    terms = [t.strip() for t in args.gap_terminos.split(',')]
    
    discoverer = RelevantFileDiscoverer(str(docs_dir))
    files = discoverer.discover(args.file_path, terms)
    
    print(discoverer.format_results(files))


if __name__ == '__main__':
    main()
