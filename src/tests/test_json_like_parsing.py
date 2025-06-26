"""
Test for parsing properly formatted JSON objects with quoted keys and values.
"""

import os

from typer.testing import CliRunner

from minibook.main import app


def test_json_like_parsing(tmp_path):
    """Test parsing of properly formatted JSON objects with quoted keys and values."""
    # Create a runner for testing Typer CLI applications
    runner = CliRunner()

    output_dir = tmp_path
    os.makedirs(output_dir, exist_ok=True)

    # Test with a properly formatted JSON object with quoted keys and values
    json_like_input = '{"GitHub": "https://github.com", "Python": "https://python.org"}'

    # Create the command arguments
    args = [
        "--title", "JSON-like Test",
        "--description", "Testing JSON-like parsing",
        "--output", str(output_dir),
        "--format", "html",
        "--links", json_like_input
    ]

    # Run the command
    result = runner.invoke(app, args)

    # Print the output for debugging
    print(f"Command output: {result.stdout}")

    # Check that the command executed successfully
    assert result.exit_code == 0, f"Command failed with error: {result.stdout}"

    # Check that the HTML file was created
    output_file = output_dir / "index.html"
    assert os.path.exists(output_file)

    # Read the file and check its contents
    with open(output_file) as f:
        content = f.read()

    # Check that all links are in the content
    assert "https://github.com" in content
    assert "https://python.org" in content
