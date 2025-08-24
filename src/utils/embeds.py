"""
Embed creation utilities for the Azeroth Herald bot.
Contains functions to create various Discord embeds.
"""

import discord
from typing import List, Dict, Optional


def create_checklist_embed(blue_post_summary: Optional[Dict] = None):
    """Creates and returns the weekly checklist Discord embed with optional blue post integration."""
    embed = discord.Embed(
        title="WoW Weekly Checklist",
        description="Here are the key tasks to complete before the weekly reset!",
        color=discord.Color.blue()
    )
    # You can find WoW-themed image URLs online to make it look nicer
    embed.set_thumbnail(url="https://static.wikia.nocookie.net/wowpedia/images/3/3e/Alliance_Crest_of_Lordaeron.png")

    # Add blue post information first if available
    if blue_post_summary:
        _add_blue_post_fields_to_embed(embed, blue_post_summary, is_weekly_checklist=True)

    # The Great Vault Section
    embed.add_field(
        name="🏆 The Great Vault",
        value=(
            "- **Raiding:** Defeat 2, 4, or 7 raid bosses.\n"
            "- **Mythic+:** Complete 1, 4, or 8 M+ dungeons.\n"
            "- **PvP:** Earn Honor in rated PvP modes."
        ),
        inline=False
    )

    # World Content Section
    embed.add_field(
        name="🌍 World & Outdoor Content",
        value=(
            "- Defeat the weekly **World Boss**.\n"
            "- Complete the main weekly quest in **Dornogal** (e.g., 'Aiding the...').\n"
            "- Pick up the weekly **Dungeon Quests**.\n"
            "- Complete your weekly **Delves**."
        ),
        inline=False
    )

    # Professions & Events Section
    embed.add_field(
        name="🛠️ Professions & Events",
        value=(
            "- Complete weekly **Profession Quests** for knowledge points.\n"
            "- Fulfill Public **Crafting Orders**.\n"
            "- Check for active **Weekly Events** like Timewalking."
        ),
        inline=False
    )
    
    # Quick tip about affixes
    embed.add_field(
        name="💡 Pro Tips",
        value=(
            "• Use `!affixes` to see this week's Mythic+ affixes\n"
            "• Use `!cutoffs` to check season rating cutoffs\n"
            "• Plan your runs based on current affixes!"
        ),
        inline=False
    )

    embed.set_footer(text="Good luck this week, champion! | Azeroth Herald")
    return embed


def create_monday_warning_embed(blue_post_summary: Optional[Dict] = None):
    """Creates and returns the Monday warning embed with optional blue post integration."""
    embed = discord.Embed(
        title="⚠️ Weekly Reset Reminder",
        description="The weekly reset is tomorrow (Tuesday)! Don't forget to complete your weekly tasks.",
        color=discord.Color.orange()
    )
    embed.set_thumbnail(url="https://static.wikia.nocookie.net/wowpedia/images/3/3e/Alliance_Crest_of_Lordaeron.png")
    
    # Add blue post information first if available
    if blue_post_summary:
        _add_blue_post_fields_to_embed(embed, blue_post_summary, is_weekly_checklist=False)
    
    embed.add_field(
        name="🕐 Time Left",
        value="Less than 24 hours until weekly reset!",
        inline=False
    )
    
    embed.add_field(
        name="📋 Quick Reminder",
        value=(
            "- Complete your **Great Vault** activities\n"
            "- Defeat the **World Boss**\n"
            "- Finish weekly **Delves** and **M+ dungeons**\n"
            "- Don't forget **Profession Quests**"
        ),
        inline=False
    )
    
    embed.set_footer(text="Use !checklist for the full weekly checklist | Azeroth Herald")
    return embed


def _add_blue_post_fields_to_embed(embed: discord.Embed, blue_post_summary: Dict, is_weekly_checklist: bool = True):
    """Helper function to add blue post information to embeds."""
    if not blue_post_summary:
        return
    
    # This week's information
    if blue_post_summary.get('this_week'):
        this_week_posts = blue_post_summary['this_week']
        this_week_text = ""
        
        for i, post in enumerate(this_week_posts[:3]):  # Limit to 3 posts
            post_line = f"• **{post['title'][:60]}{'...' if len(post['title']) > 60 else ''}**"
            if post.get('url'):
                post_line = f"• **[{post['title'][:60]}{'...' if len(post['title']) > 60 else ''}]({post['url']})**"
            this_week_text += post_line + "\n"
        
        if this_week_text:
            embed.add_field(
                name="📢 This Week's Updates",
                value=this_week_text.strip(),
                inline=False
            )
    
    # Next week's information (only for Monday warning or if specifically mentioned)
    if blue_post_summary.get('next_week') and (not is_weekly_checklist or len(blue_post_summary['next_week']) > 0):
        next_week_posts = blue_post_summary['next_week']
        next_week_text = ""
        
        for i, post in enumerate(next_week_posts[:2]):  # Limit to 2 posts for next week
            post_line = f"• **{post['title'][:60]}{'...' if len(post['title']) > 60 else ''}**"
            if post.get('url'):
                post_line = f"• **[{post['title'][:60]}{'...' if len(post['title']) > 60 else ''}]({post['url']})**"
            next_week_text += post_line + "\n"
        
        if next_week_text:
            embed.add_field(
                name="🔮 Looking Ahead",
                value=next_week_text.strip(),
                inline=False
            )
    
    # General important posts (only if there's space and content)
    if blue_post_summary.get('general') and len(embed.fields) < 6:  # Don't overcrowd the embed
        general_posts = blue_post_summary['general']
        if general_posts:
            general_text = ""
            
            for i, post in enumerate(general_posts[:2]):  # Limit to 2 general posts
                post_line = f"• **{post['title'][:60]}{'...' if len(post['title']) > 60 else ''}**"
                if post.get('url'):
                    post_line = f"• **[{post['title'][:60]}{'...' if len(post['title']) > 60 else ''}]({post['url']})**"
                general_text += post_line + "\n"
            
            if general_text:
                embed.add_field(
                    name="ℹ️ Recent Updates",
                    value=general_text.strip(),
                    inline=False
                )


def create_affixes_embed(affixes_data, region='us'):
    """Creates and returns the affixes embed."""
    embed = discord.Embed(
        title=f"🗡️ This Week's Mythic+ Affixes ({region.upper()})",
        description=affixes_data.get('title', 'Current Mythic+ Affixes'),
        color=discord.Color.purple()
    )
    
    # Add each affix as a field
    for affix in affixes_data.get('affix_details', []):
        # Format the description to be more readable
        description = affix.get('description', 'No description available')
        if len(description) > 100:
            description = description[:97] + "..."
        
        embed.add_field(
            name=f"⚔️ {affix.get('name', 'Unknown')}",
            value=description,
            inline=False
        )
    
    # Add leaderboard link if available
    if 'leaderboard_url' in affixes_data:
        embed.add_field(
            name="📊 Leaderboards",
            value=f"[View Rankings]({affixes_data['leaderboard_url']})",
            inline=False
        )
    
    embed.set_footer(text="Data from Raider.IO | Azeroth Herald")
    return embed


def create_season_cutoffs_embed(cutoffs_data, region='us'):
    """Creates and returns the season cutoffs embed."""
    embed = discord.Embed(
        title=f"🏆 M+ Season Cutoffs ({region.upper()})",
        description="Current season rating cutoffs for different percentiles",
        color=discord.Color.gold()
    )
    
    # Get cutoffs data
    cutoffs = cutoffs_data.get('cutoffs', {})
    
    if not cutoffs:
        embed.add_field(
            name="❌ No Data Available",
            value="Season cutoff data is not available for this region.",
            inline=False
        )
        return embed
    
    # Add cutoffs for different percentiles
    percentiles = ['p999', 'p99', 'p95', 'p90', 'p75', 'p50', 'p25', 'p10']
    percentile_names = {
        'p999': '🥇 Top 0.1%',
        'p99': '🥈 Top 1%', 
        'p95': '🥉 Top 5%',
        'p90': '💎 Top 10%',
        'p75': '🔥 Top 25%',
        'p50': '⭐ Top 50%',
        'p25': '📈 Top 75%',
        'p10': '🎯 Top 90%'
    }
    
    cutoff_text = ""
    for percentile in percentiles:
        if percentile in cutoffs:
            score = cutoffs[percentile]
            name = percentile_names.get(percentile, percentile.upper())
            cutoff_text += f"{name}: **{score}**\n"
    
    if cutoff_text:
        embed.add_field(
            name="📊 Rating Cutoffs",
            value=cutoff_text,
            inline=False
        )
    
    # Add season info if available
    if 'season' in cutoffs_data:
        embed.add_field(
            name="🗓️ Season Info",
            value=f"Season: **{cutoffs_data['season']}**",
            inline=True
        )
    
    # Add last updated info if available
    if 'last_updated' in cutoffs_data:
        embed.add_field(
            name="🕐 Last Updated", 
            value=cutoffs_data['last_updated'],
            inline=True
        )
    
    embed.add_field(
        name="💡 What This Means",
        value="These scores show the minimum rating needed to be in each percentile of players for the current season.",
        inline=False
    )
    
    embed.set_footer(text="Data from Raider.IO | Azeroth Herald")
    return embed


def create_blue_tracker_embed(post_data):
    """Creates and returns a Discord embed for a blue tracker post."""
    title = post_data['title'][:256]  # Discord title limit
    author = post_data.get('author', 'Unknown')
    time_posted = post_data.get('time_posted', 'Unknown')
    url = post_data.get('url')
    
    description_parts = []
    if author != 'Unknown':
        description_parts.append(f"**Author:** {author}")
    if time_posted != 'Unknown':
        description_parts.append(f"**Posted:** {time_posted}")
    
    # Add content preview if available
    preview = post_data.get('content_preview', '')
    if preview and len(preview) > 50:
        description_parts.append(f"\n{preview}")
    
    # Add note about URL type if it's a search link
    if url and 'search=' in url:
        description_parts.append(f"\n*Click title to search for this post on Wowhead*")
    
    description = "\n".join(description_parts)[:4096]  # Discord description limit
    
    embed = discord.Embed(
        title=title,
        description=description,
        color=0x00b4d8,  # Blue color for Blizzard posts
        url=url if url else None
    )
    
    # Add Blizzard-themed thumbnail
    embed.set_thumbnail(url="https://images.blz-contentstack.com/v3/assets/blt95b381df7c12c15c/blt2477dceb7fdcaa86/5f0f9a41baa6c218a505c97d/wow-circle-blue.png")
    
    footer_text = "Wowhead Blue Tracker | Azeroth Herald"
    if url and 'blue-tracker/topic/' in url:
        footer_text += " | Click title for direct link"
    elif url and 'wowhead.com/news/' in url:
        footer_text += " | Click title for news article"
    
    embed.set_footer(text=footer_text)
    
    return embed


def create_news_embed(article_data, is_reset_relevant=False):
    """Creates and returns a Discord embed for a Wowhead news article."""
    title = article_data['title'][:256]  # Discord title limit
    author = article_data.get('author', 'Wowhead Staff')
    time_posted = article_data.get('time_posted', 'Recently')
    url = article_data.get('url')
    
    description_parts = []
    if author != 'Wowhead Staff':
        description_parts.append(f"**Author:** {author}")
    if time_posted != 'Recently':
        description_parts.append(f"**Posted:** {time_posted}")
    
    # Add content preview if available
    preview = article_data.get('content_preview', '')
    if preview and len(preview) > 50:
        description_parts.append(f"\n{preview}")
    
    # Add special note for reset-relevant articles
    if is_reset_relevant:
        description_parts.append(f"\n*🎯 This article is relevant to weekly reset activities*")
    
    description = "\n".join(description_parts)[:4096]  # Discord description limit
    
    # Choose color based on relevance
    color = 0x264653 if is_reset_relevant else 0xf4a261  # Darker green for reset-relevant, orange for general
    
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        url=url if url else None
    )
    
    # Add Wowhead-themed thumbnail
    embed.set_thumbnail(url="https://wow.zamimg.com/images/wow/icons/large/achievement_general_stayclassy.jpg")
    
    footer_text = "Wowhead News | Azeroth Herald"
    if is_reset_relevant:
        footer_text = "Weekly Reset Relevant | " + footer_text
    
    embed.set_footer(text=footer_text)
    
    return embed
