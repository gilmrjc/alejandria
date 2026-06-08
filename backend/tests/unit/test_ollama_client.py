"""Unit tests for OllamaClient."""

import pytest

from shared.llm.ollama_client import OllamaClient


@pytest.mark.asyncio
async def test_ollama_client_init():
    """Test OllamaClient initialization."""
    client = OllamaClient()
    assert client.ollama_url is not None
    assert client.model == "qwen2.5:7b"
    assert client.timeout == 30.0


@pytest.mark.asyncio
async def test_ollama_client_custom_model():
    """Test OllamaClient with custom model."""
    client = OllamaClient(model="custom-model")
    assert client.model == "custom-model"


def test_calculate_similarity():
    """Test similarity calculation."""
    client = OllamaClient()
    similarity = client._calculate_similarity("test document", "test document")
    assert similarity == 1.0

    similarity = client._calculate_similarity("test", "other")
    assert similarity == 0.0


def test_filter_duplicate_gaps():
    """Test duplicate gap filtering."""
    client = OllamaClient()
    new_gaps = [
        {"question": "How does authentication work?"},
        {"question": "What is the database schema?"},
    ]
    existing_gaps = [
        {"question": "How does authentication work?"},
    ]

    filtered = client._filter_duplicate_gaps(new_gaps, existing_gaps)
    assert len(filtered) == 1
    assert filtered[0]["question"] == "What is the database schema?"
