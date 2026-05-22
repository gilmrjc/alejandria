#!/usr/bin/env python3
"""Script para actualizar IDs de documentos al formato correcto XXX-###"""

import re
from pathlib import Path
from typing import Dict, Tuple

# Mapeo de prefijos antiguos a nuevos
PREFIX_MAPPINGS = {
    'PROD-REQ-': 'REQ-',
    'PROD-PRD-': 'PRD-',
    'PROD-FUN-': 'FEA-',
    'ENG-ARC-': 'ARC-',
    'ENG-EPC-': 'EPC-',
    'ENG-TRD-': 'TRD-',
    'ENG-TS-': 'TS-',
    'ESTR-CUL-': 'CUL-',
    'ESTR-POL-': 'POL-',
    'ESTR-STR-': 'STR-',
    'FEAT-ONB-': 'FEA-',
    'FEAT-UI-': 'FEA-',
}

def fix_id_in_file(file_path: Path) -> Tuple[bool, str]:
    """Actualiza el ID y referencias en un archivo si es necesario."""
    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        modified = False
        old_id = None
        new_id = None
        
        # Primero actualizar el ID principal
        for i, line in enumerate(lines):
            if line.startswith('id:'):
                old_id = line.split(':', 1)[1].strip()
                
                # Buscar prefijo que necesita ser cambiado
                new_id = old_id
                for old_prefix, new_prefix in PREFIX_MAPPINGS.items():
                    if old_id.startswith(old_prefix):
                        new_id = new_prefix + old_id[len(old_prefix):]
                        break
                
                if new_id != old_id:
                    lines[i] = f"id: {new_id}"
                    modified = True
                    print(f"✓ {file_path.relative_to(Path.cwd())}: {old_id} → {new_id}")
                break
        
        # Luego actualizar todas las referencias (target:)
        for i, line in enumerate(lines):
            if 'target:' in line:
                for old_prefix, new_prefix in PREFIX_MAPPINGS.items():
                    if old_prefix in line:
                        lines[i] = line.replace(old_prefix, new_prefix)
                        modified = True
                        break
        
        # También actualizar referencias en el cuerpo del documento (formato [ID](path))
        for i, line in enumerate(lines):
            for old_prefix, new_prefix in PREFIX_MAPPINGS.items():
                if old_prefix in line:
                    lines[i] = line.replace(old_prefix, new_prefix)
                    modified = True
                    break
        
        if modified:
            file_path.write_text('\n'.join(lines), encoding='utf-8')
            return True, new_id or old_id
        
        return False, old_id
    except Exception as e:
        print(f"✗ Error procesando {file_path}: {e}")
        return False, str(e)

def main():
    """Procesa todos los archivos markdown en docs/"""
    docs_dir = Path(__file__).parent.parent / 'docs'
    
    if not docs_dir.exists():
        print(f"Directorio docs no encontrado: {docs_dir}")
        return
    
    md_files = list(docs_dir.rglob('*.md'))
    print(f"Procesando {len(md_files)} archivos markdown...\n")
    
    modified_count = 0
    for file_path in md_files:
        modified, _ = fix_id_in_file(file_path)
        if modified:
            modified_count += 1
    
    print(f"\n✓ Total de archivos modificados: {modified_count}")

if __name__ == '__main__':
    main()
