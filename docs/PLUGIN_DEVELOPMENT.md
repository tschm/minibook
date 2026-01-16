# Plugin Development Guide

This guide explains how to create custom output format plugins for MiniBook.

## Overview

MiniBook uses a plugin architecture to support multiple output formats. Each plugin extends the `OutputPlugin` base class and implements the `generate()` method to produce output in a specific format.

## Built-in Plugins

MiniBook includes the following built-in plugins:

| Plugin | Format | Extension | Description |
|--------|--------|-----------|-------------|
| HTMLPlugin | html | .html | Responsive HTML with Tailwind CSS |
| MarkdownPlugin | markdown, md | .md | Standard Markdown |
| JSONPlugin | json | .json | Structured JSON data |
| PDFPlugin | pdf | .pdf | PDF document (requires fpdf2) |
| RSTPlugin | rst, restructuredtext | .rst | reStructuredText |
| EPUBPlugin | epub | .epub | EPUB ebook (requires ebooklib) |
| AsciiDocPlugin | asciidoc, adoc | .adoc | AsciiDoc format |

## Creating a Custom Plugin

### Step 1: Import the Base Class

```python
from minibook.plugins import OutputPlugin
```

### Step 2: Create Your Plugin Class

```python
class MyFormatPlugin(OutputPlugin):
    """Plugin for generating MyFormat output."""

    name = "myformat"           # Unique identifier for the plugin
    extension = ".myf"          # File extension for output
    description = "Generate MyFormat output"  # Description shown in help

    def generate(
        self,
        title: str,
        links: list[tuple[str, str]],
        subtitle: str | None = None,
        output_file: str | Path = "output.myf",
        **kwargs,
    ) -> str:
        """Generate output in MyFormat.

        Args:
            title: The title of the document
            links: List of (name, url) tuples
            subtitle: Optional description/subtitle
            output_file: Path to the output file
            **kwargs: Additional format-specific options

        Returns:
            str: Path to the generated output file
        """
        # Your generation logic here
        content = f"Title: {title}\n"

        if subtitle:
            content += f"Description: {subtitle}\n"

        content += "\nLinks:\n"
        for name, url in links:
            content += f"  - {name}: {url}\n"

        # Write to file
        output_path = Path(output_file)
        with output_path.open("w") as f:
            f.write(content)

        return str(output_path)
```

### Step 3: Register Your Plugin

To use your plugin with MiniBook, you need to register it in the `PLUGINS` dictionary:

```python
from minibook.plugins import PLUGINS

# Register your plugin
PLUGINS["myformat"] = MyFormatPlugin
PLUGINS["myf"] = MyFormatPlugin  # Optional: add an alias
```

## Plugin Interface Reference

### Required Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | str | Unique identifier for the plugin (e.g., "html", "json") |
| `extension` | str | File extension including dot (e.g., ".html", ".pdf") |
| `description` | str | Human-readable description |

### Required Methods

#### `generate()`

```python
def generate(
    self,
    title: str,
    links: list[tuple[str, str]],
    subtitle: str | None = None,
    output_file: str | Path = "output.ext",
    **kwargs,
) -> str:
```

**Parameters:**
- `title` (str): The title of the document
- `links` (list[tuple[str, str]]): List of (name, url) tuples
- `subtitle` (str | None): Optional description or subtitle
- `output_file` (str | Path): Path where output should be written
- `**kwargs`: Additional format-specific options

**Returns:**
- `str`: Path to the generated output file

## Best Practices

### 1. Use Shared Utilities

MiniBook provides shared utilities in `minibook.utils`:

```python
from minibook.utils import get_timestamp, load_template

# Get formatted timestamp
timestamp = get_timestamp()  # Returns "YYYY-MM-DD HH:MM:SS"

# Load a Jinja2 template (for HTML-like formats)
template = load_template(template_path)
```

### 2. Handle Optional Dependencies

If your plugin requires optional dependencies, use lazy imports:

```python
def generate(self, title, links, **kwargs):
    try:
        import some_optional_library
    except ImportError as e:
        raise ImportError(
            "MyFormat generation requires some_optional_library. "
            "Install with: pip install some_optional_library"
        ) from e

    # Continue with generation...
```

### 3. Include Metadata

Include generation metadata in your output when appropriate:

```python
from minibook.main import get_git_repo_url
from minibook.utils import get_timestamp

metadata = {
    "generated_by": "MiniBook",
    "timestamp": get_timestamp(),
    "repository_url": get_git_repo_url(),
}
```

### 4. Validate Input

Validate input parameters before processing:

```python
def generate(self, title, links, **kwargs):
    if not title:
        raise ValueError("Title is required")

    if not links:
        raise ValueError("At least one link is required")

    # Continue with generation...
```

### 5. Support Custom Options via kwargs

Use `**kwargs` to accept format-specific options:

```python
def generate(self, title, links, **kwargs):
    # Get optional parameters with defaults
    page_size = kwargs.get("page_size", "A4")
    font_size = kwargs.get("font_size", 12)

    # Use in generation...
```

## Example: XML Plugin

Here's a complete example of a custom XML plugin:

```python
"""XML output plugin for MiniBook."""

from pathlib import Path
from xml.etree import ElementTree as ET

from minibook.plugins import OutputPlugin
from minibook.main import get_git_repo_url
from minibook.utils import get_timestamp


class XMLPlugin(OutputPlugin):
    """XML output plugin."""

    name = "xml"
    extension = ".xml"
    description = "Generate XML output"

    def generate(
        self,
        title: str,
        links: list[tuple[str, str]],
        subtitle: str | None = None,
        output_file: str | Path = "links.xml",
        **kwargs,
    ) -> str:
        """Generate XML output.

        Args:
            title: The title of the document
            links: List of (name, url) tuples
            subtitle: Optional description
            output_file: Path to the output XML file
            **kwargs: Additional options (encoding)

        Returns:
            str: Path to the generated XML file
        """
        encoding = kwargs.get("encoding", "utf-8")

        # Create root element
        root = ET.Element("minibook")

        # Add metadata
        meta = ET.SubElement(root, "metadata")
        ET.SubElement(meta, "title").text = title
        if subtitle:
            ET.SubElement(meta, "description").text = subtitle
        ET.SubElement(meta, "generated_by").text = "MiniBook"
        ET.SubElement(meta, "timestamp").text = get_timestamp()
        ET.SubElement(meta, "repository_url").text = get_git_repo_url()

        # Add links
        links_elem = ET.SubElement(root, "links")
        for name, url in links:
            link = ET.SubElement(links_elem, "link")
            ET.SubElement(link, "name").text = name
            ET.SubElement(link, "url").text = url

        # Write to file
        tree = ET.ElementTree(root)
        output_path = Path(output_file)

        with output_path.open("wb") as f:
            tree.write(f, encoding=encoding, xml_declaration=True)

        return str(output_path)


# Register the plugin
from minibook.plugins import PLUGINS
PLUGINS["xml"] = XMLPlugin
```

## Testing Your Plugin

Create tests for your plugin following MiniBook's testing patterns:

```python
import pytest
from pathlib import Path

from my_plugin import MyFormatPlugin


class TestMyFormatPlugin:
    """Tests for MyFormatPlugin."""

    def test_basic_generation(self, tmp_path):
        """Test basic output generation."""
        plugin = MyFormatPlugin()
        links = [("Python", "https://python.org")]
        output_file = tmp_path / "output.myf"

        result = plugin.generate(
            title="Test",
            links=links,
            output_file=output_file,
        )

        assert Path(result).exists()
        content = Path(result).read_text()
        assert "Test" in content
        assert "Python" in content

    def test_with_subtitle(self, tmp_path):
        """Test generation with subtitle."""
        plugin = MyFormatPlugin()
        links = [("Python", "https://python.org")]
        output_file = tmp_path / "output.myf"

        plugin.generate(
            title="Test",
            subtitle="A test document",
            links=links,
            output_file=output_file,
        )

        content = output_file.read_text()
        assert "A test document" in content
```

## Debugging

Enable verbose output when testing:

```bash
minibook --title "Test" --links '{"a": "https://a.com"}' --format myformat
```

Check that your plugin:
1. Is properly registered in `PLUGINS`
2. Returns the correct output file path
3. Writes valid content to the output file
4. Handles edge cases (empty links, special characters, etc.)
