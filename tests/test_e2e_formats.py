"""End-to-end tests for all MiniBook output formats.

This module tests the CLI with all supported output formats to ensure
they work correctly in an end-to-end scenario.
"""

import json
import subprocess
import sys
from pathlib import Path

# Test data used across all format tests
TEST_LINKS = [
    ("Python", "https://www.python.org"),
    ("GitHub", "https://www.github.com"),
    ("Wikipedia", "https://www.wikipedia.org"),
]

TEST_LINKS_JSON = json.dumps({name: url for name, url in TEST_LINKS})
TEST_TITLE = "E2E Format Test"
TEST_SUBTITLE = "Testing all output formats"


def _run_minibook_cli(tmp_path: Path, format_name: str, extra_args: list | None = None) -> subprocess.CompletedProcess:
    """Run the minibook CLI with the given format.

    Args:
        tmp_path: Temporary directory for output
        format_name: Output format (html, markdown, json, pdf, rst, epub, asciidoc)
        extra_args: Additional CLI arguments

    Returns:
        CompletedProcess with the result
    """
    cmd = [
        sys.executable,
        "-m",
        "minibook.main",
        "--title",
        TEST_TITLE,
        "--subtitle",
        TEST_SUBTITLE,
        "--output",
        str(tmp_path),
        "--links",
        TEST_LINKS_JSON,
        "--format",
        format_name,
    ]

    if extra_args:
        cmd.extend(extra_args)

    # Set up environment with PYTHONPATH
    import os

    env = os.environ.copy()
    src_path = str((Path(__file__).parent.parent / "src").resolve())
    env["PYTHONPATH"] = src_path + os.pathsep + env.get("PYTHONPATH", "")

    return subprocess.run(cmd, capture_output=True, text=True, env=env)


class TestHTMLFormat:
    """E2E tests for HTML output format."""

    def test_html_generation(self, tmp_path):
        """Test HTML format generation via CLI."""
        result = _run_minibook_cli(tmp_path, "html")

        assert result.returncode == 0, f"HTML generation failed: {result.stderr}"

        html_file = tmp_path / "index.html"
        assert html_file.exists(), "HTML file was not created"

        content = html_file.read_text()
        assert TEST_TITLE in content
        assert TEST_SUBTITLE in content
        assert "https://www.python.org" in content
        assert "https://www.github.com" in content
        # Check for CSP nonce
        assert "nonce=" in content


class TestMarkdownFormat:
    """E2E tests for Markdown output format."""

    def test_markdown_generation(self, tmp_path):
        """Test Markdown format generation via CLI."""
        result = _run_minibook_cli(tmp_path, "markdown")

        assert result.returncode == 0, f"Markdown generation failed: {result.stderr}"

        md_file = tmp_path / "links.md"
        assert md_file.exists(), "Markdown file was not created"

        content = md_file.read_text()
        assert f"# {TEST_TITLE}" in content
        assert TEST_SUBTITLE in content
        assert "[Python](https://www.python.org)" in content
        assert "[GitHub](https://www.github.com)" in content

    def test_markdown_alias_md(self, tmp_path):
        """Test 'md' alias for markdown format."""
        result = _run_minibook_cli(tmp_path, "md")

        assert result.returncode == 0, f"MD alias generation failed: {result.stderr}"
        assert (tmp_path / "links.md").exists()


class TestJSONFormat:
    """E2E tests for JSON output format."""

    def test_json_generation(self, tmp_path):
        """Test JSON format generation via CLI."""
        result = _run_minibook_cli(tmp_path, "json")

        assert result.returncode == 0, f"JSON generation failed: {result.stderr}"

        json_file = tmp_path / "links.json"
        assert json_file.exists(), "JSON file was not created"

        content = json.loads(json_file.read_text())
        assert content["title"] == TEST_TITLE
        assert content["description"] == TEST_SUBTITLE
        assert len(content["links"]) == 3
        assert content["links"][0]["name"] == "Python"
        assert content["links"][0]["url"] == "https://www.python.org"
        assert "metadata" in content
        assert content["metadata"]["generated_by"] == "MiniBook"


class TestRSTFormat:
    """E2E tests for reStructuredText output format."""

    def test_rst_generation(self, tmp_path):
        """Test RST format generation via CLI."""
        result = _run_minibook_cli(tmp_path, "rst")

        assert result.returncode == 0, f"RST generation failed: {result.stderr}"

        rst_file = tmp_path / "output.rst"
        assert rst_file.exists(), "RST file was not created"

        content = rst_file.read_text()
        assert TEST_TITLE in content
        assert TEST_SUBTITLE in content
        # RST link format
        assert "`Python <https://www.python.org>`_" in content

    def test_rst_alias_restructuredtext(self, tmp_path):
        """Test 'restructuredtext' alias for RST format."""
        result = _run_minibook_cli(tmp_path, "restructuredtext")

        assert result.returncode == 0, f"RST alias generation failed: {result.stderr}"
        assert (tmp_path / "output.rst").exists()


class TestAsciiDocFormat:
    """E2E tests for AsciiDoc output format."""

    def test_asciidoc_generation(self, tmp_path):
        """Test AsciiDoc format generation via CLI."""
        result = _run_minibook_cli(tmp_path, "asciidoc")

        assert result.returncode == 0, f"AsciiDoc generation failed: {result.stderr}"

        adoc_file = tmp_path / "output.adoc"
        assert adoc_file.exists(), "AsciiDoc file was not created"

        content = adoc_file.read_text()
        assert f"= {TEST_TITLE}" in content
        assert TEST_SUBTITLE in content
        # AsciiDoc link format
        assert "link:https://www.python.org[Python]" in content

    def test_asciidoc_alias_adoc(self, tmp_path):
        """Test 'adoc' alias for AsciiDoc format."""
        result = _run_minibook_cli(tmp_path, "adoc")

        assert result.returncode == 0, f"Adoc alias generation failed: {result.stderr}"
        assert (tmp_path / "output.adoc").exists()


class TestPDFFormat:
    """E2E tests for PDF output format."""

    def test_pdf_generation(self, tmp_path):
        """Test PDF format generation via CLI."""
        result = _run_minibook_cli(tmp_path, "pdf")

        assert result.returncode == 0, f"PDF generation failed: {result.stderr}"

        pdf_file = tmp_path / "links.pdf"
        assert pdf_file.exists(), "PDF file was not created"

        # PDF files start with %PDF
        content = pdf_file.read_bytes()
        assert content.startswith(b"%PDF"), "Invalid PDF file format"


class TestEPUBFormat:
    """E2E tests for EPUB output format."""

    def test_epub_generation(self, tmp_path):
        """Test EPUB format generation via CLI."""
        result = _run_minibook_cli(tmp_path, "epub")

        assert result.returncode == 0, f"EPUB generation failed: {result.stderr}"

        epub_file = tmp_path / "output.epub"
        assert epub_file.exists(), "EPUB file was not created"

        # EPUB files are ZIP archives starting with PK
        content = epub_file.read_bytes()
        assert content.startswith(b"PK"), "Invalid EPUB file format (not a ZIP archive)"


class TestAllFormatsSequentially:
    """Test all formats in sequence to ensure they don't interfere with each other."""

    def test_generate_all_formats(self, tmp_path):
        """Generate all formats in sequence and verify each output."""
        formats_and_files = [
            ("html", "index.html"),
            ("markdown", "links.md"),
            ("json", "links.json"),
            ("rst", "output.rst"),
            ("asciidoc", "output.adoc"),
            ("pdf", "links.pdf"),
            ("epub", "output.epub"),
        ]

        results = {}
        for format_name, expected_file in formats_and_files:
            # Create a subdirectory for each format
            format_dir = tmp_path / format_name
            format_dir.mkdir()

            result = _run_minibook_cli(format_dir, format_name)
            results[format_name] = {
                "returncode": result.returncode,
                "stderr": result.stderr,
                "file_exists": (format_dir / expected_file).exists(),
            }

        # Assert all formats succeeded
        for format_name, result in results.items():
            assert result["returncode"] == 0, f"{format_name} failed: {result['stderr']}"
            assert result["file_exists"], f"{format_name} output file not created"


class TestInvalidFormat:
    """Test error handling for invalid format."""

    def test_invalid_format_rejected(self, tmp_path):
        """Test that invalid format names are rejected with helpful error."""
        result = _run_minibook_cli(tmp_path, "invalid_format")

        # Error message should mention the invalid format and available formats
        assert "invalid_format" in result.stderr
        assert "Unknown output format" in result.stderr
        # Should list available formats
        assert "html" in result.stderr
        assert "markdown" in result.stderr
        assert "json" in result.stderr
        assert "pdf" in result.stderr
