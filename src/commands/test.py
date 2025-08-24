"""
Test command for the Azeroth Herald bot.
"""

import discord
from discord.ext import commands


class TestCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='test', help='Test command to verify bot functionality.')
    async def test_command(self, ctx):
        """Simple test command to verify bot is working."""
        embed = discord.Embed(
            title="✅ Bot Test",
            description="The bot is working correctly!",
            color=discord.Color.green()
        )
        embed.add_field(
            name="Status",
            value="All systems operational",
            inline=False
        )
        embed.set_footer(text="Azeroth Herald is ready for adventure!")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(TestCommand(bot))
