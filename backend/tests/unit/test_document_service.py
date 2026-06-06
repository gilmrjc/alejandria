"""Unit tests for document business logic."""

from shared.schemas.document import generate_slug, sanitize_markdown


class TestSlugGeneration:
    """Test slug generation business logic."""

    def test_slug_basic(self):
        """Test basic slug generation from title."""
        title = "My Document Title"
        slug = generate_slug(title)
        assert slug == "my-document-title"

    def test_slug_with_special_chars(self):
        """Test slug generation with special characters."""
        title = "My Document! @#$%"
        slug = generate_slug(title)
        assert slug == "my-document"

    def test_slug_with_accents(self):
        """Test slug generation removes accents."""
        title = "Mi Documento Español"
        slug = generate_slug(title)
        assert slug == "mi-documento-espanol"

    def test_slug_with_umlauts(self):
        """Test slug generation removes umlauts."""
        title = "Dokument über Änderungen"
        slug = generate_slug(title)
        assert slug == "dokument-uber-anderungen"

    def test_slug_long_title_truncated(self):
        """Test slug is truncated to max 100 characters."""
        title = "A" * 150
        slug = generate_slug(title)
        assert len(slug) == 100
        assert slug == "a" * 100

    def test_slug_empty_title(self):
        """Test slug generation with empty title."""
        title = ""
        slug = generate_slug(title)
        assert slug == "untitled"

    def test_slug_consecutive_hyphens_removed(self):
        """Test consecutive hyphens are removed."""
        title = "My  Document   Title"
        slug = generate_slug(title)
        assert slug == "my-document-title"

    def test_slug_leading_trailing_hyphens_removed(self):
        """Test leading and trailing hyphens are removed."""
        title = "  My Document Title  "
        slug = generate_slug(title)
        assert slug == "my-document-title"

    def test_slug_with_numbers(self):
        """Test slug generation with numbers."""
        title = "Document 123 Version 2.0"
        slug = generate_slug(title)
        assert slug == "document-123-version-2-0"


class TestMarkdownSanitization:
    """Test markdown sanitization business logic."""

    def test_sanitize_basic_markdown(self):
        """Test basic markdown is passed through (Bleach only sanitizes HTML)."""
        content = "# Title\n\n**Bold** and *italic* text."
        sanitized = sanitize_markdown(content)
        # Bleach doesn't convert markdown, only sanitizes existing HTML
        assert sanitized == content

    def test_sanitize_removes_script_tags(self):
        """Test script tags are removed (Bleach strips tags but keeps content)."""
        content = "<script>alert('xss')</script>Content"
        sanitized = sanitize_markdown(content)
        assert "<script>" not in sanitized
        assert "</script>" not in sanitized
        # Bleach strips the tags but keeps the text content
        assert "Content" in sanitized

    def test_sanitize_removes_onclick_attributes(self):
        """Test onclick attributes are removed."""
        content = '<a href="#" onclick="alert(1)">Click</a>'
        sanitized = sanitize_markdown(content)
        assert "onclick" not in sanitized
        assert '<a href="#">Click</a>' in sanitized

    def test_sanitize_allows_safe_html(self):
        """Test safe HTML tags are preserved."""
        content = "<p>Paragraph</p><ul><li>Item</li></ul>"
        sanitized = sanitize_markdown(content)
        assert "<p>Paragraph</p>" in sanitized
        assert "<ul>" in sanitized
        assert "<li>Item</li>" in sanitized

    def test_sanitize_allows_code_blocks(self):
        """Test code blocks are preserved."""
        content = "<pre><code class=\"python\">print('hello')</code></pre>"
        sanitized = sanitize_markdown(content)
        assert "<pre>" in sanitized
        assert '<code class="python">' in sanitized
        assert "print('hello')" in sanitized

    def test_sanitize_allows_http_https_links(self):
        """Test http and https links are preserved."""
        content = '<a href="https://example.com">Link</a>'
        sanitized = sanitize_markdown(content)
        assert '<a href="https://example.com">Link</a>' in sanitized

    def test_sanitize_removes_javascript_links(self):
        """Test javascript protocol links are removed."""
        content = '<a href="javascript:alert(1)">Link</a>'
        sanitized = sanitize_markdown(content)
        assert "javascript:" not in sanitized

    def test_sanitize_allows_blockquotes(self):
        """Test blockquotes are preserved."""
        content = "<blockquote>Quote</blockquote>"
        sanitized = sanitize_markdown(content)
        assert "<blockquote>Quote</blockquote>" in sanitized

    def test_sanitize_allows_headings(self):
        """Test heading tags are preserved."""
        content = "<h1>H1</h1><h2>H2</h2><h3>H3</h3>"
        sanitized = sanitize_markdown(content)
        assert "<h1>H1</h1>" in sanitized
        assert "<h2>H2</h2>" in sanitized
        assert "<h3>H3</h3>" in sanitized
