"""
Warning command for the Azeroth Herald bot.
"""

from discord.ext import commands
from src.utils.embeds import create_monday_warning_embed
from src.utils.blue_tracker import BlueTrackerScraper


class WarningCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.blue_tracker = BlueTrackerScraper(region_filter='us')  # Only US posts

    @commands.command(name='warning', help='Displays the Monday reset warning on demand with recent blue posts.')
    async def post_warning(self, ctx):
        """Command to manually post the Monday warning with blue post integration."""
        try:
            # Get reset-relevant blue posts
            reset_posts = self.blue_tracker.get_reset_relevant_posts(days_back=7)
            blue_post_summary = self.blue_tracker.summarize_reset_info(reset_posts)
            
            embed = create_monday_warning_embed(blue_post_summary if reset_posts else None)
            
            if reset_posts:
                await ctx.send(f"⚠️ **Reset Warning** (with {len(reset_posts)} recent updates)", embed=embed)
            else:
                await ctx.send(embed=embed)
                
        except Exception as e:
            print(f"Error in warning command: {e}")
            # Fallback to basic embed if blue post integration fails
            embed = create_monday_warning_embed()
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(WarningCommand(bot))
