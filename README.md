# 📦 [minibook](https://tschm.github.io/minibook/book)

[![PyPI version](https://badge.fury.io/py/minibook.svg)](https://badge.fury.io/py/minibook)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)
[![CI](https://github.com/tschm/minibook/actions/workflows/ci.yml/badge.svg)](https://github.com/tschm/minibook/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/tschm/minibook/badge.svg?branch=main)](https://coveralls.io/github/tschm/minibook?branch=main)
[![Created with qCradle](https://img.shields.io/badge/Created%20with-qCradle-blue?style=flat-square)](https://github.com/tschm/package)

## 📚 MiniBook

MiniBook is a simple tool that creates a minibook
from a list of links. It supports two different output formats:

1. **HTML** - A clean, responsive webpage using Jinja2 templates and Tailwind CSS
2. **MkDocs** - A complete MkDocs project structure
that can be built into a static site

## 🚀 Getting Started

### **🔧 Set Up Environment**

```bash
make install
```

This installs/updates [uv](https://github.com/astral-sh/uv),
creates your virtual environment and installs dependencies.

For adding or removing packages:

```bash
uv add/remove requests  # for main dependencies
uv add/remove requests --dev  # for dev dependencies
```

### **✅ Configure Pre-commit Hooks**

```bash
make fmt
```

Installs hooks to maintain code quality and formatting.

### **📝 Update Project Info**

- Edit `pyproject.toml` to update authors and email addresses
- Configure GitHub Pages (branch: gh-pages) in repository settings

## 📋 Usage

MiniBook can be used to create either an HTML page
or a MkDocs project from a list of links.

### Examples

#### HTML Output

Create an HTML page with a custom title and three links:

```bash
minibook --title "My Favorite Sites" \
         --format html \
         --links '{"python": "https://www.python.org", "github": "https://www.github.com", "wikipedia": "https://www.wikipedia.org"}'
```

#### MkDocs Output

Create a MkDocs project with a custom title and three links:

```bash
minibook --title "My Favorite Sites" \
         --format mkdocs \
         --output minibook_site \
         --links '{"python": "https://www.python.org", "github": "https://www.github.com", "wikipedia": "https://www.wikipedia.org"}'
```

After generating the MkDocs project, you can build and serve it using MkDocs:

```bash
cd minibook_site
mkdocs build  # Build the site
mkdocs serve  # Serve the site locally at http://127.0.0.1:8000/
```

#### Using Links Tuples

You can also provide links as tuples with custom names for each link:

```bash
minibook --title "My Favorite Sites" \
         --links '[{"name": "Python", "url": "https://www.python.org"}, {"name": "GitHub", "url": "https://www.github.com"}, {"name": "Wikipedia", "url": "https://www.wikipedia.org"}]'
```

This allows you to specify a different name for
each link, rather than using the URL as the name.

#### Validating Links

You can validate that all links are accessible before creating the minibook:

```bash
minibook --title "My Favorite Sites" \
         --links '{"python": "https://www.python.org", "github": "https://www.github.com"}' \
         --validate-links
```

This will check each link to ensure it's accessible. If any links are invalid, you'll be prompted to continue or abort.

## 🛠️ Development Commands

```bash
make tests   # Run test suite
make marimo  # Start Marimo notebooks
```

## 👥 Contributing

- 🍴 Fork the repository
- 🌿 Create your feature branch (git checkout -b feature/amazing-feature)
- 💾 Commit your changes (git commit -m 'Add some amazing feature')
- 🚢 Push to the branch (git push origin feature/amazing-feature)
- 🔍 Open a Pull Request
