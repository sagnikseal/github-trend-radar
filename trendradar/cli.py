"""
CLI entry point for GitHub Trend Radar.

Commands:
    trendradar scan [--topic TOPIC] [--limit N]
    trendradar velocity [--topic TOPIC] [--limit N]
    trendradar ideas [--niche NICHE] [--difficulty LEVEL]
    trendradar export [--output FILE] [--all]
    trendradar status
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

from rich.console import Console

from trendradar.client.github import DEMAND_TOPICS, GitHubClient, RateLimitError
from trendradar.core.incubator import generate_ideas
from trendradar.core.models import Difficulty, TrendReport
from trendradar.core.velocity import rank_by_velocity
from trendradar.renderers.markdown import generate_html_dashboard, generate_markdown
from trendradar.renderers.terminal import (
    console,
    print_banner,
    print_ideas,
    print_rate_limit,
    print_velocity_table,
)

console = Console()


def cmd_scan(args: argparse.Namespace) -> None:
    """Run a live scan for a specific topic."""
    client = GitHubClient()
    topic = args.topic
    limit = args.limit

    with console.status(f"[cyan]Scanning GitHub for topic: [bold]{topic}[/bold]…[/cyan]"):
        try:
            repos = client.search_repositories(topic=topic, limit=limit)
        except RateLimitError as e:
            console.print(f"[red]Error:[/red] {e}")
            sys.exit(1)

    ranked = rank_by_velocity(repos)
    report = TrendReport(
        generated_at=datetime.utcnow(),
        topic=topic,
        repositories=ranked,
        total_scanned=len(repos),
    )
    print_velocity_table(report)

    rl = client.check_rate_limit()
    print_rate_limit(rl)


def cmd_velocity(args: argparse.Namespace) -> None:
    """Rank repositories by star velocity for a topic."""
    # velocity is currently an alias for scan with the same logic
    cmd_scan(args)


def cmd_ideas(args: argparse.Namespace) -> None:
    """Show project ideas from the incubator."""
    difficulty = None
    if args.difficulty:
        try:
            difficulty = Difficulty(args.difficulty.capitalize())
        except ValueError:
            console.print(f"[red]Invalid difficulty:[/red] {args.difficulty}. "
                          "Choose from: Beginner, Intermediate, Advanced.")
            sys.exit(1)

    ideas = generate_ideas(
        niche_filter=args.niche,
        difficulty_filter=difficulty,
        limit=args.limit,
    )

    if not ideas:
        console.print("[yellow]No ideas found matching those filters.[/yellow]")
        return

    print_ideas(ideas)


def cmd_export(args: argparse.Namespace) -> None:
    """Export trend data to Markdown and/or HTML dashboard."""
    client = GitHubClient()
    topics_to_scan = list(DEMAND_TOPICS.keys()) if args.all else [args.topic]
    limit = args.limit

    reports: list[TrendReport] = []
    for topic in topics_to_scan:
        with console.status(f"[cyan]Scanning topic: [bold]{topic}[/bold]…[/cyan]"):
            try:
                repos = client.search_repositories(topic=topic, limit=limit)
                ranked = rank_by_velocity(repos)
                reports.append(TrendReport(
                    generated_at=datetime.utcnow(),
                    topic=topic,
                    repositories=ranked,
                    total_scanned=len(repos),
                ))
            except RateLimitError as e:
                console.print(f"[yellow]Skipping {topic}:[/yellow] {e}")
                continue

    ideas = generate_ideas(limit=10)

    # Write Markdown
    md_path = Path(args.output)
    md_content = generate_markdown(reports, ideas)
    md_path.write_text(md_content, encoding="utf-8")
    console.print(f"[green]✓[/green] Markdown written to [bold]{md_path}[/bold]")

    # Write HTML dashboard to docs/
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    html_path = docs_dir / "index.html"
    html_content = generate_html_dashboard(reports, ideas)
    html_path.write_text(html_content, encoding="utf-8")
    console.print(f"[green]✓[/green] HTML dashboard written to [bold]{html_path}[/bold]")

    # Write JSON data for external consumption
    data_path = docs_dir / "data.json"
    import json
    data = {
        "generated_at": datetime.utcnow().isoformat(),
        "reports": [
            {
                "topic": r.topic,
                "total_scanned": r.total_scanned,
                "repositories": [
                    {
                        "name": m.repo.full_name,
                        "url": m.repo.url,
                        "stars": m.repo.stars,
                        "forks": m.repo.forks,
                        "stars_per_day": m.stars_per_day,
                        "velocity_score": m.velocity_score,
                        "tier": m.tier.value,
                        "language": m.repo.language,
                    }
                    for m in r.repositories
                ],
            }
            for r in reports
        ],
    }
    data_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    console.print(f"[green]✓[/green] JSON data written to [bold]{data_path}[/bold]")


def cmd_status(args: argparse.Namespace) -> None:
    """Show GitHub API rate limit status."""
    client = GitHubClient()
    info = client.check_rate_limit()
    auth_label = "[green]Authenticated[/green]" if info["authenticated"] else "[yellow]Unauthenticated[/yellow]"
    console.print(f"\n[bold]GitHub API Status[/bold]")
    console.print(f"  Mode      : {auth_label}")
    console.print(f"  Remaining : {info['remaining']} / {info['limit']}")
    console.print(f"  Resets at : {info['reset_at']}")
    if not info["authenticated"]:
        console.print(
            "\n[dim]Tip: Set [bold]GITHUB_TOKEN[/bold] env variable to increase limits to 5,000/hr.[/dim]\n"
            "[dim]Get a free token at: https://github.com/settings/tokens[/dim]"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trendradar",
        description="📡 GitHub Trend Radar — Real-time demand intelligence & project incubator",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- scan ---
    p_scan = subparsers.add_parser("scan", help="Scan GitHub for trending repositories by topic")
    p_scan.add_argument("--topic", "-t", default="mcp", help="GitHub topic to scan (default: mcp)")
    p_scan.add_argument("--limit", "-l", type=int, default=20, help="Max repositories to fetch (default: 20)")
    p_scan.set_defaults(func=cmd_scan)

    # --- velocity ---
    p_vel = subparsers.add_parser("velocity", help="Rank repositories by star velocity")
    p_vel.add_argument("--topic", "-t", default="llm", help="GitHub topic to rank (default: llm)")
    p_vel.add_argument("--limit", "-l", type=int, default=20, help="Max repositories (default: 20)")
    p_vel.set_defaults(func=cmd_velocity)

    # --- ideas ---
    p_ideas = subparsers.add_parser("ideas", help="Browse project ideas from the incubator")
    p_ideas.add_argument("--niche", "-n", default=None, help="Filter by demand niche (e.g. 'MCP')")
    p_ideas.add_argument("--difficulty", "-d", default=None,
                         help="Filter by difficulty: beginner, intermediate, advanced")
    p_ideas.add_argument("--limit", "-l", type=int, default=8, help="Max ideas to show (default: 8)")
    p_ideas.set_defaults(func=cmd_ideas)

    # --- export ---
    p_export = subparsers.add_parser("export", help="Export trends to Markdown and HTML dashboard")
    p_export.add_argument("--output", "-o", default="TRENDS.md", help="Markdown output file (default: TRENDS.md)")
    p_export.add_argument("--topic", "-t", default="mcp", help="Topic when not using --all (default: mcp)")
    p_export.add_argument("--limit", "-l", type=int, default=15, help="Repos per topic (default: 15)")
    p_export.add_argument("--all", "-a", action="store_true", help="Scan all curated demand topics")
    p_export.set_defaults(func=cmd_export)

    # --- status ---
    p_status = subparsers.add_parser("status", help="Show GitHub API rate limit status")
    p_status.set_defaults(func=cmd_status)

    return parser


def main() -> None:
    print_banner()
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
