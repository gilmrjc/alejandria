"""Unit tests for GapGroupingService."""

from shared.services.gap_grouping_service import GapGroupingService


def test_extract_keywords():
    """Test keyword extraction."""
    service = GapGroupingService(session=None)
    text = "How does the authentication system work with JWT tokens?"
    keywords = service._extract_keywords(text)
    assert "authentication" in keywords
    assert "system" in keywords
    # "tokens?" includes punctuation, so check for the word with punctuation
    assert any("tokens" in kw for kw in keywords)
    assert "does" not in keywords  # Common word removed
    assert "with" not in keywords  # Common word removed


def test_extract_keywords_empty():
    """Test keyword extraction with empty text."""
    service = GapGroupingService(session=None)
    keywords = service._extract_keywords("")
    assert keywords == []


def test_extract_keywords_short_words():
    """Test that short words are filtered out."""
    service = GapGroupingService(session=None)
    text = "API and DB"
    keywords = service._extract_keywords(text)
    assert len(keywords) == 0  # All words too short
