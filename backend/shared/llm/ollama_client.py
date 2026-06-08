"""Ollama client for LLM chat and gap detection with tool use support."""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Callable

import httpx

from shared.config.settings import settings
from shared.utils.retry import retry_with_backoff

logger = logging.getLogger(__name__)


# Import MCP tools dynamically using function introspection
def _get_mcp_tools():
    """
    Get tools from MCP server by importing functions and extracting their schemas.
    This reuses the existing tool definitions from the MCP server.
    """
    try:
        # Import the actual functions from mcp_server
        from mcp_server.server import (
            list_gaps,
            read_document,
            search_similar_documents,
        )
        
        def _extract_tool_schema(func):
            """Extract OpenAI-compatible tool schema from function using introspection."""
            import inspect
            sig = inspect.signature(func)
            doc = func.__doc__ or f"Tool {func.__name__}"
            
            # Get first paragraph as description
            description = doc.split("\n\n")[0].strip() if "\n\n" in doc else doc.strip()
            
            # Build parameters schema
            properties = {}
            required = []
            
            for name, param in sig.parameters.items():
                # Skip internal/session parameters
                if name in ['session', 'should_close', 'ctx', 'context']:
                    continue
                    
                # Determine type from annotation
                param_type = "string"
                if param.annotation != inspect.Parameter.empty:
                    if param.annotation in (int, 'int'):
                        param_type = "integer"
                    elif param.annotation in (bool, 'bool'):
                        param_type = "boolean"
                    elif param.annotation in (float, 'float'):
                        param_type = "number"
                
                # Check if required (no default value)
                if param.default == inspect.Parameter.empty:
                    required.append(name)
                
                # Extract parameter description from docstring Args section
                param_desc = f"Parameter {name}"
                if "Args:" in doc:
                    args_section = doc.split("Args:")[1].split("Returns:")[0] if "Returns:" in doc else doc.split("Args:")[1]
                    for line in args_section.split("\n"):
                        line = line.strip()
                        if line.startswith(f"{name}:"):
                            param_desc = line.split(":", 1)[1].strip()
                            break
                        elif line.startswith(f"{name} "):
                            param_desc = line[len(name):].strip().lstrip(":- ")
                            break
                
                prop = {
                    "type": param_type,
                    "description": param_desc
                }
                
                # Add default if exists
                if param.default != inspect.Parameter.empty and param.default is not None:
                    prop["default"] = param.default
                
                properties[name] = prop
            
            return {
                "type": "function",
                "function": {
                    "name": func.__name__,
                    "description": description,
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "required": required
                    }
                }
            }
        
        # Define which tools to expose to Ollama
        tool_funcs = [
            search_similar_documents,
            list_gaps,
            read_document,
        ]
        
        return [_extract_tool_schema(f) for f in tool_funcs]
        
    except ImportError as e:
        logger.warning(f"Could not import MCP server: {e}")
        return []
    except Exception as e:
        logger.warning(f"Error extracting MCP tools: {e}")
        import traceback
        traceback.print_exc()
        return []

# Lazy load tools
AVAILABLE_TOOLS = _get_mcp_tools()


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


class OllamaClient:
    """Client for Ollama LLM API for chat and gap detection."""

    def __init__(self, ollama_url: str = None, model: str = "qwen3.6:latest"):
        """
        Initialize Ollama client.

        Args:
            ollama_url: Ollama API URL (defaults to settings.ollama_url)
            model: Model name to use (default: qwen3.6:latest)
        """
        self.ollama_url = ollama_url or settings.ollama_url
        self.model = model
        self.timeout = 30.0  # Default timeout for chat requests

    async def chat(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = 0.7,
        timeout: float = None,
    ) -> str:
        """
        Send a chat request to Ollama.

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature (0.0 to 1.0)
            timeout: Request timeout in seconds

        Returns:
            LLM response text
        """
        if timeout is None:
            timeout = self.timeout

        logger.info(
            f"Chat request - Model: {self.model}, Temperature: {temperature}, Timeout: {timeout}"
        )

        # Log complete prompts for debugging (truncated in production)
        max_log_length = 2000  # Show up to 2000 chars in logs
        prompt_display = (
            prompt[:max_log_length] + "..." if len(prompt) > max_log_length else prompt
        )
        logger.info(f"User prompt ({len(prompt)} chars):\n{prompt_display}")

        if system_prompt:
            system_display = (
                system_prompt[:max_log_length] + "..."
                if len(system_prompt) > max_log_length
                else system_prompt
            )
            logger.info(
                f"System prompt ({len(system_prompt)} chars):\n{system_display}"
            )

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        async def _call_ollama_streaming():
            """
            Use streaming to avoid timeouts on long generation tasks.
            Streaming keeps the connection alive by receiving tokens incrementally.
            """
            logger.info(f"Using streaming mode to handle long generation (timeout: {timeout}s)")
            
            accumulated_content = []
            last_chunk_time = asyncio.get_event_loop().time()
            
            async with httpx.AsyncClient(timeout=timeout) as client:
                try:
                    async with client.stream(
                        "POST",
                        f"{self.ollama_url}/api/chat",
                        json={
                            "model": self.model,
                            "messages": messages,
                            "stream": True,  # Enable streaming
                            "options": {"temperature": temperature},
                        },
                    ) as response:
                        logger.info(f"Response status: {response.status_code}")
                        response.raise_for_status()
                        
                        chunk_count = 0
                        async for line in response.aiter_lines():
                            if not line.strip():
                                continue
                            
                            try:
                                chunk = json.loads(line)
                                chunk_count += 1
                                
                                # Check if this is the final chunk
                                if chunk.get("done", False):
                                    logger.info(f"Streaming complete. Received {chunk_count} chunks")
                                    break
                                
                                # Accumulate content from message
                                message = chunk.get("message", {})
                                content_piece = message.get("content", "")
                                if content_piece:
                                    accumulated_content.append(content_piece)
                                    
                                    # Log progress every 50 chunks
                                    if chunk_count % 50 == 0:
                                        current_content = "".join(accumulated_content)
                                        logger.info(f"Streaming progress: {chunk_count} chunks, {len(current_content)} chars so far")
                                
                                # Update last chunk time for liveness check
                                last_chunk_time = asyncio.get_event_loop().time()
                                
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse chunk: {e}, line: {line[:100]}")
                                continue
                    
                    # Combine all content pieces
                    full_content = "".join(accumulated_content)
                    
                    # Log complete response
                    content_display = (
                        full_content[:max_log_length] + "..."
                        if len(full_content) > max_log_length
                        else full_content
                    )
                    logger.info(f"Response ({len(full_content)} chars):\n{content_display}")
                    
                    return full_content
                    
                except httpx.HTTPStatusError as e:
                    logger.error(
                        f"HTTP error {e.response.status_code}: {e.response.text}"
                    )
                    raise
                except httpx.ReadTimeout:
                    logger.error(
                        f"Read timeout after {timeout} seconds. The model may be taking longer than expected."
                    )
                    logger.error(
                        "Consider increasing timeout or using a smaller model for this task."
                    )
                    raise
                except Exception as e:
                    logger.error(f"Request error: {type(e).__name__}: {e}")
                    raise

        return await retry_with_backoff(
            _call_ollama_streaming,
            max_retries=3,
            base_delay=0.5,
            max_delay=5.0,
            retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException),
        )

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

        DEPRECATED: Use GapDetectionService instead for better separation of concerns.
        This method is kept for backwards compatibility.

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
        import warnings
        warnings.warn(
            "OllamaClient.detect_gaps is deprecated. Use GapDetectionService instead.",
            DeprecationWarning,
            stacklevel=2
        )
        
        from shared.services.gap_detection_service import GapDetectionService
        
        service = GapDetectionService(ollama_client=self)
        return await service.detect_gaps(
            document_title=document_title,
            document_content=document_content,
            document_type=document_type,
            existing_gaps=existing_gaps,
            role_affected=role_affected,
            project_id=project_id,
            use_tools=use_tools,
        )

    async def chat_with_tools(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = 0.7,
        timeout: float = None,
        tool_handlers: dict[str, Callable] = None,
        max_tool_calls: int = 5,
    ) -> str:
        """
        Chat with tool use support (function calling).
        
        The LLM can decide to call tools during the conversation to get additional
        information. This enables the agent to search for related documents,
        check existing gaps, etc.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            timeout: Request timeout
            tool_handlers: Dict mapping tool names to handler functions
            max_tool_calls: Maximum number of tool calls to prevent infinite loops
            
        Returns:
            Final LLM response after all tool calls
        """
        if timeout is None:
            timeout = self.timeout
            
        if tool_handlers is None:
            tool_handlers = {}
            
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        logger.info(f"Starting chat with tools support (max {max_tool_calls} tool calls)")
        
        for call_count in range(max_tool_calls + 1):
            logger.info(f"Chat iteration {call_count + 1}/{max_tool_calls + 1}")
            
            # Make request with tools
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    f"{self.ollama_url}/api/chat",
                    json={
                        "model": self.model,
                        "messages": messages,
                        "stream": False,
                        "tools": AVAILABLE_TOOLS,
                        "options": {"temperature": temperature},
                    },
                )
                response.raise_for_status()
                data = response.json()
            
            message = data.get("message", {})
            content = message.get("content", "")
            tool_calls = message.get("tool_calls", [])
            
            # If no tool calls, we're done
            if not tool_calls:
                logger.info(f"No tool calls requested. Final response received.")
                return content
                
            # Process tool calls
            logger.info(f"LLM requested {len(tool_calls)} tool call(s)")
            
            # Add assistant message with tool calls
            messages.append({
                "role": "assistant",
                "content": content,
                "tool_calls": tool_calls
            })
            
            # Execute each tool call
            for tool_call in tool_calls:
                function_name = tool_call.get("function", {}).get("name")
                arguments = tool_call.get("function", {}).get("arguments", {})
                
                logger.info(f"Executing tool: {function_name} with args: {arguments}")
                
                # Execute tool handler
                if function_name in tool_handlers:
                    try:
                        tool_result = await tool_handlers[function_name](**arguments)
                        tool_result_str = json.dumps(tool_result, default=str)
                    except Exception as e:
                        tool_result_str = f"Error executing {function_name}: {e}"
                        logger.error(tool_result_str)
                else:
                    tool_result_str = f"Tool {function_name} not implemented"
                    logger.warning(tool_result_str)
                
                # Add tool response
                messages.append({
                    "role": "tool",
                    "content": tool_result_str
                })
                logger.info(f"Tool result: {tool_result_str[:200]}...")
        
        logger.warning(f"Max tool calls ({max_tool_calls}) reached. Returning last response.")
        return content
    
    def _create_mcp_tool_handlers(self, project_id: str) -> dict[str, Callable]:
        """
        Create tool handlers that call MCP server functions directly.
        Note: MCP functions are synchronous, so we wrap them to be async-compatible.
        
        Args:
            project_id: Project ID for context
            
        Returns:
            Dict of tool handler functions that wrap MCP server calls
        """
        from mcp_server.server import (
            list_gaps,
            read_document,
            search_similar_documents,
        )
        import asyncio
        
        async def wrapped_search_similar_documents(query: str, limit: int = 5):
            """Call MCP search_similar_documents with project_id."""
            logger.info(f"[Tool] search_similar_documents: {query[:50]}...")
            try:
                # Run synchronous MCP function in thread pool
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None,  # Default executor
                    lambda: search_similar_documents(
                        query=query,
                        project_id=project_id,
                        limit=limit
                    )
                )
                # Simplify result for LLM
                return {
                    "total": result.get("total", 0),
                    "results": [
                        {
                            "title": r.get("title", "Unknown"),
                            "slug": r.get("slug", "unknown"),
                            "score": r.get("score", 0),
                            "snippet": r.get("chunk_content", "")[:200]
                        }
                        for r in result.get("results", [])[:3]
                    ]
                }
            except Exception as e:
                logger.error(f"Error in search_similar_documents: {e}")
                return {"error": str(e)}
        
        async def wrapped_list_gaps(document_slug: str, status: str = None):
            """Call MCP list_gaps for a document."""
            logger.info(f"[Tool] list_gaps: {document_slug}")
            try:
                # Run synchronous MCP function in thread pool
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None,
                    lambda: list_gaps(
                        document_slug=document_slug,
                        status=status
                    )
                )
                # Simplify for LLM
                gaps = result.get("gaps", [])
                return {
                    "total": len(gaps),
                    "gaps": [
                        {
                            "question": g.get("question", ""),
                            "priority": g.get("priority", "medium"),
                            "status": g.get("status", "pending")
                        }
                        for g in gaps
                    ]
                }
            except Exception as e:
                logger.error(f"Error in list_gaps: {e}")
                return {"error": str(e)}
        
        async def wrapped_read_document(document_slug: str, include_metadata: bool = False):
            """Call MCP read_document."""
            logger.info(f"[Tool] read_document: {document_slug}")
            try:
                # Run synchronous MCP function in thread pool
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None,
                    lambda: read_document(
                        document_slug=document_slug,
                        include_metadata=include_metadata
                    )
                )
                # Simplify for LLM - limit content size
                content = result.get("content", "")
                return {
                    "slug": result.get("slug", document_slug),
                    "title": result.get("title", "Unknown"),
                    "content": content[:3000] if len(content) > 3000 else content,
                    "content_length": len(content),
                    "truncated": len(content) > 3000
                }
            except Exception as e:
                logger.error(f"Error in read_document: {e}")
                return {"error": str(e)}
        
        return {
            "search_similar_documents": wrapped_search_similar_documents,
            "list_gaps": wrapped_list_gaps,
            "read_document": wrapped_read_document,
        }

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
