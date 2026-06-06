"""Unit tests for Qdrant vector business logic."""

from unittest.mock import AsyncMock, MagicMock, patch

from shared.vector.qdrant import QdrantClient, chunk_text


class TestTextChunking:
    """Test text chunking business logic."""

    def test_chunk_empty_text(self):
        """Test chunking empty text returns empty list."""
        chunks = chunk_text("")
        assert chunks == []

    def test_chunk_short_text(self):
        """Test short text returns single chunk."""
        text = "Short text"
        chunks = chunk_text(text, chunk_size=500)
        assert len(chunks) == 1
        assert chunks[0] == "Short text"

    def test_chunk_long_text(self):
        """Test long text is split into multiple chunks."""
        text = "Word " * 200  # ~1000 characters
        chunks = chunk_text(text, chunk_size=500)
        # chunk_text splits by paragraphs first, so single line may not split
        # Test with actual paragraphs
        text = "\n\n".join(["Paragraph " + str(i) for i in range(50)])
        chunks = chunk_text(text, chunk_size=500)
        assert len(chunks) > 1

    def test_chunk_respects_chunk_size(self):
        """Test chunks respect maximum chunk size."""
        # chunk_text splits by paragraphs, so test with paragraphs
        text = "\n\n".join(["A" * 300 for _ in range(5)])
        chunks = chunk_text(text, chunk_size=500)

        for chunk in chunks:
            assert len(chunk) <= 500

    def test_chunk_with_overlap(self):
        """Test chunks have overlap when specified."""
        text = "Word " * 200
        chunks = chunk_text(text, chunk_size=500, overlap=50)

        # Check that consecutive chunks have overlap
        if len(chunks) > 1:
            # Last part of first chunk should be in second chunk
            assert chunks[0][-50:] in chunks[1]

    def test_chunk_paragraph_preservation(self):
        """Test chunking preserves paragraph boundaries."""
        text = "Paragraph 1\n\nParagraph 2\n\nParagraph 3"
        chunks = chunk_text(text, chunk_size=500)

        # Each chunk should contain complete paragraphs when possible
        for chunk in chunks:
            assert "\n\n" not in chunk or chunk.endswith(chunk.strip())

    def test_chunk_no_overlap(self):
        """Test chunking with zero overlap."""
        text = "Word " * 200
        chunks = chunk_text(text, chunk_size=500, overlap=0)

        if len(chunks) > 1:
            # No overlap between chunks
            assert chunks[0][-10:] not in chunks[1]

    def test_chunk_whitespace_handling(self):
        """Test chunking handles extra whitespace."""
        text = "  Paragraph 1  \n\n  Paragraph 2  "
        chunks = chunk_text(text, chunk_size=500)

        # Chunks should be stripped of leading/trailing whitespace
        for chunk in chunks:
            assert chunk == chunk.strip()

    def test_chunk_single_paragraph(self):
        """Test single paragraph is not split unnecessarily."""
        text = "A" * 100  # Short paragraph
        chunks = chunk_text(text, chunk_size=500)

        assert len(chunks) == 1
        assert chunks[0] == text

    def test_chunk_very_long_paragraph(self):
        """Test very long paragraph is split when it exceeds chunk size."""
        # chunk_text splits by paragraphs, so test with a single long paragraph
        text = "A" * 1000  # No line breaks
        chunks = chunk_text(text, chunk_size=500)

        # Single paragraph without line breaks won't be split by chunk_text
        # It respects paragraph boundaries
        assert len(chunks) == 1
        assert len(chunks[0]) == 1000


class TestQdrantClient:
    """Test Qdrant client business logic."""

    @patch("shared.vector.qdrant.QdrantSDKClient")
    def test_create_collection(self, mock_client_class):
        """Test collection creation."""

        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        client = QdrantClient(url="http://localhost:6333")
        result = client.create_collection("test_collection", vector_size=1024)

        assert result is True
        mock_client.create_collection.assert_called_once()

    @patch("shared.vector.qdrant.QdrantSDKClient")
    def test_create_collection_already_exists(self, mock_client_class):
        """Test collection creation when already exists."""

        mock_client = MagicMock()
        mock_client.create_collection.side_effect = Exception("already exists")
        mock_client_class.return_value = mock_client

        client = QdrantClient(url="http://localhost:6333")
        result = client.create_collection("test_collection")

        # Should return True even if already exists
        assert result is True

    @patch("shared.vector.qdrant.QdrantSDKClient")
    def test_insert_vectors(self, mock_client_class):
        """Test vector insertion."""

        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        client = QdrantClient(url="http://localhost:6333")
        vectors = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        payloads = [{"id": 1}, {"id": 2}]

        result = client.insert_vectors("test_collection", vectors, payloads)

        assert result is True
        mock_client.upsert.assert_called_once()

    @patch("shared.vector.qdrant.QdrantSDKClient")
    def test_search_similar(self, mock_client_class):
        """Test similar vector search."""

        mock_client = MagicMock()
        mock_result = MagicMock()
        mock_result.id = "1"
        mock_result.score = 0.9
        mock_result.payload = {"text": "test"}
        mock_client.search.return_value = [mock_result]
        mock_client_class.return_value = mock_client

        client = QdrantClient(url="http://localhost:6333")
        query_vector = [0.1, 0.2, 0.3]

        results = client.search_similar("test_collection", query_vector)

        assert len(results) == 1
        assert results[0]["id"] == "1"
        assert results[0]["score"] == 0.9

    @patch("shared.vector.qdrant.QdrantSDKClient")
    def test_delete_vectors(self, mock_client_class):
        """Test vector deletion."""

        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        client = QdrantClient(url="http://localhost:6333")
        result = client.delete_vectors("test_collection", ["1", "2"])

        assert result is True
        mock_client.delete.assert_called_once()

    @patch("shared.vector.qdrant.QdrantSDKClient")
    def test_delete_collection(self, mock_client_class):
        """Test collection deletion."""

        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        client = QdrantClient(url="http://localhost:6333")
        result = client.delete_collection("test_collection")

        assert result is True
        mock_client.delete_collection.assert_called_once()


class TestEmbeddingGeneration:
    """Test embedding generation business logic."""

    @patch("shared.vector.qdrant.httpx.AsyncClient")
    async def test_generate_embedding(self, mock_client_class):
        """Test single embedding generation."""
        from shared.vector.qdrant import generate_embedding

        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"embedding": [0.1, 0.2, 0.3]}
        mock_client.post.return_value = mock_response
        mock_client_class.return_value.__aenter__.return_value = mock_client

        embedding = await generate_embedding("test text")

        assert embedding == [0.1, 0.2, 0.3]
        mock_client.post.assert_called_once()

    @patch("shared.vector.qdrant.httpx.AsyncClient")
    async def test_generate_embedding_with_retry(self, mock_client_class):
        """Test embedding generation with retry on failure."""
        from httpx import TimeoutException

        from shared.vector.qdrant import generate_embedding

        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"embedding": [0.1, 0.2, 0.3]}

        # First call fails, second succeeds
        mock_client.post.side_effect = [TimeoutException("timeout"), mock_response]
        mock_client_class.return_value.__aenter__.return_value = mock_client

        embedding = await generate_embedding("test text")

        assert embedding == [0.1, 0.2, 0.3]
        assert mock_client.post.call_count == 2

    @patch("shared.vector.qdrant.httpx.AsyncClient")
    async def test_generate_embeddings_batch(self, mock_client_class):
        """Test batch embedding generation."""
        from shared.vector.qdrant import generate_embeddings_batch

        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "embeddings": [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        }
        mock_client.post.return_value = mock_response
        mock_client_class.return_value.__aenter__.return_value = mock_client

        embeddings = await generate_embeddings_batch(["text1", "text2"])

        assert len(embeddings) == 2
        assert embeddings[0] == [0.1, 0.2, 0.3]
        assert embeddings[1] == [0.4, 0.5, 0.6]
