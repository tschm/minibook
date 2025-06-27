# 📦 [minibook](https://tschm.github.io/minibook/)

[![PyPI version](https://badge.fury.io/py/minibook.svg)](https://badge.fury.io/py/minibook)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
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
         --output "artifacts" \
         --links '{"python": "https://www.python.org", "github": "https://www.github.com", "wikipedia": "https://www.wikipedia.org"}'
```


#### Different JSON Formats for Links

MiniBook supports several JSON formats for the `links` parameter:

1. **Dictionary Format** (used in previous examples):

```bash
minibook --title "My Favorite Sites" \
         --output "artifacts" \
         --links '{"python": "https://www.python.org", "github": "https://www.github.com", "wikipedia": "https://www.wikipedia.org"}'
```

2. **List of Objects Format**:

```bash
minibook --title "My Favorite Sites" \
         --output "artifacts" \
         --links '[{"name": "Python", "url": "https://www.python.org"}, {"name": "GitHub", "url": "https://www.github.com"}, {"name": "Wikipedia", "url": "https://www.wikipedia.org"}]'
```

3. **List of Arrays Format**:

```bash
minibook --title "My Favorite Sites" \
         --output "artifacts" \
         --links '[["Python", "https://www.python.org"], ["GitHub", "https://www.github.com"], ["Wikipedia", "https://www.wikipedia.org"]]'
```

4. **Multi-line JSON Format** (useful in YAML files):

```bash
minibook --title "My Favorite Sites" \
         --output "artifacts" \
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
         --output "artifacts" \
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
| `output` | Output directory for generated files | No | "artifacts" |

### Complete Example

When using this action with GitHub Pages, you must set
the following permissions in your workflow:

- `contents: read`: To read repository contents
- `pages: write`: To deploy to GitHub Pages
- `id-token: write`: For authentication during deployment

You must also set the environment to `github-pages` for GitHub Pages deployment:

Here's a complete workflow example that generates a minibook and deploys it to GitHub Pages:

```yaml
# Workflow name - appears in the GitHub Actions UI
name: "Documentation"

# Trigger configuration - when should this workflow run
on:
  push:
    branches:
      - main  # Run only when changes are pushed to the main branch

# Permissions required for GitHub Pages deployment
permissions:
  contents: read  # Read access to repository contents
  pages: write    # Write access to GitHub Pages
  id-token: write # Write access to OIDC token for authentication

# Environment configuration for GitHub Pages
environment:
  name: github-pages  # Predefined GitHub Pages environment

# Jobs that make up this workflow
jobs:
  # Job to run tests and generate test reports
  test:
    runs-on: ubuntu-latest  # Use the latest Ubuntu runner
    steps:
      # Step 1: Check out the repository code
      - name: Checkout repository
        uses: actions/checkout@v4  # Official GitHub checkout action

      # Step 2: Run your test suite
      - name: Run tests
        # Your test execution step here
        # This could be another action or custom script
        # Example: run pytest, jest, or other test frameworks

      # Step 3: Upload test results as an artifact for later use
      - name: Upload test results
        uses: actions/upload-artifact@v4  # Official GitHub artifact upload action
        with:
          name: test-results  # Name of the artifact
          path: tests/        # Directory containing test results to upload

  # Job to generate API documentation
  pdoc:
    runs-on: ubuntu-latest  # Use the latest Ubuntu runner
    steps:
      # Step 1: Check out the repository code
      - name: Checkout repository
        uses: actions/checkout@v4  # Official GitHub checkout action

      # Step 2: Generate API documentation
      - name: Generate API docs
        # Your API documentation generation step here
        # This could be pdoc3, Sphinx, JSDoc, or other documentation tools
        # Example: pdoc --html --output-dir pdoc/ your_package/

      # Step 3: Upload API documentation as an artifact for later use
      - name: Upload API documentation
        uses: actions/upload-artifact@v4  # Official GitHub artifact upload action
        with:
          name: api-docs  # Name of the artifact
          path: pdoc/     # Directory containing API docs to upload

  # Job to build and publish the book documentation
  book:
    runs-on: ubuntu-latest  # Use the latest Ubuntu runner
    needs: [test, pdoc]     # This job will only run after test and pdoc jobs complete successfully
    steps:
      # Generate Minibook and Deploy to GitHub Pages
      # The book action automatically downloads all artifacts from the jobs defined in needs
      - name: Generate Minibook and Deploy to GitHub Pages
        uses: tschm/minibook/.github/actions/book@main  # Use the minibook action
        with:
          # Title that appears at the top of the generated page
          title: "Project Documentation"
          # Subtitle/description that appears below the title
          subtitle: "Documentation and useful links for the project"
          # JSON object defining links to include in the minibook
          # Each key is the link text, and each value is the URL
          links: |
            {
              "GitHub": "https://github.com/username/repo",
              "API Reference": "./artifacts/api-docs/index.html",  # Link to the API docs artifact
              "Test Results": "./artifacts/test-results/html-report/report.html"  # Link to the test results artifact
            }
```

## 👥 Contributing

- 🍴 Fork the repository
- 🌿 Create your feature branch (git checkout -b feature/amazing-feature)
- 💾 Commit your changes (git commit -m 'Add some amazing feature')
- 🚢 Push to the branch (git push origin feature/amazing-feature)
- 🔍 Open a Pull Request
