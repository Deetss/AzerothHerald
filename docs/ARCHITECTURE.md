# Modular Bot Structure

The Azeroth Herald bot has been refactored into a modular structure for better maintainability and organization.

## Project Structure

```
AzerothHerald/
├── bot.py                 # Main bot entry point
├── dev_runner.py          # Development runner with auto-reload
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # Project documentation
├── docs/                 # Documentation files
│   ├── ARCHITECTURE.md   # This file
│   ├── DEVELOPMENT.md    # Development guide
│   └── test_commands.md  # Command testing guide
└── src/                  # Source code directory
    ├── __init__.py
    ├── commands/         # Individual command modules
    │   ├── __init__.py
    │   ├── affixes.py    # !affixes command
    │   ├── checklist.py  # !checklist command
    │   ├── cutoffs.py    # !cutoffs command
    │   ├── help.py       # !help command
    │   ├── test.py       # !test command
    │   ├── time.py       # !time command
    │   └── warning.py    # !warning command
    ├── utils/            # Utility functions
    │   ├── __init__.py
    │   ├── api.py        # API calls (Raider.IO)
    │   ├── embeds.py     # Discord embed creation
    │   └── error_handler.py  # Centralized error handling
    └── tasks/            # Scheduled tasks
        ├── __init__.py
        └── scheduler.py  # Weekly posting scheduler
```

## Benefits of Modular Structure

1. **Separation of Concerns**: Each command is in its own file, making it easier to maintain and debug.
2. **Reusability**: Utility functions can be shared across multiple commands.
3. **Easier Testing**: Individual components can be tested in isolation.
4. **Better Organization**: Related functionality is grouped together.
5. **Scalability**: Adding new commands is as simple as creating a new file in the `src/commands/` directory.
6. **Clear Package Structure**: The `src/` directory creates a clear Python package hierarchy.

## Import Structure

With the new `src/` directory structure, all imports follow a consistent pattern:

### From Main Bot (`bot.py`)
```python
from src.tasks.scheduler import ScheduledTasks
from src.utils.error_handler import handle_command_error
```

### Within Commands (`src/commands/*.py`)
```python
from src.utils.embeds import create_checklist_embed
from src.utils.api import fetch_affixes
```

### Within Tasks (`src/tasks/*.py`)
```python
from src.utils.embeds import create_checklist_embed, create_monday_warning_embed
```

This structure ensures that all modules can find each other correctly and maintains consistency across the project.

## Adding New Commands

To add a new command:

1. Create a new Python file in the `src/commands/` directory (e.g., `newcommand.py`)
2. Follow this template:

```python
"""
New command for the Azeroth Herald bot.
"""

import discord
from discord.ext import commands

class NewCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='newcommand', help='Description of the new command.')
    async def new_command(self, ctx):
        """Command implementation."""
        embed = discord.Embed(
            title="New Command",
            description="This is a new command!",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(NewCommand(bot))
```

3. Add the module name to the `command_modules` list in `bot.py`:

```python
command_modules = [
    'src.commands.checklist',
    'src.commands.warning',
    'src.commands.time',
    'src.commands.affixes',
    'src.commands.cutoffs',
    'src.commands.help',
    'src.commands.test',
    'src.commands.newcommand'  # Add your new command here
]
```

## Key Components

### Main Bot (`bot.py`)
- Initializes the Discord bot
- Loads all command modules dynamically
- Sets up error handling
- Starts scheduled tasks

### Commands (`src/commands/`)
- Each command is a separate Discord.py Cog
- Follows consistent structure and naming
- Uses utility functions for common operations
- Import utilities using `from src.utils import ...`

### Utilities (`src/utils/`)
- **embeds.py**: Creates reusable Discord embeds
- **api.py**: Handles external API calls (Raider.IO)
- **error_handler.py**: Centralized error handling for commands

### Tasks (`src/tasks/`)
- **scheduler.py**: Manages scheduled posting (Monday warnings, Tuesday checklists)
- Imports utilities using `from src.utils import ...`

## Running the Bot

The bot can be run using any of the existing methods:
- `python bot.py`
- VS Code task: "Run Discord Bot"
- Development runner: `python dev_runner.py`

All existing functionality remains the same - the refactoring only improved the code organization without changing any user-facing features.
