"""
Time command for the Azeroth Herald bot.
"""

import discord
from discord.ext import commands
from datetime import datetime, timezone, timedelta


class TimeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='time', help='Shows current UTC time and next scheduled posts.')
    async def show_time(self, ctx):
        """Command to show current time and schedule information."""
        now = datetime.now(timezone.utc)
        
        # Calculate next Monday 18:00 UTC
        days_until_monday = (7 - now.weekday()) % 7 if now.weekday() != 0 else 0
        if now.weekday() == 0 and now.hour >= 18:  # Past Monday posting time
            days_until_monday = 7
        next_monday = now.replace(hour=18, minute=0, second=0, microsecond=0) + timedelta(days=days_until_monday)
        
        # Calculate next Tuesday 16:00 UTC
        days_until_tuesday = (8 - now.weekday()) % 7 if now.weekday() != 1 else 0
        if now.weekday() == 1 and now.hour >= 16:  # Past Tuesday posting time
            days_until_tuesday = 7
        next_tuesday = now.replace(hour=16, minute=0, second=0, microsecond=0) + timedelta(days=days_until_tuesday)
        
        embed = discord.Embed(
            title="🕐 Bot Schedule Information",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="Current Time (UTC)",
            value=f"{now.strftime('%A, %B %d, %Y at %H:%M:%S')}",
            inline=False
        )
        
        embed.add_field(
            name="Next Monday Warning",
            value=f"{next_monday.strftime('%A, %B %d, %Y at %H:%M')} UTC\n(1:00 PM CDT)",
            inline=True
        )
        
        embed.add_field(
            name="Next Tuesday Checklist",
            value=f"{next_tuesday.strftime('%A, %B %d, %Y at %H:%M')} UTC\n(11:00 AM CDT)",
            inline=True
        )
        
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(TimeCommand(bot))
