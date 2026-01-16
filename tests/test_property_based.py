"""Property-based tests using Hypothesis for the MiniBook package."""

import json
import string

from hypothesis import given, settings
from hypothesis import strategies as st

from minibook.main import (
    parse_links_from_json,
    validate_link_name,
    validate_url_format,
)


# Strategy for generating valid HTTP/HTTPS URLs
valid_url_strategy = st.builds(
    lambda scheme, domain, path: f"{scheme}://{domain}.com{path}",
    scheme=st.sampled_from(["http", "https"]),
    domain=st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=20),
    path=st.text(alphabet=string.ascii_lowercase + "/", min_size=0, max_size=30).map(
        lambda s: "/" + s if s else ""
    ),
)

# Strategy for generating invalid URL schemes
invalid_scheme_strategy = st.sampled_from(
    ["javascript:alert(1)", "data:text/html,test", "file:///etc/passwd", "ftp://example.com"]
)

# Strategy for generating valid link names
valid_name_strategy = st.text(min_size=1, max_size=100).filter(lambda s: s.strip())


class TestValidateUrlFormatProperty:
    """Property-based tests for validate_url_format function."""

    @given(url=valid_url_strategy)
    @settings(max_examples=100)
    def test_valid_urls_always_pass(self, url):
        """Valid HTTP/HTTPS URLs should always pass validation."""
        is_valid, error = validate_url_format(url)
        assert is_valid is True
        assert error is None

    @given(scheme=invalid_scheme_strategy)
    @settings(max_examples=50)
    def test_invalid_schemes_always_fail(self, scheme):
        """Invalid URL schemes should always fail validation."""
        is_valid, error = validate_url_format(scheme)
        assert is_valid is False
        assert error is not None

    @given(text=st.text(min_size=0, max_size=10))
    @settings(max_examples=100)
    def test_empty_or_whitespace_fails(self, text):
        """Empty or whitespace-only strings should fail validation."""
        if not text.strip():
            is_valid, error = validate_url_format(text)
            assert is_valid is False
            assert "non-empty string" in error

    @given(value=st.one_of(st.none(), st.integers(), st.floats(), st.lists(st.text())))
    @settings(max_examples=50)
    def test_non_string_types_fail(self, value):
        """Non-string types should fail validation."""
        is_valid, error = validate_url_format(value)
        assert is_valid is False


class TestValidateLinkNameProperty:
    """Property-based tests for validate_link_name function."""

    @given(name=valid_name_strategy)
    @settings(max_examples=100)
    def test_non_empty_strings_pass(self, name):
        """Non-empty strings should pass validation."""
        is_valid, error = validate_link_name(name)
        assert is_valid is True
        assert error is None

    @given(text=st.text(alphabet=" \t\n\r", min_size=0, max_size=20))
    @settings(max_examples=50)
    def test_whitespace_only_fails(self, text):
        """Whitespace-only strings should fail validation."""
        is_valid, error = validate_link_name(text)
        assert is_valid is False

    @given(value=st.one_of(st.none(), st.integers(), st.floats()))
    @settings(max_examples=50)
    def test_non_string_types_fail(self, value):
        """Non-string types should fail validation."""
        is_valid, error = validate_link_name(value)
        assert is_valid is False


class TestParseLinksProperty:
    """Property-based tests for parse_links_from_json function."""

    @given(
        links=st.dictionaries(
            keys=st.text(min_size=1, max_size=50).filter(lambda s: s.strip()),
            values=valid_url_strategy,
            min_size=1,
            max_size=10,
        )
    )
    @settings(max_examples=50)
    def test_dict_format_parses_correctly(self, links):
        """Dictionary format should parse all valid entries."""
        json_str = json.dumps(links)
        result, warnings = parse_links_from_json(json_str)

        # All valid links should be parsed
        assert len(result) == len(links)
        assert len(warnings) == 0

        # Check that all links are present
        result_dict = dict(result)
        for name, url in links.items():
            assert name in result_dict
            assert result_dict[name] == url

    @given(
        links=st.lists(
            st.tuples(
                st.text(min_size=1, max_size=50).filter(lambda s: s.strip()),
                valid_url_strategy,
            ),
            min_size=1,
            max_size=10,
        )
    )
    @settings(max_examples=50)
    def test_list_of_arrays_format_parses_correctly(self, links):
        """List of arrays format should parse all valid entries."""
        json_str = json.dumps(links)
        result, warnings = parse_links_from_json(json_str)

        # All valid links should be parsed
        assert len(result) == len(links)
        assert len(warnings) == 0

    @given(
        links=st.lists(
            st.fixed_dictionaries(
                {
                    "name": st.text(min_size=1, max_size=50).filter(lambda s: s.strip()),
                    "url": valid_url_strategy,
                }
            ),
            min_size=1,
            max_size=10,
        )
    )
    @settings(max_examples=50)
    def test_list_of_objects_format_parses_correctly(self, links):
        """List of objects format should parse all valid entries."""
        json_str = json.dumps(links)
        result, warnings = parse_links_from_json(json_str)

        # All valid links should be parsed
        assert len(result) == len(links)
        assert len(warnings) == 0

    @given(
        valid_links=st.dictionaries(
            keys=st.text(min_size=1, max_size=50).filter(lambda s: s.strip()),
            values=valid_url_strategy,
            min_size=0,
            max_size=5,
        ),
        invalid_count=st.integers(min_value=1, max_value=5),
    )
    @settings(max_examples=30)
    def test_mixed_valid_invalid_links(self, valid_links, invalid_count):
        """Mixed valid and invalid links should produce appropriate warnings."""
        # Add some invalid links
        mixed_links = dict(valid_links)
        for i in range(invalid_count):
            mixed_links[f"invalid_{i}"] = "javascript:alert(1)"

        json_str = json.dumps(mixed_links)
        result, warnings = parse_links_from_json(json_str)

        # Only valid links should be in result
        assert len(result) == len(valid_links)
        # Warnings should be generated for invalid links
        assert len(warnings) == invalid_count
