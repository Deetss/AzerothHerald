"""
Cutoffs command for the Azeroth Herald bot.
"""

import discord
from discord.ext import commands
from src.utils.api import fetch_season_cutoffs
from src.utils.embeds import create_season_cutoffs_embed


class CutoffsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='cutoffs', help='Shows current M+ season rating cutoffs.')
    async def show_cutoffs(self, ctx, region='us'):
        """Command to show current season M+ rating cutoffs."""
        # Validate region
        valid_regions = ['us', 'eu', 'kr', 'tw', 'cn']
        if region.lower() not in valid_regions:
            embed = discord.Embed(
                title="❌ Invalid Region",
                description=f"Invalid region `{region}`. Valid regions are: {', '.join(valid_regions)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        # Show loading message
        loading_embed = discord.Embed(
            title="⏳ Loading Season Cutoffs...",
            description="Fetching current season rating cutoffs from Raider.IO...",
            color=discord.Color.orange()
        )
        loading_message = await ctx.send(embed=loading_embed)
        
        try:
            # Fetch cutoffs data
            cutoffs_data, error = await fetch_season_cutoffs(region.lower())
            
            if error:
                embed = discord.Embed(
                    title="❌ Failed to Fetch Cutoffs",
                    description=f"Error: {error}",
                    color=discord.Color.red()
                )
                embed.add_field(
                    name="What to do",
                    value="Please try again later or check if the Raider.IO API is available.",
                    inline=False
                )
                await loading_message.edit(embed=embed)
                return
            
            # Create and send the cutoffs embed
            embed = create_season_cutoffs_embed(cutoffs_data, region.lower())
            await loading_message.edit(embed=embed)
            
        except Exception as e:
            embed = discord.Embed(
                title="❗ Unexpected Error",
                description="An unexpected error occurred while fetching season cutoffs.",
                color=discord.Color.red()
            )
            embed.add_field(
                name="Error Details",
                value=str(e)[:1000],  # Limit error message length
                inline=False
            )
            await loading_message.edit(embed=embed)
            print(f"Error in cutoffs command: {e}")


async def setup(bot):
    await bot.add_cog(CutoffsCommand(bot))
