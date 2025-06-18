# 📦 [minibook](https://tschm.github.io/minibook/book)

[![PyPI version](https://badge.fury.io/py/minibook.svg)](https://badge.fury.io/py/minibook)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)
[![CI](https://github.com/tschm/minibook/actions/workflows/ci.yml/badge.svg)](https://github.com/tschm/minibook/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/tschm/minibook/badge.svg?branch=main)](https://coveralls.io/github/tschm/minibook?branch=main)
[![Created with qCradle](https://img.shields.io/badge/Created%20with-qCradle-blue?style=flat-square)](https://github.com/tschm/package)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/tschm/minibook)

## 📚 MiniBook

MiniBook is a simple tool that creates a minibook from a list of links. It supports two different output formats:

1. **HTML** - A clean, responsive webpage using Jinja2 templates and Tailwind CSS
2. **MkDocs** - A complete MkDocs project structure that can be built into a static site

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

MiniBook can be used to create either an HTML page or a MkDocs project from a list of links.

### Command-line Arguments

```bash
./run_minibook.py [-h] [-t TITLE] [-d DESCRIPTION] [-o OUTPUT] [-l LINKS [LINKS ...]] [--format {html,mkdocs}]
```

Arguments:
- `-h, --help`: Show the help message and exit
- `-t, --title TITLE`: Title of the minibook (default: "My Links")
- `-d, --description DESCRIPTION`: Description of the minibook
- `-o, --output OUTPUT`: Output file or directory (default: "minibook.html")
- `-l, --links LINKS [LINKS ...]`: List of URLs (space-separated)
- `--format {html,mkdocs}`: Output format: html or mkdocs (default: html)

### Interactive Mode

If you don't provide links via command-line arguments, MiniBook will enter interactive mode, allowing you to enter links one by one:

```bash
./run_minibook.py
```

Then follow the prompts to enter your links.

### Examples

#### HTML Output

Create an HTML page with a custom title and three links:

```bash
./run_minibook.py --title "My Favorite Sites" --format html --links https://www.python.org https://www.github.com https://www.wikipedia.org
```

#### MkDocs Output

Create a MkDocs project with a custom title and three links:

```bash
./run_minibook.py --title "My Favorite Sites" --format mkdocs --output minibook_site --links https://www.python.org https://www.github.com https://www.wikipedia.org
```

After generating the MkDocs project, you can build and serve it using MkDocs:

```bash
cd minibook_site
mkdocs build  # Build the site
mkdocs serve  # Serve the site locally at http://127.0.0.1:8000/
```

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

## ⚠️ Trusted publishing failure

That's good news!

You are not able to publish to PyPI unless you have registered your project
on PyPI. You get the following message:

```bash
Trusted publishing exchange failure:

Token request failed: the server refused the request for
the following reasons:

invalid-publisher: valid token, but no corresponding
publisher (All lookup strategies exhausted)
This generally indicates a trusted publisher
configuration error, but could
also indicate an internal error on GitHub or PyPI's part.

The claims rendered below are for debugging purposes only.
You should not
use them to configure a trusted publisher unless they
already match your expectations.
```

Please register your repository. The 'release.yml' flow is
publishing from the 'release' environment. Once you have
registered your new repo it should all work.
