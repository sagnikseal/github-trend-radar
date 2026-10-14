"""
Rate-limit resilient GitHub REST API client.

Works out of the box without a token (60 req/hr).
Set GITHUB_TOKEN environment variable to upgrade to 5,000 req/hr.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime
from typing import Any

from trendradar.core.models import Repository


BASE_URL = "https://api.github.com"

# Curated high-demand topics aligned with current GitHub trends
DEMAND_TOPICS: dict[str, str] = {
    "mcp": "Model Context Protocol",
    "ai-agent": "AI Agents & Autonomy",
    "browser-use": "Browser Automation AI",
    "llm": "Large Language Models",
    "local-ai": "Local AI Runtimes",
    "rag": "Retrieval-Augmented Generation",
    "self-hosted": "Self-Hosted SaaS",
    "developer-tools": "Developer Tooling",
    "autonomous-agent": "Autonomous Agents",
    "langchain": "LangChain Ecosystem",
}


class RateLimitError(Exception):
    """Raised when GitHub API rate limit is exceeded."""
    pass


class GitHubClient:
    """
    Lightweight GitHub API client with automatic rate-limit handling
    and optional GITHUB_TOKEN authentication.
    """

    def __init__(self, token: str | None = None) -> None:
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self._request_count = 0

    @property
    def headers(self) -> dict[str, str]:
        h = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "github-trend-radar/1.0",
        }
        if self.token:
            h["Authorization"] = f"token {self.token}"
        return h

    def _get(self, url: str, retries: int = 3) -> Any:
        """Make a GET request with exponential backoff on rate limits."""
        req = urllib.request.Request(url, headers=self.headers)
        for attempt in range(retries):
            try:
                with urllib.request.urlopen(req, timeout=15) as resp:
                    self._request_count += 1
                    return json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                if e.code == 403:
                    wait = 2 ** (attempt + 2)
                    print(f"  ⏳ Rate limited. Waiting {wait}s before retry...")
                    time.sleep(wait)
                elif e.code == 422:
                    raise ValueError(f"Invalid query for URL: {url}") from e
                else:
                    raise
        raise RateLimitError(
            "GitHub API rate limit exceeded. Set GITHUB_TOKEN env variable to increase limits.\n"
            "  Get a free token at: https://github.com/settings/tokens"
        )

    def check_rate_limit(self) -> dict[str, Any]:
        """Return current API rate limit status."""
        data = self._get(f"{BASE_URL}/rate_limit")
        core = data.get("resources", {}).get("search", {})
        return {
            "limit": core.get("limit", 0),
            "remaining": core.get("remaining", 0),
            "reset_at": datetime.utcfromtimestamp(core.get("reset", 0)).strftime("%H:%M UTC"),
            "authenticated": self.token is not None,
        }

    def search_repositories(
        self,
        topic: str,
        min_stars: int = 50,
        limit: int = 30,
    ) -> list[Repository]:
        """Search GitHub repositories by topic, ordered by stars."""
        query = f"topic:{topic} stars:>={min_stars}"
        url = (
            f"{BASE_URL}/search/repositories"
            f"?q={urllib.parse.quote(query)}"
            f"&sort=stars&order=desc&per_page={min(limit, 100)}"
        )
        data = self._get(url)
        repos = []
        for item in data.get("items", [])[:limit]:
            try:
                repo = self._parse_repo(item)
                repos.append(repo)
            except (KeyError, ValueError):
                continue
        return repos

    def search_repositories_by_query(
        self,
        query: str,
        limit: int = 30,
    ) -> list[Repository]:
        """Search GitHub repositories by raw query string."""
        import urllib.parse
        url = (
            f"{BASE_URL}/search/repositories"
            f"?q={urllib.parse.quote(query)}"
            f"&sort=stars&order=desc&per_page={min(limit, 100)}"
        )
        data = self._get(url)
        repos = []
        for item in data.get("items", [])[:limit]:
            try:
                repo = self._parse_repo(item)
                repos.append(repo)
            except (KeyError, ValueError):
                continue
        return repos

    def _parse_repo(self, item: dict[str, Any]) -> Repository:
        """Parse a raw GitHub API repository item into a Repository model."""
        def parse_dt(s: str) -> datetime:
            return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")

        return Repository(
            name=item["name"],
            full_name=item["full_name"],
            url=item["html_url"],
            description=item.get("description") or "",
            stars=item.get("stargazers_count", 0),
            forks=item.get("forks_count", 0),
            open_issues=item.get("open_issues_count", 0),
            language=item.get("language"),
            topics=item.get("topics", []),
            created_at=parse_dt(item["created_at"]),
            pushed_at=parse_dt(item["pushed_at"]),
            owner_type=item.get("owner", {}).get("type", "User"),
        )


# Make urllib.parse available within this module
import urllib.parse  # noqa: E402 (moved to avoid circular)
