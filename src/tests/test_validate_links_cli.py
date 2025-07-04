"""Tests for the command-line functionality with the --validate-links flag."""


from typer.testing import CliRunner

from minibook.main import app


def test_command_line_with_validate_links(tmp_path, monkeypatch):
    """Test the main function with the --validate-links flag."""
    # Create a runner for testing Typer CLI applications
    runner = CliRunner()

    # Create a temporary output file
    html_output = tmp_path

    # Create the command arguments
    args = [
        "--title", "Validate Links Test",
        "--subtitle", "Testing link validation",
        "--output", str(html_output),
        "--links", '{"Python": "https://www.python.org", "GitHub": "https://www.github.com"}',
        "--validate-links"
    ]

    # Mock the validate_url function to always return valid
    def mock_validate_url(url, timeout=5):
        return True, None

    # Apply the mocks
    monkeypatch.setattr('minibook.main.validate_url', mock_validate_url)
    monkeypatch.setattr('typer.confirm', lambda _: True)

    # Run the command
    result = runner.invoke(app, args)

    # Check that the command executed successfully
    assert result.exit_code == 0, f"Command failed with error: {result.stdout}"

    # Check that the HTML file was created
    assert (html_output / "index.html").exists()

    # Read the file and check its contents
    with (html_output / "index.html").open() as f:
        content = f.read()

    # Check that all links are in the content
    assert "https://www.python.org" in content
    assert "https://www.github.com" in content


def test_command_line_with_invalid_links(tmp_path, monkeypatch):
    """Test the main function with the --validate-links flag and invalid links."""
    # Create a runner for testing Typer CLI applications
    runner = CliRunner()

    # Create a temporary output file
    html_output = tmp_path

    # Create the command arguments
    args = [
        "--title", "Invalid Links Test",
        "--subtitle", "Testing invalid links",
        "--output", str(html_output),
        "--links", '{"Python": "https://www.python.org", "GitHub": "https://www.github.com"}',
        "--validate-links"
    ]

    # Mock the validate_url function to return invalid for GitHub

    def mock_validate_url(url, timeout=5):
        if "github.com" in url:
            return False, "Connection error"
        return True, None

    # Apply the mocks
    monkeypatch.setattr('minibook.main.validate_url', mock_validate_url)
    monkeypatch.setattr('typer.confirm', lambda _: True)

    # Run the command
    result = runner.invoke(app, args)

    # Check that the command executed successfully (because we confirmed to continue)
    assert result.exit_code == 0, f"Command failed with error: {result.stdout}"

    # Check that the HTML file was created
    assert (html_output / "index.html").exists()

    # Read the file and check its contents
    with (html_output / "index.html").open() as f:
        content = f.read()

    # Check that all links are in the content (even the invalid one)
    assert "https://www.python.org" in content
    assert "https://www.github.com" in content


def test_command_line_with_invalid_links_abort(tmp_path, monkeypatch):
    """Test the main function with the --validate-links flag and invalid links, aborting."""
    # Create a runner for testing Typer CLI applications
    runner = CliRunner()

    # Create a temporary output file
    html_output = tmp_path

    # Create the command arguments
    args = [
        "--title", "Abort Links Test",
        "--subtitle", "Testing aborting with invalid links",
        "--output", str(html_output),
        "--links", '{"Python": "https://www.python.org", "GitHub": "https://www.github.com"}',
        "--validate-links"
    ]

    # Mock the validate_url function to return invalid for GitHub
    def mock_validate_url(url, timeout=5):
        if "github.com" in url:
            return False, "Connection error"
        return True, None

    # Apply the mocks
    monkeypatch.setattr('minibook.main.validate_url', mock_validate_url)
    monkeypatch.setattr('typer.confirm', lambda _: False)

    # Run the command
    result = runner.invoke(app, args, catch_exceptions=False)

    # Check that the error message is in the stderr output
    assert "Aborting due to invalid links." in result.stderr

    # Since we're using the CLI runner, we can't rely on the exit code
    # but we can check that the HTML file was NOT created

    # Check that the HTML file was NOT created
    assert not (html_output / "index.html").exists()
