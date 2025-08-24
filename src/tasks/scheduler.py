"""
Scheduled tasks for the Azeroth Herald bot.
Contains the scheduled posting functionality.
"""

import os
from datetime import datetime, timezone
from discord.ext import tasks
from src.utils.embeds import create_checklist_embed, create_monday_warning_embed


class ScheduledTasks:
    def __init__(self, bot):
        self.bot = bot
        self.target_channel_id = int(os.getenv('TARGET_CHANNEL_ID'))
        
    def start_tasks(self):
        """Start all scheduled tasks."""
        self.scheduled_posts.start()
        print("Scheduled tasks started - Bot will post Monday warnings at 1:00 PM CDT and Tuesday checklists at 11:00 AM CDT")
    
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
                    embed = create_monday_warning_embed()
                    await channel.send(embed=embed)
                    print(f"Monday warning posted at {now}")
                else:
                    print(f"Could not find channel with ID {self.target_channel_id}")
            
            # Tuesday Checklist: 11:00 AM CDT (16:00 UTC)
            elif (now.weekday() == 1 and  # Tuesday
                  now.hour == 16 and 
                  now.minute == 0):
                
                channel = self.bot.get_channel(self.target_channel_id)
                if channel:
                    embed = create_checklist_embed()
                    await channel.send("🎉 **Weekly Reset is Here!** 🎉", embed=embed)
                    print(f"Tuesday checklist posted at {now}")
                else:
                    print(f"Could not find channel with ID {self.target_channel_id}")
                    
        except Exception as e:
            print(f"Error in scheduled_posts: {e}")

    @scheduled_posts.before_loop
    async def before_scheduled_posts(self):
        """Wait until the bot is ready before starting the scheduled tasks."""
        await self.bot.wait_until_ready()
