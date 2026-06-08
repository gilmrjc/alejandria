"""Service layer for gap detection using LLM analysis."""

import json
import logging
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from shared.llm.ollama_client import OllamaClient
from shared.config.settings import settings

logger = logging.getLogger(__name__)


def save_prompt_to_file(prompt_type: str, content: str, document_id: str = None):
    """
    Save complete prompt to file for debugging purposes.

    Args:
        prompt_type: Type of prompt (system, user, response)
        content: Content to save
        document_id: Optional document ID for naming
    """
    from datetime import datetime

    # Create debug directory if it doesn't exist
    debug_dir = Path("/tmp/alejandria_debug")
    debug_dir.mkdir(exist_ok=True)

    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    doc_suffix = f"_{document_id[:8]}" if document_id else ""
    filename = f"{timestamp}{doc_suffix}_{prompt_type}.txt"
    filepath = debug_dir / filename

    # Save content
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    logger.info(f"Saved {prompt_type} prompt to: {filepath}")
    return filepath


class GapDetectionService:
    """Service for gap detection using LLM analysis."""

    def __init__(self, session: Session = None, ollama_client: OllamaClient = None):
        """
        Initialize GapDetectionService.

        Args:
            session: Optional database session
            ollama_client: Optional OllamaClient instance (creates default if not provided)
        """
        self.session = session
        self.ollama_client = ollama_client or OllamaClient()

    async def detect_gaps(
        self,
        document_title: str,
        document_content: str,
        document_type: str = "technical",
        existing_gaps: list[dict[str, Any]] = None,
        role_affected: str = "developer",
        project_id: str = None,
        use_tools: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Detect gaps in a document using LLM analysis with optional tool support.

        Args:
            document_title: Title of the document
            document_content: Content of the document
            document_type: Type of document (technical, architecture, requirements, etc.)
            existing_gaps: List of existing gaps to avoid duplicates
            role_affected: Role affected by gaps (developer, architect, product, etc.)
            project_id: Project ID for tool context (required if use_tools=True)
            use_tools: Whether to enable MCP tools for enhanced analysis

        Returns:
            List of detected gaps with metadata
        """
        if existing_gaps is None:
            existing_gaps = []

        logger.info(f"Starting gap detection for document: {document_title}")
        logger.info(f"Document content length: {len(document_content)} characters")
        logger.info(f"Existing gaps: {len(existing_gaps)}")
        logger.info(f"Use tools: {use_tools}, Project ID: {project_id}")

        # Build existing gaps summary
        existing_gaps_summary = "\n".join(
            [f"- {gap.get('question', '')}" for gap in existing_gaps]
        )
        if not existing_gaps_summary:
            existing_gaps_summary = "No existing gaps"

        # Build system prompt
        system_prompt = """Eres un experto analista de documentación técnica especializado en identificar brechas, inconsistencias e información faltante en documentos técnicos. Tu rol es analizar documentos e identificar áreas donde la información está incompleta, poco clara o contradictoria.

Tu análisis debe enfocarse en:
1. Información crítica faltante (cómo, por qué, detalles de implementación)
2. Inconsistencias entre secciones
3. Declaraciones ambiguas que necesitan clarificación
4. Contexto o prerrequisitos faltantes
5. Especificaciones técnicas poco claras

Para cada brecha identificada, proporciona:
- Question: Una pregunta clara y específica sobre la información faltante
- Context missing: Descripción de qué información está faltando
- Type: Tipo de brecha (implementation, clarification, consistency, prerequisite)
- Severity: Nivel de impacto (low, medium, high, critical)
- Role affected: Quién necesita esta información (developer, architect, product, stakeholder, other)

IMPORTANTE: Devuelve SOLAMENTE un array JSON puro, sin código fences, sin markdown, sin texto adicional. El JSON debe ser válido y parseable directamente."""

        # Build user prompt
        user_prompt = f"""Analiza el siguiente documento para identificar brechas, inconsistencias e información faltante.

=== INFORMACIÓN DEL DOCUMENTO ===
- Título: {document_title}
- Tipo: {document_type}
- Rol afectado: {role_affected}

=== CONTENIDO DEL DOCUMENTO ===
{document_content}

=== BRECHAS EXISTENTES (evitar duplicados) ===
{existing_gaps_summary}

=== INSTRUCCIONES DE ANÁLISIS ===
1. Identifica brechas donde falta información crítica (cómo, por qué, detalles de implementación)
2. Busca inconsistencias entre diferentes secciones
3. Encuentra declaraciones ambiguas que necesitan clarificación
4. Verifica si falta contexto o prerrequisitos
5. Identifica especificaciones técnicas poco claras

=== FORMATO DE SALIDA ===
Devuelve SOLAMENTE un array JSON puro de brechas con la siguiente estructura:
[
  {{
    "question": "string",
    "context_missing": "string",
    "type": "implementation|clarification|consistency|prerequisite",
    "severity": "low|medium|high|critical",
    "role_affected": "developer|architect|product|stakeholder|other"
  }}
]

IMPORTANTE: No uses código fences (```json), no agregues texto adicional, no uses markdown. Devuelve únicamente el JSON válido y parseable."""

        logger.info("Sending prompt to LLM...")
        logger.info(f"System prompt length: {len(system_prompt)} chars")
        logger.info(f"User prompt length: {len(user_prompt)} chars")

        # Save complete prompts to files for debugging
        doc_id = document_title.replace(" ", "_")[:20]  # Use document title as ID
        save_prompt_to_file("system", system_prompt, doc_id)
        save_prompt_to_file("user", user_prompt, doc_id)

        try:
            # Calculate adaptive timeout based on document size
            # Estimate tokens: ~4 characters per token (rough approximation)
            estimated_tokens = len(user_prompt) // 4

            # Exploration phase: conservative timeout calculation
            # Assumption: 2 tokens/second generation speed (conservative estimate)
            # Safety margin: 2x (100% extra time for exploration phase variability)
            tokens_per_second = 2.0
            safety_margin = 2.0  # 100% extra time
            max_timeout = 600.0  # 10 minutes max (conservative for exploration)

            # Calculate: time needed = tokens / speed * margin
            estimated_time = estimated_tokens / tokens_per_second
            timeout = estimated_time * safety_margin
            timeout = min(timeout, max_timeout)

            logger.info(f"Adaptive timeout calculated: {timeout:.1f} seconds")
            logger.info(f"  - Document estimated tokens: {estimated_tokens}")
            logger.info(f"  - Assumed generation speed: {tokens_per_second} tokens/sec")
            logger.info(f"  - Estimated raw time: {estimated_time:.1f}s")
            logger.info(f"  - Safety margin: {safety_margin}x ({safety_margin*100:.0f}%)")
            logger.info(f"  - Max timeout cap: {max_timeout}s")

            # Use tools if enabled and project_id is provided
            if use_tools and project_id:
                logger.info("Using chat_with_tools for enhanced gap detection")
                tool_handlers = self.ollama_client._create_mcp_tool_handlers(project_id)
                
                # Enhance system prompt to encourage tool use
                enhanced_system_prompt = system_prompt + """

Tienes acceso a herramientas que te permiten:
- search_similar_documents: Buscar documentos relacionados en el proyecto
- list_gaps: Consultar gaps existentes en otros documentos
- read_document: Leer contenido de documentos relacionados

Usa estas herramientas cuando sea útil para:
- Encontrar contexto en documentos relacionados
- Verificar si información ya existe en otros documentos
- Identificar patrones de gaps similares en otros documentos
"""
                
                response = await self.ollama_client.chat_with_tools(
                    prompt=user_prompt,
                    system_prompt=enhanced_system_prompt,
                    temperature=0.3,
                    timeout=timeout,
                    tool_handlers=tool_handlers,
                    max_tool_calls=3,
                )
            else:
                logger.info("Using standard chat without tools")
                response = await self.ollama_client.chat(
                    prompt=user_prompt,
                    system_prompt=system_prompt,
                    temperature=0.3,  # Lower temperature for more consistent output
                    timeout=timeout,
                )

            logger.info(f"Received response from LLM (length: {len(response)})")

            # Save complete response to file
            save_prompt_to_file("response", response, doc_id)

            # Show first 500 chars in log
            logger.info(f"Raw response preview: {response[:500]}...")

            # Clean response: remove code fences and extra text
            cleaned_response = response.strip()
            
            # Remove markdown code fences if present
            if cleaned_response.startswith("```"):
                # Find the first ``` and last ```
                first_fence = cleaned_response.find("```")
                last_fence = cleaned_response.rfind("```")
                if first_fence != -1 and last_fence != -1 and first_fence != last_fence:
                    # Extract content between fences
                    cleaned_response = cleaned_response[first_fence + 3:last_fence].strip()
                    # Remove language identifier if present (e.g., "json")
                    if cleaned_response.startswith("json"):
                        cleaned_response = cleaned_response[4:].strip()
                    elif cleaned_response.startswith("JSON"):
                        cleaned_response = cleaned_response[4:].strip()
            
            # Try to find JSON array in the response if it's embedded in text
            if not cleaned_response.startswith("["):
                # Look for first [ and last ]
                first_bracket = cleaned_response.find("[")
                last_bracket = cleaned_response.rfind("]")
                if first_bracket != -1 and last_bracket != -1:
                    cleaned_response = cleaned_response[first_bracket:last_bracket + 1]
            
            logger.info(f"Cleaned response preview: {cleaned_response[:500]}...")

            # Parse JSON response
            gaps = json.loads(cleaned_response)

            logger.info(f"Successfully parsed {len(gaps)} gaps from JSON")

            # Filter duplicates based on similarity with existing gaps
            filtered_gaps = self._filter_duplicate_gaps(gaps, existing_gaps)

            logger.info(
                f"Detected {len(gaps)} gaps, filtered to {len(filtered_gaps)} after deduplication"
            )
            return filtered_gaps

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            logger.error(f"Response was: {response}")
            return []
        except Exception as e:
            logger.error(f"Gap detection failed: {type(e).__name__}: {e}")
            logger.error("Exception details:", exc_info=True)
            return []

    def _filter_duplicate_gaps(
        self, new_gaps: list[dict[str, Any]], existing_gaps: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """
        Filter out gaps that are similar to existing gaps.

        Args:
            new_gaps: Newly detected gaps
            existing_gaps: Existing gaps in the database

        Returns:
            Filtered list of new gaps
        """
        if not existing_gaps:
            return new_gaps

        filtered = []
        existing_questions = [gap.get("question", "").lower() for gap in existing_gaps]

        for new_gap in new_gaps:
            new_question = new_gap.get("question", "").lower()

            # Simple similarity check: check if question is too similar
            is_duplicate = False
            for existing_question in existing_questions:
                similarity = self._calculate_similarity(new_question, existing_question)
                if similarity > 0.8:  # 80% similarity threshold
                    is_duplicate = True
                    break

            if not is_duplicate:
                filtered.append(new_gap)

        return filtered

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate simple similarity between two texts using word overlap.

        Args:
            text1: First text
            text2: Second text

        Returns:
            Similarity score between 0 and 1
        """
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union) if union else 0.0
