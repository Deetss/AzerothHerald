"""
Wowhead news command for the Azeroth Herald bot.
Provides manual news checking and posting for WoW-related articles.
"""

import discord
from discord.ext import commands
from src.utils.wowhead_news import WowheadNewsScraper
from src.utils.embeds import create_news_embed
from src.utils.error_handler import handle_command_error


class WowheadNewsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.news_scraper = WowheadNewsScraper()

    @commands.command(name='news')
    async def check_news(self, ctx, action: str = "check"):
        """
        Check for new Wowhead news articles or test the functionality.
        
        Usage:
        !news - Check for new articles since last check
        !news latest - Get the latest articles (ignores cache)
        !news reset - Get articles relevant to weekly reset activities
        !news test - Test the scraper functionality
        !news clear - Reset the cache (admin use)
        """
        try:
            if action.lower() == "test":
                await self._test_news_scraper(ctx)
            elif action.lower() == "latest":
                await self._get_latest_articles(ctx)
            elif action.lower() == "reset":
                await self._get_reset_relevant(ctx)
            elif action.lower() == "clear":
                await self._clear_cache(ctx)
            else:
                await self._check_new_articles(ctx)
                
        except Exception as e:
            await handle_command_error(ctx, e, "checking Wowhead news")

    async def _test_news_scraper(self, ctx):
        """Test the news scraper."""
        await ctx.send("🔍 Testing Wowhead news scraper...")
        
        # Test fetching the page
        soup = self.news_scraper.fetch_news_page()
        if not soup:
            await ctx.send("❌ Failed to fetch Wowhead news page.")
            return
        
        # Test parsing
        articles = self.news_scraper.parse_articles(soup)
        reset_relevant = [article for article in articles if self.news_scraper.is_reset_relevant(article)]
        
        embed = discord.Embed(
            title="🧪 Wowhead News Test Results",
            color=0xf4a261
        )
        
        embed.add_field(
            name="📊 Parsing Results",
            value=f"Total relevant articles: {len(articles)}\nReset-relevant articles: {len(reset_relevant)}",
            inline=False
        )
        
        if articles:
            latest_article = articles[0]
            embed.add_field(
                name="📰 Latest Article",
                value=f"**Title:** {latest_article['title'][:100]}...\n**Author:** {latest_article.get('author', 'Unknown')}",
                inline=False
            )
        
        embed.set_footer(text="Test completed | Azeroth Herald")
        await ctx.send(embed=embed)

    async def _get_latest_articles(self, ctx):
        """Get the latest articles regardless of cache."""
        await ctx.send("📰 Fetching latest Wowhead news articles...")
        
        soup = self.news_scraper.fetch_news_page()
        if not soup:
            await ctx.send("❌ Failed to fetch Wowhead news page.")
            return
        
        articles = self.news_scraper.parse_articles(soup)[:5]  # Limit to 5
        
        if not articles:
            await ctx.send("📭 No relevant articles found.")
            return
        
        await ctx.send(f"📢 Found {len(articles)} relevant article(s):")
        
        for article in articles:
            embed = create_news_embed(article)
            await ctx.send(embed=embed)

    async def _get_reset_relevant(self, ctx):
        """Get articles relevant to weekly reset activities."""
        await ctx.send("🔍 Fetching reset-relevant articles...")
        
        articles = self.news_scraper.get_reset_relevant_articles()
        
        if not articles:
            await ctx.send("📭 No reset-relevant articles found.")
            return
        
        await ctx.send(f"📢 Found {len(articles)} reset-relevant article(s):")
        
        for article in articles:
            embed = create_news_embed(article, is_reset_relevant=True)
            await ctx.send(embed=embed)

    async def _check_new_articles(self, ctx):
        """Check for new articles since last cache."""
        # Check if this is the first run
        cache = self.news_scraper.load_cache()
        is_first_run = len(cache.get('seen_articles', [])) == 0 and cache.get('last_check') is None
        
        if is_first_run:
            await ctx.send("🔍 First time checking Wowhead news - fetching recent articles...")
        else:
            await ctx.send("🔍 Checking for new Wowhead news articles...")
        
        new_articles = self.news_scraper.get_new_articles()
        
        if not new_articles:
            if is_first_run:
                await ctx.send("📭 No relevant articles found on Wowhead at this time.")
            else:
                await ctx.send("📭 No new articles found since last check.")
            return
        
        if is_first_run:
            await ctx.send(f"📢 Found {len(new_articles)} recent relevant article(s) (showing up to 3 to avoid spam):")
        else:
            await ctx.send(f"📢 Found {len(new_articles)} new article(s):")
        
        for article in new_articles:
            embed = create_news_embed(article)
            await ctx.send(embed=embed)

    async def _clear_cache(self, ctx):
        """Clear the news cache."""
        try:
            import os
            cache_file = "wowhead_news_cache.json"
            if os.path.exists(cache_file):
                os.remove(cache_file)
                await ctx.send("🗑️ Wowhead news cache has been cleared. Next check will be treated as first run.")
            else:
                await ctx.send("ℹ️ No cache file found - already in first run state.")
        except Exception as e:
            await ctx.send(f"❌ Error clearing cache: {e}")

    @commands.command(name='newssummary')
    async def news_summary(self, ctx):
        """
        Get a summary of recent news organized by category.
        """
        try:
            await ctx.send("📊 Generating news summary...")
            
            articles = self.news_scraper.get_reset_relevant_articles(days_back=14)
            
            if not articles:
                await ctx.send("📭 No recent relevant articles found.")
                return
            
            summary = self.news_scraper.summarize_reset_info(articles)
            
            embed = discord.Embed(
                title="📊 Wowhead News Summary",
                description="Recent articles organized by category (last 2 weeks)",
                color=0xf4a261
            )
            
            # Add fields for each category
            categories = [
                ('⚔️ Mythic+ & Dungeons', summary.get('mythic_plus', [])),
                ('🏛️ Raids', summary.get('raids', [])),
                ('🔧 Patches & Hotfixes', summary.get('patches', [])),
                ('🎊 Events', summary.get('events', [])),
                ('📰 General', summary.get('general', []))
            ]
            
            for category_name, category_articles in categories:
                if category_articles:
                    article_list = []
                    for article in category_articles[:3]:  # Limit to 3 per category
                        title = article['title'][:50] + "..." if len(article['title']) > 50 else article['title']
                        article_list.append(f"• [{title}]({article['url']})")
                    
                    if len(category_articles) > 3:
                        article_list.append(f"• *... and {len(category_articles) - 3} more*")
                    
                    embed.add_field(
                        name=category_name,
                        value="\n".join(article_list)[:1024],  # Discord field limit
                        inline=False
                    )
            
            if not any(summary.values()):
                embed.add_field(
                    name="ℹ️ No Recent Articles",
                    value="No articles found in the specified categories.",
                    inline=False
                )
            
            embed.set_footer(text="Wowhead News Summary | Azeroth Herald")
            await ctx.send(embed=embed)
            
        except Exception as e:
            await handle_command_error(ctx, e, "generating news summary")


async def setup(bot):
    await bot.add_cog(WowheadNewsCommand(bot))
