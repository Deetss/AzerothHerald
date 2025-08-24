"""
Affixes command for the Azeroth Herald bot.
"""

import discord
from discord.ext import commands
from src.utils.api import fetch_affixes
from src.utils.embeds import create_affixes_embed


class AffixesCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='affixes', help='Shows current Mythic+ affixes for the week.')
    async def show_affixes(self, ctx, region='us'):
        """Command to show current Mythic+ affixes."""
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
            title="⏳ Loading Affixes...",
            description="Fetching current Mythic+ affixes from Raider.IO...",
            color=discord.Color.orange()
        )
        loading_message = await ctx.send(embed=loading_embed)
        
        try:
            # Fetch affixes data
            affixes_data, error = await fetch_affixes(region.lower())
            
            if error:
                embed = discord.Embed(
                    title="❌ Failed to Fetch Affixes",
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
            
            # Create and send the affixes embed
            embed = create_affixes_embed(affixes_data, region.lower())
            await loading_message.edit(embed=embed)
            
        except Exception as e:
            embed = discord.Embed(
                title="❗ Unexpected Error",
                description="An unexpected error occurred while fetching affixes.",
                color=discord.Color.red()
            )
            embed.add_field(
                name="Error Details",
                value=str(e)[:1000],  # Limit error message length
                inline=False
            )
            await loading_message.edit(embed=embed)
            print(f"Error in affixes command: {e}")


async def setup(bot):
    await bot.add_cog(AffixesCommand(bot))
