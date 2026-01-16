"""Tests for the output format plugins."""

import json
import tempfile
from pathlib import Path

import pytest

from minibook.plugins import (
    HTMLPlugin,
    JSONPlugin,
    MarkdownPlugin,
    get_plugin,
    list_plugins,
)


class TestHTMLPlugin:
    """Tests for the HTML output plugin."""

    def test_generate_creates_html_file(self):
        """Test that HTML plugin creates an HTML file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "index.html"
            plugin = HTMLPlugin()

            result = plugin.generate(
                title="Test Title",
                links=[("Link 1", "https://example.com")],
                output_file=output_file,
            )

            assert Path(result).exists()
            content = Path(result).read_text()
            assert "Test Title" in content
            # Check URL appears in href attribute context
            assert 'href="https://example.com"' in content

    def test_generate_with_subtitle(self):
        """Test HTML generation with subtitle."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "index.html"
            plugin = HTMLPlugin()

            plugin.generate(
                title="Test",
                links=[("Link", "https://example.com")],
                subtitle="A test subtitle",
                output_file=output_file,
            )

            content = output_file.read_text()
            assert "A test subtitle" in content

    def test_plugin_attributes(self):
        """Test HTML plugin has correct attributes."""
        plugin = HTMLPlugin()
        assert plugin.name == "html"
        assert plugin.extension == ".html"


class TestMarkdownPlugin:
    """Tests for the Markdown output plugin."""

    def test_generate_creates_markdown_file(self):
        """Test that Markdown plugin creates a Markdown file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "links.md"
            plugin = MarkdownPlugin()

            result = plugin.generate(
                title="Test Title",
                links=[("Link 1", "https://example.com"), ("Link 2", "https://example.org")],
                output_file=output_file,
            )

            assert Path(result).exists()
            content = Path(result).read_text()
            assert "# Test Title" in content
            assert "[Link 1](https://example.com)" in content
            assert "[Link 2](https://example.org)" in content

    def test_generate_with_subtitle(self):
        """Test Markdown generation with subtitle."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "links.md"
            plugin = MarkdownPlugin()

            plugin.generate(
                title="Test",
                links=[("Link", "https://example.com")],
                subtitle="A test subtitle",
                output_file=output_file,
            )

            content = output_file.read_text()
            assert "*A test subtitle*" in content

    def test_plugin_attributes(self):
        """Test Markdown plugin has correct attributes."""
        plugin = MarkdownPlugin()
        assert plugin.name == "markdown"
        assert plugin.extension == ".md"


class TestJSONPlugin:
    """Tests for the JSON output plugin."""

    def test_generate_creates_json_file(self):
        """Test that JSON plugin creates a valid JSON file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "links.json"
            plugin = JSONPlugin()

            result = plugin.generate(
                title="Test Title",
                links=[("Link 1", "https://example.com"), ("Link 2", "https://example.org")],
                output_file=output_file,
            )

            assert Path(result).exists()
            content = Path(result).read_text()

            # Should be valid JSON
            data = json.loads(content)
            assert data["title"] == "Test Title"
            assert len(data["links"]) == 2
            assert data["links"][0]["name"] == "Link 1"
            assert data["links"][0]["url"] == "https://example.com"

    def test_generate_with_subtitle(self):
        """Test JSON generation with subtitle."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "links.json"
            plugin = JSONPlugin()

            plugin.generate(
                title="Test",
                links=[("Link", "https://example.com")],
                subtitle="A test subtitle",
                output_file=output_file,
            )

            content = output_file.read_text()
            data = json.loads(content)
            assert data["description"] == "A test subtitle"

    def test_json_has_metadata(self):
        """Test that JSON output includes metadata."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "links.json"
            plugin = JSONPlugin()

            plugin.generate(
                title="Test",
                links=[("Link", "https://example.com")],
                output_file=output_file,
            )

            content = output_file.read_text()
            data = json.loads(content)
            assert "metadata" in data
            assert data["metadata"]["generated_by"] == "MiniBook"
            assert "timestamp" in data["metadata"]

    def test_plugin_attributes(self):
        """Test JSON plugin has correct attributes."""
        plugin = JSONPlugin()
        assert plugin.name == "json"
        assert plugin.extension == ".json"


class TestPluginRegistry:
    """Tests for the plugin registry functions."""

    def test_get_plugin_html(self):
        """Test getting HTML plugin by name."""
        plugin_cls = get_plugin("html")
        assert plugin_cls == HTMLPlugin

    def test_get_plugin_markdown(self):
        """Test getting Markdown plugin by name."""
        plugin_cls = get_plugin("markdown")
        assert plugin_cls == MarkdownPlugin

    def test_get_plugin_md_alias(self):
        """Test getting Markdown plugin by alias."""
        plugin_cls = get_plugin("md")
        assert plugin_cls == MarkdownPlugin

    def test_get_plugin_json(self):
        """Test getting JSON plugin by name."""
        plugin_cls = get_plugin("json")
        assert plugin_cls == JSONPlugin

    def test_get_plugin_case_insensitive(self):
        """Test that plugin lookup is case insensitive."""
        assert get_plugin("HTML") == HTMLPlugin
        assert get_plugin("Markdown") == MarkdownPlugin
        assert get_plugin("JSON") == JSONPlugin

    def test_get_plugin_unknown_raises(self):
        """Test that unknown plugin name raises ValueError."""
        with pytest.raises(ValueError, match="Unknown output format"):
            get_plugin("unknown")

    def test_list_plugins(self):
        """Test listing available plugins."""
        plugins = list_plugins()

        # Should have at least 3 unique plugins
        assert len(plugins) >= 3

        # Check structure
        for plugin_info in plugins:
            assert "name" in plugin_info
            assert "extension" in plugin_info
            assert "description" in plugin_info

        # Check specific plugins are listed
        names = [p["name"] for p in plugins]
        assert "html" in names
        assert "markdown" in names
        assert "json" in names
