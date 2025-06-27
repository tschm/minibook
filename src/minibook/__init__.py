"""MiniBook - A tool to create a minibook from a list of links.

Generates a clean, responsive HTML webpage using Jinja2 templates.
"""

import importlib.metadata

from .main import entrypoint, generate_html

__version__ = importlib.metadata.version("minibook")

__all__ = ["entrypoint", "generate_html"]
