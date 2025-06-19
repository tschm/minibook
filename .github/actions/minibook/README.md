# Minibook Action

This GitHub Action creates a minibook from a list of links. It supports both HTML and MkDocs output formats.

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `title` | Title of the minibook | No | "My Links" |
| `description` | Description of the minibook | No | "" |
| `output` | Output file or directory | No | "minibook.html" |
| `links` | Comma-separated list of tuples with (name;url) | Yes | N/A |
| `format` | Output format: html or mkdocs | No | "html" |
| `timestamp` | Fixed timestamp for testing purposes | No | "" |

## Usage

### Basic Example

```yaml
- name: Create HTML Minibook
  uses: ./.github/actions/minibook
  with:
    title: "My Favorite Links"
    description: "A collection of my favorite websites"
    output: "minibook.html"
    format: "html"
    links: "GitHub;https://github.com,Python;https://python.org"
```

### MkDocs Example

```yaml
- name: Create MkDocs Minibook
  uses: ./.github/actions/minibook
  with:
    title: "My Documentation"
    description: "Documentation for my project"
    output: "docs"
    format: "mkdocs"
    links: "GitHub;https://github.com,Python;https://python.org"
```

## Outputs

The action creates a minibook file (HTML) or directory (MkDocs) at the specified output path.

## Example Workflow

```yaml
name: "Create Minibook"

on:
  push:
    branches:
      - main

jobs:
  create-minibook:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Create HTML Minibook
        uses: ./.github/actions/minibook
        with:
          title: "My Links"
          description: "A collection of useful links"
          output: "minibook.html"
          format: "html"
          links: "GitHub;https://github.com,Python;https://python.org"

      - name: Upload Minibook
        uses: actions/upload-artifact@v3
        with:
          name: minibook
          path: minibook.html
```