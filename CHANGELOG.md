# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- AI agent guidance file (`AGENTS.md`) read by Claude Code, Cursor, Codex, Aider, Zed, Continue and others
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`
- MIT `LICENSE`
- GitHub issue templates (bug, feature) and pull request template
- Dependabot config for pip, GitHub Actions, and Docker updates
- GitHub Actions CI workflow (ruff lint + pytest on Python 3.9, 3.11, 3.12)
- `pyproject.toml` with ruff and pytest config
- `requirements-dev.txt` with lint/test tooling
- `tests/` directory with import smoke tests and embed unit tests
- `.editorconfig` for cross-editor consistency

### Changed
- README rewritten: real clone URL, badges, accurate project tree, UTC schedule with DST caveat, command table, deployment section
- `.vscode/tasks.json` uses portable `python`/`pip` commands instead of hardcoded Windows venv paths
- Codebase auto-formatted with ruff (whitespace, import sorting, redundant f-strings)

### Removed
- `.github/copilot-instructions.md` (replaced by tool-neutral `AGENTS.md`)
- Stale implementation notes: `docs/REFACTORING_SUMMARY.md`, `docs/BANNER_IMAGES_IMPLEMENTATION.md`, `docs/WOWHEAD_NEWS_IMPLEMENTATION.md`
- "Run Bot (Simple Dev Mode)" VS Code task (referenced a missing script)
- Fly.io secrets section from README (no workflow exists)

## [1.0.0]

Initial open-source release.
