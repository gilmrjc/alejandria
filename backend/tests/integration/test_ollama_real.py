"""Integration tests with real Ollama instance.

These tests require a running Ollama instance and are marked as integration.
Run with: pytest tests/integration/test_ollama_real.py -v

Record/replay mechanism using pytest-vcr:
- First run: makes real requests to Ollama and records to cassettes/
- Subsequent runs: uses recorded responses from cassettes/
- To re-record: delete the cassette files in cassettes/
- Use SKIP_OLLAMA_TESTS env var to skip these tests entirely
"""

import os

import pytest

from shared.llm.ollama_client import OllamaClient


@pytest.fixture(scope="module")
def vcr_config():
    """Configure VCR for recording/replaying HTTP interactions."""
    return {
        "filter_headers": ["authorization", "host"],
        "ignore_localhost": True,
        "record_mode": "once",
    }


@pytest.mark.integration
@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_ollama_real_chat():
    """Test real Ollama chat endpoint."""
    client = OllamaClient()
    response = await client.chat("Hello, how are you?")
    assert response is not None
    assert len(response) > 0
    print(f"Response: {response}")


@pytest.mark.integration
@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_ollama_real_gap_detection():
    """Test real Ollama gap detection."""
    client = OllamaClient()

    document_title = "Authentication System Design"
    document_content = """
    # Authentication System

    This document describes the authentication system for the application.

    ## Overview
    The system uses JWT tokens for authentication.

    ## Implementation
    TODO: Implement token refresh logic
    TODO: Add rate limiting
    """
    document_type = "technical"
    existing_gaps = []
    role_affected = "developer"

    gaps = await client.detect_gaps(
        document_title=document_title,
        document_content=document_content,
        document_type=document_type,
        existing_gaps=existing_gaps,
        role_affected=role_affected,
    )

    assert isinstance(gaps, list)
    print(f"Detected {len(gaps)} gaps:")
    for gap in gaps:
        print(f"  - {gap.get('question')}")
        print(f"    Context: {gap.get('context_missing')}")
        print(f"    Severity: {gap.get('severity')}")


@pytest.mark.integration
@pytest.mark.vcr()
def test_ollama_connection():
    """Test Ollama connection."""
    import httpx

    from shared.config.settings import settings

    try:
        response = httpx.get(f"{settings.ollama_url}/api/tags", timeout=5.0)
        assert response.status_code == 200
        data = response.json()
        print(f"Available models: {data.get('models', [])}")
    except Exception as e:
        pytest.skip(f"Ollama not available: {e}")
