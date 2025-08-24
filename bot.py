import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from src.tasks.scheduler import ScheduledTasks
from src.utils.error_handler import handle_command_error

# --- 1. INITIAL SETUP ---
# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Define the bot's command prefix and enable necessary intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Initialize scheduler
scheduler = None

# --- 2. COMMAND LOADING ---
async def load_commands():
    """Load all command modules."""
    command_modules = [
        'src.commands.checklist',
        'src.commands.warning',
        'src.commands.time',
        'src.commands.affixes',
        'src.commands.cutoffs',
        'src.commands.help',
        'src.commands.test',
        'src.commands.bluetrack',
        'src.commands.wowhead_news'
    ]
    
    for module in command_modules:
        try:
            await bot.load_extension(module)
            print(f"[OK] Loaded {module}")
        except Exception as e:
            print(f"[ERROR] Failed to load {module}: {e}")

# --- 3. BOT EVENTS ---
@bot.event
async def on_ready():
    """Event that runs when the bot has successfully connected to Discord."""
    global scheduler
    
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('Bot is online and ready.')
    
    # Initialize and start scheduled tasks
    scheduler = ScheduledTasks(bot)
    scheduler.start_tasks()

@bot.event
async def on_command_error(ctx, error):
    """Event that handles command errors."""
    await handle_command_error(ctx, error)

# --- 4. MAIN EXECUTION ---
async def main():
    """Main function to start the bot."""
    # Load all command modules
    await load_commands()
    
    # Start the bot
    if TOKEN is None:
        print("ERROR: DISCORD_TOKEN not found. Make sure you have a .env file with the token.")
        return
    
    # Check for optional API key
    raider_io_api_key = os.getenv('RAIDER_IO_API_KEY')
    if raider_io_api_key is None:
        print("WARNING: RAIDER_IO_API_KEY not found. The !affixes and !cutoffs commands will not work.")
        print("Add RAIDER_IO_API_KEY=your_key_here to your .env file to enable API functionality.")
    else:
        print("All environment variables loaded successfully.")
    
    try:
        await bot.start(TOKEN)
    except KeyboardInterrupt:
        print("Bot shutting down...")
    finally:
        await bot.close()

# --- 5. RUN THE BOT ---
if __name__ == "__main__":
    asyncio.run(main())
