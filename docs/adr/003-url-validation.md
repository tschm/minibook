# ADR-003: URL Validation Strategy

**Status**: Accepted

**Date**: 2026-01-17

## Context

MiniBook accepts URLs from users to include in generated pages. These URLs need validation for:

1. **Security**: Blocking dangerous schemes like `javascript:`, `data:`, `file:`
2. **Usability**: Catching obvious errors before generation
3. **Flexibility**: Supporting various valid URL formats (IPv6, IDN, auth, etc.)
4. **Performance**: Optional HTTP validation shouldn't slow down generation

We needed to balance strict security with practical usability.

## Decision

We implemented a two-tier URL validation strategy:

### Tier 1: Format Validation (Always On)

Validates URL format and scheme without making network requests:

```python
def validate_url_format(url: str) -> tuple[bool, str | None]:
    """Validate URL format and scheme."""
    if not isinstance(url, str) or not url.strip():
        return False, "URL must be a non-empty string"

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False, f"Invalid URL scheme '{parsed.scheme}'"
    if not parsed.netloc:
        return False, "URL must have a valid host"
    return True, None
```

**Always blocks**:
- `javascript:` - XSS attack vector
- `data:` - Code injection vector
- `file:` - Local file access
- `vbscript:` - Legacy script injection
- Empty/whitespace URLs

**Always allows**:
- Unicode/IDN domains
- IPv6 addresses
- URLs with authentication
- URLs with ports, fragments, query strings

### Tier 2: HTTP Validation (Optional)

When `--validate-links` is specified, makes HEAD requests to verify URLs are accessible:

```python
def validate_url(url, timeout=5, delay=0):
    """Validate if a URL is accessible."""
    response = requests.head(url, timeout=timeout, allow_redirects=True)
    if response.status_code >= 400:
        return False, f"HTTP {response.status_code}"
    return True, None
```

Features:
- **Rate limiting**: `--request-delay` option prevents overwhelming servers
- **Timeout handling**: Configurable timeout (default 5s)
- **Progress bar**: Visual feedback during validation
- **Graceful degradation**: Invalid links generate warnings but don't halt generation

### Return Pattern

Both validation functions return `tuple[bool, str | None]`:
- `(True, None)` - Valid
- `(False, "error message")` - Invalid with reason

This pattern allows clean error handling:

```python
is_valid, error = validate_url_format(url)
if not is_valid:
    warnings.append(f"Skipping {name}: {error}")
```

## Consequences

### Positive

- **Security by Default**: Dangerous schemes always blocked
- **Usability**: Common URL formats work without configuration
- **Performance**: Network validation is opt-in
- **Transparency**: Clear error messages explain why URLs are rejected
- **Flexibility**: Rate limiting prevents abuse

### Negative

- **False Positives**: Some valid schemes (ftp, mailto) are blocked
- **Network Dependency**: HTTP validation requires connectivity
- **Timeout Issues**: Slow servers may cause validation failures

### Neutral

- The scheme whitelist (http, https only) is intentionally restrictive
- Users can skip validation and include any URLs at their own risk

## Alternatives Considered

### Option A: No Validation

Rejected because:
- Security risk from `javascript:` URLs
- Poor user experience when links are broken
- Generated pages could be attack vectors

### Option B: Regex-based Validation

```python
URL_PATTERN = re.compile(r'^https?://...')
```

Rejected because:
- URLs are complex; regex is error-prone
- Python's `urlparse` is more robust
- Hard to maintain and extend

### Option C: Always Validate via HTTP

Rejected because:
- Slow for large link lists
- Requires network connectivity
- Some valid URLs may be temporarily unreachable

### Option D: Allow More Schemes

Supporting `ftp://`, `mailto:`, etc.

Partially rejected because:
- Increases attack surface
- Most use cases need only http/https
- Can be added later if needed

## Testing

URL validation is verified by:

1. **Format Tests**: Valid/invalid URL patterns
2. **Security Tests**: Dangerous schemes blocked
3. **Edge Cases**: Unicode, IPv6, auth URLs
4. **HTTP Tests**: Mock network responses
5. **Property Tests**: Hypothesis-generated URLs
