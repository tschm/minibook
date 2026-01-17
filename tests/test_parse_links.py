"""Tests for link parsing functions."""

import json

import pytest

from minibook.main import parse_links_from_json


def test_parse_links_from_json_list_of_dicts():
    """Test parsing JSON list of dictionaries."""
    json_str = (
        '[{"name": "Python", "url": "https://www.python.org"}, {"name": "GitHub", "url": "https://www.github.com"}]'
    )
    result, warnings = parse_links_from_json(json_str)
    assert result == [("Python", "https://www.python.org"), ("GitHub", "https://www.github.com")]
    assert warnings == []


def test_parse_links_from_json_list_of_arrays():
    """Test parsing JSON list of arrays."""
    json_str = '[["Python", "https://www.python.org"], ["GitHub", "https://www.github.com"]]'
    result, warnings = parse_links_from_json(json_str)
    assert result == [("Python", "https://www.python.org"), ("GitHub", "https://www.github.com")]
    assert warnings == []


def test_parse_links_from_json_dictionary():
    """Test parsing JSON dictionary."""
    json_str = '{"Python": "https://www.python.org", "GitHub": "https://www.github.com"}'
    result, warnings = parse_links_from_json(json_str)
    # Dictionary order is preserved in Python 3.7+
    assert result == [("Python", "https://www.python.org"), ("GitHub", "https://www.github.com")]
    assert warnings == []


def test_parse_links_from_json_with_whitespace():
    """Test parsing JSON with leading/trailing whitespace."""
    json_str = '  {"Python": "https://www.python.org"}  '
    result, warnings = parse_links_from_json(json_str)
    assert result == [("Python", "https://www.python.org")]
    assert warnings == []


def test_parse_links_from_json_invalid_json():
    """Test parsing invalid JSON raises JSONDecodeError."""
    json_str = "not valid json"
    with pytest.raises(json.JSONDecodeError):
        parse_links_from_json(json_str)


def test_parse_links_from_json_empty_list():
    """Test parsing empty list."""
    json_str = "[]"
    result, warnings = parse_links_from_json(json_str)
    assert result == []
    assert warnings == []


def test_parse_links_from_json_empty_dict():
    """Test parsing empty dictionary."""
    json_str = "{}"
    result, warnings = parse_links_from_json(json_str)
    assert result == []
    assert warnings == []


def test_parse_links_from_json_list_of_dicts_missing_keys():
    """Test parsing JSON list of dictionaries with missing keys."""
    json_str = '[{"name": "Python", "url": "https://www.python.org"}, {"name": "GitHub"}]'
    result, warnings = parse_links_from_json(json_str)
    # Only the first item should be parsed, second one is missing "url" key
    assert result == [("Python", "https://www.python.org")]
    assert len(warnings) == 1
    assert "missing 'name' or 'url' key" in warnings[0]


def test_parse_links_from_json_list_of_arrays_short():
    """Test parsing JSON list of arrays that are too short."""
    json_str = '[["Python", "https://www.python.org"], ["GitHub"]]'
    result, warnings = parse_links_from_json(json_str)
    # Only the first array should be parsed, second one has only 1 element
    assert result == [("Python", "https://www.python.org")]
    assert len(warnings) == 1
    assert "at least 2 elements" in warnings[0]
