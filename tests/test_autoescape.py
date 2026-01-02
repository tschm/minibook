"""Tests for Jinja2 autoescape configuration to prevent XSS vulnerabilities."""

from pathlib import Path

from minibook.main import generate_html


def test_autoescape_enabled_with_malicious_content(tmp_path):
    """Test that autoescape is enabled and prevents XSS attacks."""
    # Define test data with potentially malicious content
    title = "Test <script>alert('XSS')</script>"
    description = "Description with <img src=x onerror=alert('XSS')>"
    links = [
        ("Link with <script>alert('XSS')</script>", "https://example.com"),
        ("Normal Link", "https://example.org"),
    ]
    output_file = tmp_path / "test_autoescape.html"

    # Generate the HTML
    result = generate_html(title=title, links=links, subtitle=description, output_file=str(output_file))

    # Check that the file was created
    assert Path(result).exists()

    # Read the file and check its contents
    with Path(result).open() as f:
        content = f.read()

    # Check that the malicious scripts are escaped (HTML entities instead of raw tags)
    # The < and > should be converted to &lt; and &gt;
    assert "&lt;script&gt;" in content or "&#x3c;script&#x3e;" in content.lower()
    # The quotes may also be escaped
    assert "alert" in content  # The content itself should still be there (though escaped)
    assert "<script>alert('XSS')</script>" not in content  # But not as executable script

    # Check for the img tag with onerror
    assert "&lt;img" in content or "&#x3c;img" in content.lower()
    assert "<img src=x onerror=" not in content  # Should not have executable img tag


def test_autoescape_enabled_with_custom_template(tmp_path):
    """Test that autoescape is enabled for custom templates."""
    # Define test data with potentially malicious content
    title = "Custom Template <script>alert('XSS')</script>"
    description = "Test <b>bold</b>"
    links = [("Link <script>", "https://example.com")]
    output_file = tmp_path / "custom_autoescape.html"

    # Create a custom template file
    template_dir = tmp_path / "templates"
    template_dir.mkdir(exist_ok=True)
    template_file = template_dir / "custom.html"

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
</body>
</html>""")

    # Generate the HTML with the custom template
    result = generate_html(
        title=title, links=links, subtitle=description, output_file=str(output_file), template_path=str(template_file)
    )

    # Check that the file was created
    assert Path(result).exists()

    # Read the file and check its contents
    with Path(result).open() as f:
        content = f.read()

    # Check that the malicious scripts are escaped
    assert "&lt;script&gt;" in content or "&#x3c;script&#x3e;" in content.lower()
    assert "<script>alert('XSS')</script>" not in content


def test_autoescape_preserves_safe_html_entities(tmp_path):
    """Test that HTML entities are properly preserved and escaped."""
    # Test with content that has HTML entities
    title = "Test & Ampersand"
    description = "Copyright © 2024"
    links = [("Link & More", "https://example.com?param1=value1&param2=value2")]
    output_file = tmp_path / "test_entities.html"

    # Generate the HTML
    result = generate_html(title=title, links=links, subtitle=description, output_file=str(output_file))

    # Check that the file was created
    assert Path(result).exists()

    # Read the file and check its contents
    with Path(result).open() as f:
        content = f.read()

    # Check that ampersands are properly escaped in text content
    # but URLs in href attributes should be handled correctly
    assert "Test &amp; Ampersand" in content or "Test &#x26; Ampersand" in content.lower()
    assert "Link &amp; More" in content or "Link &#x26; More" in content.lower()
