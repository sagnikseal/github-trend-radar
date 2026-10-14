"""
Rich terminal renderer for GitHub Trend Radar.

Provides beautiful console output with velocity badges, color-coded tables,
and formatted project idea cards.
"""
from __future__ import annotations

from datetime import datetime

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import print as rprint

from trendradar.core.models import (
    ProjectIdea,
    TrendReport,
    VelocityMetrics,
    VelocityTier,
)

console = Console()

# Color mapping for velocity tiers
TIER_COLORS: dict[VelocityTier, str] = {
    VelocityTier.BREAKING: "bold red",
    VelocityTier.HIGH: "bold yellow",
    VelocityTier.RISING: "bold green",
    VelocityTier.STEADY: "dim white",
}

DIFFICULTY_COLORS = {
    "Beginner": "green",
    "Intermediate": "yellow",
    "Advanced": "red",
}


def print_banner() -> None:
    """Print the GitHub Trend Radar ASCII banner."""
    banner = """
[bold cyan]  ██████╗ ██╗████████╗██╗  ██╗██╗   ██╗██████╗     ██████╗  █████╗ ██████╗  █████╗ ██████╗ [/bold cyan]
[bold cyan] ██╔════╝ ██║╚══██╔══╝██║  ██║██║   ██║██╔══██╗    ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗[/bold cyan]
[bold cyan] ██║  ███╗██║   ██║   ███████║██║   ██║██████╔╝    ██████╔╝███████║██║  ██║███████║██████╔╝[/bold cyan]
[bold cyan] ██║   ██║██║   ██║   ██╔══██║██║   ██║██╔══██╗    ██╔══██╗██╔══██║██║  ██║██╔══██║██╔══██╗[/bold cyan]
[bold cyan] ╚██████╔╝██║   ██║   ██║  ██║╚██████╔╝██████╔╝    ██║  ██║██║  ██║██████╔╝██║  ██║██║  ██║[/bold cyan]
[bold cyan]  ╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝[/bold cyan]
"""
    console.print(banner)
    console.print(
        Panel(
            "[bold white]Real-time GitHub demand intelligence & personal project incubator[/bold white]\n"
            "[dim]Identify breakout niches before they peak · Find your next portfolio project[/dim]",
            border_style="cyan",
        )
    )


def print_velocity_table(report: TrendReport) -> None:
    """Render a rich table of velocity-ranked repositories."""
    table = Table(
        title=f"[bold cyan]📡 GitHub Trend Radar: {report.topic.upper()}[/bold cyan]\n"
              f"[dim]Scanned {report.total_scanned} repositories · Generated {report.generated_at.strftime('%Y-%m-%d %H:%M UTC')}[/dim]",
        box=box.ROUNDED,
        border_style="cyan",
        show_header=True,
        header_style="bold magenta",
        expand=True,
    )

    table.add_column("#", style="dim", width=3)
    table.add_column("Repository", style="bold white", no_wrap=True, min_width=25)
    table.add_column("Velocity", justify="center", width=18)
    table.add_column("⭐ Stars", justify="right", width=10)
    table.add_column("🍴 Forks", justify="right", width=8)
    table.add_column("Stars/Day", justify="right", width=10)
    table.add_column("Language", width=12)
    table.add_column("Description", no_wrap=False, min_width=30)

    for idx, metric in enumerate(report.repositories, 1):
        repo = metric.repo
        tier_color = TIER_COLORS[metric.tier]
        tier_text = Text(metric.tier_label, style=tier_color)

        lang = repo.language or "—"
        desc = (repo.description[:60] + "…") if len(repo.description) > 60 else repo.description

        table.add_row(
            str(idx),
            f"[link={repo.url}]{repo.full_name}[/link]",
            tier_text,
            f"{repo.stars:,}",
            f"{repo.forks:,}",
            f"{metric.stars_per_day:.1f}",
            lang,
            desc or "[dim]No description[/dim]",
        )

    console.print(table)


def print_ideas(ideas: list[ProjectIdea]) -> None:
    """Render project idea cards in the terminal."""
    console.print("\n[bold cyan]💡 Project Idea Incubator[/bold cyan]\n")

    for idx, idea in enumerate(ideas, 1):
        diff_color = DIFFICULTY_COLORS.get(idea.difficulty.value, "white")
        stack_str = " · ".join(f"[bold]{s}[/bold]" for s in idea.suggested_stack)

        content = (
            f"[bold yellow]{idx}. {idea.title}[/bold yellow]\n"
            f"[dim]Niche:[/dim] [cyan]{idea.demand_niche}[/cyan]   "
            f"[dim]Difficulty:[/dim] [{diff_color}]{idea.difficulty.value}[/{diff_color}]\n\n"
            f"{idea.description}\n\n"
            f"[dim]Stack:[/dim] {stack_str}\n\n"
            f"[dim]📈 Why it matters:[/dim] {idea.why_it_matters}\n"
            f"[dim]🏆 Portfolio value:[/dim] {idea.portfolio_value}"
        )
        console.print(Panel(content, border_style="magenta", padding=(1, 2)))

    console.print()


def print_rate_limit(info: dict) -> None:
    """Print API rate limit status."""
    auth_str = "[green]✓ Authenticated[/green]" if info["authenticated"] else "[yellow]⚠ Unauthenticated (60 req/hr)[/yellow]"
    console.print(
        f"\n[dim]API Rate Limit: {info['remaining']}/{info['limit']} remaining · "
        f"Resets at {info['reset_at']} · {auth_str}[/dim]"
    )
