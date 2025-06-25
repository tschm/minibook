"""
MiniBook - A tool to create a minibook from a list of links.
Supports both MkDocs and Jinja2/HTML generation.
"""

from .main import generate_html, generate_mkdocs_project, entrypoint

__all__ = ['generate_html', 'generate_mkdocs_project', 'entrypoint']
