"""Tests for error handling in main module."""

from unittest.mock import patch

from typer.testing import CliRunner

from minibook.main import app, parse_links_from_json, validate_url_format


class TestValidateUrlFormatExceptionHandling:
    """Tests for exception handling in validate_url_format."""

    def test_exception_handling_in_urlparse(self):
        """Test that exceptions in urlparse are caught and handled."""
        # Test with a malformed URL that might cause an exception
        # While urlparse is quite forgiving, we test the exception branch exists
        with patch("minibook.main.urlparse") as mock_urlparse:
            mock_urlparse.side_effect = Exception("Unexpected error")
            is_valid, error = validate_url_format("http://example.com")
            assert is_valid is False
            assert "Invalid URL" in error
            assert "Unexpected error" in error


class TestParseLinksWarnings:
    """Tests for warning display in parse_links_from_json."""

    def test_parse_warnings_are_collected(self):
        """Test that warnings are collected for invalid items."""
        json_str = '{"Bad": "javascript:alert(1)", "Empty": "", "Good": "https://example.com"}'
        links, warnings = parse_links_from_json(json_str)

        # Should have two warnings (one for javascript URL, one for empty URL)
        assert len(warnings) >= 2
        assert any("Bad" in w for w in warnings)
        assert len(links) == 1  # Only the good link should remain


class TestEmptyLinkList:
    """Tests for handling empty link lists."""

    def test_all_invalid_links_returns_empty_list(self):
        """Test that all invalid links result in empty list."""
        json_str = '{"JS": "javascript:void(0)", "File": "file:///etc/passwd"}'
        links, warnings = parse_links_from_json(json_str)

        assert len(links) == 0  # No valid links
        assert len(warnings) == 2  # Two warnings


class TestMainCLIErrorHandling:
    """Tests for CLI error handling."""

    def test_cli_with_warnings_displayed(self):
        """Test that CLI displays warnings for skipped items."""
        runner = CliRunner()
        result = runner.invoke(
            app,
            [
                "--links",
                '{"Bad": "javascript:alert(1)", "Good": "https://example.com"}',
                "--title",
                "Test",
            ],
        )

        # Should display warning in output (warnings go to stderr, use .output for combined)
        assert "Warning" in result.output or "warning" in result.output.lower()

    def test_cli_with_all_invalid_links(self):
        """Test that CLI handles all invalid links gracefully."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(
                app,
                [
                    "--links",
                    '{"Bad1": "javascript:alert(1)", "Bad2": "file:///etc/passwd"}',
                    "--title",
                    "Test",
                    "--output",
                    "output",
                ],
            )

            # Should display error message for no valid links
            assert "No valid links" in result.output or "Error" in result.output
            # Check warnings were displayed
            assert "Warning" in result.output or "Skipping" in result.output

    def test_cli_with_invalid_format(self):
        """Test that CLI handles invalid output format."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(
                app,
                [
                    "--links",
                    '{"Link": "https://example.com"}',
                    "--format",
                    "invalid_format",
                    "--title",
                    "Test",
                    "--output",
                    "output",
                ],
            )

            # Should display error for invalid format
            assert "Error" in result.output or "Unknown output format" in result.output

    def test_cli_with_pdf_missing_dependency(self):
        """Test that CLI handles missing PDF dependency gracefully."""
        runner = CliRunner()

        # Mock the plugin to raise ImportError
        with patch("minibook.plugins.PDFPlugin.generate") as mock_generate:
            mock_generate.side_effect = ImportError("PDF generation requires fpdf2")

            with runner.isolated_filesystem():
                result = runner.invoke(
                    app,
                    [
                        "--links",
                        '{"Link": "https://example.com"}',
                        "--format",
                        "pdf",
                        "--title",
                        "Test",
                        "--output",
                        "output",
                    ],
                )

                # Should display error message
                assert "Error" in result.output or "fpdf2" in result.output

    def test_cli_with_file_not_found(self):
        """Test that CLI handles FileNotFoundError gracefully."""
        runner = CliRunner()

        # Mock the plugin to raise FileNotFoundError
        with patch("minibook.plugins.HTMLPlugin.generate") as mock_generate:
            mock_generate.side_effect = FileNotFoundError("Custom template not found")

            with runner.isolated_filesystem():
                result = runner.invoke(
                    app,
                    [
                        "--links",
                        '{"Link": "https://example.com"}',
                        "--title",
                        "Test",
                        "--output",
                        "output",
                    ],
                )

                # Should display error message
                assert "Error" in result.output or "not found" in result.output
