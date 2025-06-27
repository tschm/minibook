"""Tests for the MiniBook package."""

from pathlib import Path

from minibook.main import generate_html


def test_generate_html(resource_dir):
    """Test generating HTML with Jinja2."""
    # Define test data
    title = "Test Links"
    description = "This is a test page created by MiniBook"
    links = [
        ("Python", "https://www.python.org"),
        ("GitHub", "https://www.github.com"),
        ("Wikipedia", "https://www.wikipedia.org")
    ]
    timestamp = "2023-06-18 12:00:00"
    output_file = resource_dir / "test_output.html"

    # Generate the HTML
    result = generate_html(
        title=title,
        links=links,
        description=description,
        timestamp=timestamp,
        output_file=str(output_file)
    )

    # Check that the file was created
    assert Path(result).exists()

    # Read the file and check its contents
    with Path(result).open() as f:
        content = f.read()

    # Check that the title, description, and links are in the content
    assert title in content
    assert description in content
    assert "https://www.python.org" in content
    assert "https://www.github.com" in content
    assert "https://www.wikipedia.org" in content
    assert timestamp in content


def test_command_line_execution(resource_dir, tmp_path):
    """Test command-line execution of MiniBook."""
    import subprocess

    # Test HTML generation
    html_output = tmp_path
    html_cmd = [
        #str(run_script),
        "uv", "run", "minibook",
        "--title", "Test Links",
        "--description", "This is a test page created by MiniBook",
        "--output", str(html_output),
        "--links",
        '{"python": "https://www.python.org"}',
        #"--links github;https://www.github.com",
        #"--links wikipedia;https://www.wikipedia.org"
    ]

    html_result = subprocess.run(html_cmd, capture_output=True, text=True)

    # Check that the command executed successfully
    assert html_result.returncode == 0, f"HTML command failed with error: {html_result.stderr}"

    # Check that the HTML file was created
    assert html_output.exists()


def test_compile_command_execution(tmp_path):
    """Test command-line execution of MiniBook using the uvx command."""
    import subprocess

    # Test HTML generation
    html_output = tmp_path
    html_cmd = [
        "minibook",
        "--title", "Test Links",
        "--description", "This is a test page created by MiniBook",
        "--output", str(html_output),
        "--links",
        '{"python": "https://www.python.org"}',
    ]

    html_result = subprocess.run(html_cmd, capture_output=True, text=True)

    # Check that the command executed successfully
    assert html_result.returncode == 0, f"HTML command failed with error: {html_result.stderr}"

    # Check that the HTML file was created
    assert html_output.exists()


def test_no_links_provided():
    """Test command-line execution of MiniBook when no links are provided."""
    import subprocess

    # Test with no links parameter
    cmd = [
        "minibook",
        "--title", "Test Links",
        "--description", "This is a test page created by MiniBook"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Check that the command failed with the expected error message
    assert result.returncode == 1, "Command should fail when no links are provided"
    assert "No links provided. Exiting." in result.stderr


def test_multiline_links(tmp_path):
    """Test command-line execution of MiniBook with multi-line links."""
    import subprocess

    # Test HTML generation with multi-line links
    html_output = tmp_path

    # Create JSON arrays for links
    multiline_links = '[{"name": "Python", "url": "https://www.python.org"}, {"name": "GitHub", "url": "https://www.github.com"}]'

    # Create a multi-line JSON object with newlines and indentation (like in book.yml)

    # Test with actual newlines
    html_cmd_newlines = [
        "minibook",
        "--title", "Multi-line Links Test",
        "--description", "Testing multi-line links",
        "--output", str(html_output),
        "--links", multiline_links,
    ]

    html_result_newlines = subprocess.run(html_cmd_newlines, capture_output=True, text=True)

    # Check that the command executed successfully
    assert html_result_newlines.returncode == 0, \
        f"HTML command with newlines failed with error: {html_result_newlines.stderr}"

    # Check that the HTML file was created
    assert html_output.exists()

    html_file = html_output / "index.html"
    # Read the file and check its contents
    with html_file.open() as f:
        content = f.read()

    # Check that all links are in the content
    assert "https://www.python.org" in content
    assert "https://www.github.com" in content
