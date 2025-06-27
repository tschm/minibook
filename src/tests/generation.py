"""Test script for MiniBook."""

import subprocess
from pathlib import Path


def test_html_generation():
    """Test HTML generation."""
    output_file = "test_output.html"

    # Run the minibook script with command-line arguments for HTML generation
    cmd = [
        "./run_minibook.py",
        "--title", "Test Links",
        "--description", "This is a test page created by MiniBook",
        "--output", output_file,
        "--links", "python;https://www.python.org,github;https://www.github.com,wikipedia;https://www.wikipedia.org"
    ]



    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("HTML generation test successful!")
        print(result.stdout)

        # Check the generated HTML file
        file_path = Path(output_file).absolute()
        print(f"Generated file: {file_path}")

        if file_path.exists():
            print(f"File size: {file_path.stat().st_size} bytes")

            # Print the first few lines of the file
            with file_path.open() as f:
                print("\nFirst 10 lines of the HTML file:")
                for i, line in enumerate(f):
                    if i < 10:
                        print(line.strip())
                    else:
                        break
        else:
            print("Error: Output file not found")
    else:
        print("HTML generation test failed!")
        print(f"Return code: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")



if __name__ == "__main__":
    print("Testing HTML generation...")
    test_html_generation()
