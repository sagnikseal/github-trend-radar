"""
Project Idea Incubator.

Analyzes high-demand GitHub topics and generates actionable personal project
blueprints complete with tech stack recommendations, difficulty ratings,
and portfolio value explanations.
"""
from __future__ import annotations

from trendradar.core.models import Difficulty, ProjectIdea


# Curated database of high-impact project ideas mapped to trending demand niches
_IDEA_DATABASE: list[ProjectIdea] = [
    ProjectIdea(
        title="Personal MCP Server for Obsidian Notes",
        demand_niche="Model Context Protocol (MCP)",
        description=(
            "Build a FastMCP server that exposes your local Obsidian markdown vault "
            "to any MCP-compatible AI client (Claude Desktop, Cursor, Windsurf). "
            "Enables semantic search, note creation, and daily summary generation via AI."
        ),
        suggested_stack=["Python", "FastMCP", "Pydantic", "Jinja2"],
        difficulty=Difficulty.INTERMEDIATE,
        portfolio_value=(
            "MCP is the hottest topic on GitHub right now. A well-documented MCP server "
            "demonstrates your ability to work with cutting-edge AI infrastructure standards."
        ),
        related_trending_repos=["modelcontextprotocol/servers", "FastMCP"],
        why_it_matters="MCP is becoming the universal plugin API for AI clients — similar to how REST shaped web APIs.",
    ),
    ProjectIdea(
        title="Browser Automation Agent for Job Applications",
        demand_niche="Browser Automation AI",
        description=(
            "A browser-use powered agent that reads job descriptions from LinkedIn/Indeed, "
            "auto-fills application forms, tracks submission status in a local SQLite database, "
            "and generates tailored cover letters using an LLM."
        ),
        suggested_stack=["Python", "browser-use", "SQLite", "OpenAI/Ollama"],
        difficulty=Difficulty.INTERMEDIATE,
        portfolio_value=(
            "Combines two of GitHub's top trending categories: browser automation and LLM agents. "
            "Highly relatable use case that resonates with recruiters and developers alike."
        ),
        related_trending_repos=["browser-use/browser-use"],
        why_it_matters="Autonomous browser agents are replacing click-heavy workflows. This project demonstrates agentic AI application development.",
    ),
    ProjectIdea(
        title="Local RAG Knowledge Base with Ollama",
        demand_niche="Local AI Runtimes",
        description=(
            "A fully offline, privacy-first knowledge base that indexes your PDFs, markdown files, "
            "and web pages. Uses Ollama to run local embeddings and an open-source LLM to answer "
            "questions over your personal documents without sending data to any cloud."
        ),
        suggested_stack=["Python", "Ollama", "ChromaDB", "LlamaIndex", "Streamlit"],
        difficulty=Difficulty.INTERMEDIATE,
        portfolio_value=(
            "Demonstrates deep understanding of RAG architecture, vector databases, and local AI "
            "inference — all three topics in the top 10 GitHub search terms."
        ),
        related_trending_repos=["ollama/ollama", "chroma-core/chroma"],
        why_it_matters="Privacy-first local AI is one of the fastest growing GitHub segments, driven by enterprise and personal data sovereignty concerns.",
    ),
    ProjectIdea(
        title="GitHub Contribution Art Generator",
        demand_niche="Developer Tooling",
        description=(
            "A CLI tool that generates a custom contribution graph pattern on your GitHub profile "
            "by scheduling and making commits at precise dates. Takes an ASCII art pattern as input "
            "and calculates the exact commit history required to render it."
        ),
        suggested_stack=["Python", "GitPython", "Rich", "Click"],
        difficulty=Difficulty.BEGINNER,
        portfolio_value=(
            "Extremely shareable and viral on Twitter/LinkedIn. Shows creative use of git internals, "
            "CLI design, and scheduling — while improving your own GitHub profile aesthetics."
        ),
        related_trending_repos=["github-profile-readme-generator"],
        why_it_matters="Fun + technical = high engagement. Projects like these go viral in developer communities and generate significant organic GitHub stars.",
    ),
    ProjectIdea(
        title="Self-Hosted Personal Dashboard (Coolify Alternative Lite)",
        demand_niche="Self-Hosted SaaS",
        description=(
            "A minimal self-hosted dashboard for tracking your deployed personal projects, "
            "uptime status, and deployment logs. Containerized with Docker Compose, supports "
            "webhook-based auto-deploy from GitHub Actions pushes."
        ),
        suggested_stack=["FastAPI", "Vue.js", "Docker Compose", "SQLite", "GitHub Actions"],
        difficulty=Difficulty.ADVANCED,
        portfolio_value=(
            "Full-stack deployment showcase combining backend API design, frontend UI, containerization, "
            "and CI/CD automation in one repository — the holy grail of portfolio projects."
        ),
        related_trending_repos=["coollabsio/coolify", "louislam/uptime-kuma"],
        why_it_matters="Self-hosted infrastructure tooling is GitHub's #4 demand category. Building in this space positions you alongside the fastest-growing OSS projects.",
    ),
    ProjectIdea(
        title="AI Code Review Bot for GitHub PRs",
        demand_niche="AI Agents & Autonomy",
        description=(
            "A GitHub App that automatically reviews Pull Requests using an LLM, comments on "
            "potential bugs, style issues, and security vulnerabilities, and summarizes the diff "
            "in plain English. Deployable as a GitHub Action with GITHUB_TOKEN authentication."
        ),
        suggested_stack=["Python", "PyGitHub", "OpenAI/Anthropic API", "GitHub Actions", "FastAPI"],
        difficulty=Difficulty.ADVANCED,
        portfolio_value=(
            "Demonstrates real-world agentic AI integration with GitHub APIs, webhook handling, "
            "and production deployment — exactly what companies building AI developer tools seek."
        ),
        related_trending_repos=["coderabbitai/coderabbit", "sourcegraph/cody"],
        why_it_matters="AI-powered code review is a multi-billion dollar market. Building an open-source version demonstrates enterprise-grade thinking.",
    ),
    ProjectIdea(
        title="Terminal Portfolio Site Generator",
        demand_niche="Developer Tooling",
        description=(
            "A CLI that generates a beautiful, interactive terminal-style portfolio website "
            "from a simple YAML config file. Deployed to GitHub Pages with a typewriter effect, "
            "ASCII art header, and command-line navigation for visitors."
        ),
        suggested_stack=["Python", "Rich", "Jinja2", "GitHub Pages", "JavaScript"],
        difficulty=Difficulty.BEGINNER,
        portfolio_value=(
            "Meta-portfolio: your tool generates portfolios, and the tool itself is in your portfolio. "
            "Highly visual, easy for recruiters to understand, and immediately shareable."
        ),
        related_trending_repos=["codecrafters-io/build-your-own-x"],
        why_it_matters="Portfolio tools are consistently among GitHub's most-forked repositories because every developer needs one.",
    ),
    ProjectIdea(
        title="Open-Source Voice Meeting Assistant",
        demand_niche="Local AI Runtimes",
        description=(
            "A local-first meeting transcription and summarizer using OpenAI Whisper for real-time "
            "speech-to-text, a local LLM (via Ollama) to extract action items, and a simple web UI "
            "to review meeting summaries — all without sending audio to any cloud service."
        ),
        suggested_stack=["Python", "Whisper", "Ollama", "FastAPI", "React"],
        difficulty=Difficulty.ADVANCED,
        portfolio_value=(
            "Addresses one of the top use cases for local AI (meeting privacy) while showcasing "
            "audio processing, streaming inference, and full-stack web development."
        ),
        related_trending_repos=["openai/whisper", "ollama/ollama"],
        why_it_matters="Local audio AI tools are the fastest-growing segment in the local-AI niche, driven by remote work and data compliance requirements.",
    ),
]


def generate_ideas(
    niche_filter: str | None = None,
    difficulty_filter: Difficulty | None = None,
    limit: int = 10,
) -> list[ProjectIdea]:
    """
    Generate actionable project ideas, optionally filtered by niche or difficulty.

    Args:
        niche_filter: Case-insensitive substring match on demand_niche.
        difficulty_filter: Exact difficulty level to filter by.
        limit: Maximum number of ideas to return.

    Returns:
        List of ProjectIdea objects.
    """
    ideas = list(_IDEA_DATABASE)

    if niche_filter:
        ideas = [i for i in ideas if niche_filter.lower() in i.demand_niche.lower()]

    if difficulty_filter:
        ideas = [i for i in ideas if i.difficulty == difficulty_filter]

    return ideas[:limit]
