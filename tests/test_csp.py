"""Tests for Content Security Policy (CSP) functionality."""

import re
import tempfile
from pathlib import Path

from minibook.main import generate_html


def test_csp_meta_tag_present():
    """Test that the CSP meta tag is present in generated HTML."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "index.html"
        generate_html("Test Title", [("Link", "https://example.com")], output_file=output_file)

        content = output_file.read_text()
        assert 'http-equiv="Content-Security-Policy"' in content


def test_nonce_is_generated():
    """Test that a nonce is generated and included in the HTML."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "index.html"
        generate_html("Test Title", [("Link", "https://example.com")], output_file=output_file)

        content = output_file.read_text()

        # Check that nonce appears in CSP header
        assert "'nonce-" in content

        # Extract nonce value from CSP
        nonce_match = re.search(r"'nonce-([A-Za-z0-9_-]+)'", content)
        assert nonce_match is not None
        nonce = nonce_match.group(1)

        # Check that nonce is applied to script tags
        assert f'<script nonce="{nonce}">' in content

        # Check that nonce is applied to style tag
        assert f'<style nonce="{nonce}">' in content


def test_nonce_is_unique_per_render():
    """Test that each render generates a unique nonce."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file1 = Path(tmpdir) / "index1.html"
        output_file2 = Path(tmpdir) / "index2.html"

        generate_html("Test Title", [("Link", "https://example.com")], output_file=output_file1)
        generate_html("Test Title", [("Link", "https://example.com")], output_file=output_file2)

        content1 = output_file1.read_text()
        content2 = output_file2.read_text()

        # Extract nonces
        nonce1_match = re.search(r"'nonce-([A-Za-z0-9_-]+)'", content1)
        nonce2_match = re.search(r"'nonce-([A-Za-z0-9_-]+)'", content2)

        assert nonce1_match is not None
        assert nonce2_match is not None

        # Nonces should be different
        assert nonce1_match.group(1) != nonce2_match.group(1)


def test_no_inline_onclick_handler():
    """Test that inline onclick handlers are not used (CSP compliance)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "index.html"
        generate_html("Test Title", [("Link", "https://example.com")], output_file=output_file)

        content = output_file.read_text()

        # There should be no onclick attributes
        assert "onclick=" not in content


def test_theme_toggle_button_has_id():
    """Test that the theme toggle button has an id for event listener attachment."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "index.html"
        generate_html("Test Title", [("Link", "https://example.com")], output_file=output_file)

        content = output_file.read_text()

        # Button should have id for event listener
        assert 'id="theme-toggle-btn"' in content


def test_csp_allows_tailwind_cdn():
    """Test that CSP allows Tailwind CSS from CDN."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "index.html"
        generate_html("Test Title", [("Link", "https://example.com")], output_file=output_file)

        content = output_file.read_text()

        # CSP should allow Tailwind CDN
        assert "https://cdn.tailwindcss.com" in content


def test_csp_allows_google_fonts():
    """Test that CSP allows Google Fonts."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "index.html"
        generate_html("Test Title", [("Link", "https://example.com")], output_file=output_file)

        content = output_file.read_text()

        # CSP should allow Google Fonts for styles
        assert "https://fonts.googleapis.com" in content
        # CSP should allow gstatic for font files
        assert "https://fonts.gstatic.com" in content


def test_bare_template_has_csp():
    """Test that the bare template also has CSP."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "index.html"
        template_path = Path(__file__).parent.parent / "src" / "minibook" / "templates" / "bare.j2"

        generate_html(
            "Test Title", [("Link", "https://example.com")], output_file=output_file, template_path=str(template_path)
        )

        content = output_file.read_text()
        assert 'http-equiv="Content-Security-Policy"' in content
        assert "'nonce-" in content
