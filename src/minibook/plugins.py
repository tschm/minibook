"""Output format plugins for MiniBook.

This module provides a plugin system for generating output in different formats.
Each plugin implements the OutputPlugin interface to provide consistent output generation.
"""

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from minibook.main import get_git_repo_url


class OutputPlugin(ABC):
    """Base class for output format plugins.

    All output plugins must implement the generate() method to produce
    output in their specific format.
    """

    name: str = "base"
    extension: str = ".txt"
    description: str = "Base output plugin"

    @abstractmethod
    def generate(
        self,
        title: str,
        links: list[tuple[str, str]],
        subtitle: str | None = None,
        output_file: str | Path = "output",
        **kwargs,
    ) -> str:
        """Generate output in the plugin's format.

        Args:
            title: The title of the document
            links: List of (name, url) tuples
            subtitle: Optional subtitle/description
            output_file: Path to the output file
            **kwargs: Additional format-specific options

        Returns:
            str: Path to the generated output file
        """
        pass


class HTMLPlugin(OutputPlugin):
    """HTML output plugin using Jinja2 templates."""

    name = "html"
    extension = ".html"
    description = "Generate HTML output with Tailwind CSS styling"

    def __init__(self, template_path: str | None = None):
        """Initialize the HTML plugin.

        Args:
            template_path: Optional path to a custom Jinja2 template
        """
        self.template_path = template_path

    def generate(
        self,
        title: str,
        links: list[tuple[str, str]],
        subtitle: str | None = None,
        output_file: str | Path = "index.html",
        **kwargs,
    ) -> str:
        """Generate HTML output.

        Args:
            title: The title of the webpage
            links: List of (name, url) tuples
            subtitle: Optional description
            output_file: Path to the output HTML file
            **kwargs: Additional options (nonce for CSP)

        Returns:
            str: Path to the generated HTML file
        """
        import secrets

        if self.template_path:
            template_file = Path(self.template_path)
            if not template_file.exists():
                raise FileNotFoundError(f"Template file not found: {self.template_path}")

            template_dir = template_file.parent
            env = Environment(
                loader=FileSystemLoader(template_dir),
                autoescape=select_autoescape(
                    enabled_extensions=("html", "htm", "xml", "j2", "jinja", "jinja2"), default=True
                ),
            )
            template = env.get_template(template_file.name)
        else:
            template_dir = Path(__file__).parent / "templates"
            env = Environment(
                loader=FileSystemLoader(template_dir),
                autoescape=select_autoescape(
                    enabled_extensions=("html", "htm", "xml", "j2", "jinja", "jinja2"), default=True
                ),
            )
            template = env.get_template("html.j2")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nonce = kwargs.get("nonce") or secrets.token_urlsafe(16)

        html = template.render(
            title=title,
            links=links,
            description=subtitle,
            timestamp=timestamp,
            repository_url=get_git_repo_url(),
            nonce=nonce,
        )

        output_path = Path(output_file)
        with output_path.open("w") as f:
            f.write(html)

        return str(output_path)


class MarkdownPlugin(OutputPlugin):
    """Markdown output plugin."""

    name = "markdown"
    extension = ".md"
    description = "Generate Markdown output"

    def generate(
        self,
        title: str,
        links: list[tuple[str, str]],
        subtitle: str | None = None,
        output_file: str | Path = "links.md",
        **kwargs,
    ) -> str:
        """Generate Markdown output.

        Args:
            title: The title of the document
            links: List of (name, url) tuples
            subtitle: Optional description
            output_file: Path to the output Markdown file
            **kwargs: Additional options

        Returns:
            str: Path to the generated Markdown file
        """
        lines = [f"# {title}", ""]

        if subtitle:
            lines.extend([f"*{subtitle}*", ""])

        lines.append("## Links")
        lines.append("")

        for name, url in links:
            lines.append(f"- [{name}]({url})")

        lines.append("")
        lines.append("---")
        lines.append("")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines.append(f"*Generated by [MiniBook](https://pypi.org/project/minibook/) on {timestamp}*")
        lines.append("")

        content = "\n".join(lines)

        output_path = Path(output_file)
        with output_path.open("w") as f:
            f.write(content)

        return str(output_path)


class JSONPlugin(OutputPlugin):
    """JSON output plugin."""

    name = "json"
    extension = ".json"
    description = "Generate JSON output"

    def generate(
        self,
        title: str,
        links: list[tuple[str, str]],
        subtitle: str | None = None,
        output_file: str | Path = "links.json",
        **kwargs,
    ) -> str:
        """Generate JSON output.

        Args:
            title: The title of the document
            links: List of (name, url) tuples
            subtitle: Optional description
            output_file: Path to the output JSON file
            **kwargs: Additional options

        Returns:
            str: Path to the generated JSON file
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data = {
            "title": title,
            "description": subtitle,
            "links": [{"name": name, "url": url} for name, url in links],
            "metadata": {
                "generated_by": "MiniBook",
                "timestamp": timestamp,
                "repository_url": get_git_repo_url(),
            },
        }

        content = json.dumps(data, indent=2)

        output_path = Path(output_file)
        with output_path.open("w") as f:
            f.write(content)

        return str(output_path)


class PDFPlugin(OutputPlugin):
    """PDF output plugin using fpdf2."""

    name = "pdf"
    extension = ".pdf"
    description = "Generate PDF output"

    def generate(
        self,
        title: str,
        links: list[tuple[str, str]],
        subtitle: str | None = None,
        output_file: str | Path = "links.pdf",
        **kwargs,
    ) -> str:
        """Generate PDF output.

        Args:
            title: The title of the document
            links: List of (name, url) tuples
            subtitle: Optional description
            output_file: Path to the output PDF file
            **kwargs: Additional options

        Returns:
            str: Path to the generated PDF file

        Raises:
            ImportError: If fpdf2 is not installed
        """
        try:
            from fpdf import FPDF
        except ImportError as e:
            raise ImportError("PDF generation requires fpdf2. Install with: uv add fpdf2") from e

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Title
        pdf.set_font("Helvetica", "B", 24)
        pdf.cell(0, 15, title, new_x="LMARGIN", new_y="NEXT", align="C")

        # Subtitle
        if subtitle:
            pdf.set_font("Helvetica", "I", 12)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 10, subtitle, new_x="LMARGIN", new_y="NEXT", align="C")
            pdf.set_text_color(0, 0, 0)

        pdf.ln(10)

        # Links section header
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "Links", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)

        # Links
        pdf.set_font("Helvetica", "", 11)
        for name, url in links:
            # Link name in bold
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 8, f"- {name}", new_x="LMARGIN", new_y="NEXT")
            # URL in blue, smaller
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(0, 0, 200)
            pdf.cell(0, 6, f"  {url}", new_x="LMARGIN", new_y="NEXT", link=url)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(2)

        # Footer
        pdf.ln(15)
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(128, 128, 128)
        pdf.cell(0, 8, f"Generated by MiniBook on {timestamp}", new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.cell(0, 6, "https://pypi.org/project/minibook/", new_x="LMARGIN", new_y="NEXT", align="C")

        output_path = Path(output_file)
        pdf.output(str(output_path))

        return str(output_path)


# Registry of available plugins
PLUGINS: dict[str, type[OutputPlugin]] = {
    "html": HTMLPlugin,
    "markdown": MarkdownPlugin,
    "md": MarkdownPlugin,  # Alias
    "json": JSONPlugin,
    "pdf": PDFPlugin,
}


def get_plugin(name: str) -> type[OutputPlugin]:
    """Get an output plugin by name.

    Args:
        name: The name of the plugin (e.g., "html", "markdown", "json")

    Returns:
        The plugin class

    Raises:
        ValueError: If the plugin name is not recognized
    """
    name_lower = name.lower()
    if name_lower not in PLUGINS:
        available = ", ".join(sorted(set(PLUGINS.keys())))
        raise ValueError(f"Unknown output format '{name}'. Available formats: {available}")
    return PLUGINS[name_lower]


def list_plugins() -> list[dict[str, str]]:
    """List all available output plugins.

    Returns:
        List of dicts with plugin info (name, extension, description)
    """
    seen = set()
    result = []
    for name, plugin_cls in PLUGINS.items():
        if plugin_cls.name not in seen:
            seen.add(plugin_cls.name)
            result.append(
                {
                    "name": plugin_cls.name,
                    "extension": plugin_cls.extension,
                    "description": plugin_cls.description,
                }
            )
    return result
