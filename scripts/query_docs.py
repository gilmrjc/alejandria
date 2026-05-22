#!/usr/bin/env python3
"""
Script para consultar y analizar documentos en docs/ basado en front matters.

Funcionalidades:
- Filtrar documentos por calificación (rating)
- Obtener dependencias de un documento con profundidad configurable
- Encontrar archivos huérfanos (sin dependencias)
- Validar front matters de documentos
- Exportar grafo de dependencias a JSON
"""

import logging
import re
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional, Set, Any, TypedDict
from dataclasses import dataclass, field
from collections import defaultdict
from functools import lru_cache


# ==================== CONFIGURACIÓN ====================

@dataclass(frozen=True)
class Config:
    """Constantes de configuración centralizadas e inmutables."""
    
    # Tipos de relaciones válidos
    valid_relationship_types: frozenset[str] = frozenset({
        'depends_on', 'implements', 'references', 
        'explains', 'extends', 'supersedes', 
        'reinforces', 'contradicts'
    })
    
    # Fases de rating válidas
    valid_rating_phases: frozenset[str] = frozenset({
        'document-critique', 'document-editing', 
        'actions-proposal', 'gap-resolution'
    })
    
    # Rango de rating válido
    min_rating: float = 0
    max_rating: float = 10
    
    # Umbrales de estado
    status_completed_threshold: float = 9
    status_in_progress_threshold: float = 7
    
    # Grupos de documentos
    groups: dict[str, list[str]] = field(default_factory=dict)
    
    # Milestones
    milestones: dict[str, list[str]] = field(default_factory=dict)
    
    def __post_init__(self):
        """Inicializa valores por defecto para dicts mutables."""
        if not self.groups:
            object.__setattr__(self, 'groups', {
                'ESTRATEGIA': ['estrategia/'],
                'ARQUITECTURA': ['arquitectura/'],
                'PRODUCTO': ['producto/'],
                'IMPLEMENTACIÓN': ['tareas/', 'propuestas/']
            })
        if not self.milestones:
            object.__setattr__(self, 'milestones', {
                'Hito 1': ['hito-01', 'milestone-1'],
                'Hito 2': ['hito-02', 'milestone-2'],
                'Hito 3': ['hito-03', 'milestone-3'],
                'Hito 4': ['hito-04', 'milestone-4'],
                'Hito 5': ['hito-05', 'milestone-5'],
                'Hito 6': ['hito-06', 'milestone-6'],
                'Hito 7': ['hito-07', 'milestone-7']
            })


# ==================== EXCEPCIONES ====================

class DocumentError(Exception):
    """Excepción base para errores de documentos."""
    pass


class ParseError(DocumentError):
    """Error al parsear un documento."""
    pass


class ValidationError(DocumentError):
    """Error de validación de front matter."""
    pass


class DocumentNotFoundError(DocumentError):
    """Documento no encontrado."""
    pass


# ==================== LOGGING ====================

def _get_logger(name: str) -> logging.Logger:
    """Helper para crear loggers con nombre consistente."""
    return logging.getLogger(f'query_docs.{name}')


def setup_logging(verbose: bool = False) -> logging.Logger:
    """Configura el sistema de logging."""
    logger = _get_logger('root')
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG if verbose else logging.INFO)
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


# ==================== MODELOS DE DATOS ====================

@dataclass
class Relationship:
    """Representa una relación entre documentos."""
    target: str
    relationship_type: str
    reason: str


@dataclass
class TraversalResult:
    """Resultado de traversar el grafo de relaciones."""
    target_id: str
    depth: int
    relationship_type: str
    reason: str
    via: Optional[str] = None


@dataclass
class ValidationErrorItem:
    """Representa un ítem de validación."""
    path: str
    issue: str
    severity: str = 'error'  # 'error' o 'warning'
    related: Optional[str] = None


class LintResults(TypedDict):
    """Resultados de lint de documentos."""
    errors: List[ValidationErrorItem]
    warnings: List[ValidationErrorItem]


@dataclass
class Document:
    """Representa un documento con su front matter."""
    path: str
    id: str
    type: str
    rating: Optional[float] = None
    rating_phase: Optional[str] = None
    related: List[Relationship] = field(default_factory=list)
    raw_front_matter: Dict[str, Any] = field(default_factory=dict)


# ==================== VALIDADOR ====================

class DocumentValidator:
    """Validador centralizado de documentos."""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
    
    def validate_relationship_type(self, rel_type: str) -> bool:
        """Valida que el tipo de relación sea válido."""
        return rel_type in self.config.valid_relationship_types
    
    def validate_rating_phase(self, phase: str) -> bool:
        """Valida que la fase de rating sea válida."""
        return phase in self.config.valid_rating_phases
    
    def validate_rating_range(self, rating: float) -> bool:
        """Valida que el rating esté en el rango permitido."""
        return self.config.min_rating <= rating <= self.config.max_rating
    
    def _add_error(self, issues: List[ValidationErrorItem], path: str, issue: str, 
                   severity: str = 'error', related: Optional[str] = None) -> None:
        """Helper para agregar errores de validación."""
        issues.append(ValidationErrorItem(path=path, issue=issue, severity=severity, related=related))
    
    def _validate_required_fields(self, doc: Document) -> List[ValidationErrorItem]:
        """Valida campos obligatorios del documento."""
        issues: List[ValidationErrorItem] = []
        
        if not doc.id:
            self._add_error(issues, doc.path, 'Campo obligatorio "id" faltante')
        if not doc.type:
            self._add_error(issues, doc.path, 'Campo obligatorio "type" faltante')
        
        return issues
    
    def _validate_id_format(self, doc: Document) -> List[ValidationErrorItem]:
        """Valida que el ID tenga el formato XXX-### (letras-guion-números)."""
        issues: List[ValidationErrorItem] = []
        
        if doc.id:
            # Patrón: letras, guion, números (ej: T-001, ABC-123)
            if not re.match(r'^[A-Za-z]+-\d+$', doc.id):
                self._add_error(issues, doc.path, 
                    f'ID "{doc.id}" no cumple el formato XXX-### (letras-guion-números)', 'warning')
        
        return issues
    
    def _validate_rating(self, doc: Document) -> List[ValidationErrorItem]:
        """Valida el campo rating y rating_phase."""
        issues: List[ValidationErrorItem] = []
        
        if doc.rating is not None:
            if not isinstance(doc.rating, (int, float)):
                self._add_error(issues, doc.path, 
                    f'Campo "rating" debe ser numérico, encontrado: {type(doc.rating).__name__}')
            elif not self.validate_rating_range(doc.rating):
                self._add_error(issues, doc.path, 
                    f'Campo "rating" debe estar entre {self.config.min_rating} y {self.config.max_rating}, encontrado: {doc.rating}', 'warning')
            
            if not doc.rating_phase:
                self._add_error(issues, doc.path, 'Campo "rating" presente pero "rating-phase" faltante', 'warning')
            elif not self.validate_rating_phase(doc.rating_phase):
                self._add_error(issues, doc.path, 
                    f'Campo "rating-phase" inválido "{doc.rating_phase}". Debe ser uno de: {self.config.valid_rating_phases}', 'warning')
        
        if doc.rating_phase and doc.rating is None:
            self._add_error(issues, doc.path, 'Campo "rating-phase" presente pero "rating" faltante', 'warning')
        
        return issues
    
    def _validate_relationship(self, rel: Relationship, doc: Document, repository: 'DocumentRepository') -> List[ValidationErrorItem]:
        """Valida una relación individual."""
        issues: List[ValidationErrorItem] = []
        
        if not rel.target:
            self._add_error(issues, doc.path, 'Relación sin campo "target"', 'warning')
            return issues
        
        if not rel.relationship_type:
            self._add_error(issues, doc.path, 'Relación sin campo "relationship_type"', 'warning', rel.target)
        elif not self.validate_relationship_type(rel.relationship_type):
            self._add_error(issues, doc.path, 
                f'Tipo de relación inválido "{rel.relationship_type}". Debe ser uno de: {self.config.valid_relationship_types}', 'warning', rel.target)
        
        if not rel.reason:
            self._add_error(issues, doc.path, f'Relación "{rel.target}" sin campo "reason"', 'warning', rel.target)
        
        if rel.target not in repository.id_to_path:
            self._add_error(issues, doc.path, f'Relación "{rel.target}" (tipo: {rel.relationship_type}) no existe', 'warning', rel.target)
        
        return issues
    
    def validate_document(self, doc: Document, repository: 'DocumentRepository') -> List[ValidationErrorItem]:
        """Valida un documento completo y retorna lista de errores."""
        issues: List[ValidationErrorItem] = []
        
        issues.extend(self._validate_required_fields(doc))
        issues.extend(self._validate_id_format(doc))
        issues.extend(self._validate_rating(doc))
        
        for rel in doc.related:
            issues.extend(self._validate_relationship(rel, doc, repository))
        
        return issues


# ==================== PARSER ====================

class DocumentParser:
    """Responsable de parsear archivos markdown y extraer front matter."""
    
    def __init__(self):
        self.logger = _get_logger('parser')
    
    @staticmethod
    def parse_front_matter(front_matter_str: str) -> Dict[str, Any]:
        """Parsea front matter YAML usando pyyaml."""
        try:
            return yaml.safe_load(front_matter_str) or {}
        except yaml.YAMLError as e:
            raise ParseError(f"Error al parsear YAML: {e}")
    
    @staticmethod
    def _calculate_relative_path(file_path: Path) -> str:
        """Calcula el path relativo al directorio docs de forma robusta."""
        try:
            # Buscar el directorio docs hacia arriba
            current = file_path
            while current != current.parent:
                if current.name == 'docs':
                    docs_dir = current.parent
                    return str(file_path.relative_to(docs_dir))
                current = current.parent
            
            # Si no encontramos docs, usar el path absoluto
            return str(file_path)
        except ValueError:
            raise ParseError(f"No se puede calcular path relativo para {file_path}")
    
    def _parse_relationships(self, related_raw: Any, file_path: str) -> List[Relationship]:
        """Parsea el campo related del front matter."""
        if not related_raw:
            return []
        
        if not isinstance(related_raw, list):
            self.logger.error(f"Error parsing {file_path}: 'related' must be an array")
            raise ValidationError("'related' must be an array")
        
        related = []
        for rel in related_raw:
            if not isinstance(rel, dict):
                self.logger.error(f"Error parsing {file_path}: each item in 'related' must be an object")
                raise ValidationError("each item in 'related' must be an object")
            
            related.append(Relationship(
                target=rel.get('target', ''),
                relationship_type=rel.get('relationship_type', ''),
                reason=rel.get('reason', '')
            ))
        
        return related
    
    @lru_cache(maxsize=128)
    def _read_file_cached(self, file_path: str) -> str:
        """Lee un archivo con caché para evitar re-lecturas."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def from_file(self, file_path: str, use_cache: bool = True) -> Optional[Document]:
        """Parsea un archivo markdown y extrae el front matter.
        
        Args:
            file_path: Path del archivo a parsear
            use_cache: Si True, usa caché para la lectura del archivo
        
        Returns:
            Documento parseado o None si no tiene front matter válido
        """
        try:
            if use_cache:
                content = self._read_file_cached(file_path)
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if not match:
                self.logger.debug(f"No front matter found in {file_path}")
                return None
            
            front_matter_str = match.group(1)
            front_matter = self.parse_front_matter(front_matter_str)
            
            if not front_matter or 'id' not in front_matter:
                self.logger.debug(f"No valid front matter in {file_path}")
                return None
            
            file_path_obj = Path(file_path)
            rel_path = self._calculate_relative_path(file_path_obj)
            
            related = self._parse_relationships(
                front_matter.get('related', []), 
                file_path
            )
            
            return Document(
                path=rel_path,
                id=front_matter.get('id', ''),
                type=front_matter.get('type', ''),
                rating=front_matter.get('rating'),
                rating_phase=front_matter.get('rating-phase'),
                related=related,
                raw_front_matter=front_matter
            )
        except ParseError:
            raise
        except ValidationError:
            raise
        except Exception as e:
            self.logger.error(f"Error parsing {file_path}: {e}")
            raise ParseError(f"Error parsing {file_path}: {e}")


# ==================== REPOSITORIO ====================

class DocumentRepository:
    """Responsable de cargar y almacenar documentos."""
    
    def __init__(self, docs_dir: str, parser: Optional[DocumentParser] = None, 
                 verbose: bool = False):
        self.docs_dir = Path(docs_dir)
        self.parser = parser or DocumentParser()
        self.documents: Dict[str, Document] = {}
        self.id_to_path: Dict[str, str] = {}
        self.logger = _get_logger('repository')
        self._load_documents(verbose)
    
    def _load_documents(self, verbose: bool = False) -> None:
        """Carga todos los documentos markdown del directorio."""
        for md_file in self.docs_dir.rglob('*.md'):
            try:
                doc = self.parser.from_file(str(md_file))
                if doc:
                    self.documents[doc.path] = doc
                    if doc.id in self.id_to_path and self.id_to_path[doc.id] != doc.path:
                        if verbose:
                            self.logger.warning(
                                f"Duplicate ID '{doc.id}' found in: "
                                f"{self.id_to_path[doc.id]} and {doc.path}. Using: {doc.path}"
                            )
                    self.id_to_path[doc.id] = doc.path
            except (ParseError, ValidationError) as e:
                self.logger.warning(f"Skipping {md_file}: {e}")
            except Exception as e:
                self.logger.error(f"Unexpected error loading {md_file}: {e}")
    
    def get_by_id(self, doc_id: str) -> Optional[Document]:
        """Obtiene un documento por su ID."""
        doc_path = self.id_to_path.get(doc_id)
        return self.documents.get(doc_path) if doc_path else None
    
    def get_by_path(self, path: str) -> Optional[Document]:
        """Obtiene un documento por su path."""
        return self.documents.get(path)
    
    def get_all(self) -> List[Document]:
        """Retorna todos los documentos."""
        return list(self.documents.values())


# ==================== TRAVERSAL DEL GRAFO ====================

class GraphTraverser:
    """Responsable de traversar el grafo de relaciones (dependencies/related)."""
    
    def __init__(self, repository: DocumentRepository):
        self.repository = repository
        self.logger = _get_logger('traverser')
    
    def traverse(self, doc: Document, depth: int = 1, visited: Optional[Set[str]] = None, 
                 parent_id: Optional[str] = None) -> List[TraversalResult]:
        """
        Traversa relaciones de un documento con profundidad.
        
        Args:
            doc: Documento a traversar
            depth: Profundidad del grafo (1 = solo relaciones directas)
            visited: Set de IDs visitados (para evitar ciclos)
            parent_id: ID del documento padre (para mostrar campo 'via')
        
        Returns:
            Lista de TraversalResult
        """
        if visited is None:
            visited = set()
        
        if doc.id in visited or depth < 1:
            return []
        
        visited.add(doc.id)
        results: List[TraversalResult] = []
        
        for rel in doc.related:
            results.append(TraversalResult(
                target_id=rel.target,
                depth=1,
                relationship_type=rel.relationship_type,
                reason=rel.reason,
                via=parent_id
            ))
            
            if depth > 1:
                rel_doc = self.repository.get_by_id(rel.target)
                if rel_doc:
                    sub_rels = self.traverse(rel_doc, depth - 1, visited.copy(), rel.target)
                    results.extend(TraversalResult(
                        target_id=r.target_id,
                        depth=r.depth + 1,
                        relationship_type=r.relationship_type,
                        reason=r.reason,
                        via=r.via
                    ) for r in sub_rels)
                else:
                    self.logger.warning(f"Referencia no encontrada: {rel.target}")
        
        return results


# ==================== ANALIZADOR ====================

class DocumentAnalyzer:
    """Responsable de analizar documentos (filtros, validaciones, etc.)."""
    
    def __init__(self, repository: DocumentRepository, validator: Optional[DocumentValidator] = None):
        self.repository = repository
        self.validator = validator or DocumentValidator()
    
    def filter_by_rating(self, min_rating: Optional[float] = None, 
                        max_rating: Optional[float] = None,
                        has_rating: Optional[bool] = None) -> List[Document]:
        """Filtra documentos por rating."""
        results: List[Document] = []
        for doc in self.repository.documents.values():
            if has_rating is not None and (doc.rating is None) != has_rating:
                continue
            if (min_rating is not None or max_rating is not None) and doc.rating is None:
                continue
            if doc.rating is not None:
                if min_rating is not None and doc.rating < min_rating:
                    continue
                if max_rating is not None and doc.rating > max_rating:
                    continue
            results.append(doc)
        return sorted(results, key=lambda d: d.rating or 0, reverse=True)
    
    def find_orphaned(self) -> List[Document]:
        """Encuentra archivos huérfanos (sin relaciones depends_on)."""
        orphaned = [
            doc for doc in self.repository.documents.values() 
            if not any(rel.relationship_type == 'depends_on' for rel in doc.related)
        ]
        return sorted(orphaned, key=lambda d: d.path)
    
    def lint_documents(self) -> LintResults:
        """Valida los front matters de todos los documentos."""
        issues: LintResults = {'errors': [], 'warnings': []}
        
        # Validar documentos individuales
        for doc in self.repository.documents.values():
            try:
                doc_issues = self.validator.validate_document(doc, self.repository)
                for issue in doc_issues:
                    if issue.severity == 'error':
                        issues['errors'].append(issue)
                    else:
                        issues['warnings'].append(issue)
            except Exception as e:
                issues['errors'].append(ValidationErrorItem(
                    path=doc.path,
                    issue=f'Error inesperado durante validación: {e}',
                    severity='error'
                ))
        
        # Detectar IDs duplicados
        id_to_docs = defaultdict(list)
        for doc in self.repository.documents.values():
            id_to_docs[doc.id].append(doc)
        
        for dup_id, docs in id_to_docs.items():
            if len(docs) > 1:
                for doc in docs:
                    issues['warnings'].append(ValidationErrorItem(
                        path=doc.path,
                        issue=f'ID duplicado "{dup_id}" encontrado en {len(docs)} documentos',
                        severity='warning'
                    ))
        
        return issues


# ==================== FORMATEADOR ====================

class OutputFormatter:
    """Responsable de formatear la salida de los comandos."""
    
    def __init__(self):
        pass
    
    def format_document(self, doc: Document, repository: DocumentRepository) -> str:
        """Formatea información de un documento."""
        lines = [
            f"\n{'='*60}",
            f"ID: {doc.id}",
            f"Tipo: {doc.type}",
            f"Path: {doc.path}",
            f"Rating: {doc.rating if doc.rating else 'Sin rating'}"
        ]
        if doc.rating_phase:
            lines.append(f"Rating Phase: {doc.rating_phase}")
        if doc.related:
            lines.append(f"Relaciones ({len(doc.related)}):")
            for rel in doc.related:
                rel_doc = repository.get_by_id(rel.target)
                rel_info = f" -> {rel_doc.path if rel_doc else 'NO ENCONTRADO'}"
                lines.append(f"  - {rel.target} [{rel.relationship_type}]{rel_info}")
                lines.append(f"    Razón: {rel.reason}")
        else:
            lines.append("Relaciones: Ninguna (aislado)")
        lines.append(f"{'='*60}")
        return "\n".join(lines)
    
    def format_relationships(self, doc_id: str, rels: List[TraversalResult], depth: int, 
                              repository: DocumentRepository) -> str:
        """Formatea las relaciones de un documento."""
        lines = [
            f"\n{'='*60}",
            f"Relaciones de {doc_id} (profundidad {depth})",
            f"{'='*60}"
        ]
        
        if rels:
            lines.append(f"\n📥 RELACIONES - {len(rels)} total:")
            by_depth = defaultdict(list)
            for rel in rels:
                by_depth[rel.depth].append(rel)
            
            for d in sorted(by_depth.keys()):
                lines.append(f"\n  Profundidad {d}:")
                for rel in by_depth[d]:
                    rel_doc = repository.get_by_id(rel.target_id)
                    if rel_doc:
                        rating_str = f" (rating: {rel_doc.rating})" if rel_doc.rating else ""
                        via_str = f" via {rel.via}" if rel.via else ""
                        lines.append(f"    - {rel.target_id}{via_str} -> {rel_doc.path}{rating_str}")
                        lines.append(f"      Tipo: {rel.relationship_type}")
                        if rel.reason:
                            lines.append(f"      Razón: {rel.reason}")
                    else:
                        via_str = f" via {rel.via}" if rel.via else ""
                        lines.append(f"    - {rel.target_id}{via_str} -> NO ENCONTRADO")
        else:
            lines.append(f"\n📥 RELACIONES: Ninguna (aislado)")
        
        lines.append(f"\n{'='*60}")
        return "\n".join(lines)
    
    def _format_doc_list(self, docs: List[Document], label: str, show_rating: bool = False) -> str:
        """Formatea lista de documentos con opción de mostrar rating."""
        lines = [f"\nEncontrados {len(docs)} {label}:"]
        for doc in docs:
            if show_rating:
                rating_str = f"{doc.rating}" if doc.rating else "sin rating"
                lines.append(f"  [{doc.id}] {doc.path} - Rating: {rating_str}")
            else:
                rating_str = f" (rating: {doc.rating})" if doc.rating else ""
                lines.append(f"  [{doc.id}] {doc.path}{rating_str}")
        return "\n".join(lines)
    
    def format_rating_list(self, docs: List[Document]) -> str:
        """Formatea lista de documentos filtrados por rating."""
        return self._format_doc_list(docs, "documentos", show_rating=True)
    
    def format_simple_list(self, docs: List[Document], label: str) -> str:
        """Formatea lista simple de documentos."""
        return self._format_doc_list(docs, label, show_rating=False)
    
    def format_lint_results(self, issues: LintResults) -> str:
        """Formatea resultados de lint."""
        if not issues['errors'] and not issues['warnings']:
            return "\n✓ Todos los front matters son válidos"
        
        lines = []
        if issues['errors']:
            lines.append(f"\n❌ {len(issues['errors'])} errores:")
            for item in issues['errors']:
                related_str = f" (rel: {item.related})" if item.related else ""
                lines.append(f"  - {item.path}{related_str}: {item.issue}")
        if issues['warnings']:
            lines.append(f"\n⚠️  {len(issues['warnings'])} advertencias:")
            for item in issues['warnings']:
                related_str = f" (rel: {item.related})" if item.related else ""
                lines.append(f"  - {item.path}{related_str}: {item.issue}")
        return "\n".join(lines)


# ==================== UTILIDADES DE EXPORTACIÓN ====================

class GraphExporter:
    """Responsable de exportar el grafo de dependencias."""
    
    def __init__(self, repository: DocumentRepository, config: Optional[Config] = None):
        self.repository = repository
        self.config = config or Config()
    
    def get_group_from_path(self, path: str) -> str:
        """Determina el grupo basado en la estructura de carpetas."""
        path_lower = path.lower()
        for group, patterns in self.config.groups.items():
            if any(pattern in path_lower for pattern in patterns):
                return group
        return 'IMPLEMENTACIÓN'
    
    def get_milestone(self, path: str) -> str:
        """Determina el milestone basado en path."""
        path_lower = path.lower()
        for milestone, patterns in self.config.milestones.items():
            if any(pattern in path_lower for pattern in patterns):
                return milestone
        return ''
    
    def get_status(self, doc: Document) -> str:
        """Determina el estado basado en rating."""
        if doc.rating is None:
            return 'pending'
        elif doc.rating >= self.config.status_completed_threshold:
            return 'completed'
        elif doc.rating >= self.config.status_in_progress_threshold:
            return 'in-progress'
        else:
            return 'pending'
    
    def export(self, output_path: str) -> None:
        """Exporta el grafo de dependencias a formato JSON."""
        nodes = []
        edges = []
        
        for doc in self.repository.documents.values():
            nodes.append({
                'id': doc.id,
                'label': Path(doc.path).name,
                'status': self.get_status(doc),
                'rating': doc.rating,
                'group': self.get_group_from_path(doc.path),
                'milestone': self.get_milestone(doc.path)
            })
        
        for doc in self.repository.documents.values():
            for rel in doc.related:
                if rel.target in self.repository.id_to_path:
                    edges.append({
                        'source': doc.id,
                        'target': rel.target,
                        'relationship_type': rel.relationship_type,
                        'reason': rel.reason
                    })
        
        graph_data = {'nodes': nodes, 'edges': edges}
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Grafo exportado a {output_path}")
        self.logger.info(f"  - Nodos: {len(nodes)}")
        self.logger.info(f"  - Edges: {len(edges)}")
        print(f"✓ Grafo exportado a {output_path}")
        print(f"  - Nodos: {len(nodes)}")
        print(f"  - Edges: {len(edges)}")


# ==================== CLI ====================

class CLI:
    """Interface de línea de comandos - orquesta los componentes."""
    
    def __init__(self, docs_dir: str, verbose: bool = False):
        self.logger = setup_logging(verbose)
        self.config = Config()
        self.validator = DocumentValidator(self.config)
        self.parser = DocumentParser()
        self.repository = DocumentRepository(docs_dir, self.parser, verbose)
        self.traverser = GraphTraverser(self.repository)
        self.analyzer = DocumentAnalyzer(self.repository, self.validator)
        self.formatter = OutputFormatter()
        self.exporter = GraphExporter(self.repository, self.config)
    
    def _get_document(self, doc_id: Optional[str] = None, path: Optional[str] = None) -> Optional[Document]:
        """Obtiene un documento por ID o path."""
        if path:
            return self.repository.get_by_path(path)
        elif doc_id:
            return self.repository.get_by_id(doc_id)
        return None
    
    
    def run(self, args):
        """Ejecuta el comando especificado."""
        if args.command == 'filter-rating':
            has_rating = None
            if args.has_rating == 'yes':
                has_rating = True
            elif args.has_rating == 'no':
                has_rating = False
            
            docs = self.analyzer.filter_by_rating(
                min_rating=args.min,
                max_rating=args.max,
                has_rating=has_rating
            )
            print(self.formatter.format_rating_list(docs))
        
        elif args.command == 'relationships':
            if not args.id and not args.path:
                print("Error: Debes especificar --id o --path")
                return
            
            doc = self._get_document(args.id, args.path)
            if not doc:
                identifier = args.path if args.path else args.id
                print(f"Documento con '{identifier}' no encontrado")
                return
            
            rels = self.traverser.traverse(doc, args.depth)
            
            print(self.formatter.format_relationships(doc.id, rels, args.depth, self.repository))
        
        elif args.command == 'orphans':
            orphans = self.analyzer.find_orphaned()
            print(self.formatter.format_simple_list(orphans, "archivos huérfanos (sin relaciones depends_on)"))
        
        elif args.command == 'show':
            if not args.id and not args.path:
                print("Error: Debes especificar --id o --path")
                return
            
            doc = self._get_document(args.id, args.path)
            if doc:
                print(self.formatter.format_document(doc, self.repository))
            else:
                identifier = args.path if args.path else args.id
                print(f"Documento con '{identifier}' no encontrado")
        
        elif args.command == 'lint':
            issues = self.analyzer.lint_documents()
            print(self.formatter.format_lint_results(issues))
        
        elif args.command == 'export-graph':
            self.exporter.export(args.output)
        
        else:
            from argparse import ArgumentParser
            parser = ArgumentParser()
            parser.print_help()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Consultar y analizar documentos en docs/ basado en front matters'
    )
    parser.add_argument('-v', '--verbose', action='store_true', help='Modo verbose')
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    filter_parser = subparsers.add_parser('filter-rating', help='Filtrar documentos por rating')
    filter_parser.add_argument('--min', type=float, help='Rating mínimo')
    filter_parser.add_argument('--max', type=float, help='Rating máximo')
    filter_parser.add_argument('--has-rating', type=str, choices=['yes', 'no'], help='Filtrar por presencia de rating')
    
    rels_parser = subparsers.add_parser('relationships', help='Obtener relaciones de un documento (dependencies y related)')
    rels_parser.add_argument('--id', help='ID del documento')
    rels_parser.add_argument('--path', help='Path del documento')
    rels_parser.add_argument('--depth', type=int, default=1, help='Profundidad del grafo')
    
    subparsers.add_parser('orphans', help='Encontrar archivos huérfanos (sin relaciones depends_on)')
    
    show_parser = subparsers.add_parser('show', help='Mostrar información de un documento')
    show_parser.add_argument('--id', help='ID del documento')
    show_parser.add_argument('--path', help='Path del documento')
    
    subparsers.add_parser('lint', help='Validar front matters')
    
    export_parser = subparsers.add_parser('export-graph', help='Exportar grafo de dependencias a JSON')
    export_parser.add_argument('--output', type=str, default='docs/dependency-graph.json', 
                                help='Path de salida para el JSON')
    
    args = parser.parse_args()
    
    script_dir = Path(__file__).parent
    docs_dir = script_dir.parent / 'docs'
    
    if not docs_dir.exists():
        print(f"Error: Directorio docs no encontrado en {docs_dir}")
        return
    
    try:
        cli = CLI(str(docs_dir), verbose=args.verbose)
        cli.run(args)
    except Exception as e:
        logging.error(f"Error fatal: {e}")
        raise


if __name__ == '__main__':
    main()
