"""
Tests for the velocity scoring engine.
"""
from datetime import datetime, timedelta

import pytest

from trendradar.core.models import Repository, VelocityTier
from trendradar.core.velocity import calculate_velocity, rank_by_velocity, _classify_tier


def make_repo(
    name: str = "test/repo",
    stars: int = 1000,
    forks: int = 100,
    age_days: int = 10,
) -> Repository:
    """Create a test Repository with configurable parameters."""
    created_at = datetime.utcnow() - timedelta(days=age_days)
    return Repository(
        name=name.split("/")[1],
        full_name=name,
        url=f"https://github.com/{name}",
        description="Test repo",
        stars=stars,
        forks=forks,
        open_issues=5,
        language="Python",
        topics=["test"],
        created_at=created_at,
        pushed_at=datetime.utcnow(),
    )


class TestClassifyTier:
    def test_breaking_threshold(self):
        assert _classify_tier(150.0) == VelocityTier.BREAKING

    def test_high_threshold(self):
        assert _classify_tier(50.0) == VelocityTier.HIGH

    def test_rising_threshold(self):
        assert _classify_tier(10.0) == VelocityTier.RISING

    def test_steady_threshold(self):
        assert _classify_tier(1.0) == VelocityTier.STEADY

    def test_exact_breaking_boundary(self):
        assert _classify_tier(100.0) == VelocityTier.BREAKING

    def test_just_below_breaking(self):
        assert _classify_tier(99.9) == VelocityTier.HIGH


class TestCalculateVelocity:
    def test_stars_per_day_calculation(self):
        repo = make_repo(stars=1000, age_days=10)
        metrics = calculate_velocity(repo)
        assert metrics.stars_per_day == pytest.approx(100.0, rel=0.01)

    def test_fork_multiplier_increases_velocity(self):
        repo_no_forks = make_repo(stars=1000, forks=0, age_days=10)
        repo_with_forks = make_repo(stars=1000, forks=500, age_days=10)
        m_no = calculate_velocity(repo_no_forks)
        m_with = calculate_velocity(repo_with_forks)
        assert m_with.velocity_score > m_no.velocity_score

    def test_very_new_repo_doesnt_divide_by_zero(self):
        """Repos created today should still produce valid metrics."""
        repo = make_repo(age_days=0)
        metrics = calculate_velocity(repo)
        assert metrics.velocity_score > 0

    def test_old_low_star_repo_is_steady(self):
        repo = make_repo(stars=100, forks=5, age_days=365)
        metrics = calculate_velocity(repo)
        assert metrics.tier == VelocityTier.STEADY

    def test_breaking_repo(self):
        repo = make_repo(stars=50000, forks=5000, age_days=3)
        metrics = calculate_velocity(repo)
        assert metrics.tier == VelocityTier.BREAKING


class TestRankByVelocity:
    def test_ranking_order(self):
        repos = [
            make_repo("a/slow", stars=1000, forks=50, age_days=365),
            make_repo("b/fast", stars=5000, forks=500, age_days=5),
            make_repo("c/medium", stars=2000, forks=200, age_days=30),
        ]
        ranked = rank_by_velocity(repos)
        # Fastest should be first
        assert ranked[0].repo.full_name == "b/fast"

    def test_empty_list(self):
        assert rank_by_velocity([]) == []

    def test_single_repo(self):
        repos = [make_repo(stars=100, age_days=10)]
        ranked = rank_by_velocity(repos)
        assert len(ranked) == 1
