# Contributing to Azeroth Herald

Thanks for your interest in improving the bot! Contributions are welcome — bug reports, fixes, features, and docs all help.

## Quick start

1. Fork the repo and clone your fork.
2. Install runtime and dev dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
3. Copy `.env.example` to `.env` and fill in a Discord bot token + test channel ID. Use a **test bot** in a personal server — never your production token.
4. Run in dev mode:
   ```bash
   python dev_runner.py
   ```

### Running tests and lint

```bash
ruff check .   # lint
pytest         # tests
```

CI runs both on every PR against Python 3.9, 3.11, and 3.12.

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for more dev-mode details.

## Project structure

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full layout. Short version:

- `src/commands/` — one Discord command per file (Cogs)
- `src/utils/` — shared helpers (embeds, API clients, scrapers)
- `src/tasks/` — scheduled background tasks

## Making changes

### Branch naming
Use short, descriptive branches: `fix/help-typo`, `feat/raid-rotation`, `docs/contributing-guide`.

### Commit style
Conventional commits are encouraged but not required. Past commits use prefixes like `feat:`, `fix:`, `refactor:`, `docs:`.

### Adding a command
1. Create `src/commands/yourcommand.py` as a Cog with an `async def setup(bot)` function.
2. Register it in `command_modules` in `bot.py`.
3. Add help text in `src/commands/help.py`.
4. Update the command list in `README.md`.

### Adding a scheduled task
1. Add the task to `src/tasks/scheduler.py`.
2. Start it from `start_tasks()`.
3. Document the cadence in `README.md`.

## Pull requests

Before opening a PR:

- [ ] Bot starts without errors (`python bot.py` or `python dev_runner.py`)
- [ ] `!test`, `!time`, and `!help` work in your test server
- [ ] Any new commands have help entries
- [ ] README is updated for user-facing changes
- [ ] No secrets, tokens, or absolute local paths committed

Open the PR against `main`. Describe what changed and why, and link any related issues.

## Using AI coding agents

This repo is friendly to AI-assisted development. Guidance for agents lives in [AGENTS.md](./AGENTS.md) — the same file is read by Claude Code, Cursor, Codex, Aider, Zed, Continue, and others. If your tool uses a different filename, point it at `AGENTS.md` rather than duplicating the guidance.

## Reporting bugs and requesting features

Use the issue templates in `.github/ISSUE_TEMPLATE/`. Include:

- What you expected
- What actually happened
- Steps to reproduce
- Bot version / commit hash if known

## Code of Conduct

This project follows the [Contributor Covenant](./CODE_OF_CONDUCT.md). By participating, you agree to abide by its terms.

## License

By contributing, you agree your contributions are licensed under the MIT License (see [LICENSE](./LICENSE)).
