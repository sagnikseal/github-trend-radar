# 📡 GitHub Trend Radar

> **Real-time GitHub demand intelligence & personal project incubator**

[![Daily Trend Scan](../../actions/workflows/daily-radar.yml/badge.svg)](../../actions/workflows/daily-radar.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code Style: Typed](https://img.shields.io/badge/code%20style-typed-green.svg)](pyproject.toml)

GitHub Trend Radar scans GitHub in real time, calculates **star velocity** (stars/day weighted by fork engagement), classifies repositories into momentum tiers, and generates actionable personal project blueprints aligned with the highest-demand niches.

🌐 **[Live Dashboard →](https://sagnikseal.github.io/github-trend-radar/)**
📊 **[Latest Trends Report →](TRENDS.md)**

---

## ✨ Features

| Feature | Description |
| --- | --- |
| 📡 **Live Scanning** | Searches GitHub across 10 curated high-demand topics |
| ⚡ **Velocity Engine** | Scores repos by stars/day × fork multiplier to find breakouts |
| 🏷️ **Momentum Tiers** | `🚀 BREAKING` / `⚡ HIGH VELOCITY` / `📈 RISING` / `➡️ STEADY` |
| 💡 **Idea Incubator** | Maps trending demand to buildable personal project blueprints |
| 📄 **Markdown Export** | Auto-generates `TRENDS.md` for your repo's landing page |
| 🌐 **Web Dashboard** | Self-contained `docs/index.html` for GitHub Pages |
| 🤖 **Auto-Updated** | GitHub Actions runs daily and commits fresh reports automatically |
| 🔑 **Token-Optional** | Works out of the box (60 req/hr); set `GITHUB_TOKEN` for 5k/hr |

---

## 🚀 Quick Start

### Install

```bash
git clone https://github.com/sagnikseal/github-trend-radar.git
cd github-trend-radar
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Run

```bash
# Scan trending MCP repositories
trendradar scan --topic mcp --limit 20

# Rank by star velocity
trendradar velocity --topic llm --limit 15

# Browse project ideas
trendradar ideas

# Filter ideas by niche or difficulty
trendradar ideas --niche "Local AI" --difficulty intermediate

# Export full report + web dashboard
trendradar export --all --output TRENDS.md

# Check API rate limit status
trendradar status
```

---

## 📐 Velocity Algorithm

$$\text{Velocity Score} = \frac{\text{Stars}}{\max(1,\ \text{Days Since Creation})} \times \left(1 + \frac{\text{Forks}}{\text{Stars} + 1}\right)$$

This rewards:
- **New repositories** with explosive momentum over old giants
- **High fork ratios** as a proxy for active builder engagement

| Tier | Stars/Day Threshold |
|------|-------------------|
| 🚀 BREAKING | ≥ 100 |
| ⚡ HIGH VELOCITY | ≥ 20 |
| 📈 RISING | ≥ 5 |
| ➡️ STEADY | < 5 |

---

## 🌐 Hosting on GitHub (Free)

### 1. Push to GitHub
```bash
git init -b main
git add .
git commit -m "🚀 Initial commit: GitHub Trend Radar"
gh repo create github-trend-radar --public --source=. --push
```

### 2. Enable GitHub Pages
Go to your repository → **Settings → Pages → Source: GitHub Actions**

### 3. Set Repository Secret (Optional but recommended)
Go to **Settings → Secrets → Actions → New secret**:
- Name: `GITHUB_TOKEN` (already provided automatically by GitHub)

Your dashboard will be live at `https://sagnikseal.github.io/github-trend-radar/` and auto-updated nightly.

---

## 🗂️ Project Structure

```
github-trend-radar/
├── .github/workflows/daily-radar.yml   # Automated daily scanner & Pages deployer
├── docs/                               # GitHub Pages root
│   ├── index.html                      # Interactive web dashboard
│   └── data.json                       # Exported JSON data
├── trendradar/
│   ├── client/github.py                # GitHub API client (rate-limit resilient)
│   ├── core/
│   │   ├── models.py                   # Type-annotated data models
│   │   ├── velocity.py                 # Star velocity & breakout scoring
│   │   └── incubator.py                # Project idea generator
│   └── renderers/
│       ├── terminal.py                 # Rich console UI
│       └── markdown.py                 # Markdown & HTML dashboard generators
├── tests/                              # Pytest test suite (offline, mocked)
├── TRENDS.md                           # Auto-generated trend report
├── pyproject.toml
└── requirements.txt
```

---

## 🧪 Running Tests

```bash
pytest tests/ -v
# With coverage:
pytest tests/ -v --cov=trendradar --cov-report=term-missing
```

---

## 🔑 GitHub Token (Optional)

Without a token, the GitHub API allows **60 requests/hour**. For full scanning of all 10 topics, a token is recommended.

```bash
export GITHUB_TOKEN=ghp_your_token_here
trendradar export --all
```

Get a free token (no extra permissions needed) at: https://github.com/settings/tokens

---

## 📊 Tracked Topics

| Topic | Category |
|-------|----------|
| `mcp` | Model Context Protocol |
| `ai-agent` | AI Agents & Autonomy |
| `browser-use` | Browser Automation AI |
| `llm` | Large Language Models |
| `local-ai` | Local AI Runtimes |
| `rag` | Retrieval-Augmented Generation |
| `self-hosted` | Self-Hosted SaaS |
| `developer-tools` | Developer Tooling |
| `autonomous-agent` | Autonomous Agents |
| `langchain` | LangChain Ecosystem |

---

## 📄 License

MIT — see [LICENSE](LICENSE)

---

*Built with Python, Rich, and the GitHub REST API.*
*⭐ Star this repository if it helped you find your next project!*
