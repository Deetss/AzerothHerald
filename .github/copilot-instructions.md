# Azeroth Herald - Discord Bot Development Instructions

## Project Overview
This is a **World of Warcraft Discord bot** built with **Python** and **discord.py** that provides:
- **Weekly checklists** for WoW activities
- **Scheduled posts** (Monday warnings, Tuesday checklists)
- **Mythic+ integration** (affixes, season cutoffs via Raider.IO API)
- **Manual commands** for on-demand information

## Architecture & Structure

### Modular Design
The project uses a **modular architecture** with clear separation of concerns:

```
src/
├── commands/     # Individual Discord commands (Cogs)
├── utils/        # Shared utilities (embeds, API calls, error handling)
└── tasks/        # Scheduled background tasks
```

### Key Files
- **`bot.py`** - Main entry point, loads commands and starts scheduler
- **`dev_runner.py`** - Development mode with auto-reload (recommended for dev)
- **`src/commands/*.py`** - Individual command modules (checklist, affixes, etc.)
- **`src/utils/embeds.py`** - Discord embed creation functions
- **`src/utils/api.py`** - External API interactions (Raider.IO)
- **`src/tasks/scheduler.py`** - Weekly posting schedule logic

## Development Guidelines

### Adding New Commands
1. Create a new file in `src/commands/` (e.g., `newcommand.py`)
2. Use the Cog pattern with `async def setup(bot)` function
3. Add the module to the `command_modules` list in `bot.py`
4. Import any utilities from `src.utils.*`

### Import Patterns
- **From main bot**: `from src.tasks.scheduler import ScheduledTasks`
- **Within commands**: `from src.utils.embeds import create_checklist_embed`
- **Within tasks**: `from src.utils.embeds import create_checklist_embed`

### Development Workflow
1. **Start dev mode**: Use "Run Bot (Development Mode)" task or `python dev_runner.py`
2. **Edit files**: Changes auto-reload instantly
3. **Test commands**: Use `!test` to verify bot functionality
4. **Check schedule**: Use `!time` to see posting schedule

## Environment Setup

### Required Environment Variables
- **`DISCORD_TOKEN`** (required) - Bot token from Discord Developer Portal
- **`TARGET_CHANNEL_ID`** (required) - Discord channel for scheduled posts
- **`RAIDER_IO_API_KEY`** (optional) - For `!affixes` and `!cutoffs` commands

### Development Tasks Available
- **"Run Bot (Development Mode)"** - Auto-reload with watchdog (recommended)
- **"Run Bot (Simple Dev Mode)"** - Auto-reload without external deps
- **"Run Discord Bot"** - Standard production mode
- **"Install Dependencies"** - Install requirements.txt

## API Integration

### Raider.IO API
- **Purpose**: Fetch current Mythic+ affixes and season cutoffs
- **Commands**: `!affixes [region]`, `!cutoffs [region]`
- **Regions**: us, eu, kr, tw, cn
- **Implementation**: `src/utils/api.py` handles requests

## Scheduled Tasks

### Posting Schedule
- **Monday 18:00 UTC** (1:00 PM CDT) - Reset warning
- **Tuesday 16:00 UTC** (11:00 AM CDT) - Weekly checklist
- **Implementation**: `src/tasks/scheduler.py` with `@tasks.loop(minutes=1)`

## Commands Available

### Core Commands
- **`!checklist`** - Weekly WoW activities checklist
- **`!warning`** - Reset warning message
- **`!time`** - Current time and schedule info
- **`!test`** - Bot functionality test
- **`!help [command]`** - Command help system

### API-Dependent Commands
- **`!affixes [region]`** - Current M+ affixes (requires API key)
- **`!cutoffs [region]`** - M+ season rating cutoffs (requires API key)

## Error Handling

### Centralized Error Management
- **File**: `src/utils/error_handler.py`
- **Handles**: Command not found, missing args, cooldowns, permissions
- **Pattern**: All errors show helpful Discord embeds with guidance

## Testing & Debugging

### Quick Tests
- **`!test`** - Verify bot is responsive
- **`!time`** - Check current time and schedule
- **`!help`** - Verify command loading

### Development Tips
- Use **development mode** for instant feedback
- Check **terminal output** for error messages
- Verify **environment variables** if commands fail
- Test **API commands** with and without API key

## Documentation References
- **README.md** - Setup and basic usage
- **docs/ARCHITECTURE.md** - Detailed architectural decisions
- **docs/DEVELOPMENT.md** - Development mode instructions
