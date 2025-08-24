"""
Error handling utilities for the Azeroth Herald bot.
"""

import discord
from discord.ext import commands


async def handle_command_error(ctx, error):
    """Centralized command error handling."""
    # Command not found
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="❌ Command Not Found",
            description=f"Sorry, I don't recognize the command `{ctx.message.content}`",
            color=discord.Color.red()
        )
        
        embed.add_field(
            name="Available Commands",
            value=(
                "`!checklist` - Show the weekly checklist\n"
                "`!warning` - Show the reset warning\n"
                "`!time` - Show current time and schedule\n"
                "`!affixes` - Show current M+ affixes\n"
                "`!cutoffs` - Show M+ season cutoffs\n"
                "`!test` - Test bot functionality\n"
                "`!help` - Show all commands"
            ),
            inline=False
        )
        
        embed.set_footer(text="Use !help for detailed command information | Azeroth Herald")
        await ctx.send(embed=embed)
        return
    
    # Missing required arguments
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="❌ Missing Arguments",
            description=f"You're missing some required arguments for this command.",
            color=discord.Color.red()
        )
        embed.add_field(
            name="Help",
            value=f"Use `!help {ctx.command.name}` for more information about this command.",
            inline=False
        )
        await ctx.send(embed=embed)
        return
    
    # Command is on cooldown
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            title="⏰ Command on Cooldown",
            description=f"This command is on cooldown. Try again in {error.retry_after:.1f} seconds.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
        return
    
    # User lacks permissions
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="🚫 Missing Permissions",
            description="You don't have the required permissions to use this command.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # Bot lacks permissions
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(
            title="🤖 Bot Missing Permissions",
            description="I don't have the required permissions to execute this command.",
            color=discord.Color.red()
        )
        embed.add_field(
            name="Required Permissions",
            value=", ".join(error.missing_permissions),
            inline=False
        )
        await ctx.send(embed=embed)
        return
    
    # Generic error handling
    else:
        embed = discord.Embed(
            title="❗ Something Went Wrong",
            description="An unexpected error occurred while processing your command.",
            color=discord.Color.red()
        )
        embed.add_field(
            name="What to do",
            value="Please try again later or contact a server administrator if the problem persists.",
            inline=False
        )
        await ctx.send(embed=embed)
        
        # Log the error for debugging
        print(f"Unhandled command error: {error}")
        print(f"Command: {ctx.command}")
        print(f"User: {ctx.author}")
        print(f"Channel: {ctx.channel}")
        return
