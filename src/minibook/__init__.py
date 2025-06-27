"""MiniBook - A tool to create a minibook from a list of links.
Supports both MkDocs and Jinja2/HTML generation.
"""

from .main import entrypoint, generate_html

__all__ = ["entrypoint", "generate_html"]
