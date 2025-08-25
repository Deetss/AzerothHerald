# Testing Discord Bot Commands

After setting up your `.env` file with the Discord token, channel ID, and Raider.IO API key, you can test the following commands:

## Manual Commands
- `!checklist` - Shows the full weekly checklist embed
- `!warning` - Shows the Monday reset warning embed  
- `!time` - Shows current UTC time and next scheduled post times
- `!affixes` - Shows current week's Mythic+ affixes (US region)
- `!affixes eu` - Shows current week's Mythic+ affixes for EU region
- `!cutoffs` - Shows current season M+ rating cutoffs (US region)
- `!cutoffs eu` - Shows current season M+ rating cutoffs for EU region
- `!test` - Test bot functionality
- `!help` - Shows all available commands

## Blue Tracker and News Commands (Enhanced with Banner Images)
- `!bluetrack` - Check for new Blizzard blue posts (with thematic banner images based on content)
- `!bluetrack latest` - Get latest blue posts regardless of cache
- `!bluetrack test` - Test the blue tracker functionality
- `!news` - Check for new Wowhead news articles (with banner images when available)
- `!news latest` - Get latest news articles regardless of cache
- `!news reset` - Get articles relevant to weekly reset activities

**Note**: Blue posts now automatically include thematic WoW images based on content keywords (e.g., Mythic+ images for dungeon content, expansion images for major announcements, conference images for GamesCom/BlizzCon panels, etc.). News articles include actual banner images when available from Wowhead, or thematic images as fallback.

## Scheduled Posts
The bot will automatically post:
- **Monday at 1:00 PM CDT (18:00 UTC)**: Reset warning message
- **Tuesday at 11:00 AM CDT (16:00 UTC)**: Full weekly checklist

## Setup Requirements
1. Create a `.env` file with:
   ```
   DISCORD_TOKEN=your_bot_token_here
   TARGET_CHANNEL_ID=your_channel_id_here
   RAIDER_IO_API_KEY=your_raider_io_key
   ```

2. Make sure your bot has permissions to:
   - Send messages
   - Embed links
   - Read message history

## Testing the Schedule
Use the `!time` command to see when the next scheduled posts will occur and verify the timezone calculations are correct.

## Testing Affixes & Cutoffs
- `!affixes` - Default US region affixes
- `!affixes eu` - European region affixes  
- `!affixes kr` - Korean region affixes
- `!cutoffs` - Default US region season cutoffs
- `!cutoffs eu` - European region season cutoffs
- Valid regions: us, eu, kr, tw, cn

### Testing Banner Images
Ensure that thematic banner images for Blue Tracker and Wowhead News commands are relevant and visually appealing.
