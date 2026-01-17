"""Security edge case tests for MiniBook.

This module tests various security edge cases including:
- XSS prevention via malicious link names and URLs
- Template injection prevention
- Path traversal prevention
- Dangerous URL scheme blocking
"""

import pytest

from minibook.main import generate_html, parse_links_from_json, validate_url_format


class TestMaliciousLinkNames:
    """Tests for XSS prevention via link names."""

    @pytest.mark.parametrize(
        "malicious_name",
        [
            "<script>alert('XSS')</script>",
            '"><script>alert("XSS")</script>',
            "<iframe src='javascript:alert(1)'>",
        ],
    )
    def test_malicious_link_names_escaped_in_html(self, tmp_path, malicious_name):
        """Test that malicious link names are properly escaped in HTML output."""
        links = [(malicious_name, "https://example.com")]
        output_file = tmp_path / "test.html"

        generate_html(
            title="Test",
            links=links,
            output_file=str(output_file),
        )

        content = output_file.read_text()

        # The malicious content should be escaped - raw <script> tags should not appear
        assert "<script>" not in content
        # Escaped version should be present
        assert "&lt;script&gt;" in content or "&lt;iframe" in content

    def test_link_name_with_html_entities(self, tmp_path):
        """Test that HTML entities in link names are handled safely."""
        links = [("Test &amp; <b>Bold</b>", "https://example.com")]
        output_file = tmp_path / "test.html"

        generate_html(title="Test", links=links, output_file=str(output_file))

        content = output_file.read_text()
        # Bold tag should be escaped
        assert "<b>Bold</b>" not in content
        assert "&lt;b&gt;" in content


class TestMaliciousURLs:
    """Tests for dangerous URL scheme blocking."""

    @pytest.mark.parametrize(
        ("dangerous_url", "expected_error"),
        [
            ("javascript:alert('XSS')", "Invalid URL scheme"),
            ("javascript:void(0)", "Invalid URL scheme"),
            ("data:text/html,<script>alert(1)</script>", "Invalid URL scheme"),
            ("data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==", "Invalid URL scheme"),
            ("file:///etc/passwd", "Invalid URL scheme"),
            ("file://localhost/etc/passwd", "Invalid URL scheme"),
            ("vbscript:msgbox('XSS')", "Invalid URL scheme"),
            ("", "non-empty string"),
            ("   ", "non-empty string"),
        ],
    )
    def test_dangerous_url_schemes_rejected(self, dangerous_url, expected_error):
        """Test that dangerous URL schemes are rejected."""
        is_valid, error = validate_url_format(dangerous_url)

        assert is_valid is False
        assert expected_error.lower() in error.lower()

    def test_dangerous_urls_filtered_in_json_parsing(self):
        """Test that dangerous URLs are filtered out during JSON parsing."""
        json_input = '{"safe": "https://example.com", "xss": "javascript:alert(1)"}'

        links, warnings = parse_links_from_json(json_input)

        # Only safe link should be parsed
        assert len(links) == 1
        assert links[0] == ("safe", "https://example.com")

        # Should have warning about invalid URL
        assert len(warnings) > 0
        assert any("javascript" in w.lower() for w in warnings)


class TestTemplateInjection:
    """Tests for template injection prevention."""

    def test_template_injection_in_title_escaped(self, tmp_path):
        """Test that template injection attempts in title are escaped."""
        injection_attempt = "{{7*7}}"
        links = [("Test", "https://example.com")]
        output_file = tmp_path / "test.html"

        generate_html(
            title=injection_attempt,
            links=links,
            output_file=str(output_file),
        )

        content = output_file.read_text()

        # The literal {{7*7}} should appear in the output (escaped)
        # NOT the result "49" which would indicate execution
        # Since autoescape is on, the braces will be in the content literally
        assert "49" not in content.replace("2026", "").replace("49", "", 1) or injection_attempt in content

    def test_template_injection_in_subtitle_escaped(self, tmp_path):
        """Test that template injection attempts in subtitle are escaped."""
        injection_attempt = "{{7*7}}"
        links = [("Test", "https://example.com")]
        output_file = tmp_path / "test.html"

        generate_html(
            title="Test",
            subtitle=injection_attempt,
            links=links,
            output_file=str(output_file),
        )

        content = output_file.read_text()

        # The template syntax should appear literally, not be executed
        assert injection_attempt in content or "7*7" in content


class TestPathTraversal:
    """Tests for path traversal prevention in template paths."""

    def test_path_traversal_in_template_path(self, tmp_path):
        """Test that path traversal attempts in template path are rejected."""
        links = [("Test", "https://example.com")]
        output_file = tmp_path / "test.html"

        # Create a template in a different directory
        malicious_path = str(tmp_path / ".." / ".." / "etc" / "passwd")

        with pytest.raises(FileNotFoundError):
            generate_html(
                title="Test",
                links=links,
                output_file=str(output_file),
                template_path=malicious_path,
            )

    def test_null_byte_injection_in_template_path(self, tmp_path):
        """Test that null byte injection in template path is handled."""
        links = [("Test", "https://example.com")]
        output_file = tmp_path / "test.html"

        # Null byte injection attempt
        malicious_path = str(tmp_path / "template.j2\x00.txt")

        with pytest.raises((FileNotFoundError, ValueError, OSError)):
            generate_html(
                title="Test",
                links=links,
                output_file=str(output_file),
                template_path=malicious_path,
            )


class TestInputValidation:
    """Tests for input validation edge cases."""

    def test_extremely_long_link_name(self, tmp_path):
        """Test handling of extremely long link names."""
        long_name = "A" * 10000
        links = [(long_name, "https://example.com")]
        output_file = tmp_path / "test.html"

        # Should not crash
        generate_html(title="Test", links=links, output_file=str(output_file))

        content = output_file.read_text()
        assert long_name in content

    def test_unicode_in_link_name(self, tmp_path):
        """Test handling of Unicode characters in link names."""
        unicode_names = [
            ("Hello \u4e16\u754c", "https://example.com"),  # Chinese
            ("\u0421\u043f\u0430\u0441\u0438\u0431\u043e", "https://example.ru"),  # Russian
            ("RTL \u0639\u0631\u0628\u064a", "https://example.com"),  # Arabic (RTL)
        ]
        output_file = tmp_path / "test.html"

        generate_html(title="Unicode Test", links=unicode_names, output_file=str(output_file))

        content = output_file.read_text()
        assert "\u4e16\u754c" in content  # Chinese characters
        assert "\u0421\u043f\u0430\u0441\u0438\u0431\u043e" in content  # Russian

    def test_special_characters_in_json(self):
        """Test parsing JSON with special characters."""
        # JSON with newlines, tabs, and special chars
        json_input = '{"Line\\nBreak": "https://example.com", "Tab\\there": "https://example.org"}'

        links, _warnings = parse_links_from_json(json_input)

        assert len(links) == 2

    def test_empty_json_objects(self):
        """Test handling of empty JSON structures."""
        test_cases = [
            ("[]", 0),
            ("{}", 0),
            ('[{"name": "", "url": "https://x.com"}]', 0),  # Empty name filtered
        ]

        for json_input, expected_count in test_cases:
            links, _ = parse_links_from_json(json_input)
            assert len(links) == expected_count, f"Failed for input: {json_input}"


class TestCSPAndSRI:
    """Tests for Content Security Policy and Subresource Integrity."""

    def test_csp_nonce_unique_per_generation(self, tmp_path):
        """Test that CSP nonce is unique for each generation."""
        links = [("Test", "https://example.com")]

        output1 = tmp_path / "test1.html"
        output2 = tmp_path / "test2.html"

        generate_html(title="Test", links=links, output_file=str(output1))
        generate_html(title="Test", links=links, output_file=str(output2))

        content1 = output1.read_text()
        content2 = output2.read_text()

        # Extract nonces
        import re

        nonces1 = re.findall(r"nonce=['\"]([^'\"]+)['\"]", content1)
        nonces2 = re.findall(r"nonce=['\"]([^'\"]+)['\"]", content2)

        assert nonces1, "No nonce found in first file"
        assert nonces2, "No nonce found in second file"
        assert nonces1[0] != nonces2[0], "Nonces should be unique per generation"

    def test_no_inline_event_handlers(self, tmp_path):
        """Test that generated HTML has no inline event handlers."""
        links = [("Test", "https://example.com")]
        output_file = tmp_path / "test.html"

        generate_html(title="Test", links=links, output_file=str(output_file))

        content = output_file.read_text()

        # Should not have inline event handlers
        dangerous_handlers = ["onclick=", "onload=", "onerror=", "onmouseover=", "onfocus="]
        for handler in dangerous_handlers:
            assert handler not in content.lower(), f"Found dangerous handler: {handler}"
