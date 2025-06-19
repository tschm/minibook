#!/usr/bin/env python3
"""
Test script for MiniBook
"""

import os
import subprocess
from pathlib import Path


def test_html_generation():
    """Test HTML generation"""
    output_file = "test_output.html"

    #links = ["python;https://www.python.org", "github;https://www.github.com"]
    #links_tuples = [(link.split(";")[0], link.split(";")[1]) for link in links]
    #print(links_tuples)

    #assert False


    # Run the minibook script with command-line arguments for HTML generation
    cmd = [
        "./run_minibook.py",
        "--title", "Test Links",
        "--description", "This is a test page created by MiniBook",
        "--output", output_file,
        "--format", "html",
        "--links", "python;https://www.python.org,github;https://www.github.com,wikipedia;https://www.wikipedia.org"
    ]



    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("HTML generation test successful!")
        print(result.stdout)

        # Check the generated HTML file
        file_path = Path(output_file).absolute()
        print(f"Generated file: {file_path}")

        if os.path.exists(file_path):
            print(f"File size: {os.path.getsize(file_path)} bytes")

            # Print the first few lines of the file
            with open(file_path) as f:
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


def test_mkdocs_generation():
    """Test MkDocs generation"""
    output_dir = "test_mkdocs_site"

    # Run the minibook script with command-line arguments for MkDocs generation
    cmd = [
        "./run_minibook.py",
        "--title", "Test Links",
        "--description", "This is a test page created by MiniBook",
        "--output", output_dir,
        "--format", "mkdocs",
        "--links",
        "https://www.python.org",
        "https://www.github.com",
        "https://www.wikipedia.org"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("MkDocs generation test successful!")
        print(result.stdout)

        # Check the generated MkDocs project
        dir_path = Path(output_dir).absolute()
        print(f"Generated directory: {dir_path}")

        if os.path.exists(dir_path):
            # List the files in the directory
            print("\nFiles in the MkDocs project:")
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    print(os.path.join(root, file))

            # Print the contents of the index.md file
            index_file = os.path.join(dir_path, "docs", "index.md")
            if os.path.exists(index_file):
                print("\nContents of index.md:")
                with open(index_file) as f:
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
