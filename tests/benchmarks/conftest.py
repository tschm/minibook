"""Fixtures for benchmark tests."""

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for benchmark output files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def small_link_list():
    """Generate a small list of links (10 items)."""
    return [(f"Link {i}", f"https://example{i}.com") for i in range(10)]


@pytest.fixture
def medium_link_list():
    """Generate a medium list of links (50 items)."""
    return [(f"Link {i}", f"https://example{i}.com") for i in range(50)]


@pytest.fixture
def large_link_list():
    """Generate a large list of links (200 items)."""
    return [(f"Link {i}", f"https://example{i}.com") for i in range(200)]


@pytest.fixture
def extra_large_link_list():
    """Generate an extra large list of links (500 items)."""
    return [(f"Link {i}", f"https://example{i}.com") for i in range(500)]
