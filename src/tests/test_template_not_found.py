"""Tests for the template not found error case in the generate_html function."""

import pytest
from typer.testing import CliRunner

from minibook.main import app, generate_html


def test_generate_html_template_not_found():
    """Test that generate_html raises FileNotFoundError when template file doesn't exist."""
    # Define test data
    title = "Test Links"
    description = "This is a test page created by MiniBook"
    links = [
        ("Python", "https://www.python.org"),
        ("GitHub", "https://www.github.com"),
        ("Wikipedia", "https://www.wikipedia.org")
    ]
    timestamp = "2023-06-18 12:00:00"
    output_file = "test_output.html"
    template_path = "nonexistent_template.j2"

    # Test that generate_html raises FileNotFoundError
    with pytest.raises(FileNotFoundError):
        generate_html(
            title=title,
            links=links,
            description=description,
            timestamp=timestamp,
            output_file=output_file,
            template_path=template_path
        )


def test_entrypoint_template_not_found(tmp_path):
    """Test the entrypoint function with a nonexistent template file."""
    # Create a runner for testing Typer CLI applications
    runner = CliRunner()

    # Create a temporary output directory
    output_dir = tmp_path

    # Create the command arguments with a nonexistent template file
    args = [
        "--title", "Template Not Found Test",
        "--description", "Testing template not found error",
        "--output", str(output_dir),
        "--template", "nonexistent_template.j2",
        "--links", '{"python": "https://www.python.org"}'
    ]

    # Run the command with catch_exceptions=False to let exceptions propagate
    result = runner.invoke(app, args, catch_exceptions=False)

    # Check that the command output contains the expected error message in stderr
    assert "Error: Template file not found" in result.stderr
