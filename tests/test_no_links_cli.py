"""Tests for the command-line functionality when no links are provided."""

from typer.testing import CliRunner

from minibook.main import app


def test_entrypoint_with_no_links():
    """Test the entrypoint function when no links are provided."""
    # Create a runner for testing Typer CLI applications
    runner = CliRunner()

    # Create the command arguments without the --links parameter
    args = [
        "--title",
        "Test Title",
        "--subtitle",
        "Test Subtitle",
    ]

    # Run the command
    result = runner.invoke(app, args)

    # Check that the command failed with exit code 1
    assert result.exit_code == 1, f"Expected exit code 1, got {result.exit_code}"

    # Check that the error message is present in output
    # Note: result.output contains combined stdout/stderr
    assert "No links provided. Exiting." in result.output
