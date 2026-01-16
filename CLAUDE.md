# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

minibook is a Python CLI tool that creates responsive HTML pages from a list of links using Jinja2 templates and Tailwind CSS. It's published on PyPI and available as a GitHub Action.

## Common Commands

```bash
make install        # Create venv and install all dependencies (uses uv)
make test           # Run pytest with coverage reports
make fmt            # Run pre-commit hooks (ruff linting + formatting)
make deptry         # Check dependency usage
```

### Running a Single Test

```bash
.venv/bin/python -m pytest tests/test_minibook.py -v
.venv/bin/python -m pytest tests/test_minibook.py::test_function_name -v
```

### CLI Usage

```bash
minibook --title "Title" --output "output-dir" --links '{"Name": "https://url.com"}'
minibook --validate-links --links '...'  # Validate URLs before generating
```

## Architecture

**Package structure:** `src/minibook/`
- `main.py` - Core module containing CLI app (Typer), HTML generation, JSON parsing, and link validation
- `templates/` - Jinja2 templates (`html.j2` for full template, `bare.j2` for minimal)

**Entry point:** `minibook = "minibook.main:app"`

**Key functions in `main.py`:**
- `generate_html()` - Main HTML generation using Jinja2
- `parse_links_from_json()` - Flexible JSON parsing (supports dict, list of objects, list of arrays)
- `validate_url()` / `validate_link_list()` - HTTP link validation with progress bar

## Code Style

- **Linter/Formatter:** Ruff (line-length 120, target Python 3.11)
- **Rules:** D (pydocstyle), E, F, I (isort), N, W, UP
- **Docstrings:** Google style convention
- **Quote style:** Double quotes

## Testing

- Framework: pytest
- Coverage reports generated in `_tests/html-coverage/`
- Tests live in `tests/` directory

## Project Tooling

- **Package manager:** uv (Astral's Python package manager)
- **Build backend:** Hatchling
- **Python versions:** 3.11, 3.12, 3.13, 3.14
- **CI:** GitHub Actions workflows in `.github/workflows/`
- **Template framework:** Uses jebel-quant/rhiza template (`.rhiza/` directory)
