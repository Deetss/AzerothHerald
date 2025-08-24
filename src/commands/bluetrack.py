"""
Blue tracker command for the Azeroth Herald bot.
Provides manual blue tracker checking and posting.
"""

import discord
from discord.ext import commands
from src.utils.blue_tracker import BlueTrackerScraper
from src.utils.embeds import create_blue_tracker_embed
from src.utils.error_handler import handle_command_error


class BlueTrackerCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.blue_tracker = BlueTrackerScraper(region_filter='us')  # Only US posts

    @commands.command(name='bluetrack')
    async def check_blue_tracker(self, ctx, action: str = "check"):
        """
        Check for new blue tracker posts or test the functionality.
        
        Usage:
        !bluetrack - Check for new posts since last check
        !bluetrack latest - Get the latest posts (ignores cache)
        !bluetrack test - Test the scraper functionality
        !bluetrack reset - Reset the cache (admin use)
        """
        try:
            if action.lower() == "test":
                await self._test_blue_tracker(ctx)
            elif action.lower() == "latest":
                await self._get_latest_posts(ctx)
            elif action.lower() == "reset":
                await self._reset_cache(ctx)
            else:
                await self._check_new_posts(ctx)
                
        except Exception as e:
            await handle_command_error(ctx, e, "checking blue tracker")

    async def _test_blue_tracker(self, ctx):
        """Test the blue tracker scraper."""
        await ctx.send("🔍 Testing Blue Tracker scraper...")
        
        # Test fetching the page
        soup = self.blue_tracker.fetch_blue_tracker_page()
        if not soup:
            await ctx.send("❌ Failed to fetch Blue Tracker page.")
            return
        
        # Test parsing
        posts = self.blue_tracker.parse_posts(soup)
        relevant_posts = [post for post in posts if self.blue_tracker.is_relevant_post(post)]
        
        embed = discord.Embed(
            title="🧪 Blue Tracker Test Results",
            color=0x00b4d8
        )
        
        embed.add_field(
            name="📊 Parsing Results",
            value=f"Total posts found: {len(posts)}\nRelevant posts: {len(relevant_posts)}",
            inline=False
        )
        
        if relevant_posts:
            latest_post = relevant_posts[0]
            embed.add_field(
                name="📝 Latest Relevant Post",
                value=f"**Title:** {latest_post['title'][:100]}...\n**Author:** {latest_post.get('author', 'Unknown')}",
                inline=False
            )
        
        embed.set_footer(text="Test completed | Azeroth Herald")
        await ctx.send(embed=embed)

    async def _get_latest_posts(self, ctx):
        """Get the latest posts regardless of cache."""
        await ctx.send("📰 Fetching latest Blue Tracker posts...")
        
        soup = self.blue_tracker.fetch_blue_tracker_page()
        if not soup:
            await ctx.send("❌ Failed to fetch Blue Tracker page.")
            return
        
        posts = self.blue_tracker.parse_posts(soup)
        relevant_posts = [post for post in posts if self.blue_tracker.is_relevant_post(post)][:5]  # Limit to 5
        
        if not relevant_posts:
            await ctx.send("📭 No relevant posts found.")
            return
        
        await ctx.send(f"📢 Found {len(relevant_posts)} relevant post(s):")
        
        for post in relevant_posts:
            embed = create_blue_tracker_embed(post)
            await ctx.send(embed=embed)

    async def _check_new_posts(self, ctx):
        """Check for new posts since last cache."""
        # Check if this is the first run
        cache = self.blue_tracker.load_cache()
        is_first_run = len(cache.get('seen_posts', [])) == 0 and cache.get('last_check') is None
        
        if is_first_run:
            await ctx.send("🔍 First time checking Blue Tracker - fetching recent posts...")
        else:
            await ctx.send("🔍 Checking for new Blue Tracker posts...")
        
        new_posts = self.blue_tracker.get_new_posts()
        
        if not new_posts:
            if is_first_run:
                await ctx.send("📭 No relevant posts found on the Blue Tracker at this time.")
            else:
                await ctx.send("📭 No new posts found since last check.")
            return
        
        if is_first_run:
            await ctx.send(f"📢 Found {len(new_posts)} recent relevant post(s) (showing up to 3 to avoid spam):")
        else:
            await ctx.send(f"📢 Found {len(new_posts)} new post(s):")
        
        for post in new_posts:
            embed = create_blue_tracker_embed(post)
            await ctx.send(embed=embed)

    async def _reset_cache(self, ctx):
        """Reset the blue tracker cache."""
        try:
            import os
            cache_file = "blue_tracker_cache.json"
            if os.path.exists(cache_file):
                os.remove(cache_file)
                await ctx.send("🗑️ Blue Tracker cache has been reset. Next check will be treated as first run.")
            else:
                await ctx.send("ℹ️ No cache file found - already in first run state.")
        except Exception as e:
            await ctx.send(f"❌ Error resetting cache: {e}")


async def setup(bot):
    await bot.add_cog(BlueTrackerCommand(bot))
