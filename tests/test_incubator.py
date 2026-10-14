"""
Tests for the project idea incubator.
"""
import pytest

from trendradar.core.incubator import generate_ideas
from trendradar.core.models import Difficulty, ProjectIdea


class TestGenerateIdeas:
    def test_returns_ideas(self):
        ideas = generate_ideas()
        assert len(ideas) > 0

    def test_respects_limit(self):
        ideas = generate_ideas(limit=3)
        assert len(ideas) <= 3

    def test_all_ideas_have_required_fields(self):
        ideas = generate_ideas()
        for idea in ideas:
            assert idea.title
            assert idea.demand_niche
            assert idea.description
            assert len(idea.suggested_stack) > 0
            assert idea.portfolio_value
            assert isinstance(idea.difficulty, Difficulty)

    def test_niche_filter(self):
        ideas = generate_ideas(niche_filter="MCP")
        for idea in ideas:
            assert "mcp" in idea.demand_niche.lower()

    def test_niche_filter_case_insensitive(self):
        ideas_upper = generate_ideas(niche_filter="MCP")
        ideas_lower = generate_ideas(niche_filter="mcp")
        assert len(ideas_upper) == len(ideas_lower)

    def test_difficulty_filter_beginner(self):
        ideas = generate_ideas(difficulty_filter=Difficulty.BEGINNER)
        for idea in ideas:
            assert idea.difficulty == Difficulty.BEGINNER

    def test_difficulty_filter_advanced(self):
        ideas = generate_ideas(difficulty_filter=Difficulty.ADVANCED)
        for idea in ideas:
            assert idea.difficulty == Difficulty.ADVANCED

    def test_nonexistent_niche_returns_empty(self):
        ideas = generate_ideas(niche_filter="XXXXXXXXNONEXISTENT")
        assert ideas == []

    def test_combined_filters(self):
        ideas = generate_ideas(niche_filter="Local AI", difficulty_filter=Difficulty.INTERMEDIATE)
        for idea in ideas:
            assert "local ai" in idea.demand_niche.lower()
            assert idea.difficulty == Difficulty.INTERMEDIATE
