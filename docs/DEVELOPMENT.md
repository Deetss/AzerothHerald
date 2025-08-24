# Development Mode Instructions

## Auto-Reload Feature

The bot now includes auto-reload functionality for development! When you make changes to Python files, the bot will automatically restart to reflect your changes.

## Available Development Tasks

You can run these tasks from VS Code's Command Palette (`Ctrl+Shift+P` → "Tasks: Run Task"):

### 1. Run Bot (Development Mode) - **Recommended**
- **File**: `dev_runner.py`
- **Features**:
  - 🔄 Instant auto-reload on file changes
  - 📤 Real-time bot output display
  - 🛡️ Graceful shutdown handling
  - 👀 Advanced file watching with `watchdog` library
  
### 2. Run Bot (Simple Dev Mode) - **Backup Option**
- **File**: `simple_dev_runner.py` 
- **Features**:
  - 🔄 Auto-reload on file changes (checks every 2 seconds)
  - 🛡️ Graceful shutdown handling
  - 📦 No external dependencies (uses only built-in Python)

### 3. Run Discord Bot - **Production**
- **File**: `bot.py`
- **Features**:
  - 🚀 Standard bot execution
  - ❌ No auto-reload (manual restart required)

## How to Use Development Mode

### Option 1: Using VS Code Tasks (Recommended)
1. Open VS Code Command Palette (`Ctrl+Shift+P`)
2. Type "Tasks: Run Task"
3. Select "Run Bot (Development Mode)" or "Run Bot (Simple Dev Mode)"
4. The bot will start in a dedicated terminal
5. Edit any `.py` file and save - the bot will automatically restart!

### Option 2: Manual Command Line
```bash
# Advanced development mode (requires watchdog)
python dev_runner.py

# Simple development mode (no external dependencies)
python simple_dev_runner.py

# Standard mode (no auto-reload)
python bot.py
```

## Development Workflow

1. **Start Development Mode**: Use one of the development tasks above
2. **Edit Code**: Make changes to `bot.py` or any Python file
3. **Save File**: The bot automatically restarts with your changes
4. **Test**: Your changes are immediately active in Discord
5. **Stop**: Press `Ctrl+C` in the terminal to stop

## Stopping the Development Server

- **VS Code**: Close the terminal or press `Ctrl+C`
- **Command Line**: Press `Ctrl+C`

The development runner will gracefully shut down the bot process.

## Troubleshooting

### If auto-reload isn't working:
1. Make sure you're editing `.py` files (only Python files trigger restarts)
2. Ensure the file is actually being saved
3. Check the terminal output for error messages

### If the bot doesn't start:
1. Verify your `.env` file has the correct `DISCORD_TOKEN`
2. Check that all dependencies are installed: `pip install -r requirements.txt`
3. Make sure you're in the correct directory

### Performance Note:
The advanced development mode (`dev_runner.py`) is more responsive but requires the `watchdog` library. The simple mode (`simple_dev_runner.py`) works with any Python installation but checks for changes less frequently.

## Production Deployment

When deploying to production, always use the standard `python bot.py` command or the "Run Discord Bot" task, not the development modes.
