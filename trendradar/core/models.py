"""
Core data models for GitHub Trend Radar.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class VelocityTier(str, Enum):
    """Tier classification based on repository momentum."""
    BREAKING = "🚀 BREAKING"
    HIGH = "⚡ HIGH VELOCITY"
    RISING = "📈 RISING"
    STEADY = "➡️  STEADY"


class Difficulty(str, Enum):
    """Estimated difficulty for building a project idea."""
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"


@dataclass
class Repository:
    """Represents a GitHub repository with metadata."""
    name: str
    full_name: str
    url: str
    description: str
    stars: int
    forks: int
    open_issues: int
    language: Optional[str]
    topics: list[str]
    created_at: datetime
    pushed_at: datetime
    owner_type: str = "User"  # "User" or "Organization"

    @property
    def age_days(self) -> float:
        """Number of days since the repository was created."""
        delta = datetime.utcnow() - self.created_at
        return max(1.0, delta.total_seconds() / 86400)


@dataclass
class VelocityMetrics:
    """Computed velocity and momentum metrics for a repository."""
    repo: Repository
    stars_per_day: float
    velocity_score: float
    tier: VelocityTier

    @property
    def tier_label(self) -> str:
        return self.tier.value


@dataclass
class TrendReport:
    """A complete trend analysis report."""
    generated_at: datetime
    topic: str
    repositories: list[VelocityMetrics]
    total_scanned: int


@dataclass
class ProjectIdea:
    """An actionable personal project idea derived from trending demand."""
    title: str
    demand_niche: str
    description: str
    suggested_stack: list[str]
    difficulty: Difficulty
    portfolio_value: str
    related_trending_repos: list[str] = field(default_factory=list)
    why_it_matters: str = ""
