"""Test cases for the main module."""

import configparser
from os import getenv
from pathlib import Path
from unittest.mock import patch

from minibook.main import get_git_repo_url, validate_url


def test_get_git_repo_url_with_environment_variable(monkeypatch):
    """Test get_git_repo_url when GITHUB_REPOSITORY is set in the environment."""
    monkeypatch.setenv("GITHUB_REPOSITORY", "user/repo")
    assert get_git_repo_url() == "https://github.com/user/repo"


def test_get_git_repo_url_without_environment_variable(monkeypatch):
    """Test get_git_repo_url when GITHUB_REPOSITORY is not set in the environment."""
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    assert get_git_repo_url() == "https://github.com/tschm/minibook"


def test_get_git_repo_url():
    """Test get_git_repo_url."""
    repo = getenv("GITHUB_REPOSITORY", default="tschm/minibook")
    assert repo == "tschm/minibook"


def test_get_git_repo_url_from_git_config_https(monkeypatch, tmp_path):
    """Test get_git_repo_url reads HTTPS remote URL from .git/config."""
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)

    # Create a fake .git/config with an HTTPS remote URL
    git_config = tmp_path / "git_config"
    cfg = configparser.ConfigParser()
    cfg['remote "origin"'] = {"url": "https://github.com/owner/myrepo.git"}
    with git_config.open("w") as f:
        cfg.write(f)

    with patch("minibook.main.Path") as mock_path_cls:

        def side_effect(arg):
            if arg == ".git/config":
                return git_config
            return Path.__new__(Path, arg)

        mock_path_cls.side_effect = side_effect
        result = get_git_repo_url()

    assert result == "https://github.com/owner/myrepo"


def test_get_git_repo_url_from_git_config_ssh_url(monkeypatch, tmp_path):
    """Test get_git_repo_url normalizes SSH remote URL from .git/config to HTTPS."""
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)

    # Create a fake .git/config with an SSH remote URL
    git_config = tmp_path / "git_config"
    cfg = configparser.ConfigParser()
    cfg['remote "origin"'] = {"url": "git@github.com:owner/myrepo.git"}
    with git_config.open("w") as f:
        cfg.write(f)

    with patch("minibook.main.Path") as mock_path_cls:

        def side_effect(arg):
            if arg == ".git/config":
                return git_config
            return Path.__new__(Path, arg)

        mock_path_cls.side_effect = side_effect
        result = get_git_repo_url()

    assert result == "https://github.com/owner/myrepo"


def test_get_git_repo_url_fallback_on_exception(monkeypatch):
    """Test get_git_repo_url falls back to hardcoded default when git config raises."""
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)

    with patch("minibook.main.configparser.ConfigParser") as mock_cfg:
        mock_cfg.side_effect = OSError("permission denied")
        result = get_git_repo_url()

    assert result == "https://github.com/tschm/minibook"


def test_validate_url_relative_path_exists(tmp_path):
    """Test validate_url returns True for a relative path that exists."""
    # Create a temporary file
    test_file = tmp_path / "report.html"
    test_file.write_text("<html></html>")

    is_valid, error = validate_url(str(test_file))
    assert is_valid is True
    assert error is None


def test_validate_url_relative_path_not_found():
    """Test validate_url returns False for a relative path that does not exist."""
    is_valid, error = validate_url("./nonexistent/path/report.html")
    assert is_valid is False
    assert "Relative path not accessible" in error
    assert "nonexistent" in error


def test_validate_url_relative_path_with_delay(tmp_path):
    """Test that delay is respected for relative path validation."""
    test_file = tmp_path / "index.html"
    test_file.write_text("<html></html>")

    with patch("minibook.main.time.sleep") as mock_sleep:
        is_valid, _error = validate_url(str(test_file), delay=0.1)
        mock_sleep.assert_called_once_with(0.1)
        assert is_valid is True
