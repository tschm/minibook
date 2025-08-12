"""Tests for the validate_url function in the MiniBook package."""

from unittest.mock import MagicMock, patch

import requests

from minibook.main import validate_url


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
    """Test the validate_url function with a connection error."""
    # Mock a connection error
    with patch("requests.head", side_effect=requests.exceptions.ConnectionError("Connection refused")) as mock_head:
        # Test a URL that causes a connection error
        is_valid, error_message = validate_url("https://nonexistent.example.com")

        # Check that the function made a HEAD request
        mock_head.assert_called_once_with("https://nonexistent.example.com", timeout=5, allow_redirects=True)

        # Check that the function returned the expected result
        assert is_valid is False
        assert error_message == "Connection error"


def test_validate_url_timeout():
    """Test the validate_url function with a timeout error."""
    # Mock a timeout error
    with patch("requests.head", side_effect=requests.exceptions.Timeout("Request timed out")) as mock_head:
        # Test a URL that causes a timeout
        is_valid, error_message = validate_url("https://slow.example.com")

        # Check that the function made a HEAD request
        mock_head.assert_called_once_with("https://slow.example.com", timeout=5, allow_redirects=True)

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
