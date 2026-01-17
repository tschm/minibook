"""URL edge case tests for MiniBook.

This module tests various URL edge cases including:
- Unicode/IDN domains
- IPv6 addresses
- URLs with authentication
- URLs with special characters
- URLs with ports and fragments
"""

import pytest

from minibook.main import validate_url_format


class TestUnicodeDomains:
    """Tests for Unicode/Internationalized Domain Names (IDN)."""

    @pytest.mark.parametrize(
        "url",
        [
            "https://例え.jp/path",  # Japanese IDN
            "https://münchen.de/",  # German umlaut
            "https://россия.рф/",  # Cyrillic
            "https://中国.cn/",  # Chinese
            "https://xn--nxasmq5b.com/",  # Punycode encoded
        ],
    )
    def test_unicode_domains_accepted(self, url):
        """Test that Unicode/IDN domains are accepted."""
        is_valid, error = validate_url_format(url)
        assert is_valid, f"URL '{url}' should be valid, got error: {error}"

    def test_mixed_unicode_ascii_domain(self):
        """Test domains with mixed Unicode and ASCII."""
        url = "https://example.中国/path"
        is_valid, _ = validate_url_format(url)
        assert is_valid


class TestIPv6URLs:
    """Tests for IPv6 URL handling."""

    @pytest.mark.parametrize(
        "url",
        [
            "http://[::1]/",  # Localhost
            "http://[2001:db8::1]/path",  # Standard IPv6
            "http://[2001:db8:85a3::8a2e:370:7334]/",  # Full IPv6
            "http://[::ffff:192.168.1.1]/",  # IPv4-mapped IPv6
            "https://[2001:db8::1]:8080/path",  # IPv6 with port
        ],
    )
    def test_ipv6_urls_accepted(self, url):
        """Test that IPv6 URLs are accepted."""
        is_valid, error = validate_url_format(url)
        assert is_valid, f"IPv6 URL '{url}' should be valid, got error: {error}"


class TestURLsWithAuthentication:
    """Tests for URLs containing authentication credentials."""

    @pytest.mark.parametrize(
        "url",
        [
            "https://user@example.com/",
            "https://user:pass@example.com/",
            "https://user:pass@example.com:8080/path",
            "https://user%40domain:pass@example.com/",  # Encoded @
        ],
    )
    def test_urls_with_auth_accepted(self, url):
        """Test that URLs with authentication are accepted."""
        is_valid, error = validate_url_format(url)
        assert is_valid, f"URL with auth '{url}' should be valid, got error: {error}"


class TestURLsWithPorts:
    """Tests for URLs with various port specifications."""

    @pytest.mark.parametrize(
        "url",
        [
            "http://example.com:80/",
            "https://example.com:443/",
            "http://example.com:8080/path",
            "https://example.com:3000/api/v1",
            "http://localhost:5000/",
            "http://127.0.0.1:8000/",
        ],
    )
    def test_urls_with_ports_accepted(self, url):
        """Test that URLs with explicit ports are accepted."""
        is_valid, error = validate_url_format(url)
        assert is_valid, f"URL with port '{url}' should be valid, got error: {error}"


class TestURLsWithFragments:
    """Tests for URLs with fragment identifiers."""

    @pytest.mark.parametrize(
        "url",
        [
            "https://example.com/#section",
            "https://example.com/page#anchor",
            "https://example.com/page?query=1#section",
            "https://example.com/#",  # Empty fragment
            "https://example.com/page#section-1.2",
        ],
    )
    def test_urls_with_fragments_accepted(self, url):
        """Test that URLs with fragments are accepted."""
        is_valid, error = validate_url_format(url)
        assert is_valid, f"URL with fragment '{url}' should be valid, got error: {error}"


class TestURLsWithQueryStrings:
    """Tests for URLs with query strings."""

    @pytest.mark.parametrize(
        "url",
        [
            "https://example.com/?",
            "https://example.com/?q=search",
            "https://example.com/?q=search&page=1",
            "https://example.com/path?key=value&other=123",
            "https://example.com/?q=hello%20world",  # URL encoded
            "https://example.com/?arr[]=1&arr[]=2",  # Array notation
        ],
    )
    def test_urls_with_query_strings_accepted(self, url):
        """Test that URLs with query strings are accepted."""
        is_valid, error = validate_url_format(url)
        assert is_valid, f"URL with query '{url}' should be valid, got error: {error}"


class TestURLsWithSpecialCharacters:
    """Tests for URLs with special characters in paths."""

    @pytest.mark.parametrize(
        "url",
        [
            "https://example.com/path%20with%20spaces",
            "https://example.com/path/to/file.html",
            "https://example.com/path-with-dashes",
            "https://example.com/path_with_underscores",
            "https://example.com/path~tilde",
            "https://example.com/path.multiple.dots.html",
            "https://example.com/path/with/trailing/slash/",
        ],
    )
    def test_urls_with_special_chars_accepted(self, url):
        """Test that URLs with special characters are accepted."""
        is_valid, error = validate_url_format(url)
        assert is_valid, f"URL with special chars '{url}' should be valid, got error: {error}"


class TestMalformedURLs:
    """Tests for malformed URLs that should be rejected."""

    @pytest.mark.parametrize(
        ("url", "expected_error_part"),
        [
            ("https://", "valid host"),  # No host
            ("http://", "valid host"),  # No host
            ("://example.com", "scheme"),  # No scheme
            ("example.com", "scheme"),  # No scheme
            ("ftp://example.com", "scheme"),  # Wrong scheme
            ("mailto:user@example.com", "scheme"),  # mailto not allowed
            ("tel:+1234567890", "scheme"),  # tel not allowed
        ],
    )
    def test_malformed_urls_rejected(self, url, expected_error_part):
        """Test that malformed URLs are rejected with appropriate errors."""
        is_valid, error = validate_url_format(url)
        assert is_valid is False, f"Malformed URL '{url}' should be invalid"
        assert expected_error_part.lower() in error.lower(), (
            f"Error for '{url}' should mention '{expected_error_part}', got: {error}"
        )


class TestEdgeCaseURLs:
    """Tests for edge case URLs."""

    def test_very_long_url(self):
        """Test handling of very long URLs."""
        long_path = "a" * 2000
        url = f"https://example.com/{long_path}"
        is_valid, error = validate_url_format(url)
        assert is_valid, f"Long URL should be valid, got error: {error}"

    def test_url_with_all_components(self):
        """Test URL with all possible components."""
        url = "https://user:pass@example.com:8080/path/to/resource?query=1&other=2#section"
        is_valid, error = validate_url_format(url)
        assert is_valid, f"Full URL should be valid, got error: {error}"

    def test_localhost_urls(self):
        """Test localhost URLs."""
        urls = [
            "http://localhost/",
            "http://localhost:3000/",
            "https://localhost/path",
            "http://127.0.0.1/",
            "http://127.0.0.1:8080/api",
        ]
        for url in urls:
            is_valid, error = validate_url_format(url)
            assert is_valid, f"Localhost URL '{url}' should be valid, got error: {error}"

    def test_url_with_empty_path(self):
        """Test URLs with empty path."""
        url = "https://example.com"
        is_valid, error = validate_url_format(url)
        assert is_valid, f"URL without path should be valid, got error: {error}"

    def test_url_case_sensitivity(self):
        """Test that URL scheme is case-insensitive."""
        urls = [
            "HTTP://example.com/",
            "HTTPS://example.com/",
            "HtTpS://example.com/",
        ]
        for url in urls:
            is_valid, error = validate_url_format(url)
            assert is_valid, f"URL '{url}' should be valid regardless of scheme case, got error: {error}"
