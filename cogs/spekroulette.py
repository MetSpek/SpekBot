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
    embed.set_thumbnail(url=game['players'][0].avatar)
    embed.add_field(name='How to play?', value=f'Spek roulette works by having a revolver with 1 bullet in it. One-by-one you pull the trigger and try to survive. Last one standing wins...')
    
    embed.add_field(name='Bid Amount:', value=f'{game["bid"]:,}\n\n **Total Amount:**\n {game["total_bid"]:,}')
    embed.add_field(name='Current Players:', value=f'{playerList}', inline=False)
    embed.set_footer(text=f"ID: {game['id']}")
    return embed

async def game_embed(game, action):
    embed = discord.Embed(title=f'Spek Roulette!')
    playerList = ''
    for player in game['alive_players']:
        if(player.id == game['current_shooter'].id):
            playerList += f'- {player.name} :gun:\n'
        else:
            playerList += f'- {player.name}\n'
    embed.add_field(name='Alive Players:', value=f'{playerList}')
    embed.add_field(name='', value=f'{action}', inline=False)
    # embed.add_field(name='Clip:', value=f'{game["clip"]}')
    embed.set_footer(text=f"ID: {game['id']}")
    return embed

async def make_clip():
    clip = [1,0,0,0,0,0]
    random.shuffle(clip)
    return clip

async def handle_shoot(game, interaction):
    if(game['clip'][game['current_shot']] == 0):
        await update_game(game)
        return True
    else:
        for player in game['alive_players']:
            if(player == game['current_shooter']):
                await update_game(game)
                game['alive_players'].remove(player)
                await check_win(game, interaction, player)
                break
        
        return False

async def check_win(game, interaction, player):
    if(len(game['alive_players']) == 1):
        await db.giveCoins(game["alive_players"][0].id, game['total_bid'])
        await interaction.response.send_message(f'<@{player.id}> shot themselves and <@{game["alive_players"][0].id}> won!')

async def update_game(game):
    game['current_shot'] = game['current_shot'] + 1
    if(game['current_shot'] > 5):
        game['current_shot'] = 0
    
    current_index = game['alive_players'].index(game['current_shooter'])
    if(current_index >= len(game['alive_players']) - 1):
        current_index = 0
    else:
        current_index += 1
    game['current_shooter'] = game['alive_players'][current_index]


class lobbyButton(discord.ui.View):
    def __init__(self, user, game):
        self.user = user
        self.game = game
        super().__init__()
    
    @checks.has_started()
    @discord.ui.button(label="join", style=discord.ButtonStyle.blurple)
    async def join(self, interaction: discord.Interaction, button: discord.Button):
        game = await find_game(self.game)

        
        if interaction.user in game['players']:
            await interaction.response.send_message("You are already playing in this instance!", ephemeral=True)
            return

        if(game['state'] != 'lfp'):
            await interaction.response.send_message("The game has already started")
            return
        
        if(len(game['players']) >= 6):
            await interaction.response.send_message("The game is already full")
            return
        
        if not await db.checkCoins(interaction.user.id, game["bid"]):
            await interaction.response.send_message("You do not have enough SpekCoins to bid this high!", ephemeral=True)
            return
        
        game['players'].append(interaction.user)
        game['total_bid'] += game['bid']
        view = lobbyButton(self.user, game["id"])
        embed = await lobby_embed(game)
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label="start", style=discord.ButtonStyle.green)
    async def start(self, interaction: discord.Interaction, button: discord.Button):
        if self.user != interaction.user.id:
            await interaction.response.send_message("You are not the owner of this instance!", ephemeral=True)
            return

        game = await find_game(self.game)
       
        if len(game['players']) <= 1:
            await interaction.response.send_message("There aren't enough players to start the game", ephemeral=True)
            return
        
        for player in game['players']:
            await db.removeCoins(player.id, game['bid'])

        game['state'] = "started"
        game['alive_players'] = game['players']
        random.shuffle(game['alive_players'])
        game['current_shooter'] = game['alive_players'][0]
        game['clip'] = await make_clip()
        embed = await game_embed(game, 'Let the games begin!')
        view = gameButton(interaction.user.id, game["id"])
        await interaction.response.send_message(embed=embed, view=view)
        # await interaction.response.send_message(f"Start game: {game}")
    
    @discord.ui.button(label="cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.Button):
        if self.user != interaction.user.id:
            await interaction.response.send_message("You are not the owner of this instance!", ephemeral=True)
            return

        embed = discord.Embed(title=f'Spek Roulette!')
        embed.add_field(name='Match Cancelled...', value='')
        await interaction.response.edit_message(embed=embed, view=None)

class gameButton(discord.ui.View):
    def __init__(self, user, game):
        self.user = user
        self.game = game
        super().__init__()
    
    @discord.ui.button(label="shoot", style=discord.ButtonStyle.green)
    async def shoot(self, interaction: discord.Interaction, button: discord.Button):
        game = await find_game(self.game)

        if(interaction.user.id != game['current_shooter'].id):
            await interaction.response.send_message("It's not your turn yet!", ephemeral=True)
            return

        if(await handle_shoot(game, interaction)):
            embed = await game_embed(game, f'{interaction.user.name} has survived this round...')
        else:
            game['clip'] = await make_clip()
            embed = await game_embed(game, f'{interaction.user.name} has died...')
            
        
        view = gameButton(interaction.user.id, game["id"])
        await interaction.response.edit_message(embed=embed, view=view)
            

class spekRoulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("SpekRoulette commands are online!")
    
    @checks.has_started()
    @app_commands.command(name="spekroulette", description="Play Spek Roulette!")
    @app_commands.describe(bid = "The amount you want to bid")
    async def spekroulette(self, interaction: discord.Interaction, bid : int):

        if(bid <= 0):
            await interaction.response.send_message("You must at least bid 1 SpekCoin!", ephemeral=True)
            return

        if not await db.checkCoins(interaction.user.id, bid):
            await interaction.response.send_message("You do not have enough SpekCoins to bid this high!", ephemeral=True)
            return
        

        game = {
            "id" : hex(int(str(interaction.user.id) + str(int(time.time())))),
            "players" : [],
            "bid" : bid,
            "total_bid" : bid,
            "alive_players" : [], 
            "state" : "lfp",
            "current_shooter" : {},
            "clip" : [],
            "current_shot" : 0
        }

        game['players'].append(interaction.user)
        games.append(game)
        view = lobbyButton(interaction.user.id, game["id"])
        embed = await lobby_embed(game)
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(spekRoulette(bot))