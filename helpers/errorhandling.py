import discord
from discord.ext import commands
from discord import app_commands
from helpers import checks

async def on_tree_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, checks.NotStarted):
        await interaction.response.send_message(f"You have not started with this bot. Use /arcadeStart to start with the Spek Arcade!", ephemeral=True)
    else:
        await interaction.response.send_message(error)