"""
Tests for the invalid format case in the entrypoint function.
"""

import os
from typer.testing import CliRunner

from minibook.main import app


def test_invalid_format(tmp_path):
    """Test the entrypoint function with an invalid format."""
    # Create a runner for testing Typer CLI applications
    runner = CliRunner()

    # Create a temporary output file
    output_file = tmp_path / "invalid_format_test_output.html"

    # Create the command arguments with an invalid format
    args = [
        "--title", "Invalid Format Test",
        "--description", "Testing invalid format",
        "--output", str(output_file),
        "--format", "invalid",  # Invalid format
        "--links", '{"Python": "https://www.python.org", "GitHub": "https://www.github.com"}'
    ]

    # Run the command
    result = runner.invoke(app, args)

    # Print the output for debugging
    print(f"Command output: {result.stdout}")
    print(f"Command error: {result.stderr}")
    print(f"Exit code: {result.exit_code}")

    # Check that the error output contains the invalid format message
    assert "Invalid format: invalid. Must be 'html' or 'mkdocs'." in result.stderr

    # Check that the HTML file was NOT created
    assert not os.path.exists(output_file)
