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
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from shared.config.settings import settings
from shared.llm.ollama_client import OllamaClient


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
    client = OllamaClient()

    # Detectar gaps
    print("Analizando documento...")
    print("-" * 80)

    gaps = await client.detect_gaps(
        document_title="Sistema de Autenticación",
        document_content=SAMPLE_DOCUMENT,
        document_type="technical",
        existing_gaps=[],
        role_affected="developer",
    )

    print(f"\n✓ Análisis completado")
    print(f"✓ Gaps detectados: {len(gaps)}")
    print()

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

    response = await client.chat("Hola, ¿cómo estás?")
    print(f"Respuesta: {response}")
    print()


async def main():
    """Función principal."""
    try:
        # Probar chat básico
        await test_chat()

        # Probar detección de gaps
        gaps = await test_gap_detection()

        if gaps:
            print("=" * 80)
            print("✓ Prueba completada exitosamente")
            print("=" * 80)
        else:
            print("=" * 80)
            print("⚠ No se detectaron gaps")
            print("=" * 80)

    except Exception as e:
        print("=" * 80)
        print(f"✗ Error: {e}")
        print("=" * 80)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
