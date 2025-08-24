"""
Help command for the Azeroth Herald bot.
"""

import discord
from discord.ext import commands


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', help='Shows this help message.')
    async def custom_help(self, ctx, command_name=None):
        """Custom help command with WoW theming."""
        if command_name is None:
            # Show general help
            embed = discord.Embed(
                title="🛡️ Azeroth Herald - Command Guide",
                description="Your companion for World of Warcraft weekly tasks with enhanced visual experience!",
                color=discord.Color.gold()
            )
            
            embed.set_thumbnail(url="https://static.wikia.nocookie.net/wowpedia/images/3/3e/Alliance_Crest_of_Lordaeron.png")
            
            embed.add_field(
                name="📋 Weekly Commands",
                value=(
                    "`!checklist` - Show the complete weekly checklist with recent Blizzard updates\n"
                    "`!warning` - Show the reset warning with recent Blizzard updates\n"
                    "`!time` - Show current time and schedule info\n"
                    "`!affixes` - Show current Mythic+ affixes\n"
                    "`!cutoffs` - Show M+ season rating cutoffs\n"
                    "`!bluetrack` - Check for new Blizzard posts **(with banner images)**\n"
                    "`!news` - Check for new Wowhead articles **(with banner images)**\n"
                    "`!newssummary` - Get categorized news summary\n"
                    "`!test` - Test bot functionality"
                ),
                inline=False
            )
            
            embed.add_field(
                name="📅 Automatic Schedule",
                value=(
                    "**Monday 1:00 PM CDT** - Reset warning with recent updates\n"
                    "**Tuesday 11:00 AM CDT** - Weekly checklist with recent updates\n"
                    "**Every 30 minutes** - Blue tracker monitoring for new US Blizzard posts\n"
                    "**Every 2 hours** - Wowhead news monitoring for reset-relevant articles"
                ),
                inline=False
            )
            
            embed.add_field(
                name="ℹ️ More Info",
                value=(
                    "Use `!help <command>` for detailed information about a specific command.\n\n"
                    "**✨ New Feature**: Blue posts and news articles now include banner images "
                    "and thematic WoW visuals for a more engaging experience!"
                ),
                inline=False
            )
            
            embed.set_footer(text="For Azeroth! | Enhanced with banner images | Made with ❤️ for the WoW community")
            
        else:
            # Show help for specific command
            command = self.bot.get_command(command_name.lower())
            if command:
                embed = discord.Embed(
                    title=f"Help: !{command.name}",
                    description=command.help or "No description available.",
                    color=discord.Color.blue()
                )
                
                if command.name == "checklist":
                    embed.add_field(
                        name="Usage", 
                        value="`!checklist`",
                        inline=False
                    )
                    embed.add_field(
                        name="Description",
                        value="Displays the complete WoW weekly checklist with Great Vault, world content, and profession tasks. Also includes recent Blizzard updates that may affect your weekly activities.",
                        inline=False
                    )
                elif command.name == "warning":
                    embed.add_field(
                        name="Usage", 
                        value="`!warning`",
                        inline=False
                    )
                    embed.add_field(
                        name="Description",
                        value="Shows the Monday reset warning reminder with recent Blizzard updates. This is automatically posted every Monday and includes any important announcements affecting the weekly reset.",
                        inline=False
                    )
                elif command.name == "time":
                    embed.add_field(
                        name="Usage", 
                        value="`!time`",
                        inline=False
                    )
                    embed.add_field(
                        name="Description",
                        value="Shows the current UTC time and when the next scheduled posts will occur.",
                        inline=False
                    )
                elif command.name == "test":
                    embed.add_field(
                        name="Usage", 
                        value="`!test`",
                        inline=False
                    )
                    embed.add_field(
                        name="Description",
                        value="Simple test command to verify the bot is working correctly.",
                        inline=False
                    )
                elif command.name == "affixes":
                    embed.add_field(
                        name="Usage", 
                        value="`!affixes [region]`",
                        inline=False
                    )
                    embed.add_field(
                        name="Description",
                        value="Shows the current week's Mythic+ affixes. Optional region parameter (us, eu, kr, tw, cn). Defaults to 'us'.",
                        inline=False
                    )
                    embed.add_field(
                        name="Examples",
                        value="`!affixes` - Shows US affixes\n`!affixes eu` - Shows EU affixes",
                        inline=False
                    )
                elif command.name == "cutoffs":
                    embed.add_field(
                        name="Usage", 
                        value="`!cutoffs [region]`",
                        inline=False
                    )
                    embed.add_field(
                        name="Description",
                        value="Shows the current season's Mythic+ rating cutoffs for different percentiles. Optional region parameter (us, eu, kr, tw, cn). Defaults to 'us'.",
                        inline=False
                    )
                    embed.add_field(
                        name="Examples",
                        value="`!cutoffs` - Shows US cutoffs\n`!cutoffs eu` - Shows EU cutoffs",
                        inline=False
                    )
                elif command.name == "bluetrack":
                    embed.add_field(
                        name="Usage", 
                        value="`!bluetrack [action]`",
                        inline=False
                    )
                    embed.add_field(
                        name="Description",
                        value="Monitors Wowhead Blue Tracker for new official Blizzard posts. The bot automatically checks every 30 minutes.",
                        inline=False
                    )
                    embed.add_field(
                        name="Actions",
                        value="`!bluetrack` - Check for new posts since last check\n`!bluetrack latest` - Show latest posts (ignores cache)\n`!bluetrack test` - Test the scraper functionality\n`!bluetrack reset` - Reset cache (admin use)",
                        inline=False
                    )
                elif command.name == "news":
                    embed.add_field(
                        name="Usage", 
                        value="`!news [action]`",
                        inline=False
                    )
                    embed.add_field(
                        name="Description",
                        value="Check for new WoW-related articles from Wowhead. Filters for relevant content and reset-related news.",
                        inline=False
                    )
                    embed.add_field(
                        name="Actions",
                        value="`!news` - Check for new articles since last check\n`!news latest` - Show latest articles (ignores cache)\n`!news reset` - Show reset-relevant articles\n`!news test` - Test the scraper functionality\n`!news clear` - Clear cache (admin use)",
                        inline=False
                    )
                elif command.name == "newssummary":
                    embed.add_field(
                        name="Usage", 
                        value="`!newssummary`",
                        inline=False
                    )
                    embed.add_field(
                        name="Description",
                        value="Get a categorized summary of recent Wowhead news articles. Groups articles by Mythic+, Raids, Patches, Events, and General topics.",
                        inline=False
                    )
            else:
                embed = discord.Embed(
                    title="❌ Command Not Found",
                    description=f"No command named `{command_name}` found.",
                    color=discord.Color.red()
                )
                embed.add_field(
                    name="Available Commands",
                    value="Use `!help` to see all available commands.",
                    inline=False
                )
        
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
