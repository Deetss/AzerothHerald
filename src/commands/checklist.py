"""
Checklist command for the Azeroth Herald bot.
"""

from discord.ext import commands
from src.utils.embeds import create_checklist_embed
from src.utils.blue_tracker import BlueTrackerScraper


class ChecklistCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.blue_tracker = BlueTrackerScraper(region_filter='us')  # Only US posts

    @commands.command(name='checklist', help='Displays the WoW weekly checklist on demand with recent blue posts.')
    async def post_checklist(self, ctx):
        """Command to manually post the checklist with blue post integration."""
        try:
            # Get reset-relevant blue posts
            reset_posts = self.blue_tracker.get_reset_relevant_posts(days_back=7)
            blue_post_summary = self.blue_tracker.summarize_reset_info(reset_posts)
            
            embed = create_checklist_embed(blue_post_summary if reset_posts else None)
            
            if reset_posts:
                await ctx.send(f"📋 **Weekly Checklist** (with {len(reset_posts)} recent updates)", embed=embed)
            else:
                await ctx.send(embed=embed)
                
        except Exception as e:
            print(f"Error in checklist command: {e}")
            # Fallback to basic embed if blue post integration fails
            embed = create_checklist_embed()
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ChecklistCommand(bot))
