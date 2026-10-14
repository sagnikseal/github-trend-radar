"""
Star velocity and breakout scoring engine.

Velocity Formula:
    velocity = (stars / max(1, age_days)) * (1 + forks / (stars + 1))

This formula rewards:
  - Rapid star accumulation relative to age (new breakouts score high)
  - Community forks as a multiplier (indicates active builder interest)
"""
from __future__ import annotations

from trendradar.core.models import Repository, VelocityMetrics, VelocityTier


# Thresholds for tier classification (stars per day)
TIER_THRESHOLDS = {
    VelocityTier.BREAKING: 100.0,
    VelocityTier.HIGH: 20.0,
    VelocityTier.RISING: 5.0,
}


def calculate_velocity(repo: Repository) -> VelocityMetrics:
    """
    Calculate star velocity and breakout score for a repository.

    Returns a VelocityMetrics object with tier classification.
    """
    age_days = repo.age_days
    stars_per_day = repo.stars / age_days

    # Fork multiplier: signals active engagement beyond passive starring
    fork_ratio = repo.forks / (repo.stars + 1)
    velocity_score = stars_per_day * (1.0 + fork_ratio)

    tier = _classify_tier(stars_per_day)

    return VelocityMetrics(
        repo=repo,
        stars_per_day=round(stars_per_day, 2),
        velocity_score=round(velocity_score, 2),
        tier=tier,
    )


def _classify_tier(stars_per_day: float) -> VelocityTier:
    """Classify a repository into a velocity tier based on stars/day."""
    for tier, threshold in TIER_THRESHOLDS.items():
        if stars_per_day >= threshold:
            return tier
    return VelocityTier.STEADY


def rank_by_velocity(repos: list[Repository]) -> list[VelocityMetrics]:
    """
    Score and rank a list of repositories by velocity score descending.

    Args:
        repos: List of Repository objects to rank.

    Returns:
        Sorted list of VelocityMetrics, highest velocity first.
    """
    metrics = [calculate_velocity(r) for r in repos]
    return sorted(metrics, key=lambda m: m.velocity_score, reverse=True)
