"""MiniBook - A tool to create a webpage from a list of links.

Supports both MkDocs and Jinja2/HTML generation.
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import requests
import typer
from jinja2 import Environment, FileSystemLoader


def get_git_repo_url():
    """Retrieve the Git repository URL.

    This function attempts to fetch the Git repository URL by first using the
    ``git config get-url origin`` command. If that fails, it falls back to using
    the value of the environment variable ``GITHUB_REPOSITORY``. If the environment
    variable is present, the function constructs the appropriate repository URL
    in the format of ``https://github.com/{repository}``.
    If not, it returns ``https://github.com/tschm/minibook`` by default.

    :return: The URL of the Git repository if either the git command succeeds or the
             ``GITHUB_REPOSITORY`` environment variable exists.
    :rtype: str
    """
    try:
        url = (
            subprocess.check_output(
                ["git", "config", "get-url", "origin"],
                stderr=subprocess.DEVNULL,
            )
            .decode("utf-8")
            .strip()
        )
        return url
    except subprocess.CalledProcessError:
        # Fallback to environment variable if git command fails
        github_repo = os.getenv("GITHUB_REPOSITORY", default="tschm/minibook")
        return f"https://github.com/{github_repo}"


def validate_url(url, timeout=5):
    """Validate if a URL is accessible.

    Args:
        url (str): The URL to validate
        timeout (int, optional): Timeout in seconds for the request

    Returns:
        tuple: (is_valid, error_message) where is_valid is a boolean and error_message is a string
               error_message is None if the URL is valid

    """
    try:
        # Make a HEAD request to check if the URL is accessible
        # HEAD is more efficient than GET as it doesn't download the full content
        response = requests.head(url, timeout=timeout, allow_redirects=True)

        # If the HEAD request fails, try a GET request as some servers don't support HEAD
        if response.status_code >= 400:
            response = requests.get(url, timeout=timeout, allow_redirects=True)

        # Check if the response status code indicates success
        if response.status_code < 400:
            return True, None
        else:
            return False, f"HTTP error: {response.status_code}"

    except requests.exceptions.Timeout:
        return False, "Timeout error"
    except requests.exceptions.ConnectionError:
        return False, "Connection error"
    except requests.exceptions.RequestException as e:
        return False, f"Request error: {e!s}"
    except Exception as e:
        return False, f"Unexpected error: {e!s}"


def generate_html(title, links, description=None, timestamp=None, output_file="minibook.html", template_path=None):
    """Generate an HTML page with the given title and links using Jinja2.

    Args:
        title (str): The title of the webpage
        links (list): A list of tuples with (name, url)
        description (str, optional): A description to include on the page
        timestamp (str, optional): A fixed timestamp for testing purposes
        output_file (str, optional): The output HTML file
        template_path (str, optional): Path to a custom Jinja2 template file

    Returns:
        str: The path to the generated HTML file

    """
    # Set up Jinja2 environment
    if template_path:
        # Use custom template if provided
        template_file = Path(template_path)
        if not template_file.exists():
            raise FileNotFoundError(f"Template file not found: {template_path}")

        template_dir = template_file.parent
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template(template_file.name)
    else:
        # Use default template
        template_dir = Path(__file__).parent / "templates"
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("html.j2")

    # Use the provided timestamp or generate a new one
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Render the template with our data
    html = template.render(
        title=title, links=links, description=description, timestamp=timestamp, repository_url=get_git_repo_url()
    )

    # Save the HTML to a file
    with Path(output_file).open("w") as f:
        f.write(html)

    return output_file


app = typer.Typer(help="Create a minibook from a list of links")


@app.command()
def entrypoint(
    title: str = typer.Option("My Links", "--title", "-t", help="Title of the minibook"),
    description: str | None = typer.Option(None, "--description", "-d", help="Description of the minibook"),
    output: str = typer.Option(None, "--output", "-o", help="Output directory"),
    links: str = typer.Option(
        None,
        "--links",
        "-l",
        help="JSON formatted links: can be a list of objects with name/url keys, a list of arrays, or a dictionary",
    ),
    timestamp: str | None = typer.Option(None, "--timestamp", help="Fixed timestamp for testing purposes"),
    validate_links: bool = typer.Option(False, "--validate-links", help="Validate that all links are accessible"),
    template: str | None = typer.Option(
        None, "--template", help="Path to a custom Jinja2 template file for HTML output"
    ),
) -> int:
    """Create a minibook from a list of links."""
    if links is None:
        typer.echo("No links provided. Exiting.", err=True)
        sys.exit(1)

    # Ensure links is a string, not a list
    # if isinstance(links, list):
    #     links = "\n".join(links)

    typer.echo(f"Parsing links: {links}")

    link_tuples = []

    # Try to parse as JSON first
    try:
        # Clean up the JSON string - remove leading/trailing whitespace and handle multi-line strings
        cleaned_links = links.strip()

        # Parse the JSON string into a Python object
        json_data = json.loads(cleaned_links)
        typer.echo(f"Parsed JSON data: {json_data}")
        typer.echo(f"Instance of JSON data: {type(json_data)}")

        # Handle different JSON formats
        if isinstance(json_data, list):
            # If it's a list of lists/arrays: [["name", "url"], ...]
            if all(isinstance(item, list) for item in json_data):
                for item in json_data:
                    if len(item) >= 2:
                        link_tuples.append((item[0], item[1]))
            # If it's a list of objects: [{"name": "...", "url": "..."}, ...]
            elif all(isinstance(item, dict) for item in json_data):
                for item in json_data:
                    if "name" in item and "url" in item:
                        link_tuples.append((item["name"], item["url"]))
        # If it's a dictionary: {"name1": "url1", "name2": "url2", ...}
        elif isinstance(json_data, dict):
            for name, url in json_data.items():
                link_tuples.append((name, url))

        typer.echo(f"Parsed JSON links: {link_tuples}")

    # Fall back to the original parsing logic for backward compatibility
    except (json.JSONDecodeError, TypeError):
        typer.echo("JSON parsing failed, falling back to legacy format")

    # Validate links if requested
    if validate_links:
        typer.echo("Validating links...")
        invalid_links = []

        with typer.progressbar(link_tuples) as progress:
            for name, url in progress:
                is_valid, error_message = validate_url(url)
                if not is_valid:
                    invalid_links.append((name, url, error_message))

        # Report invalid links
        if invalid_links:
            typer.echo(f"\nFound {len(invalid_links)} invalid links:", err=True)
            for name, url, error in invalid_links:
                typer.echo(f"  - {name} ({url}): {error}", err=True)

            # Ask user if they want to continue
            if not typer.confirm("Do you want to continue with invalid links?"):
                typer.echo("Aborting due to invalid links.", err=True)
                return 1
        else:
            typer.echo("All links are valid!")

    # Generate HTML using Jinja2
    output_file = Path(output) / "index.html"
    try:
        output_path = generate_html(title, link_tuples, description, timestamp, output_file, template)
        typer.echo(f"HTML minibook created successfully: {Path(output_path).absolute()}")
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        return 1

    return 0


if __name__ == "__main__":
    app()  # pragma: no cover
