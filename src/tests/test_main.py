import os
from minibook.main import get_git_repo_url
from unittest.mock import patch


def test_get_git_repo_url_with_environment_variable(monkeypatch):
    """Test get_git_repo_url when GITHUB_REPOSITORY is set in the environment."""
    monkeypatch.setenv("GITHUB_REPOSITORY", "user/repo")
    assert get_git_repo_url() == "https://github.com/user/repo"


def test_get_git_repo_url_without_environment_variable(monkeypatch):
    """Test get_git_repo_url when GITHUB_REPOSITORY is not set in the environment."""
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    assert get_git_repo_url() is None


def test_get_git_repo_url_with_empty_environment_variable(monkeypatch):
    """Test get_git_repo_url when GITHUB_REPOSITORY is set but empty."""
    monkeypatch.setenv("GITHUB_REPOSITORY", "")
    assert get_git_repo_url() is None

def test_get_git_repo_url():
    """Test get_git_repo_url."""
    repo = os.getenv("GITHUB_REPOSITORY")
    assert repo is None, f"Repo is {repo}"

