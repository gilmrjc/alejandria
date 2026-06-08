#!/usr/bin/env python3
"""
Script para probar el sistema de detección de gaps con datos reales.

Este script permite probar el sistema de detección de gaps usando Ollama real
con un documento de ejemplo.

Uso:
    python scripts/test-gap-detection-real.py

Requisitos:
    - Ollama corriendo en OLLAMA_URL (default: http://localhost:11434)
    - Modelo qwen2.5:7b disponible en Ollama
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Configurar logging para mostrar INFO y DEBUG
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from shared.config.settings import settings
from shared.llm.ollama_client import OllamaClient

print("=" * 80)
print("Configuración de Ollama")
print("=" * 80)
print(f"OLLAMA_URL desde settings: {settings.ollama_url}")
print(f"OLLAMA_URL desde env: {os.environ.get('OLLAMA_URL', 'No definida')}")
print()


# Documento de ejemplo para pruebas
SAMPLE_DOCUMENT = """
# Sistema de Autenticación

## Visión General
Este documento describe el sistema de autenticación para la aplicación Alejandria.

## Arquitectura
El sistema utiliza tokens JWT para autenticación de usuarios.

### Flujo de Autenticación
1. Usuario envía credenciales
2. Servidor valida credenciales
3. Servidor genera token JWT
4. Cliente almacena token
5. Cliente envía token en requests subsiguientes

## Implementación

### Endpoint de Login
POST /api/v1/auth/login

Request body:
```json
{
  "username": "string",
  "password": "string"
}
```

Response:
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

### Validación de Token
TODO: Implementar middleware de validación de tokens
TODO: Agregar lógica de refresh token
TODO: Configurar expiración de tokens

### Seguridad
TODO: Implementar rate limiting
TODO: Agregar protección contra brute force
TODO: Configurar HTTPS obligatorio en producción

## Errores Comunes
TODO: Documentar códigos de error
TODO: Implementar manejo de errores de autenticación

## Testing
TODO: Escribir tests de integración para autenticación
TODO: Crear tests de carga para endpoint de login
"""


async def test_gap_detection():
    """Prueba el sistema de detección de gaps con el documento de ejemplo."""
    print("=" * 80)
    print("Prueba de Detección de Gaps con Ollama Real")
    print("=" * 80)
    print()

    print(f"Ollama URL: {settings.ollama_url}")
    print()

    # Crear cliente Ollama
    print("Creando cliente Ollama...")
    client = OllamaClient()
    print(f"✓ Cliente creado con URL: {client.ollama_url}")
    print(f"✓ Modelo: {client.model}")
    print(f"✓ Timeout: {client.timeout} segundos")
    print()

    # Detectar gaps
    print("Iniciando análisis de documento...")
    print(f"Tamaño del documento: {len(SAMPLE_DOCUMENT)} caracteres")
    print("Primeros 200 caracteres del documento:")
    print(f"  {SAMPLE_DOCUMENT[:200]}...")
    print("-" * 80)

    try:
        print("Llamando a client.detect_gaps()...")
        print(
            "Nota: Este proceso puede tardar 60-120 segundos dependiendo del tamaño del documento."
        )
        print(
            "      El modelo está analizando el documento completo en busca de gaps..."
        )
        gaps = await client.detect_gaps(
            document_title="Sistema de Autenticación",
            document_content=SAMPLE_DOCUMENT,
            document_type="technical",
            existing_gaps=[],
            role_affected="developer",
        )

        print("\n✓ Análisis completado exitosamente")
        print(f"✓ Gaps detectados: {len(gaps)}")
        print()

        if not gaps:
            print("⚠ No se detectaron gaps. Esto puede significar:")
            print("   - El documento está completo")
            print("   - El LLM no encontró información faltante")
            print("   - Hubo un error en el procesamiento (revisa los logs detallados)")
            print()

    except Exception as e:
        print(f"\n✗ Error durante detección de gaps: {type(e).__name__}: {e}")
        print("\nDetalles del error:")
        import traceback

        traceback.print_exc()
        print()
        raise

    # Mostrar gaps detectados
    for i, gap in enumerate(gaps, 1):
        print(f"Gap #{i}")
        print(f"  Pregunta: {gap.get('question')}")
        print(f"  Contexto faltante: {gap.get('context_missing')}")
        print(f"  Tipo: {gap.get('type')}")
        print(f"  Severidad: {gap.get('severity')}")
        print(f"  Rol afectado: {gap.get('role_affected')}")
        print()

    return gaps


async def test_chat():
    """Prueba el chat básico con Ollama."""
    print("=" * 80)
    print("Prueba de Chat con Ollama Real")
    print("=" * 80)
    print()

    client = OllamaClient()
    print(f"Cliente creado con URL: {client.ollama_url}")
    print("Enviando mensaje a Ollama...")

    try:
        response = await client.chat("Hola, ¿cómo estás?")
        print(f"✓ Respuesta recibida: {response[:100]}...")
        print()
    except Exception as e:
        print(f"✗ Error en chat: {e}")
        raise


async def main():
    """Función principal."""
    print("Iniciando pruebas...")
    print(f"Python: {sys.version}")
    print()

    try:
        # Probar chat básico
        await test_chat()

        # Probar detección de gaps
        gaps = await test_gap_detection()

        if gaps:
            print("=" * 80)
            print("✓ Prueba completada exitosamente")
            print(f"✓ Total de gaps detectados: {len(gaps)}")
            print("=" * 80)
        else:
            print("=" * 80)
            print("⚠ No se detectaron gaps")
            print("=" * 80)

    except Exception as e:
        print("=" * 80)
        print(f"✗ Error en la prueba: {e}")
        print("=" * 80)
        print("\nStack trace:")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
