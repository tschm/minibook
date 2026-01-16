"""Custom exceptions for MiniBook.

This module defines a hierarchy of exceptions for better error handling
and more informative error messages throughout the MiniBook codebase.
"""


class MinibookError(Exception):
    """Base exception for all MiniBook errors.

    All MiniBook-specific exceptions inherit from this class,
    allowing callers to catch all MiniBook errors with a single except clause.

    Examples:
        >>> try:
        ...     raise MinibookError("Something went wrong")
        ... except MinibookError as e:
        ...     print(f"MiniBook error: {e}")
        MiniBook error: Something went wrong
    """

    pass


class ValidationError(MinibookError):
    """Exception raised when input validation fails.

    This exception is raised when user input doesn't meet
    the required format or constraints.

    Attributes:
        field: The name of the field that failed validation
        value: The invalid value that was provided
        message: Description of what went wrong

    Examples:
        >>> raise ValidationError("url", "javascript:alert(1)", "Invalid URL scheme")
        Traceback (most recent call last):
        ...
        minibook.exceptions.ValidationError: Invalid URL scheme (field: url, value: javascript:alert(1))
    """

    def __init__(self, field: str, value: str | None = None, message: str = "Validation failed"):
        self.field = field
        self.value = value
        self.message = message

        if value is not None:
            super().__init__(f"{message} (field: {field}, value: {value})")
        else:
            super().__init__(f"{message} (field: {field})")


class URLValidationError(ValidationError):
    """Exception raised when URL validation fails.

    A specialized validation error for URL-specific issues.

    Examples:
        >>> raise URLValidationError("javascript:alert(1)", "Dangerous URL scheme")
        Traceback (most recent call last):
        ...
        minibook.exceptions.URLValidationError: Dangerous URL scheme (field: url, value: javascript:alert(1))
    """

    def __init__(self, url: str, message: str = "Invalid URL"):
        super().__init__(field="url", value=url, message=message)
        self.url = url


class LinkNameValidationError(ValidationError):
    """Exception raised when link name validation fails.

    Examples:
        >>> raise LinkNameValidationError("", "Link name cannot be empty")
        Traceback (most recent call last):
        ...
        minibook.exceptions.LinkNameValidationError: Link name cannot be empty (field: name, value: )
    """

    def __init__(self, name: str, message: str = "Invalid link name"):
        super().__init__(field="name", value=name, message=message)
        self.name = name


class TemplateError(MinibookError):
    """Exception raised when template operations fail.

    This exception covers template loading, parsing, and rendering errors.

    Attributes:
        template_path: Path to the template that caused the error
        message: Description of what went wrong

    Examples:
        >>> raise TemplateError("/path/to/missing.j2", "Template file not found")
        Traceback (most recent call last):
        ...
        minibook.exceptions.TemplateError: Template file not found: /path/to/missing.j2
    """

    def __init__(self, template_path: str | None = None, message: str = "Template error"):
        self.template_path = template_path

        if template_path:
            super().__init__(f"{message}: {template_path}")
        else:
            super().__init__(message)


class TemplateNotFoundError(TemplateError):
    """Exception raised when a template file cannot be found.

    Examples:
        >>> raise TemplateNotFoundError("/path/to/missing.j2")
        Traceback (most recent call last):
        ...
        minibook.exceptions.TemplateNotFoundError: Template file not found: /path/to/missing.j2
    """

    def __init__(self, template_path: str):
        super().__init__(template_path, "Template file not found")


class PluginError(MinibookError):
    """Exception raised when plugin operations fail.

    This exception covers plugin loading, registration, and execution errors.

    Attributes:
        plugin_name: Name of the plugin that caused the error
        message: Description of what went wrong

    Examples:
        >>> raise PluginError("pdf", "Required dependency fpdf2 not installed")
        Traceback (most recent call last):
        ...
        minibook.exceptions.PluginError: Plugin 'pdf' error: Required dependency fpdf2 not installed
    """

    def __init__(self, plugin_name: str | None = None, message: str = "Plugin error"):
        self.plugin_name = plugin_name

        if plugin_name:
            super().__init__(f"Plugin '{plugin_name}' error: {message}")
        else:
            super().__init__(message)


class PluginNotFoundError(PluginError):
    """Exception raised when a requested plugin is not found.

    Examples:
        >>> raise PluginNotFoundError("unknown_format")
        Traceback (most recent call last):
        ...
        minibook.exceptions.PluginNotFoundError: Plugin 'unknown_format' error: Output format not found
    """

    def __init__(self, plugin_name: str):
        super().__init__(plugin_name, "Output format not found")


class PluginDependencyError(PluginError):
    """Exception raised when a plugin's dependencies are not installed.

    Attributes:
        dependency: The missing dependency name
        install_command: Command to install the dependency

    Examples:
        >>> raise PluginDependencyError("pdf", "fpdf2", "pip install minibook[pdf]")
        Traceback (most recent call last):
        ...
        minibook.exceptions.PluginDependencyError: Plugin 'pdf' error: Missing dependency 'fpdf2'. Install with: pip install minibook[pdf]
    """

    def __init__(self, plugin_name: str, dependency: str, install_command: str | None = None):
        self.dependency = dependency
        self.install_command = install_command

        message = f"Missing dependency '{dependency}'"
        if install_command:
            message += f". Install with: {install_command}"

        super().__init__(plugin_name, message)


class ParseError(MinibookError):
    """Exception raised when parsing input fails.

    This exception is raised when JSON or other input formats cannot be parsed.

    Attributes:
        input_type: The type of input being parsed (e.g., "JSON", "YAML")
        message: Description of what went wrong

    Examples:
        >>> raise ParseError("JSON", "Invalid JSON syntax")
        Traceback (most recent call last):
        ...
        minibook.exceptions.ParseError: Failed to parse JSON: Invalid JSON syntax
    """

    def __init__(self, input_type: str = "input", message: str = "Parse error"):
        self.input_type = input_type
        super().__init__(f"Failed to parse {input_type}: {message}")


class JSONParseError(ParseError):
    """Exception raised when JSON parsing fails.

    Examples:
        >>> raise JSONParseError("Unexpected token at position 5")
        Traceback (most recent call last):
        ...
        minibook.exceptions.JSONParseError: Failed to parse JSON: Unexpected token at position 5
    """

    def __init__(self, message: str = "Invalid JSON"):
        super().__init__("JSON", message)


class OutputError(MinibookError):
    """Exception raised when output generation fails.

    Attributes:
        output_path: Path where output was being written
        message: Description of what went wrong

    Examples:
        >>> raise OutputError("/output/file.html", "Permission denied")
        Traceback (most recent call last):
        ...
        minibook.exceptions.OutputError: Failed to write output to /output/file.html: Permission denied
    """

    def __init__(self, output_path: str | None = None, message: str = "Output error"):
        self.output_path = output_path

        if output_path:
            super().__init__(f"Failed to write output to {output_path}: {message}")
        else:
            super().__init__(message)
