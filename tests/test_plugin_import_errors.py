"""Tests for plugin import error handling."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

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
            plugin = IncompletePlugin()
    
    def test_output_plugin_base_class_generate(self):
        """Test calling generate on the base class directly (coverage for pass statement)."""
        # This test ensures the abstract method's pass statement is covered
        # We bypass the abstract method check to call the base implementation
        original_abstractmethods = OutputPlugin.__abstractmethods__
        OutputPlugin.__abstractmethods__ = frozenset()
        
        try:
            # Now we can instantiate the base class
            plugin = OutputPlugin()
            result = plugin.generate("Title", [("Link", "https://example.com")])
            # The base implementation just has 'pass', so it returns None
            assert result is None
        finally:
            # Restore the abstract methods
            OutputPlugin.__abstractmethods__ = original_abstractmethods


class TestPDFPluginImportError:
    """Tests for PDF plugin import error handling."""

    def test_pdf_plugin_raises_import_error_when_fpdf2_missing(self):
        """Test that PDFPlugin raises ImportError when fpdf2 is not installed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "test.pdf"
            plugin = PDFPlugin()
            
            # Mock the import to simulate missing fpdf2
            with patch.dict("sys.modules", {"fpdf": None}):
                with patch("builtins.__import__", side_effect=ImportError("No module named 'fpdf'")):
                    with pytest.raises(ImportError) as exc_info:
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
            
            # Mock the import to simulate missing ebooklib
            with patch.dict("sys.modules", {"ebooklib": None}):
                with patch("builtins.__import__", side_effect=ImportError("No module named 'ebooklib'")):
                    with pytest.raises(ImportError) as exc_info:
                        plugin.generate(
                            title="Test",
                            links=[("Link", "https://example.com")],
                            output_file=output_file,
                        )
                    
                    assert "ebooklib" in str(exc_info.value)
