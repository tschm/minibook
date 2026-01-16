"""Tests for input validation functions."""

from minibook.main import parse_links_from_json, validate_link_name, validate_url_format


class TestValidateUrlFormat:
    """Tests for validate_url_format function."""

    def test_valid_http_url(self):
        """Test that valid http URLs pass validation."""
        is_valid, error = validate_url_format("http://example.com")
        assert is_valid is True
        assert error is None

    def test_valid_https_url(self):
        """Test that valid https URLs pass validation."""
        is_valid, error = validate_url_format("https://example.com")
        assert is_valid is True
        assert error is None

    def test_valid_url_with_path(self):
        """Test that valid URLs with paths pass validation."""
        is_valid, error = validate_url_format("https://example.com/path/to/page")
        assert is_valid is True
        assert error is None

    def test_valid_url_with_query(self):
        """Test that valid URLs with query strings pass validation."""
        is_valid, error = validate_url_format("https://example.com?foo=bar&baz=qux")
        assert is_valid is True
        assert error is None

    def test_javascript_url_rejected(self):
        """Test that javascript: URLs are rejected."""
        is_valid, error = validate_url_format("javascript:alert(1)")
        assert is_valid is False
        assert "Invalid URL scheme 'javascript'" in error

    def test_data_url_rejected(self):
        """Test that data: URLs are rejected."""
        is_valid, error = validate_url_format("data:text/html,<script>alert(1)</script>")
        assert is_valid is False
        assert "Invalid URL scheme 'data'" in error

    def test_file_url_rejected(self):
        """Test that file: URLs are rejected."""
        is_valid, error = validate_url_format("file:///etc/passwd")
        assert is_valid is False
        assert "Invalid URL scheme 'file'" in error

    def test_empty_string_rejected(self):
        """Test that empty strings are rejected."""
        is_valid, error = validate_url_format("")
        assert is_valid is False
        assert "non-empty string" in error

    def test_whitespace_only_rejected(self):
        """Test that whitespace-only strings are rejected."""
        is_valid, error = validate_url_format("   ")
        assert is_valid is False
        assert "non-empty string" in error

    def test_non_string_rejected(self):
        """Test that non-string values are rejected."""
        is_valid, error = validate_url_format(123)
        assert is_valid is False
        assert "non-empty string" in error

    def test_none_rejected(self):
        """Test that None is rejected."""
        is_valid, error = validate_url_format(None)
        assert is_valid is False
        assert "non-empty string" in error

    def test_url_without_host_rejected(self):
        """Test that URLs without a host are rejected."""
        is_valid, error = validate_url_format("https://")
        assert is_valid is False
        assert "valid host" in error

    def test_no_scheme_rejected(self):
        """Test that URLs without a scheme are rejected."""
        is_valid, error = validate_url_format("example.com")
        assert is_valid is False
        assert "Invalid URL scheme" in error


class TestValidateLinkName:
    """Tests for validate_link_name function."""

    def test_valid_name(self):
        """Test that valid names pass validation."""
        is_valid, error = validate_link_name("My Link")
        assert is_valid is True
        assert error is None

    def test_empty_string_rejected(self):
        """Test that empty strings are rejected."""
        is_valid, error = validate_link_name("")
        assert is_valid is False
        assert "non-empty string" in error

    def test_whitespace_only_rejected(self):
        """Test that whitespace-only strings are rejected."""
        is_valid, error = validate_link_name("   ")
        assert is_valid is False
        assert "non-empty string" in error

    def test_non_string_rejected(self):
        """Test that non-string values are rejected."""
        is_valid, error = validate_link_name(123)
        assert is_valid is False
        assert "non-empty string" in error

    def test_none_rejected(self):
        """Test that None is rejected."""
        is_valid, error = validate_link_name(None)
        assert is_valid is False
        assert "non-empty string" in error


class TestParseLinksValidation:
    """Tests for validation within parse_links_from_json."""

    def test_javascript_url_skipped_with_warning(self):
        """Test that javascript: URLs are skipped with a warning."""
        json_str = '{"XSS": "javascript:alert(1)", "Valid": "https://example.com"}'
        result, warnings = parse_links_from_json(json_str)
        assert result == [("Valid", "https://example.com")]
        assert len(warnings) == 1
        assert "XSS" in warnings[0]
        assert "javascript" in warnings[0]

    def test_data_url_skipped_with_warning(self):
        """Test that data: URLs are skipped with a warning."""
        json_str = '{"Bad": "data:text/html,test", "Good": "https://example.com"}'
        result, warnings = parse_links_from_json(json_str)
        assert result == [("Good", "https://example.com")]
        assert len(warnings) == 1
        assert "data" in warnings[0]

    def test_empty_url_skipped_with_warning(self):
        """Test that empty URLs are skipped with a warning."""
        json_str = '{"Empty": "", "Valid": "https://example.com"}'
        result, warnings = parse_links_from_json(json_str)
        assert result == [("Valid", "https://example.com")]
        assert len(warnings) == 1
        assert "non-empty string" in warnings[0]

    def test_non_string_url_skipped_with_warning(self):
        """Test that non-string URL values are skipped with a warning."""
        json_str = '{"Number": 123, "Valid": "https://example.com"}'
        result, warnings = parse_links_from_json(json_str)
        assert result == [("Valid", "https://example.com")]
        assert len(warnings) == 1

    def test_multiple_invalid_items_all_warned(self):
        """Test that multiple invalid items each generate warnings."""
        json_str = '{"JS": "javascript:x", "Data": "data:x", "Valid": "https://example.com"}'
        result, warnings = parse_links_from_json(json_str)
        assert result == [("Valid", "https://example.com")]
        assert len(warnings) == 2

    def test_all_invalid_returns_empty_list(self):
        """Test that all invalid items returns empty list with warnings."""
        json_str = '{"JS": "javascript:x", "Data": "data:x"}'
        result, warnings = parse_links_from_json(json_str)
        assert result == []
        assert len(warnings) == 2

    def test_list_format_validates_urls(self):
        """Test that list format also validates URLs."""
        json_str = '[["Bad", "javascript:alert(1)"], ["Good", "https://example.com"]]'
        result, warnings = parse_links_from_json(json_str)
        assert result == [("Good", "https://example.com")]
        assert len(warnings) == 1

    def test_dict_list_format_validates_urls(self):
        """Test that dict list format also validates URLs."""
        json_str = '[{"name": "Bad", "url": "javascript:x"}, {"name": "Good", "url": "https://example.com"}]'
        result, warnings = parse_links_from_json(json_str)
        assert result == [("Good", "https://example.com")]
        assert len(warnings) == 1
