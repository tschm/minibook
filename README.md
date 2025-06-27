# 📦 [minibook](https://tschm.github.io/minibook/)

[![PyPI version](https://badge.fury.io/py/minibook.svg)](https://badge.fury.io/py/minibook)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)
[![CI](https://github.com/tschm/minibook/actions/workflows/ci.yml/badge.svg)](https://github.com/tschm/minibook/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/tschm/minibook/badge.svg?branch=main)](https://coveralls.io/github/tschm/minibook?branch=main)
[![Created with qCradle](https://img.shields.io/badge/Created%20with-qCradle-blue?style=flat-square)](https://github.com/tschm/package)

## 📚 MiniBook

MiniBook is a simple tool that creates a minibook
from a list of links. It generates a clean, responsive HTML webpage using Jinja2 templates and Tailwind CSS.

## 📋 Usage

MiniBook can be used to create an HTML page from a list of links.

### Example

Create an HTML page with a custom title and three links:

```bash
minibook --title "My Favorite Sites" \
         --links '{"python": "https://www.python.org", "github": "https://www.github.com", "wikipedia": "https://www.wikipedia.org"}'
```


#### Different JSON Formats for Links

MiniBook supports several JSON formats for the `links' parameter:

1. **Dictionary Format** (used in previous examples):

```bash
minibook --title "My Favorite Sites" \
         --links '{"python": "https://www.python.org", "github": "https://www.github.com", "wikipedia": "https://www.wikipedia.org"}'
```

2. **List of Objects Format**:

```bash
minibook --title "My Favorite Sites" \
         --links '[{"name": "Python", "url": "https://www.python.org"}, {"name": "GitHub", "url": "https://www.github.com"}, {"name": "Wikipedia", "url": "https://www.wikipedia.org"}]'
```

3. **List of Arrays Format**:

```bash
minibook --title "My Favorite Sites" \
         --links '[["Python", "https://www.python.org"], ["GitHub", "https://www.github.com"], ["Wikipedia", "https://www.wikipedia.org"]]'
```

4. **Multi-line JSON Format** (useful in YAML files):

```bash
minibook --title "My Favorite Sites" \
         --links '{
           "Python": "https://www.python.org",
           "GitHub": "https://www.github.com",
           "Wikipedia": "https://www.wikipedia.org"
         }'
```

These formats allow you to specify different names for each link,
rather than using the URL as the name.

#### Validating Links

You can validate that all links are accessible before creating the minibook:

```bash
minibook --title "My Favorite Sites" \
         --links '{"python": "https://www.python.org", "github": "https://www.github.com"}' \
         --validate-links
```

This will check each link to ensure it's accessible.
If any links are invalid, you'll be prompted to continue or abort.

## 🔄 GitHub Action

MiniBook is also available as a GitHub Action that
you can use in your workflows to generate documentation sites.

### Using the Action

To use the MiniBook action in your GitHub workflow:

```yaml
- name: Generate Minibook
  uses: tschm/minibook/.github/actions/book@main
  with:
    title: "My Documentation"
    subtitle: "Documentation for my project"
    links: |
      {
        "GitHub": "https://github.com",
        "Tests": "./tests/index.html",
        "API Reference": "./api/index.html"
      }
```

### Action Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `title` | Title of the minibook | No | "My Links" |
| `subtitle` | Description of the minibook | No | "" |
| `links` | JSON formatted links | Yes | N/A |
| `template` | Path to a custom Jinja2 template file for HTML output | No | "" |

### Complete Example

Here's a complete workflow example that generates a minibook and deploys it to GitHub Pages:

```yaml
name: "Documentation"

on:
  push:
    branches:
      - main

permissions:
  contents: read
  pages: write
  id-token: write

environment:
  name: github-pages

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Generate API docs
        # Your API documentation generation step here
        # This could be another action or custom script

      - name: Generate Minibook and Deploy to GitHub Pages
        uses: tschm/minibook/.github/actions/book@main
        with:
          title: "Project Documentation"
          subtitle: "Documentation and useful links for the project"
          links: |
            {
              "GitHub": "https://github.com/username/repo",
              "API Reference": "./api/index.html",
              "User Guide": "./guide/index.html"
            }
```

## 👥 Contributing

- 🍴 Fork the repository
- 🌿 Create your feature branch (git checkout -b feature/amazing-feature)
- 💾 Commit your changes (git commit -m 'Add some amazing feature')
- 🚢 Push to the branch (git push origin feature/amazing-feature)
- 🔍 Open a Pull Request
