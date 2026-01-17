"""Tests for plugin import error handling."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from minibook.plugins import EPUBPlugin, OutputPlugin, PDFPlugin


class TestOutputPluginAbstract:
    """Tests for abstract OutputPlugin base class."""

    def test_output_plugin_requires_implementation(self):
        """Test that OutputPlugin.generate requires implementation in subclasses."""

        # Create a minimal concrete implementation that doesn't override generate
        class IncompletePlugin(OutputPlugin):
            name = "incomplete"
            extension = ".txt"
            description = "Incomplete plugin"
            # Note: deliberately not implementing generate()

        # Attempting to instantiate should raise TypeError because generate() is abstract
        with pytest.raises(TypeError, match="abstract"):
            IncompletePlugin()

    def test_output_plugin_base_class_generate(self):
        """Test calling generate on the base class directly (coverage for pass statement)."""

        # This test ensures the abstract method's pass statement is covered
        # Create a concrete subclass that properly implements the abstract method
        class MinimalPlugin(OutputPlugin):
            name = "minimal"
            extension = ".txt"
            description = "Minimal plugin for testing"

            def generate(self, title, links, subtitle=None, output_file="output", **kwargs):
                # Call the parent's generate method to cover its pass statement
                # This will return None as the base implementation just has 'pass'
                return super().generate(title, links, subtitle, output_file, **kwargs)

        # Instantiate and test
        plugin = MinimalPlugin()
        result = plugin.generate("Title", [("Link", "https://example.com")])
        # The base implementation just has 'pass', so it returns None
        assert result is None


class TestPDFPluginImportError:
    """Tests for PDF plugin import error handling."""

    def test_pdf_plugin_raises_import_error_when_fpdf2_missing(self):
        """Test that PDFPlugin raises ImportError when fpdf2 is not installed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "test.pdf"
            plugin = PDFPlugin()

            # Mock the FPDF variable in the plugins module to simulate missing fpdf2
            with (
                patch("minibook.plugins.FPDF", None),
                pytest.raises(ImportError) as exc_info,
            ):
                plugin.generate(
                    title="Test",
                    links=[("Link", "https://example.com")],
                    output_file=output_file,
                )

            assert "fpdf2" in str(exc_info.value)


class TestEPUBPluginImportError:
    """Tests for EPUB plugin import error handling."""

    def test_epub_plugin_raises_import_error_when_ebooklib_missing(self):
        """Test that EPUBPlugin raises ImportError when ebooklib is not installed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "test.epub"
            plugin = EPUBPlugin()

            # Mock the epub variable in the plugins module to simulate missing ebooklib
            with (
                patch("minibook.plugins.epub", None),
                pytest.raises(ImportError) as exc_info,
            ):
                plugin.generate(
                    title="Test",
                    links=[("Link", "https://example.com")],
                    output_file=output_file,
                )

            assert "ebooklib" in str(exc_info.value)
