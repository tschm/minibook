"""Tests for the MiniBook package."""

from pathlib import Path

import pytest

from minibook.main import generate_html


def test_generate_html(tmp_path):
    """Test generating HTML with Jinja2."""
    # Define test data
    title = "Test Links"
    description = "This is a test page created by MiniBook"
    links = [
        ("Python", "https://www.python.org"),
        ("GitHub", "https://www.github.com"),
        ("Wikipedia", "https://www.wikipedia.org")
    ]
    output_file = tmp_path / "test_output.html"

    # Generate the HTML
    result = generate_html(
        title=title,
        links=links,
        description=description,
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


def test_command_line_execution(tmp_path):
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


def test_generate_html_with_custom_template(tmp_path):
    """Test generating HTML with a custom template."""
    # Define test data
    title = "Custom Template Test"
    description = "This is a test page with a custom template"
    links = [
        ("Python", "https://www.python.org"),
        ("GitHub", "https://www.github.com")
    ]
    output_file = tmp_path / "custom_template_output.html"

    # Create a custom template file
    template_dir = tmp_path / "templates"
    template_dir.mkdir(exist_ok=True)
    template_file = template_dir / "custom.j2"

    with template_file.open("w") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}</h1>
    {% if description %}
    <p>{{ description }}</p>
    {% endif %}
    <ul>
    {% for name, url in links %}
        <li><a href="{{ url }}">{{ name }}</a></li>
    {% endfor %}
    </ul>
    <p>Generated on: {{ timestamp }}</p>
    <p>Repository: <a href="{{ repository_url }}">{{ repository_url }}</a></p>
</body>
</html>""")

    # Generate the HTML with the custom template
    result = generate_html(
        title=title,
        links=links,
        description=description,
        output_file=str(output_file),
        template_path=str(template_file)
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


def test_generate_html_with_nonexistent_template(tmp_path):
    """Test generating HTML with a nonexistent template file."""
    # Define test data
    title = "Nonexistent Template Test"
    links = [("Python", "https://www.python.org")]
    output_file = tmp_path / "nonexistent_template_output.html"

    # Use a nonexistent template file
    nonexistent_template = tmp_path / "nonexistent.j2"

    # Generate the HTML with the nonexistent template should raise FileNotFoundError
    with pytest.raises(FileNotFoundError) as excinfo:
        generate_html(
            title=title,
            links=links,
            output_file=str(output_file),
            template_path=str(nonexistent_template)
        )

    # Check that the error message contains the template path
    assert str(nonexistent_template) in str(excinfo.value)


def test_command_line_with_nonexistent_template(tmp_path):
    """Test the command-line with a nonexistent template file."""
    from typer.testing import CliRunner

    from minibook.main import app

    # Create a runner for testing Typer CLI applications
    runner = CliRunner()

    # Create a temporary output directory
    output_dir = tmp_path

    # Use a nonexistent template file
    nonexistent_template = tmp_path / "nonexistent.j2"

    # Create the command arguments
    args = [
        "--title", "Nonexistent Template Test",
        "--description", "Testing nonexistent template",
        "--output", str(output_dir),
        "--links", '{"Python": "https://www.python.org"}',
        "--template", str(nonexistent_template)
    ]

    # Run the command
    result = runner.invoke(app, args, catch_exceptions=False)

    # Check that the error message is in the stderr output
    assert "Error: Template file not found" in result.stderr

    # Since we're using the CLI runner, we can't rely on the exit code
    # but we can check that the HTML file was NOT created

    # Check that the HTML file was NOT created
    assert not (output_dir / "index.html").exists()
