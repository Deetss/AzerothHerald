# AGENTS.md

Guidance for AI coding agents (Claude Code, Cursor, Codex, Aider, Zed, Continue, etc.) working in this repository. Human contributors should read [CONTRIBUTING.md](./CONTRIBUTING.md) instead.

## Project at a glance

**Azeroth Herald** is a Discord bot for World of Warcraft players. It posts weekly checklists, reset warnings, and monitors Wowhead/Blizzard sources for relevant news.

- **Language:** Python 3.8+
- **Runtime:** `discord.py`
- **Entry points:** `bot.py` (production), `dev_runner.py` (auto-reload dev mode)
- **External APIs:** Raider.IO (Mythic+ data, optional), Wowhead scraping (news + blue tracker)

## Repository layout

```
src/
├── commands/   # Discord commands as Cogs (one file per command)
├── utils/      # Shared helpers — embeds, API clients, scrapers, error handling
└── tasks/      # Scheduled background loops (weekly posts, monitors)
```

Key files:

| File | Purpose |
| --- | --- |
| `bot.py` | Bot entry point. Loads cogs, starts scheduler. |
| `dev_runner.py` | Dev runner with auto-reload via `watchdog`. |
| `src/commands/<name>.py` | One Cog per command. Must expose `async def setup(bot)`. |
| `src/utils/embeds.py` | Discord embed builders — reuse these instead of constructing embeds inline. |
| `src/utils/api.py` | Raider.IO client. |
| `src/utils/blue_tracker.py` | Wowhead Blue Tracker scraper. |
| `src/utils/wowhead_news.py` | Wowhead news scraper. |
| `src/utils/error_handler.py` | Centralized error handling — route new error cases here. |
| `src/tasks/scheduler.py` | All scheduled tasks (`@tasks.loop`). |

## Conventions

### Adding a command

1. Create `src/commands/<name>.py` as a Cog.
2. Expose `async def setup(bot): await bot.add_cog(...)`.
3. Register the module in the `command_modules` list in `bot.py`.
4. Reuse helpers from `src.utils.*` — don't reinvent embed building or API clients.
5. Add a help entry in `src/commands/help.py`.
6. If user-facing, update the command list in `README.md`.

### Adding a scheduled task

1. Add the task method to `src/tasks/scheduler.py`.
2. Start it from `start_tasks()`.
3. Document the cadence in `README.md` under "Automatic Schedule".

### Adding a utility

1. Place in `src/utils/`. Keep each module narrow (one external service or one concern).
2. Add new runtime deps to `requirements.txt`.

### Imports

Always import from the package root:

```python
from src.utils.embeds import create_checklist_embed
from src.tasks.scheduler import ScheduledTasks
```

### Error handling

Route command errors through `src/utils/error_handler.py`. Surface user-friendly Discord embeds — never dump tracebacks into channels.

### Secrets

- Never commit `.env`. It's gitignored.
- Required: `DISCORD_TOKEN`, `TARGET_CHANNEL_ID`. Optional: `RAIDER_IO_API_KEY`.
- New secrets go in `.env.example` (with placeholder values) and the README env-vars table.

## Dev workflow

```bash
pip install -r requirements-dev.txt    # runtime + lint + test deps
cp .env.example .env                   # fill in your token + channel id
python dev_runner.py                   # auto-reload on save
```

### Local validation before committing

```bash
ruff check .   # must pass — CI enforces this
pytest         # must pass — CI enforces this
```

### Live-bot smoke tests once running

- `!test` — sanity check
- `!time` — verify schedule loaded
- `!help` — verify all cogs loaded

## Things to avoid

- **Don't** add comments, docstrings, or type annotations to code you weren't asked to change.
- **Don't** silently swallow exceptions — surface them via `error_handler.py`.
- **Don't** hardcode tokens, channel IDs, or absolute paths.
- **Don't** edit `.vscode/tasks.json` to add platform-specific paths — keep it portable (`python`, not `C:/.../python.exe`).
- **Don't** add backwards-compat shims for features that don't exist yet.

## Tool-specific notes

- **Claude Code:** `CLAUDE.md` points here. No additional config needed.
- **Cursor / Codex / Aider / Zed / Continue:** All read `AGENTS.md` by convention.
- **GitHub Copilot:** No `.github/copilot-instructions.md` is maintained — this file is the single source of truth.

If your agent reads a different file by default, symlink or point it at this one rather than duplicating guidance.
