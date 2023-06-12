import discord
from discord.ext import commands
from discord import app_commands
from helpers import checks
import random
import numpy as np
from scipy.signal import convolve2d
import db as db


active_players = {}
games = []
rewards = {
    "win" : 1000,
    "draw" : 200,
    "loss" : 100
}

async def add_active_player(game):
        active_players[game["player1"].id] = games.index(game)
        active_players[game["player2"].id] = games.index(game)

async def remove_active_player(game):
    active_players.pop(game["player1"].id)
    if game["player2"].id in active_players:
        active_players.pop(game["player2"].id)

async def show_board(game):
        embed = discord.Embed(title=f'Connect 4!', description=f'{game["player1"].name} - :red_circle: \n {game["player2"].name} - :yellow_circle:')
        board = ""
        embed.add_field(name="", value=f':one::two::three::four::five::six::seven:', inline=False)
        for row in game["board"]:
            line = ""
            for place in row:
                match place:
                    case 0:
                        line += ":black_large_square:"
                    case 1:
                        line += ":red_circle:"
                    case 2:
                        line += ":yellow_circle:" 
            board += line + "\n"
        embed.add_field(name="", value=f'{board}', inline=False)

        turn = ""
        match game["turn"]:
            case 1:
                turn = "It's <@" + str(game["player1"].id) + ">'s :red_circle: turn!"
            case 2:
                turn = "It's <@" + str(game["player2"].id) + ">'s :yellow_circle: turn!"
        embed.add_field(name="", value=turn, inline=False)
        return embed

async def check_win(game):
    horizontal_kernel = np.array([[ 1, 1, 1, 1]])
    vertical_kernel = np.transpose(horizontal_kernel)
    diag1_kernel = np.eye(4, dtype=np.uint8)
    diag2_kernel = np.fliplr(diag1_kernel)
    detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]

    board = game["board"]

    board2d = []
    match game["turn"]:
        case 1:
            for row in board:
                row2d = []
                for space in row:
                    if space == 2:
                        row2d.append(0)
                    else:
                        row2d.append(space)
                board2d.append(row2d)
        case 2:
            for row in board:
                row2d = []
                for space in row:
                    if space == 1:
                        row2d.append(0)
                    elif space == 2:
                        row2d.append(1)
                    else:
                        row2d.append(space)
                board2d.append(row2d)

    for kernel in detection_kernels:
        if (convolve2d(board2d, kernel, mode="valid") == 4).any():
            return 1
    
    spots_left : int = 0
    for row in board:
        if row.count(0):
            spots_left += 1
    
    if spots_left == 0:
        return 3
    return 0

async def give_rewards(game, id, type):
    match type:
        case "win/loss":
            if game["player1"].id == id:
                await db.giveCoins(game["player1"].id, rewards["win"])
                await db.giveCoins(game["player2"].id, rewards["loss"])
            else:
                await db.giveCoins(game["player1"].id, rewards["loss"])
                await db.giveCoins(game["player2"].id, rewards["win"])
        case "draw":
            await db.giveCoins(game["player1"].id, rewards["draw"])
            await db.giveCoins(game["player2"].id, rewards["draw"])


class connect4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Connect4 commands are online!")

    @checks.has_started()
    @app_commands.command(name="c4challenge", description="Challenges a given user to play Connect 4.")
    @app_commands.describe(member = "The user to invite")
    async def c4challenge(self, interaction: discord.Interaction, member: discord.Member):
        if member.id == 1095362700617461930:
            await interaction.response.send_message("You cannot play against the bot dummy!", ephemeral=True)
            return
        elif interaction.user.id == member.id:
            pass
            #await interaction.response.send_message("You can't play against yourself!", ephemeral=True)
            #return
        elif member.id in active_players:
            await interaction.response.send_message("That person is already playing!", ephemeral=True)
            return
       
        game = {
            "player1" : interaction.user,
            "player2" : member,
            "board" : [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],
            "turn": random.randint(1,2),
            "state" : "invited" 
        }
        games.append(game)
        await interaction.response.send_message(f'<@{interaction.user.id}> challenged <@{member.id}>. Do you accept? Use /c4accept to accept the challenge.')
    
    @checks.has_started()
    @app_commands.command(name="c4accept", description="Accepts the challenge given by an user")
    async def c4accept(self, interaction: discord.Interaction):
        if games == []:
            await interaction.response.send_message(f"You are not invited to any game.", ephemeral=True)
            return
        for game in games:
            if game["player2"].id == interaction.user.id:
                game["state"] = "started"
                await add_active_player(game)
                embed = await show_board(game)
                await interaction.response.send_message(f'<@{interaction.user.id}> accepted the challenge from <@{game["player1"].id}>!', embed=embed)
            else:
                await interaction.response.send_message(f"You are not invited to any game.", ephemeral=True)
                return
    
    @checks.has_started()
    @app_commands.command(name="c4drop", description="Drops a token on the given column while it's your turn.")
    @app_commands.describe(column = "The column to drop your token")
    async def c4drop(self, interaction: discord.Interaction, column : str):
        if not interaction.user.id in active_players:
            await interaction.response.send_message(f'You are not in any game.', ephemeral=True)
            return
        
        if int(column) <= 0 or int(column) >= 8:
            await interaction.response.send_message(f'Please select a valid spot.', ephemeral=True)
            return

        game_id = active_players[interaction.user.id]
        game = games[game_id]
        match game["turn"]:
            case 1:
                if interaction.user.id != game["player1"].id:
                    await interaction.response.send_message(f"It's not your turn yet.", ephemeral=True)
                    return
            case 2:
                if interaction.user.id != game["player2"].id:
                    await interaction.response.send_message(f"It's not your turn yet.", ephemeral=True)
                    return

        board = game["board"]
 
        column_id = int(column) -1

        player_token = game["turn"]

        size = range(len(board))
        for row in size:
            if row == 5 and board[row][column_id] == 0:
                board[row][column_id] = player_token
                break
            elif board[row][column_id] != 0:
                if row - 1 > 0:
                    board[row - 1][column_id] = player_token
                    break
                else:
                    await interaction.response.send_message(f"That column is full. Please select another one.", ephemeral=True)
                    return

        if await check_win(game) == 1:
            game["turn"] = 3
            embed = await show_board(game)
            await interaction.response.send_message(f'<@{interaction.user.id}> won and got {rewards["win"]} SpekCoins, GG!', embed=embed)
            await give_rewards(game, interaction.user.id, "win/loss")
            await remove_active_player(game)
            games.remove(game)
            return
        elif await check_win(game) == 3:
            game["turn"] = 3
            embed = await show_board(game)
            await give_rewards(game, interaction.user.id, "draw")
            await interaction.response.send_message(f"It's a draw!", embed=embed)
            await remove_active_player(game)
            games.remove(game)
            return

        if game["turn"] == 1:
            game["turn"] =2
        elif game["turn"] == 2:
            game["turn"] = 1

        if not game["turn"] == 3:
            embed = await show_board(game)
            await interaction.response.send_message(embed=embed)

        
    @c4challenge.error
    async def on_c4challenge_error(self, interaction, error):
        if isinstance(error, commands.UserNotFound):
            await interaction.response.send_message("User not found.", ephemeral=True)
        else:
            await interaction.response.send_message("An internal error has occured. Please contact the developer", ephemeral=True)

    @c4accept.error
    async def on_c4accept_error(self, interaction, error):
        await interaction.response.send_message("An internal error has occured. Please contact the developer", ephemeral=True)

    @c4drop.error
    async def on_c4drop_error(self, interaction, error):
        await interaction.response.send_message("An internal error has occured. Please contact the developer", ephemeral=True)

async def setup(bot):
    await bot.add_cog(connect4(bot))