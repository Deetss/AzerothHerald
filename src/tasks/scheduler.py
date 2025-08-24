"""
Scheduled tasks for the Azeroth Herald bot.
Contains the scheduled posting functionality and blue tracker monitoring.
"""

import os
import discord
from datetime import datetime, timezone
from discord.ext import tasks
from src.utils.embeds import create_checklist_embed, create_monday_warning_embed, create_blue_tracker_embed, create_news_embed
from src.utils.blue_tracker import BlueTrackerScraper
from src.utils.wowhead_news import WowheadNewsScraper


class ScheduledTasks:
    def __init__(self, bot):
        self.bot = bot
        self.target_channel_id = int(os.getenv('TARGET_CHANNEL_ID'))
        self.blue_tracker = BlueTrackerScraper(region_filter='us')  # Only US posts
        self.news_scraper = WowheadNewsScraper()
        
    def start_tasks(self):
        """Start all scheduled tasks."""
        self.scheduled_posts.start()
        self.blue_tracker_monitor.start()
        self.news_monitor.start()
        print("Scheduled tasks started - Bot will post Monday warnings at 1:00 PM CDT and Tuesday checklists at 11:00 AM CDT")
        print("Blue tracker monitoring started - Checking for new Blizzard posts every 30 minutes (US region only)")
        print("Wowhead news monitoring started - Checking for new articles every 2 hours")
    
    @tasks.loop(minutes=1)
    async def scheduled_posts(self):
        """Scheduled task that runs every minute to check if it's time to post."""
        try:
            now = datetime.now(timezone.utc)
            
            # Monday Warning: 1:00 PM CDT (18:00 UTC)
            if (now.weekday() == 0 and  # Monday (0=Monday, 6=Sunday)
                now.hour == 18 and 
                now.minute == 0):
                
                channel = self.bot.get_channel(self.target_channel_id)
                if channel:
                    # Get reset-relevant blue posts for Monday warning
                    reset_posts = self.blue_tracker.get_reset_relevant_posts(days_back=7)
                    blue_post_summary = self.blue_tracker.summarize_reset_info(reset_posts)
                    
                    # Also get reset-relevant news articles
                    reset_news = self.news_scraper.get_reset_relevant_articles(days_back=7)
                    news_summary = self.news_scraper.summarize_reset_info(reset_news)
                    
                    embed = create_monday_warning_embed(blue_post_summary if reset_posts else None)
                    await channel.send(embed=embed)
                    
                    # Post news summary if there are relevant articles
                    if reset_news:
                        news_embed = discord.Embed(
                            title="📰 Recent Reset-Relevant News",
                            description="Important Wowhead articles from this week",
                            color=0x264653
                        )
                        
                        for category, articles in news_summary.items():
                            if articles:
                                article_list = []
                                for article in articles[:2]:  # Limit to 2 per category for Monday
                                    title = article['title'][:40] + "..." if len(article['title']) > 40 else article['title']
                                    article_list.append(f"• [{title}]({article['url']})")
                                
                                category_names = {
                                    'mythic_plus': '⚔️ Mythic+ & Dungeons',
                                    'raids': '🏛️ Raids',
                                    'patches': '🔧 Patches & Hotfixes',
                                    'events': '🎊 Events',
                                    'general': '📰 General'
                                }
                                
                                news_embed.add_field(
                                    name=category_names.get(category, category.title()),
                                    value="\n".join(article_list),
                                    inline=True
                                )
                        
                        if any(news_summary.values()):
                            news_embed.set_footer(text="Wowhead News Summary | Azeroth Herald")
                            await channel.send(embed=news_embed)
                    
                    print(f"Monday warning posted at {now} with {len(reset_posts)} relevant US blue posts and {len(reset_news)} news articles")
                else:
                    print(f"Could not find channel with ID {self.target_channel_id}")
            
            # Tuesday Checklist: 11:00 AM CDT (16:00 UTC)
            elif (now.weekday() == 1 and  # Tuesday
                  now.hour == 16 and 
                  now.minute == 0):
                
                channel = self.bot.get_channel(self.target_channel_id)
                if channel:
                    # Get reset-relevant blue posts for Tuesday checklist
                    reset_posts = self.blue_tracker.get_reset_relevant_posts(days_back=7)
                    blue_post_summary = self.blue_tracker.summarize_reset_info(reset_posts)
                    
                    embed = create_checklist_embed(blue_post_summary if reset_posts else None)
                    await channel.send("🎉 **Weekly Reset is Here!** 🎉", embed=embed)
                    print(f"Tuesday checklist posted at {now} with {len(reset_posts)} relevant US blue posts")
                else:
                    print(f"Could not find channel with ID {self.target_channel_id}")
                    
        except Exception as e:
            print(f"Error in scheduled_posts: {e}")

    @scheduled_posts.before_loop
    async def before_scheduled_posts(self):
        """Wait until the bot is ready before starting the scheduled tasks."""
        await self.bot.wait_until_ready()

    @tasks.loop(minutes=30)
    async def blue_tracker_monitor(self):
        """Monitor blue tracker for new posts every 30 minutes."""
        try:
            # Check if this is the first automated run
            cache = self.blue_tracker.load_cache()
            is_first_run = len(cache.get('seen_posts', [])) == 0 and cache.get('last_check') is None
            
            new_posts = self.blue_tracker.get_new_posts()
            
            if new_posts:
                channel = self.bot.get_channel(self.target_channel_id)
                if channel:
                    if is_first_run:
                        # Don't spam on first automated run, just log
                        print(f"Blue tracker first run: found {len(new_posts)} US posts, marked as seen but not posting to avoid spam")
                    else:
                        for post in new_posts:
                            embed = create_blue_tracker_embed(post)
                            await channel.send("📢 **New Blizzard Post!**", embed=embed)
                            print(f"Posted US blue tracker update: {post['title']}")
                else:
                    print(f"Could not find channel with ID {self.target_channel_id}")
                    
        except Exception as e:
            print(f"Error in blue_tracker_monitor: {e}")

    @blue_tracker_monitor.before_loop
    async def before_blue_tracker_monitor(self):
        """Wait until the bot is ready before starting blue tracker monitoring."""
        await self.bot.wait_until_ready()

    @tasks.loop(hours=2)
    async def news_monitor(self):
        """Monitor Wowhead news for new articles every 2 hours."""
        try:
            # Check if this is the first automated run
            cache = self.news_scraper.load_cache()
            is_first_run = len(cache.get('seen_articles', [])) == 0 and cache.get('last_check') is None
            
            new_articles = self.news_scraper.get_new_articles()
            
            if new_articles:
                channel = self.bot.get_channel(self.target_channel_id)
                if channel:
                    if is_first_run:
                        # Don't spam on first automated run, just log
                        print(f"Wowhead news first run: found {len(new_articles)} articles, marked as seen but not posting to avoid spam")
                    else:
                        # Only post reset-relevant articles automatically to avoid spam
                        reset_relevant_articles = [article for article in new_articles if self.news_scraper.is_reset_relevant(article)]
                        
                        for article in reset_relevant_articles:
                            embed = create_news_embed(article, is_reset_relevant=True)
                            await channel.send("📰 **New Reset-Relevant News!**", embed=embed)
                            print(f"Posted Wowhead news update: {article['title']}")
                        
                        # Log other articles but don't post them
                        other_articles = len(new_articles) - len(reset_relevant_articles)
                        if other_articles > 0:
                            print(f"Found {other_articles} other new articles (not reset-relevant, not posting automatically)")
                else:
                    print(f"Could not find channel with ID {self.target_channel_id}")
                    
        except Exception as e:
            print(f"Error in news_monitor: {e}")

    @news_monitor.before_loop
    async def before_news_monitor(self):
        """Wait until the bot is ready before starting news monitoring."""
        await self.bot.wait_until_ready()
