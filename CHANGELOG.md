# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Content Security Policy headers in generated HTML
- Rate limiting for URL validation (`--request-delay` option)
- This changelog

## [1.1.0] - 2026-01-02

### Added
- Input validation to prevent XSS attacks (URL scheme whitelist)
- Comprehensive package metadata in pyproject.toml
- PyPI downloads and CodeFactor badges

### Changed
- Refactored entrypoint into smaller focused functions
- Improved Jinja2 autoescape configuration

### Security
- Block javascript:, data:, and file: URL schemes

## [1.0.2] - 2025-09

### Fixed
- Relative screenshot link for PyPI documentation

## [1.0.1] - 2025-08

### Added
- Quickstart section with screenshot in README
- CodeQL security analysis workflow

### Security
- Fixed incomplete URL sanitization (code scanning alert #17)
- Improved href attribute validation in tests

## [1.0.0] - 2025-06

### Added
- Initial production release
- HTML page generation from JSON link lists
- Multiple JSON input formats (dict, list of objects, list of arrays)
- Link validation with progress bars
- Jinja2 template customization
- Tailwind CSS with dark/light theme toggle
- GitHub Action for CI/CD integration
