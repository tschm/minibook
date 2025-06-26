"""
Tests for the MkDocs generation with HTML output file.
"""

import os
import shutil
from typer.testing import CliRunner

from minibook.main import app


def test_mkdocs_html_output(tmp_path):
    """Test the entrypoint function with MkDocs format and HTML output file."""
    # Create a runner for testing Typer CLI applications
    runner = CliRunner()

    # Create a temporary output file with .html extension
    output_file = tmp_path / "output.html"

    # Create the command arguments
    args = [
        "--title", "MkDocs HTML Output Test",
        "--description", "Testing MkDocs with HTML output file",
        "--output", str(output_file),
        "--format", "mkdocs",  # MkDocs format
        "--links", '{"Python": "https://www.python.org", "GitHub": "https://www.github.com"}'
    ]

    # Run the command
    result = runner.invoke(app, args)

    # Print the output for debugging
    print(f"Command output: {result.stdout}")

    # Check that the command executed successfully
    assert result.exit_code == 0, f"Command failed with error: {result.stdout}"

    # Check that the default directory was created
    default_dir = "minibook_site"
    assert os.path.exists(default_dir), f"Default directory {default_dir} not found"

    # Check that the docs directory was created
    docs_dir = os.path.join(default_dir, "docs")
    assert os.path.exists(docs_dir), f"Docs directory {docs_dir} not found"

    # Check that the index.md file was created
    index_file = os.path.join(docs_dir, "index.md")
    assert os.path.exists(index_file), f"Index file {index_file} not found"

    # Check that the mkdocs.yml file was created
    mkdocs_file = os.path.join(default_dir, "mkdocs.yml")
    assert os.path.exists(mkdocs_file), f"MkDocs file {mkdocs_file} not found"

    # Clean up the default directory
    shutil.rmtree(default_dir)