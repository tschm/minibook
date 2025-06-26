"""Test script for MiniBook."""

import subprocess
from pathlib import Path


def test_html_generation():
    """Test HTML generation."""
    output_dir = "test_output_html"

    # Create the output directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True)

    # Run the minibook script with command-line arguments for HTML generation
    cmd = [
        "uv", "run", "minibook",
        "--title", "Test Links",
        "--description", "This is a test page created by MiniBook",
        "--output", output_dir,
        "--format", "html",
        "--links", '{"python": "https://www.python.org", "github": "https://www.github.com", "wikipedia": "https://www.wikipedia.org"}'
    ]



    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("HTML generation test successful!")
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
                    print("\nFirst 10 lines of the HTML file:")
                    for i, line in enumerate(f):
                        if i < 10:
                            print(line.strip())
                        else:
                            break
            else:
                print("Error: index.html not found in output directory")
        else:
            print("Error: Output directory not found")
    else:
        print("HTML generation test failed!")
        print(f"Return code: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")


def test_mkdocs_generation():
    """Test MkDocs generation."""
    output_dir = "test_mkdocs_site"

    # Create the output directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True)

    # Run the minibook script with command-line arguments for MkDocs generation
    cmd = [
        "uv", "run", "minibook",
        "--title", "Test Links",
        "--description", "This is a test page created by MiniBook",
        "--output", output_dir,
        "--format", "mkdocs",
        "--links", '{"python": "https://www.python.org", "github": "https://www.github.com", "wikipedia": "https://www.wikipedia.org"}'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("MkDocs generation test successful!")
        print(result.stdout)

        # Check the generated MkDocs project
        dir_path = Path(output_dir).absolute()
        print(f"Generated directory: {dir_path}")

        if dir_path.exists():
            # List the files in the directory
            print("\nFiles in the MkDocs project:")
            for file_path in dir_path.glob("**/*"):
                if file_path.is_file():
                    print(file_path)

            # Print the contents of the index.md file
            index_file = dir_path / "docs" / "index.md"
            if index_file.exists():
                print("\nContents of index.md:")
                with index_file.open() as f:
                    print(f.read())
            else:
                print("Error: index.md not found")
        else:
            print("Error: Output directory not found")
    else:
        print("MkDocs generation test failed!")
        print(f"Return code: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")


if __name__ == "__main__":
    print("Testing HTML generation...")
    test_html_generation()

    print("\n" + "="*50 + "\n")

    print("Testing MkDocs generation...")
    test_mkdocs_generation()
