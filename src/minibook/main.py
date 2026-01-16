"""MiniBook - A tool to create a webpage from a list of links.

Generates a clean, responsive HTML webpage using Jinja2 templates.
"""

import json
import sys
from datetime import datetime
from os import getenv
from pathlib import Path
from urllib.parse import urlparse

import requests
import typer
from jinja2 import Environment, FileSystemLoader, select_autoescape


def validate_url_format(url: str) -> tuple[bool, str | None]:
    """Validate URL format and scheme.

    Checks that the URL is a non-empty string with http or https scheme.
    Blocks potentially dangerous schemes like javascript:, data:, and file:.

    Args:
        url: The URL string to validate.

    Returns:
        A tuple of (is_valid, error_message). error_message is None if valid.

    Examples:
        Valid HTTP and HTTPS URLs return (True, None):

        >>> validate_url_format("https://example.com")
        (True, None)
        >>> validate_url_format("http://example.com/path/to/page")
        (True, None)
        >>> validate_url_format("https://example.com?query=value&foo=bar")
        (True, None)

        JavaScript URLs are rejected to prevent XSS attacks:

        >>> validate_url_format("javascript:alert(1)")
        (False, "Invalid URL scheme 'javascript', must be http or https")

        Data URLs are rejected to prevent code injection:

        >>> validate_url_format("data:text/html,<script>alert(1)</script>")
        (False, "Invalid URL scheme 'data', must be http or https")

        File URLs are rejected to prevent local file access:

        >>> validate_url_format("file:///etc/passwd")
        (False, "Invalid URL scheme 'file', must be http or https")

        Empty strings and whitespace-only strings are rejected:

        >>> validate_url_format("")
        (False, 'URL must be a non-empty string')
        >>> validate_url_format("   ")
        (False, 'URL must be a non-empty string')

        Non-string values are rejected:

        >>> validate_url_format(None)
        (False, 'URL must be a non-empty string')
        >>> validate_url_format(123)
        (False, 'URL must be a non-empty string')

        URLs without a valid host are rejected:

        >>> validate_url_format("https://")
        (False, 'URL must have a valid host')

        URLs without a scheme are rejected:

        >>> validate_url_format("example.com")
        (False, "Invalid URL scheme '', must be http or https")

    """
    if not isinstance(url, str) or not url.strip():
        return False, "URL must be a non-empty string"

    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False, f"Invalid URL scheme '{parsed.scheme}', must be http or https"
        if not parsed.netloc:
            return False, "URL must have a valid host"
        return True, None
    except Exception as e:
        return False, f"Invalid URL: {e}"


def validate_link_name(name: str) -> tuple[bool, str | None]:
    r"""Validate link name.

    Ensures the link name is a non-empty string. Names are used as display
    text for links in the generated HTML.

    Args:
        name: The link name string to validate.

    Returns:
        A tuple of (is_valid, error_message). error_message is None if valid.

    Examples:
        Valid non-empty strings return (True, None):

        >>> validate_link_name("My Link")
        (True, None)
        >>> validate_link_name("GitHub")
        (True, None)
        >>> validate_link_name("A")
        (True, None)

        Empty strings are rejected:

        >>> validate_link_name("")
        (False, 'Name must be a non-empty string')

        Whitespace-only strings are rejected:

        >>> validate_link_name("   ")
        (False, 'Name must be a non-empty string')
        >>> validate_link_name("\t\n")
        (False, 'Name must be a non-empty string')

        Non-string values are rejected:

        >>> validate_link_name(None)
        (False, 'Name must be a non-empty string')
        >>> validate_link_name(123)
        (False, 'Name must be a non-empty string')
        >>> validate_link_name(["list"])
        (False, 'Name must be a non-empty string')

    """
    if not isinstance(name, str) or not name.strip():
        return False, "Name must be a non-empty string"
    return True, None


def get_git_repo_url():
    """Retrieve the GitHub repository URL.

    This function generates the GitHub repository URL based on the repository name
    retrieved from the environment variable 'GITHUB_REPOSITORY'. If the environment
    variable is not set, it defaults to 'tschm/minibook'. This URL can then be used
    for interactions with the repository.

    :return: The full URL for the GitHub repository.
    :rtype: str
    """
    # Fallback to environment variable if git command fails
    github_repo = getenv("GITHUB_REPOSITORY", default="tschm/minibook")
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


def generate_html(title, links, subtitle=None, output_file="index.html", template_path=None):
    """Generate an HTML page with the given title and links using Jinja2.

    Args:
        title (str): The title of the webpage
        links (list): A list of tuples with (name, url)
        subtitle (str, optional): A description to include on the page
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
        env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(
                enabled_extensions=("html", "htm", "xml", "j2", "jinja", "jinja2"), default=True
            ),
        )
        template = env.get_template(template_file.name)
    else:
        # Use default template
        template_dir = Path(__file__).parent / "templates"
        env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(
                enabled_extensions=("html", "htm", "xml", "j2", "jinja", "jinja2"), default=True
            ),
        )
        template = env.get_template("html.j2")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Render the template with our data
    html = template.render(
        title=title, links=links, description=subtitle, timestamp=timestamp, repository_url=get_git_repo_url()
    )

    # Save the HTML to a file
    with Path(output_file).open("w") as f:
        f.write(html)

    return output_file


def parse_links_from_json(links_json: str) -> tuple[list[tuple[str, str]], list[str]]:
    """Parse links from a JSON string into a list of tuples.

    Supports multiple JSON formats:
    - List of objects: [{"name": "...", "url": "..."}, ...]
    - List of arrays: [["name", "url"], ...]
    - Dictionary: {"name1": "url1", "name2": "url2", ...}

    Validates that names and URLs are non-empty strings and that URLs use
    http or https schemes. Invalid items are skipped with warnings.

    Args:
        links_json (str): JSON-formatted string containing links

    Returns:
        tuple[list[tuple[str, str]], list[str]]: A tuple containing:
            - List of valid (name, url) tuples
            - List of warning messages for skipped items

    Raises:
        json.JSONDecodeError: If the JSON string is invalid

    """
    cleaned_links = links_json.strip()
    json_data = json.loads(cleaned_links)

    link_tuples = []
    warnings = []

    def validate_and_append(name, url, context: str = ""):
        """Validate a name/url pair and append if valid, otherwise add warning."""
        # Validate name
        name_valid, name_error = validate_link_name(name)
        if not name_valid:
            warnings.append(f"Skipping item{context}: {name_error}")
            return

        # Validate URL
        url_valid, url_error = validate_url_format(url)
        if not url_valid:
            warnings.append(f"Skipping '{name}'{context}: {url_error}")
            return

        link_tuples.append((name, url))

    # Handle different JSON formats
    if isinstance(json_data, list):
        # If it's a list of lists/arrays: [["name", "url"], ...]
        if all(isinstance(item, list) for item in json_data):
            for i, item in enumerate(json_data):
                if len(item) >= 2:
                    validate_and_append(item[0], item[1], f" at index {i}")
                else:
                    warnings.append(f"Skipping item at index {i}: array must have at least 2 elements")
        # If it's a list of objects: [{"name": "...", "url": "..."}, ...]
        elif all(isinstance(item, dict) for item in json_data):
            for i, item in enumerate(json_data):
                if "name" in item and "url" in item:
                    validate_and_append(item["name"], item["url"], f" at index {i}")
                else:
                    warnings.append(f"Skipping item at index {i}: missing 'name' or 'url' key")
    # If it's a dictionary: {"name1": "url1", "name2": "url2", ...}
    elif isinstance(json_data, dict):
        for name, url in json_data.items():
            validate_and_append(name, url)

    return link_tuples, warnings


def validate_link_list(link_tuples: list[tuple[str, str]]) -> tuple[bool, list[tuple[str, str, str]]]:
    """Validate a list of links and return invalid ones.

    Args:
        link_tuples (list[tuple[str, str]]): List of (name, url) tuples to validate

    Returns:
        tuple[bool, list[tuple[str, str, str]]]: A tuple containing:
            - bool: True if all links are valid, False otherwise
            - list: List of (name, url, error_message) tuples for invalid links

    """
    invalid_links = []

    with typer.progressbar(link_tuples) as progress:
        for name, url in progress:
            is_valid, error_message = validate_url(url)
            if not is_valid:
                invalid_links.append((name, url, error_message))

    return len(invalid_links) == 0, invalid_links


app = typer.Typer(help="Create a minibook from a list of links")


@app.command()
def entrypoint(
    title: str = typer.Option("My Links", "--title", "-t", help="Title of the minibook"),
    subtitle: str | None = typer.Option(None, "--subtitle", help="Subtitle of the minibook"),
    output: str = typer.Option("artifacts", "--output", "-o", help="Output directory"),
    links: str = typer.Option(
        None,
        "--links",
        "-l",
        help="JSON formatted links: can be a list of objects with name/url keys, a list of arrays, or a dictionary",
    ),
    validate_links: bool = typer.Option(False, "--validate-links", help="Validate that all links are accessible"),
    template: str | None = typer.Option(
        None, "--template", help="Path to a custom Jinja2 template file for HTML output"
    ),
) -> int:
    """Create a minibook from a list of links."""
    if links is None:
        typer.echo("No links provided. Exiting.", err=True)
        sys.exit(1)

    typer.echo(f"Parsing links: {links}")

    # Parse links from JSON
    try:
        link_tuples, parse_warnings = parse_links_from_json(links)
        typer.echo(f"Parsed JSON links: {link_tuples}")

        # Display warnings for skipped items
        if parse_warnings:
            typer.echo(f"\nWarning: {len(parse_warnings)} item(s) skipped due to validation errors:", err=True)
            for warning in parse_warnings:
                typer.echo(f"  - {warning}", err=True)

        # Exit if no valid links remain
        if not link_tuples:
            typer.echo("Error: No valid links to process.", err=True)
            return 1

    except (json.JSONDecodeError, TypeError):
        typer.echo("JSON parsing failed, falling back to legacy format")
        return 1

    # Validate links if requested
    if validate_links:
        typer.echo("Validating links...")
        all_valid, invalid_links = validate_link_list(link_tuples)

        # Report invalid links
        if not all_valid:
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
        output_path = generate_html(title, link_tuples, subtitle, output_file, template)
        typer.echo(f"HTML minibook created successfully: {Path(output_path).absolute()}")
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        return 1

    return 0


if __name__ == "__main__":
    app()  # pragma: no cover
