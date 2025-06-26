"""Test script for MiniBook custom template functionality."""

import subprocess
from pathlib import Path


def test_custom_template():
    """Test HTML generation with a custom template."""
    output_dir = "test_custom_template_output"
    template_path = Path(__file__).parent / "resources" / "custom_template.j2"

    # Create the output directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True)

    # Run the minibook script with command-line arguments for HTML generation with custom template
    cmd = [
        "uv", "run", "minibook",
        "--title", "Custom Template Test",
        "--description", "This is a test page created with a custom template",
        "--output", output_dir,
        "--format", "html",
        "--template", str(template_path),
        "--links", '{"python": "https://www.python.org", "github": "https://www.github.com", "wikipedia": "https://www.wikipedia.org"}'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("Custom template test successful!")
        print(result.stdout)

        # Check the generated HTML file
        dir_path = Path(output_dir).absolute()
        print(f"Generated directory: {dir_path}")

        if dir_path.exists():
            # Check for the index.html file
            html_file = dir_path / "index.html"
            if html_file.exists():
                print(f"HTML file found: {html_file}")
                print(f"File size: {html_file.stat().st_size} bytes")

                # Print the first few lines of the file
                with html_file.open() as f:
                    print("\nFirst 20 lines of the HTML file:")
                    for i, line in enumerate(f):
                        if i < 20:
                            print(line.strip())
                        else:
                            break
            else:
                print("Error: index.html not found in output directory")
        else:
            print("Error: Output directory not found")
    else:
        print("Custom template test failed!")
        print(f"Return code: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")


if __name__ == "__main__":
    test_custom_template()