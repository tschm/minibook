"""Pytest configuration for benchmark tests.

This file can be used to add custom fixtures or configuration
for your benchmark tests.

Security Notes:
- S101 (assert usage): Asserts are appropriate in test code for validating conditions
- S603/S607 (subprocess usage): Any subprocess calls use controlled inputs in test environments
"""


def pytest_html_report_title(report):
    """Set the HTML report title."""
    report.title = "Benchmark Tests"
