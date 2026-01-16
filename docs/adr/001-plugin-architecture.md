# ADR-001: Plugin Architecture for Output Formats

**Status**: Accepted

**Date**: 2026-01-17

## Context

MiniBook was originally designed to generate only HTML output. As the project evolved, users requested support for additional output formats such as Markdown, JSON, PDF, RST, EPUB, and AsciiDoc.

We needed to decide how to support multiple output formats:

1. **Option A**: Add format-specific code directly to `main.py`
2. **Option B**: Create a plugin system with a common interface
3. **Option C**: Use separate CLI commands for each format

## Decision

We chose **Option B**: Implement a plugin architecture with a common `OutputPlugin` base class.

### Key Design Elements

1. **Abstract Base Class**: All plugins inherit from `OutputPlugin` which defines:
   - `name`: Unique identifier (e.g., "html", "json")
   - `extension`: File extension (e.g., ".html", ".json")
   - `description`: Human-readable description
   - `generate()`: Abstract method for output generation

2. **Plugin Registry**: A `PLUGINS` dictionary maps format names to plugin classes:
   ```python
   PLUGINS = {
       "html": HTMLPlugin,
       "markdown": MarkdownPlugin,
       "md": MarkdownPlugin,  # Alias
       ...
   }
   ```

3. **Lazy Imports**: Plugins with optional dependencies (PDF, EPUB) import their libraries only when `generate()` is called, keeping core dependencies minimal.

4. **CLI Integration**: The `--format` option selects the output format at runtime.

## Consequences

### Positive

- **Extensibility**: New formats can be added by creating a single class
- **Consistency**: All formats follow the same interface
- **Maintainability**: Format-specific code is isolated in dedicated classes
- **Optional Dependencies**: Users only need to install dependencies for formats they use
- **Testability**: Each plugin can be tested independently

### Negative

- **Complexity**: More code than a simple if/else chain
- **Discovery**: Users must know available formats (mitigated by `--help`)
- **Single File**: All built-in plugins are in one file (`plugins.py`)

### Neutral

- Future work could split plugins into separate files with entry-point-based discovery
- External plugins could be supported via Python entry points

## Alternatives Considered

### Option A: Direct Code in main.py

```python
if format == "html":
    generate_html(...)
elif format == "json":
    generate_json(...)
```

Rejected because:
- Leads to a large, hard-to-maintain main module
- No clear interface for adding new formats
- Harder to test individual formats

### Option C: Separate CLI Commands

```bash
minibook-html ...
minibook-json ...
```

Rejected because:
- Inconsistent user experience
- Code duplication for argument parsing
- Harder to maintain multiple entry points
