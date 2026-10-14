"""
Tests for the GitHub API client (offline, mocked).
"""
import json
import unittest.mock as mock
from datetime import datetime, timedelta

import pytest

from trendradar.client.github import GitHubClient, RateLimitError
from trendradar.core.models import Repository


def _make_api_item(
    name: str = "cool-project",
    stars: int = 5000,
    forks: int = 500,
    age_days: int = 30,
) -> dict:
    """Build a fake GitHub Search API repository item."""
    created_at = datetime.utcnow() - timedelta(days=age_days)
    pushed_at = datetime.utcnow()
    return {
        "name": name,
        "full_name": f"user/{name}",
        "html_url": f"https://github.com/user/{name}",
        "description": f"A cool {name} project",
        "stargazers_count": stars,
        "forks_count": forks,
        "open_issues_count": 10,
        "language": "Python",
        "topics": ["ai", "test"],
        "created_at": created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "pushed_at": pushed_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "owner": {"type": "User"},
    }


class TestGitHubClientParsing:
    def test_parse_single_repo(self):
        client = GitHubClient()
        item = _make_api_item(name="my-repo", stars=1000, forks=100)
        repo = client._parse_repo(item)

        assert isinstance(repo, Repository)
        assert repo.name == "my-repo"
        assert repo.full_name == "user/my-repo"
        assert repo.stars == 1000
        assert repo.forks == 100
        assert repo.language == "Python"
        assert "ai" in repo.topics

    def test_parse_repo_with_no_description(self):
        client = GitHubClient()
        item = _make_api_item()
        item["description"] = None
        repo = client._parse_repo(item)
        assert repo.description == ""

    def test_parse_repo_with_no_language(self):
        client = GitHubClient()
        item = _make_api_item()
        item["language"] = None
        repo = client._parse_repo(item)
        assert repo.language is None

    def test_age_days_is_positive(self):
        client = GitHubClient()
        item = _make_api_item(age_days=30)
        repo = client._parse_repo(item)
        assert repo.age_days >= 29  # Allow 1 day of tolerance


class TestGitHubClientSearch:
    def test_search_repositories_uses_correct_url(self):
        client = GitHubClient()
        fake_response = json.dumps({"items": [_make_api_item()], "total_count": 1}).encode()

        with mock.patch.object(client, "_get", return_value={"items": [_make_api_item()], "total_count": 1}) as mock_get:
            repos = client.search_repositories(topic="mcp", limit=5)
            call_url = mock_get.call_args[0][0]
            # URL may be encoded (topic%3Amcp) or plain (topic:mcp) — both are correct
            assert "topic" in call_url and "mcp" in call_url
            assert len(repos) == 1

    def test_search_returns_list_of_repositories(self):
        client = GitHubClient()
        items = [_make_api_item(name=f"repo-{i}", stars=i * 100) for i in range(1, 4)]
        with mock.patch.object(client, "_get", return_value={"items": items}):
            repos = client.search_repositories(topic="llm", limit=10)
            assert len(repos) == 3
            assert all(isinstance(r, Repository) for r in repos)

    def test_no_token_sets_unauthenticated(self):
        client = GitHubClient(token=None)
        import os
        # Ensure GITHUB_TOKEN is not in env for this test
        with mock.patch.dict(os.environ, {}, clear=True):
            c = GitHubClient(token=None)
            assert c.token is None
            assert "Authorization" not in c.headers

    def test_token_sets_authorization_header(self):
        client = GitHubClient(token="ghp_testtoken123")
        assert "Authorization" in client.headers
        assert "ghp_testtoken123" in client.headers["Authorization"]
