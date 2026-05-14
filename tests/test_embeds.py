"""Unit tests for embed builders.

These don't need a Discord connection — they just build local objects.
"""

import discord

from src.utils.embeds import create_checklist_embed, create_monday_warning_embed


def test_checklist_embed_no_blue_posts():
    embed = create_checklist_embed()
    assert isinstance(embed, discord.Embed)
    assert embed.title == "WoW Weekly Checklist"


def test_checklist_embed_with_blue_posts():
    summary = {"posts": [], "total_count": 0}
    embed = create_checklist_embed(blue_post_summary=summary)
    assert isinstance(embed, discord.Embed)


def test_monday_warning_embed():
    embed = create_monday_warning_embed()
    assert isinstance(embed, discord.Embed)
