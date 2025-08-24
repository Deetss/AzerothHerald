# Azeroth Herald - WoW Discord Bot

A Discord bot for World of Warcraft players that provides weekly checklists and reminders for important in-game activities.

## Features

- **Weekly Checklist**: Displays a comprehensive checklist of weekly WoW activities
- **Scheduled Posts**: Automatic Monday warnings and Tuesday checklists
- **Mythic+ Integration**: Shows current week's affixes and season cutoffs
- **Manual Commands**: Full set of commands for on-demand information
- **Modular Architecture**: Clean, maintainable code structure

## Setup

### Prerequisites

- Python 3.8 or higher
- A Discord bot token
- Discord server with appropriate permissions

### Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd AzerothHerald
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Add your Discord bot token to the `.env` file
   - Set your target channel ID in the `.env` file

4. Run the bot:
   ```bash
   python bot.py
   ```

### Development Mode

For development with auto-reload functionality:

```bash
# Advanced development mode (recommended)
python dev_runner.py

# Simple development mode (no external dependencies)
python simple_dev_runner.py
```

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed development instructions.

## Configuration

### Environment Variables

- `DISCORD_TOKEN`: Your Discord bot token (required)
- `TARGET_CHANNEL_ID`: The Discord channel ID where the bot will post (required)
- `RAIDER_IO_API_KEY`: Raider.IO API key for M+ data (optional)

### Getting a Discord Bot Token

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section
4. Create a bot and copy the token
5. Add the token to your `.env` file

### Getting a Channel ID

1. Enable Developer Mode in Discord (User Settings > Advanced)
2. Right-click on the channel you want to use
3. Click "Copy Channel ID"
4. Add the ID to your `.env` file

## Commands

- `!checklist` - Displays the weekly WoW checklist
- `!warning` - Shows the reset warning message
- `!time` - Shows current time and schedule information
- `!affixes [region]` - Shows current Mythic+ affixes (requires API key)
- `!cutoffs [region]` - Shows M+ season rating cutoffs (requires API key)
- `!test` - Tests bot functionality
- `!help [command]` - Shows help information

## Automatic Schedule

- **Monday 1:00 PM CDT**: Weekly reset warning
- **Tuesday 11:00 AM CDT**: New weekly checklist

## Project Structure

The bot uses a modular architecture for better maintainability:

```
├── bot.py                 # Main bot entry point
├── commands/             # Individual command modules
├── utils/                # Utility functions (embeds, API calls, error handling)
└── tasks/                # Scheduled tasks
```

For detailed information about the architecture, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Contributing

Feel free to submit issues and pull requests to improve the bot!

## License

This project is open source and available under the MIT License.
