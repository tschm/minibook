"""MiniBook - A tool to create a minibook from a list of links.

Generates a clean, responsive HTML webpage using Jinja2 templates.
"""

from .main import entrypoint, generate_html

__all__ = ["entrypoint", "generate_html"]
