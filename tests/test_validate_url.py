"""Tests for the validate_url function in the MiniBook package."""

from unittest.mock import MagicMock, patch

import requests

from minibook.main import validate_link_list, validate_url


def test_validate_url_valid():
    """Test the validate_url function with valid URLs."""
    # Mock a successful HEAD request
    mock_response = MagicMock()
    mock_response.status_code = 200

    with patch("requests.head", return_value=mock_response) as mock_head:
        # Test a valid URL
        is_valid, error_message = validate_url("https://www.example.com")

        # Check that the function made a HEAD request
        mock_head.assert_called_once_with("https://www.example.com", timeout=5, allow_redirects=True)

        # Check that the function returned the expected result
        assert is_valid is True
        assert error_message is None


def test_validate_url_invalid_head_valid_get():
    """Test the validate_url function with a URL that fails HEAD but succeeds with GET."""
    # Mock a failed HEAD request
    mock_head_response = MagicMock()
    mock_head_response.status_code = 405  # Method Not Allowed

    # Mock a successful GET request
    mock_get_response = MagicMock()
    mock_get_response.status_code = 200

    with (
        patch("requests.head", return_value=mock_head_response) as mock_head,
        patch("requests.get", return_value=mock_get_response) as mock_get,
    ):
        # Test a URL that fails HEAD but succeeds with GET
        is_valid, error_message = validate_url("https://www.example.com")

        # Check that the function made a HEAD request
        mock_head.assert_called_once_with("https://www.example.com", timeout=5, allow_redirects=True)

        # Check that the function made a GET request
        mock_get.assert_called_once_with("https://www.example.com", timeout=5, allow_redirects=True)

        # Check that the function returned the expected result
        assert is_valid is True
        assert error_message is None


def test_validate_url_invalid():
    """Test the validate_url function with invalid URLs."""
    # Mock a failed HEAD request
    mock_head_response = MagicMock()
    mock_head_response.status_code = 404  # Not Found

    # Mock a failed GET request
    mock_get_response = MagicMock()
    mock_get_response.status_code = 404  # Not Found

    with (
        patch("requests.head", return_value=mock_head_response) as mock_head,
        patch("requests.get", return_value=mock_get_response) as mock_get,
    ):
        # Test an invalid URL
        is_valid, error_message = validate_url("https://www.example.com/nonexistent")

        # Check that the function made a HEAD request
        mock_head.assert_called_once_with("https://www.example.com/nonexistent", timeout=5, allow_redirects=True)

        # Check that the function made a GET request
        mock_get.assert_called_once_with("https://www.example.com/nonexistent", timeout=5, allow_redirects=True)

        # Check that the function returned the expected result
        assert is_valid is False
        assert "HTTP error: 404" in error_message


def test_validate_url_connection_error():
    """Test the validate_url function with a connection error (retried)."""
    # Mock a connection error - with retries, head will be called DEFAULT_RETRIES+1 times
    with (
        patch("requests.head", side_effect=requests.exceptions.ConnectionError("Connection refused")) as mock_head,
        patch("time.sleep"),  # Skip actual sleep during retries
    ):
        # Test a URL that causes a connection error
        is_valid, error_message = validate_url("https://nonexistent.example.com")

        # With DEFAULT_RETRIES=2, head is called 3 times total
        assert mock_head.call_count == 3

        # Check that the function returned the expected result
        assert is_valid is False
        assert error_message == "Connection error"


def test_validate_url_timeout():
    """Test the validate_url function with a timeout error (retried)."""
    # Mock a timeout error - with retries, head will be called DEFAULT_RETRIES+1 times
    with (
        patch("requests.head", side_effect=requests.exceptions.Timeout("Request timed out")) as mock_head,
        patch("time.sleep"),  # Skip actual sleep during retries
    ):
        # Test a URL that causes a timeout
        is_valid, error_message = validate_url("https://slow.example.com")

        # With DEFAULT_RETRIES=2, head is called 3 times total
        assert mock_head.call_count == 3

        # Check that the function returned the expected result
        assert is_valid is False
        assert error_message == "Timeout error"


def test_validate_url_request_exception():
    """Test the validate_url function with a request exception."""
    # Mock a request exception
    with patch("requests.head", side_effect=requests.exceptions.RequestException("Request failed")) as mock_head:
        # Test a URL that causes a request exception
        is_valid, error_message = validate_url("https://example.com")

        # Check that the function made a HEAD request
        mock_head.assert_called_once_with("https://example.com", timeout=5, allow_redirects=True)

        # Check that the function returned the expected result
        assert is_valid is False
        assert error_message == "Request error: Request failed"


def test_validate_url_general_exception():
    """Test the validate_url function with a general exception."""
    # Mock a general exception
    with patch("requests.head", side_effect=Exception("Something went wrong")) as mock_head:
        # Test a URL that causes a general exception
        is_valid, error_message = validate_url("https://example.com")

        # Check that the function made a HEAD request
        mock_head.assert_called_once_with("https://example.com", timeout=5, allow_redirects=True)

        # Check that the function returned the expected result
        assert is_valid is False
        assert error_message == "Unexpected error: Something went wrong"


def test_validate_url_with_delay():
    """Test that the delay parameter causes a sleep before the request."""
    mock_response = MagicMock()
    mock_response.status_code = 200

    with (
        patch("requests.head", return_value=mock_response) as mock_head,
        patch("minibook.main.time.sleep") as mock_sleep,
    ):
        # Test with a delay
        is_valid, error_message = validate_url("https://example.com", delay=0.5)

        # Check that sleep was called with the delay
        mock_sleep.assert_called_once_with(0.5)

        # Check that the request was made
        mock_head.assert_called_once()

        # Check the result
        assert is_valid is True
        assert error_message is None


def test_validate_url_zero_delay_no_sleep():
    """Test that zero delay does not call sleep."""
    mock_response = MagicMock()
    mock_response.status_code = 200

    with (
        patch("requests.head", return_value=mock_response),
        patch("minibook.main.time.sleep") as mock_sleep,
    ):
        # Test with zero delay (default)
        validate_url("https://example.com", delay=0)

        # Sleep should not be called
        mock_sleep.assert_not_called()


def test_validate_link_list_with_delay():
    """Test that validate_link_list passes delay to validate_url."""
    mock_response = MagicMock()
    mock_response.status_code = 200

    link_tuples = [("Link1", "https://example1.com"), ("Link2", "https://example2.com")]

    with (
        patch("requests.head", return_value=mock_response),
        patch("minibook.main.time.sleep") as mock_sleep,
    ):
        all_valid, invalid_links = validate_link_list(link_tuples, delay=0.1)

        # Sleep should be called twice (once for each link)
        assert mock_sleep.call_count == 2
        mock_sleep.assert_called_with(0.1)

        # All links should be valid
        assert all_valid is True
        assert len(invalid_links) == 0
