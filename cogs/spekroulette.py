import discord
from discord.ext import commands
from discord import app_commands
from helpers import checks
import db as db
import random
import time

active_players = {}
games = []

class gameButton(discord.ui.View):
    def __init__(self, user, game):
        self.user = user
        self.game = game
        super().__init__()
    
    @discord.ui.button(label="start", style=discord.ButtonStyle.green)
    async def start(self, interaction: discord.Interaction, button: discord.Button):
        if self.user != interaction.user.id:
            await interaction.response.send_message("You are not the owner of this instance!", ephemeral=True)
            return

        await interaction.response.send_message(f"Start game: {self.game}")
    
    @discord.ui.button(label="join", style=discord.ButtonStyle.blurple)
    async def join(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message(f"Join game: {self.game}")

class spekRoulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("SpekRoulette commands are online!")
    
    @checks.has_started()
    @app_commands.command(name="spekroulette", description="Play Spek Roulette!")
    async def spekroulette(self, interaction: discord.Interaction):
        game = {
            "id" : hex(int(str(interaction.user.id) + str(int(time.time())))),
            "players" : [], 
            "state" : "lfp" 
        }

        games.append(game)
        view = gameButton(interaction.user.id, game["id"])
        embed = discord.Embed(title=f"Spek Roulette!")
        embed.add_field(name="Current Players:", value=f"- {interaction.user.name}")
        embed.set_footer(text=f"ID: {game['id']}")
        await interaction.response.send_message(embed=embed, view=view)
    
    @checks.has_started()
    @app_commands.command(name="spektest", description="test")
    async def spektest(self, interaction: discord.Interaction):
        await interaction.response.send_message("THIS SHOULD ONLY BE IN THE TEST SERVER")


async def setup(bot):
    await bot.add_cog(spekRoulette(bot))