"""
Warning command for the Azeroth Herald bot.
"""

from discord.ext import commands
from src.utils.embeds import create_monday_warning_embed


class WarningCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='warning', help='Displays the Monday reset warning on demand.')
    async def post_warning(self, ctx):
        """Command to manually post the Monday warning."""
        embed = create_monday_warning_embed()
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(WarningCommand(bot))
