"""
Embed creation utilities for the Azeroth Herald bot.
Contains functions to create various Discord embeds.
"""

import discord


def create_checklist_embed():
    """Creates and returns the weekly checklist Discord embed."""
    embed = discord.Embed(
        title="WoW Weekly Checklist",
        description="Here are the key tasks to complete before the weekly reset!",
        color=discord.Color.blue()
    )
    # You can find WoW-themed image URLs online to make it look nicer
    embed.set_thumbnail(url="https://static.wikia.nocookie.net/wowpedia/images/3/3e/Alliance_Crest_of_Lordaeron.png")

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


def create_monday_warning_embed():
    """Creates and returns the Monday warning embed."""
    embed = discord.Embed(
        title="⚠️ Weekly Reset Reminder",
        description="The weekly reset is tomorrow (Tuesday)! Don't forget to complete your weekly tasks.",
        color=discord.Color.orange()
    )
    embed.set_thumbnail(url="https://static.wikia.nocookie.net/wowpedia/images/3/3e/Alliance_Crest_of_Lordaeron.png")
    
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
