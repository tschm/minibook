# ADR-002: Security: CSP and Jinja2 Autoescape

**Status**: Accepted

**Date**: 2026-01-17

## Context

MiniBook generates HTML pages that may include user-provided content (titles, link names, descriptions). This creates potential security vulnerabilities:

1. **Cross-Site Scripting (XSS)**: Malicious content in link names could execute JavaScript
2. **Content Injection**: Attackers could inject HTML to alter page appearance
3. **Inline Script Risks**: The generated page includes inline scripts for theme toggling

We needed security measures that:
- Prevent XSS attacks from user input
- Allow legitimate functionality (theme toggle, styling)
- Follow modern web security best practices
- Work without requiring a web server (static HTML files)

## Decision

We implemented a defense-in-depth security strategy with two primary mechanisms:

### 1. Jinja2 Autoescape

Enable autoescape for all HTML-like templates:

```python
env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=select_autoescape(
        enabled_extensions=("html", "htm", "xml", "j2", "jinja", "jinja2"),
        default=True
    ),
)
```

This automatically HTML-escapes all template variables, converting:
- `<` to `&lt;`
- `>` to `&gt;`
- `&` to `&amp;`
- `"` to `&quot;`

### 2. Content Security Policy (CSP) with Nonces

Generate a unique nonce for each page render:

```python
nonce = secrets.token_urlsafe(16)
```

Include CSP meta tag in generated HTML:

```html
<meta http-equiv="Content-Security-Policy" content="
    default-src 'self';
    script-src 'self' https://cdn.tailwindcss.com 'nonce-{{ nonce }}';
    style-src 'self' https://fonts.googleapis.com 'nonce-{{ nonce }}';
    font-src https://fonts.gstatic.com;
    img-src 'self' data:;
    base-uri 'self';
    form-action 'self'
">
```

### 3. Subresource Integrity (SRI)

External scripts include SRI hashes:

```html
<script src="https://cdn.tailwindcss.com/3.4.17"
        integrity="sha384-..."
        crossorigin="anonymous"></script>
```

## Consequences

### Positive

- **XSS Prevention**: User input is automatically escaped
- **Defense in Depth**: Multiple security layers protect against attacks
- **No unsafe-inline**: CSP blocks inline scripts without valid nonces
- **CDN Protection**: SRI prevents tampered CDN resources from executing
- **Modern Standards**: Follows OWASP security recommendations

### Negative

- **Nonce Management**: Each render needs a unique nonce
- **CSP Complexity**: Strict CSP can break custom templates if not configured correctly
- **Browser Support**: Older browsers may not fully support CSP Level 2

### Neutral

- Custom templates must use the `nonce` variable for inline scripts/styles
- The CSP allows specific CDN hosts (Tailwind, Google Fonts)

## Alternatives Considered

### Option A: No Security (Rely on User Trust)

Rejected because:
- Any user input could become an attack vector
- Generated HTML might be served publicly
- Violates secure-by-default principles

### Option B: Sanitization Instead of Escaping

```python
from bleach import clean
sanitized = clean(user_input, tags=[], strip=True)
```

Rejected because:
- More complex than autoescape
- Risk of incomplete sanitization
- Jinja2 autoescape is battle-tested

### Option C: CSP without Nonces (Hash-based)

```html
script-src 'sha256-...'
```

Rejected because:
- Requires pre-computing hashes of all inline scripts
- Any script change requires hash update
- Less flexible than nonces

## Security Testing

The implementation is verified by:

1. **XSS Tests**: Verify `<script>` tags in user input are escaped
2. **CSP Tests**: Verify nonce presence and uniqueness
3. **SRI Tests**: Verify integrity attributes on CDN scripts
4. **Input Validation Tests**: Verify dangerous URL schemes are blocked
