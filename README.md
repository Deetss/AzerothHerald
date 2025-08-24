# Azeroth Herald - WoW Discord Bot

A Discord bot for World of Warcraft players that provides weekly checklists and reminders for important in-game activities.

## Features

- **Weekly Checklist**: Displays a comprehensive checklist of weekly WoW activities
- **Scheduled Posts**: Automatic Monday warnings and Tuesday checklists
- **Blue Post Integration**: Automatically includes relevant Blizzard updates in weekly reminders
- **Wowhead News Integration**: Monitors for reset-relevant articles and news updates
- **Enhanced Visual Experience**: Banner images and thematic visuals for posts and articles
- **Mythic+ Integration**: Shows current week's affixes and season cutoffs
- **Blue Tracker Monitoring**: Monitors Wowhead Blue Tracker for new Blizzard posts
- **News Monitoring**: Automatically tracks Wowhead news for relevant WoW articles
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

- `!checklist` - Displays the weekly WoW checklist with recent Blizzard updates
- `!warning` - Shows the reset warning message with recent Blizzard updates
- `!time` - Shows current time and schedule information
- `!affixes [region]` - Shows current Mythic+ affixes (requires API key)
- `!cutoffs [region]` - Shows M+ season rating cutoffs (requires API key)
- `!bluetrack` - Manually check for new Blizzard posts
- `!news [action]` - Check for new Wowhead articles (check/latest/reset/test/clear)
- `!newssummary` - Get categorized summary of recent Wowhead news
- `!test` - Tests bot functionality
- `!help [command]` - Shows help information

## Automatic Schedule

- **Monday 1:00 PM CDT**: Weekly reset warning with relevant Blizzard updates and news
- **Tuesday 11:00 AM CDT**: New weekly checklist with relevant Blizzard updates
- **Every 30 minutes**: Checks for new Blizzard posts on the Blue Tracker
- **Every 2 hours**: Monitors Wowhead news for reset-relevant articles

## Blue Post Integration

The bot automatically monitors the Wowhead Blue Tracker for official Blizzard posts and integrates relevant information into weekly reminders:

### What Gets Included
- **Hotfixes and patches** that affect weekly activities
- **Class and dungeon tuning** announcements
- **Mythic+ and raid changes** for the current week
- **Weekly event** announcements and changes
- **Season updates** and timing information
- **Maintenance and downtime** notifications

### How It Works
- The bot analyzes recent Blizzard posts (past 7 days) for reset-relevant content
- Posts are categorized as "This Week", "Next Week", or "Recent Updates"
- Information is automatically added to Monday warnings and Tuesday checklists
- Only official posts from Blizzard Community Managers are included
- Manual commands (`!checklist`, `!warning`) also include this information

### Benefits
- Stay informed about changes that affect your weekly routine
- Never miss important hotfixes or tuning changes
- Get advance notice of upcoming content or maintenance
- See everything in one place alongside your weekly checklist

## Enhanced Visual Experience

The bot now includes rich visual elements to make posts more engaging and informative:

### Banner Images
- **Blue Posts**: Display banner images from the original posts when available
- **News Articles**: Show featured images from Wowhead articles
- **Automatic Fallbacks**: When original images aren't available, thematic WoW images are used based on content

### Thematic Image Selection
When posts or articles don't have specific images, the bot automatically selects appropriate WoW-themed images based on content:

- **Mythic+ content**: Dungeon achievement images
- **Raid content**: Raid boss and encounter images  
- **PvP content**: Arena and battleground achievement images
- **Class updates**: Character and specialization images
- **Maintenance/Hotfixes**: Technical and engineering themed images
- **Seasonal content**: Event and celebration images
- **General updates**: WoW logo and general achievement images

### Visual Consistency
- All embeds maintain consistent branding with appropriate thumbnails
- Color coding helps distinguish between different types of content
- Clean layout ensures information remains readable while being visually appealing

## Wowhead News Integration

The bot also monitors Wowhead news for relevant WoW articles and content updates:

### What Gets Tracked
- **Mythic+ guides and updates** for dungeon strategies
- **Raid guides and analysis** for current content
- **Class guides and rotation updates** for optimization
- **Patch notes and previews** for upcoming changes
- **Event coverage and previews** for seasonal content
- **Developer interviews** and announcements

### Relevance Filtering
- Articles are filtered for WoW-specific content (excludes other Blizzard games)
- Reset-relevant articles are prioritized for automatic posting
- General WoW news is available through manual commands
- Articles are categorized by type (Mythic+, Raids, Patches, Events, General)

### Manual Commands
- `!news` - Check for new articles since last check
- `!news latest` - Get latest articles regardless of cache
- `!news reset` - Show only reset-relevant articles
- `!newssummary` - Get categorized summary of recent articles

### Automatic Monitoring
- Checks for new articles every 2 hours
- Only posts reset-relevant articles automatically to avoid spam
- Other articles are tracked but require manual commands to view

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
