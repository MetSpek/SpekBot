import discord
from discord.ext import commands
from discord import app_commands
from helpers import checks
import db as db
import random
import time

active_players = {}
games = []

async def find_game(id):
    for game in games:
        if game['id'] == id:
            return game

async def lobby_embed(game):
    embed = discord.Embed(title=f'Spek Roulette!')
    playerList = ''
    for player in game['players']:
        playerList += f'- {player.name}\n'
    embed.add_field(name='Current Players:', value=f'{playerList}')
    embed.set_footer(text=f"ID: {game['id']}")
    return embed

class gameButton(discord.ui.View):
    def __init__(self, user, game):
        self.user = user
        self.game = game
        super().__init__()
    
    
    @discord.ui.button(label="join", style=discord.ButtonStyle.blurple)
    async def join(self, interaction: discord.Interaction, button: discord.Button):
        game = await find_game(self.game)
        # if interaction.user in game['players']:
        #     await interaction.response.send_message("You are already playing in this instance!", ephemeral=True)
        #     return
        game['players'].append(interaction.user)
        view = gameButton(self.user, game["id"])
        embed = await lobby_embed(game)
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label="start", style=discord.ButtonStyle.green)
    async def start(self, interaction: discord.Interaction, button: discord.Button):
        if self.user != interaction.user.id:
            await interaction.response.send_message("You are not the owner of this instance!", ephemeral=True)
            return

        game = await find_game(self.game)
        game['state'] = "started"
        await interaction.response.send_message(f"Start game: {game}")

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
        embed = await lobby_embed(game)
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(spekRoulette(bot))