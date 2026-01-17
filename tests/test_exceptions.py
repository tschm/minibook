"""Tests for exception classes and error handling."""

from minibook.exceptions import (
    JSONParseError,
    LinkNameValidationError,
    OutputError,
    ParseError,
    PluginDependencyError,
    PluginError,
    PluginNotFoundError,
    TemplateError,
    TemplateNotFoundError,
    URLValidationError,
    ValidationError,
)


class TestValidationError:
    """Tests for ValidationError exception."""

    def test_validation_error_with_value(self):
        """Test ValidationError with a value."""
        error = ValidationError("url", "javascript:alert(1)", "Invalid URL scheme")
        assert "Invalid URL scheme" in str(error)
        assert "url" in str(error)
        assert "javascript:alert(1)" in str(error)

    def test_validation_error_without_value(self):
        """Test ValidationError without a value."""
        error = ValidationError("name", None, "Name is required")
        assert "Name is required" in str(error)
        assert "name" in str(error)
        # Should not include "value:" when value is None
        assert str(error) == "Name is required (field: name)"


class TestTemplateError:
    """Tests for TemplateError exception."""

    def test_template_error_with_path(self):
        """Test TemplateError with template path."""
        error = TemplateError("/path/to/template.j2", "Template not found")
        assert "Template not found" in str(error)
        assert "/path/to/template.j2" in str(error)

    def test_template_error_without_path(self):
        """Test TemplateError without template path."""
        error = TemplateError(None, "Template error occurred")
        assert str(error) == "Template error occurred"
        # Should not include path when it's None


class TestOutputError:
    """Tests for OutputError exception."""

    def test_output_error_with_path(self):
        """Test OutputError with output path."""
        error = OutputError("/output/file.html", "Permission denied")
        assert "Failed to write output to /output/file.html" in str(error)
        assert "Permission denied" in str(error)

    def test_output_error_without_path(self):
        """Test OutputError without output path."""
        error = OutputError(None, "Output error occurred")
        assert str(error) == "Output error occurred"
        # Should not include path when it's None


class TestURLValidationError:
    """Tests for URLValidationError exception."""

    def test_url_validation_error(self):
        """Test URLValidationError initialization."""
        error = URLValidationError("javascript:alert(1)", "Dangerous URL scheme")
        assert "Dangerous URL scheme" in str(error)
        assert "javascript:alert(1)" in str(error)
        assert "url" in str(error)
        assert error.url == "javascript:alert(1)"


class TestLinkNameValidationError:
    """Tests for LinkNameValidationError exception."""

    def test_link_name_validation_error(self):
        """Test LinkNameValidationError initialization."""
        error = LinkNameValidationError("", "Link name cannot be empty")
        assert "Link name cannot be empty" in str(error)
        assert "name" in str(error)
        assert error.name == ""


class TestTemplateNotFoundError:
    """Tests for TemplateNotFoundError exception."""

    def test_template_not_found_error(self):
        """Test TemplateNotFoundError initialization."""
        error = TemplateNotFoundError("/path/to/missing.j2")
        assert "Template file not found" in str(error)
        assert "/path/to/missing.j2" in str(error)


class TestPluginError:
    """Tests for PluginError exception."""

    def test_plugin_error_with_name(self):
        """Test PluginError with plugin name."""
        error = PluginError("pdf", "Required dependency not installed")
        assert "Plugin 'pdf' error" in str(error)
        assert "Required dependency not installed" in str(error)

    def test_plugin_error_without_name(self):
        """Test PluginError without plugin name."""
        error = PluginError(None, "Generic plugin error")
        assert str(error) == "Generic plugin error"
        # Should not include "Plugin" when name is None


class TestPluginNotFoundError:
    """Tests for PluginNotFoundError exception."""

    def test_plugin_not_found_error(self):
        """Test PluginNotFoundError initialization."""
        error = PluginNotFoundError("unknown_format")
        assert "Plugin 'unknown_format' error" in str(error)
        assert "Output format not found" in str(error)


class TestPluginDependencyError:
    """Tests for PluginDependencyError exception."""

    def test_plugin_dependency_error_with_install_command(self):
        """Test PluginDependencyError with install command."""
        error = PluginDependencyError("pdf", "fpdf2", "pip install minibook[pdf]")
        assert "Missing dependency 'fpdf2'" in str(error)
        assert "Install with: pip install minibook[pdf]" in str(error)
        assert error.dependency == "fpdf2"
        assert error.install_command == "pip install minibook[pdf]"

    def test_plugin_dependency_error_without_install_command(self):
        """Test PluginDependencyError without install command."""
        error = PluginDependencyError("epub", "ebooklib", None)
        assert "Missing dependency 'ebooklib'" in str(error)
        # Should not include "Install with" when install_command is None
        assert "Install with" not in str(error)


class TestParseError:
    """Tests for ParseError exception."""

    def test_parse_error(self):
        """Test ParseError initialization."""
        error = ParseError("YAML", "Invalid YAML syntax")
        assert "Failed to parse YAML" in str(error)
        assert "Invalid YAML syntax" in str(error)


class TestJSONParseError:
    """Tests for JSONParseError exception."""

    def test_json_parse_error(self):
        """Test JSONParseError initialization."""
        error = JSONParseError("Unexpected token at position 5")
        assert "Failed to parse JSON" in str(error)
        assert "Unexpected token at position 5" in str(error)
