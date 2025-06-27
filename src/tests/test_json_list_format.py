"""Tests for the JSON list format case in the entrypoint function."""

from typer.testing import CliRunner

from minibook.main import app


def test_json_list_format(tmp_path):
    """Test the entrypoint function with a JSON list format."""
    # Create a runner for testing Typer CLI applications
    runner = CliRunner()

    # Create a temporary output directory
    output_dir = tmp_path

    # Test with a JSON list of lists format
    json_list_input = '[["Python", "https://www.python.org"], ["GitHub", "https://www.github.com"]]'

    # Create the command arguments
    args = [
        "--title", "JSON List Format Test",
        "--description", "Testing JSON list format",
        "--output", str(output_dir),
        "--links", json_list_input
    ]

    # Run the command
    result = runner.invoke(app, args)

    # Print the output for debugging
    print(f"Command output: {result.stdout}")

    # Check that the command executed successfully
    assert result.exit_code == 0, f"Command failed with error: {result.stdout}"

    # Check that the HTML file was created
    output_file = output_dir / "index.html"
    assert output_file.exists()

    # Read the file and check its contents
    with open(output_file) as f:
        content = f.read()

    # Check that all links are in the content
    assert "https://www.python.org" in content
    assert "https://www.github.com" in content
