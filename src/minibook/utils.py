"""Utility functions for MiniBook.

This module provides shared utility functions used across MiniBook modules.
"""

from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template, select_autoescape

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

# Extensions that should have autoescape enabled
AUTOESCAPE_EXTENSIONS = ("html", "htm", "xml", "j2", "jinja", "jinja2")


def get_timestamp() -> str:
    r"""Generate a formatted timestamp string.

    Returns:
        A timestamp string in the format 'YYYY-MM-DD HH:MM:SS'.

    Examples:
        >>> import re
        >>> ts = get_timestamp()
        >>> bool(re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', ts))
        True
    """
    return datetime.now().strftime(TIMESTAMP_FORMAT)


def create_jinja_env(template_dir: Path) -> Environment:
    """Create a Jinja2 environment with secure defaults.

    Args:
        template_dir: Directory containing template files.

    Returns:
        A configured Jinja2 Environment with autoescape enabled.
    """
    return Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(enabled_extensions=AUTOESCAPE_EXTENSIONS, default=True),
    )


def load_template(template_path: str | None = None, default_template: str = "html.j2") -> Template:
    """Load a Jinja2 template from a path or use the default.

    Args:
        template_path: Optional path to a custom Jinja2 template file.
        default_template: Name of the default template to use if no custom path provided.

    Returns:
        A loaded Jinja2 Template object.

    Raises:
        FileNotFoundError: If the specified template file does not exist.

    Examples:
        >>> template = load_template()  # Uses default html.j2
        >>> template.name
        'html.j2'
        >>> template = load_template(default_template="bare.j2")
        >>> template.name
        'bare.j2'
    """
    if template_path:
        template_file = Path(template_path)
        if not template_file.exists():
            msg = f"Template file not found: {template_path}"
            raise FileNotFoundError(msg)

        template_dir = template_file.parent
        env = create_jinja_env(template_dir)
        return env.get_template(template_file.name)

    # Use default template from package
    template_dir = Path(__file__).parent / "templates"
    env = create_jinja_env(template_dir)
    return env.get_template(default_template)
