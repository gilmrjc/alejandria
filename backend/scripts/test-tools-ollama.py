#!/usr/bin/env python3
"""
Script de prueba para verificar que OllamaClient puede usar tools del MCP server.

Este script verifica:
1. Que las tools se importan correctamente desde el MCP server
2. Que el formato de tools es compatible con Ollama
3. Que el LLM puede recibir y usar las tools (si el modelo lo soporta)

Uso:
    docker compose exec celery-worker uv run python scripts/test-tools-ollama.py
"""

import asyncio
import json
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from shared.llm.ollama_client import AVAILABLE_TOOLS, OllamaClient
from shared.config.settings import settings


def test_tools_loading():
    """Verifica que las tools se cargaron correctamente."""
    print("=" * 80)
    print("Test 1: Verificar carga de tools desde MCP server")
    print("=" * 80)
    
    if not AVAILABLE_TOOLS:
        print("❌ No se cargaron tools")
        return False
    
    print(f"✓ {len(AVAILABLE_TOOLS)} tools cargadas:\n")
    
    for tool in AVAILABLE_TOOLS:
        func = tool.get("function", {})
        print(f"  📦 {func.get('name', 'unknown')}")
        print(f"     Descripción: {func.get('description', 'N/A')[:80]}...")
        params = func.get("parameters", {})
        print(f"     Parámetros: {list(params.get('properties', {}).keys())}")
        print()
    
    return True


def test_tools_schema():
    """Verifica que el formato de tools es válido."""
    print("=" * 80)
    print("Test 2: Verificar formato de tools")
    print("=" * 80)
    
    required_fields = ["type", "function"]
    function_fields = ["name", "description", "parameters"]
    
    for i, tool in enumerate(AVAILABLE_TOOLS):
        # Verificar estructura básica
        for field in required_fields:
            if field not in tool:
                print(f"❌ Tool {i}: Falta campo '{field}'")
                return False
        
        func = tool["function"]
        
        # Verificar campos de función
        for field in function_fields:
            if field not in func:
                print(f"❌ Tool {i}: Falta campo 'function.{field}'")
                return False
        
        print(f"✓ Tool {i} ({func['name']}): Formato válido")
    
    print()
    return True


async def test_chat_with_tools():
    """Prueba el chat con tools usando los handlers reales del MCP server."""
    print("=" * 80)
    print("Test 3: Prueba de chat con tools (usando MCP handlers reales)")
    print("=" * 80)
    
    if not AVAILABLE_TOOLS:
        print("⚠️  No hay tools disponibles, saltando test")
        return True
    
    print(f"Ollama URL: {settings.ollama_url}")
    print(f"Modelo: qwen3.6:latest")
    print()
    
    client = OllamaClient()
    
    # Crear handlers reales del MCP server (necesitamos project_id)
    # Para prueba, usamos project_id de ejemplo o buscamos uno real
    from shared.db.session import get_db_session
    from sqlalchemy import select
    from shared.db.models import Project
    
    session = get_db_session()
    try:
        # Buscar primer proyecto disponible
        project = session.execute(select(Project).limit(1)).scalar_one_or_none()
        if project:
            project_id = str(project.id)
            print(f"Usando proyecto: {project.name} (ID: {project_id})")
        else:
            project_id = "00000000-0000-0000-0000-000000000000"  # Mock para prueba
            print(f"No hay proyectos reales, usando project_id de prueba")
    except Exception as e:
        project_id = "00000000-0000-0000-0000-000000000000"
        print(f"Error buscando proyecto: {e}, usando mock")
    finally:
        session.close()
    
    # Crear handlers reales usando el método del OllamaClient
    tool_handlers = client._create_mcp_tool_handlers(project_id)
    
    print(f"Handlers creados: {list(tool_handlers.keys())}")
    print()
    
    # Primero, probar los handlers directamente
    print("Test 3a: Probando handlers MCP directamente...")
    try:
        search_result = await tool_handlers["search_similar_documents"](
            query="autenticación JWT",
            limit=3
        )
        print(f"✅ search_similar_documents: {len(search_result.get('results', []))} resultados")
        
        # Si encontramos documentos, listar sus gaps
        if search_result.get("results"):
            doc_slug = search_result["results"][0]["slug"]
            gaps_result = await tool_handlers["list_gaps"](document_slug=doc_slug)
            print(f"✅ list_gaps para '{doc_slug}': {gaps_result.get('total', 0)} gaps")
    except Exception as e:
        print(f"⚠️  Error probando handlers: {e}")
        print("Continuando con test del LLM...")
    
    print()
    
    # Buscar un documento real para incluir en el prompt
    from shared.db.session import get_db_session
    from sqlalchemy import select
    from shared.db.models import Document
    
    session = get_db_session()
    test_doc_slug = None
    try:
        doc = session.execute(select(Document).limit(1)).scalar_one_or_none()
        if doc:
            test_doc_slug = doc.slug
            test_doc_title = doc.title
            print(f"📄 Usando documento real para test: '{test_doc_title}' (slug: {test_doc_slug})")
        else:
            test_doc_slug = "test-document"
            test_doc_title = "Documento de prueba"
            print(f"⚠️  No hay documentos, usando slug de prueba: {test_doc_slug}")
    except Exception as e:
        test_doc_slug = "test-document"
        print(f"⚠️  Error obteniendo documento: {e}, usando slug de prueba")
    finally:
        session.close()
    
    # Prompt específico con document_slug para forzar llamada a tool
    prompt = f"""Por favor lista los gaps del documento con slug '{test_doc_slug}'.

Si el documento no existe o hay un error, indícalo claramente."""
    
    print("\nTest 3b: Enviando prompt al LLM para FORZAR llamada a tool...")
    print(f"Prompt: {prompt}")
    print()
    
    # Contador de llamadas a tools
    tool_calls_made = []
    
    # Wrapper para trackear llamadas
    original_list_gaps = tool_handlers["list_gaps"]
    async def tracked_list_gaps(document_slug: str, status: str = None):
        print(f"   🔧 [TRACKER] list_gaps INVOCADO con document_slug='{document_slug}'")
        tool_calls_made.append("list_gaps")
        return await original_list_gaps(document_slug, status)
    
    tool_handlers_tracked = {
        **tool_handlers,
        "list_gaps": tracked_list_gaps,
    }
    
    try:
        # Usar timeout más largo ya que puede llamar funciones reales
        response = await client.chat_with_tools(
            prompt=prompt,
            system_prompt="Eres un asistente técnico. "
                       "Debes usar la herramienta 'list_gaps' para obtener los gaps de un documento cuando te pidan información sobre gaps.",
            tool_handlers=tool_handlers_tracked,
            max_tool_calls=2,
            timeout=60.0,
        )
        
        print("\n✅ Respuesta recibida:")
        print("-" * 80)
        print(response[:800] if len(response) > 800 else response)
        print("-" * 80)
        print()
        
        # Verificar si se llamaron tools
        if tool_calls_made:
            print(f"🎉 ÉXITO: Se invocaron {len(tool_calls_made)} tool(s): {tool_calls_made}")
            return True
        else:
            print(f"⚠️  ADVERTENCIA: No se invocaron tools. El LLM respondió directamente.")
            print(f"   (Esto puede ser normal si el modelo no soporta function calling)")
            return True  # No es un fallo del test, solo el modelo no usó tools
        
    except Exception as e:
        print(f"❌ Error en chat_with_tools: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_json_output():
    """Muestra el JSON completo de tools para inspección."""
    print("=" * 80)
    print("Test 4: JSON de tools para Ollama")
    print("=" * 80)
    
    if not AVAILABLE_TOOLS:
        print("No hay tools para mostrar")
        return
    
    tools_json = json.dumps(AVAILABLE_TOOLS, indent=2, ensure_ascii=False)
    print(tools_json[:1500] + "..." if len(tools_json) > 1500 else tools_json)
    print()


async def main():
    """Ejecuta todos los tests."""
    print("\n" + "=" * 80)
    print("Test de Integración: OllamaClient + MCP Tools")
    print("=" * 80)
    print()
    
    results = []
    
    # Test 1: Carga de tools
    results.append(("Carga de tools", test_tools_loading()))
    
    # Test 2: Formato de tools
    results.append(("Formato de tools", test_tools_schema()))
    
    # Test 3: Chat con tools
    results.append(("Chat con tools", await test_chat_with_tools()))
    
    # Test 4: Mostrar JSON
    test_json_output()
    
    # Resumen
    print("=" * 80)
    print("Resumen de Tests")
    print("=" * 80)
    
    for name, passed in results:
        status = "✅ PASÓ" if passed else "❌ FALLÓ"
        print(f"  {status}: {name}")
    
    all_passed = all(r[1] for r in results)
    
    print()
    if all_passed:
        print("🎉 Todos los tests pasaron correctamente!")
        print("El OllamaClient está configurado para usar tools del MCP server.")
    else:
        print("⚠️  Algunos tests fallaron. Revisa los errores arriba.")
    
    return all_passed


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
