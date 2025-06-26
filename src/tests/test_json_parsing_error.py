"""
Tests for the JSON parsing error handling in the entrypoint function.
"""

from typer.testing import CliRunner

from minibook.main import app


def test_json_parsing_error(tmp_path):
    """Test the entrypoint function with a JSON parsing error."""
    # Create a runner for testing Typer CLI applications
    runner = CliRunner()

    # Create a temporary output directory
    output_dir = tmp_path

    # Test with an invalid JSON format that will cause a parsing error
    invalid_json = '{invalid json}'

    # Create the command arguments
    args = [
        "--title", "JSON Parsing Error Test",
        "--description", "Testing JSON parsing error handling",
        "--output", str(output_dir),
        "--format", "html",
        "--links", invalid_json
    ]

    # Run the command
    result = runner.invoke(app, args)

    # Print the output for debugging
    print(f"Command output: {result.stdout}")

    # Check that the command executed successfully (it should fall back to legacy format)
    assert result.exit_code == 0, f"Command failed with error: {result.stdout}"

    # Check that the output contains the JSON parsing error message
    assert "JSON parsing failed, falling back to legacy format" in result.stdout
