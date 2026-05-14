# Azeroth Herald — WoW Discord Bot

[![CI](https://github.com/Deetss/AzerothHerald/actions/workflows/ci.yml/badge.svg)](https://github.com/Deetss/AzerothHerald/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![discord.py](https://img.shields.io/badge/discord.py-2.x-5865F2.svg)](https://github.com/Rapptz/discord.py)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A Discord bot for World of Warcraft players. Posts weekly checklists, reset warnings, and surfaces relevant Blizzard blue posts and Wowhead news on a schedule.

## Contents

- [Features](#features)
- [Quick start](#quick-start)
- [Configuration](#configuration)
- [Commands](#commands)
- [Automatic schedule](#automatic-schedule)
- [Project structure](#project-structure)
- [Deployment](#deployment)
- [Development](#development)
- [Contributing](#contributing)
- [Built with AI agents?](#built-with-ai-agents)
- [License](#license)

## Features

- **Weekly checklist** of WoW activities, posted on reset
- **Reset warning** the day before, with relevant blue posts attached
- **Mythic+ integration** — current affixes and season cutoffs via Raider.IO
- **Blue Tracker monitoring** — polls Wowhead's Blue Tracker every 30 minutes for new Blizzard posts
- **Wowhead news monitoring** — polls every 2 hours, only auto-posts reset-relevant articles to avoid spam
- **Banner images & thematic fallbacks** — posts use the source's image when available, with WoW-themed fallback art selected by content type
- **Modular architecture** — one Cog per command, easy to extend

## Quick start

```bash
git clone https://github.com/Deetss/AzerothHerald.git
cd AzerothHerald
pip install -r requirements.txt
cp .env.example .env   # fill in DISCORD_TOKEN and TARGET_CHANNEL_ID
python bot.py
```

Requires **Python 3.8+** and a Discord bot token with the **Message Content Intent** enabled.

## Configuration

Environment variables (loaded from `.env`):

| Variable | Required | Purpose |
| --- | :---: | --- |
| `DISCORD_TOKEN` | yes | Bot token from the Discord Developer Portal |
| `TARGET_CHANNEL_ID` | yes | Channel ID for scheduled posts |
| `RAIDER_IO_API_KEY` | no | Enables `!affixes` and `!cutoffs` |

### Getting a Discord bot token

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create an application.
2. Under **Bot**, click *Add Bot* and copy the token.
3. Enable the **Message Content Intent** (required for prefix commands).
4. Paste the token into `.env`.

### Getting a channel ID

Enable Developer Mode (User Settings → Advanced), right-click any channel, and pick *Copy Channel ID*.

### Inviting the bot

Generate an OAuth2 URL with the `bot` scope and at minimum these permissions: *Read Messages*, *Send Messages*, *Embed Links*, *Attach Files*.

## Commands

Prefix is `!`.

| Command | Description |
| --- | --- |
| `!checklist` | Weekly WoW activities checklist with recent blue posts |
| `!warning` | Reset warning message with recent blue posts |
| `!time` | Current UTC time and the next scheduled posts |
| `!affixes [region]` | Current Mythic+ affixes — *requires `RAIDER_IO_API_KEY`* |
| `!cutoffs [region]` | M+ season rating cutoffs — *requires `RAIDER_IO_API_KEY`* |
| `!bluetrack` | Manually check for new Blizzard blue posts |
| `!news [check\|latest\|reset\|test\|clear]` | Inspect or refresh Wowhead news state |
| `!newssummary` | Categorized summary of recent Wowhead news |
| `!test` | Sanity check that the bot is responsive |
| `!help [command]` | Help for all commands or a specific one |

Regions for `!affixes` / `!cutoffs`: `us`, `eu`, `kr`, `tw`, `cn` (default: `us`).

## Automatic schedule

All times are fixed in UTC. Local US-Central times are approximate and shift by one hour across daylight saving transitions.

| When (UTC) | Local (US Central) | What |
| --- | --- | --- |
| Monday 18:00 | 1:00 PM CDT / 12:00 PM CST | Reset warning + blue posts |
| Tuesday 16:00 | 11:00 AM CDT / 10:00 AM CST | Weekly checklist + blue posts |
| Every 30 min | — | Blue Tracker poll (US region) |
| Every 2 hours | — | Wowhead news poll (auto-posts only reset-relevant articles) |

## Project structure

```
.
├── bot.py                # Entry point — loads cogs, starts scheduler
├── dev_runner.py         # Dev runner with watchdog-based auto-reload
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── docker-dev.sh
├── src/
│   ├── commands/         # One Cog per command
│   ├── utils/            # Embeds, API clients, scrapers, error handling
│   └── tasks/            # Scheduled background loops
└── docs/                 # Architecture and development notes
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full layout and design rationale.

## Deployment

### Docker

```bash
./docker-dev.sh dev    # development with hot reload
./docker-dev.sh prod   # production mode
```

Or with `docker compose` directly:

```bash
docker compose up bot-dev    # development
docker compose up bot-prod   # production
```

The bot reads its config from `.env`, so make sure that file exists alongside the compose file before starting.

### Heroku / Worker hosts

A `Procfile` is included (`worker: python bot.py`) for platforms that use it.

## Development

Use `dev_runner.py` for auto-reload on file changes:

```bash
python dev_runner.py
```

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for details on the dev runner, VS Code tasks, and debugging tips.

## Contributing

Contributions are very welcome — bug reports, fixes, features, and docs. See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, conventions, and the PR checklist. All participants are expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Built with AI agents?

This repo is friendly to AI-assisted development. Project-wide guidance for AI coding agents (Claude Code, Cursor, Codex, Aider, Zed, Continue, etc.) lives in [AGENTS.md](AGENTS.md) — point your tool at that file rather than duplicating guidance per-tool.

## License

Released under the [MIT License](LICENSE).
