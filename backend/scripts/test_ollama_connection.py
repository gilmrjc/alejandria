#!/usr/bin/env python3
"""Test Ollama connection from within Docker container."""

import asyncio
import httpx

async def test_ollama():
    ollama_url = "http://100.89.40.80:11434"
    
    print(f"Testing Ollama at: {ollama_url}")
    print()
    
    # Test /api/tags
    print("1. Testing /api/tags...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{ollama_url}/api/tags")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✓ /api/tags works")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    
    # Test /api/embeddings
    print("2. Testing /api/embeddings...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{ollama_url}/api/embeddings",
                json={"model": "BGE-M3:latest", "prompt": "test"},
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✓ /api/embeddings works")
            else:
                print(f"   ✗ Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    
    # Test /api/embed
    print("3. Testing /api/embed...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{ollama_url}/api/embed",
                json={"model": "BGE-M3:latest", "input": "test"},
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✓ /api/embed works")
            else:
                print(f"   ✗ Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_ollama())
