"""Test cases for the main module."""

from os import getenv

from minibook.main import get_git_repo_url


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
