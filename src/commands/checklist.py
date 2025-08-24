"""
Checklist command for the Azeroth Herald bot.
"""

from discord.ext import commands
from src.utils.embeds import create_checklist_embed


class ChecklistCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='checklist', help='Displays the WoW weekly checklist on demand.')
    async def post_checklist(self, ctx):
        """Command to manually post the checklist."""
        embed = create_checklist_embed()
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ChecklistCommand(bot))
