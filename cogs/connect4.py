import discord
from discord.ext import commands
import random
import numpy as np
from scipy.signal import convolve2d

active_players = {}
games = []

def add_active_player(game):
        active_players[game["player1"].id] = games.index(game)
        active_players[game["player2"].id] = games.index(game)

def remove_active_player(game):
    active_players.pop(game["player1"].id)
    active_players.pop(game["player2"].id)

def show_board(game):
        embed = discord.Embed(title=f'Connect 4!', description=f'{game["player1"].name} - :red_circle: \n {game["player2"].name} - :blue_circle:')
        board = ""
        embed.add_field(name="", value=f':one: :two: :three: :four: :five: :six: :seven:', inline=False)
        for row in game["board"]:
            line = ""
            for place in row:
                match place:
                    case 0:
                        line += ":black_large_square: "
                    case 1:
                        line += ":red_circle: "
                    case 2:
                        line += ":blue_circle: " 
            board += line + "\n"
        embed.add_field(name="", value=f'{board}', inline=False)

        turn = ""
        match game["turn"]:
            case 1:
                turn = "It's <@" + str(game["player1"].id) + ">'s :red_circle: turn!"
            case 2:
                turn = "It's <@" + str(game["player2"].id) + ">'s :blue_circle: turn!"
        embed.add_field(name="", value=turn, inline=False)
        return embed

def check_win(game):
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

class connect4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Connect4 commands are online!")

    @commands.command(name="c4challenge", aliases=['c4c'], description="Challenges an user to play Connect 4.")
    async def c4challenge(self, ctx, member: discord.Member):
        if member.id == 1095362700617461930:
            raise NoBot(ctx)
        elif ctx.message.author.id == member.id:
            raise SameUser(ctx)
        elif member.id in active_players:
            raise AlreadyPlaying(ctx)
       
        game = {
            "player1" : ctx.message.author,
            "player2" : member,
            "board" : [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],
            "turn": random.randint(1,2),
            "state" : "invited" 
        }
        games.append(game)
        await ctx.send(f'<@{ctx.message.author.id}> challenged <@{member.id}>. Do you accept?')
    
    @commands.command(name="c4accept", aliases=['c4a'], description="Accepts the challenge given by another user.")
    async def c4accept(self, ctx):
        if games == []:
            raise NotInvited(ctx)
        for game in games:
            if game["player2"].id == ctx.message.author.id:
                game["state"] = "started"
                add_active_player(game)
                await ctx.send(f'<@{ctx.message.author.id}> accepted the challenge from <@{game["player1"].id}>!')
                embed = show_board(game)
                await ctx.send(embed=embed)
            else:
                raise NotInvited(ctx)
    
    @commands.command(name="c4drop", aliases=['c4d'], description="Drops a token on the given column while it's your turn.")
    async def c4drop(self, ctx, column):
        if not ctx.message.author.id in active_players:
            raise NoGame(ctx)
        
        if int(column) <= 0 or int(column) >= 8:
            raise NoValidSpot(ctx)

        game_id = active_players[ctx.message.author.id]
        game = games[game_id]

        match game["turn"]:
            case 1:
                if ctx.message.author.id != game["player1"].id:
                    raise NotYourTurn(ctx)
            case 2:
                if ctx.message.author.id != game["player2"].id:
                    raise NotYourTurn(ctx)

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
                    raise ColumnFull(ctx)

        if check_win(game) == 1:
            game["turn"] = 3
            embed = show_board(game)
            await ctx.send(embed=embed)
            await ctx.send(f'<@{ctx.message.author.id}> won, GG!')
            games.remove(game)
            remove_active_player(game)
            return
        elif check_win(game) == 3:
            game["turn"] = 3
            embed = show_board(game)
            await ctx.send(embed=embed)
            await ctx.send(f"It's a draw!")
            games.remove(game)
            remove_active_player(game)
            return

        if game["turn"] == 1:
            game["turn"] =2
        elif game["turn"] == 2:
            game["turn"] = 1

        embed = show_board(game)
        await ctx.send(embed=embed)

        
    @c4challenge.error
    async def on_c4challenge_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("An internal error has occured.")
        if isinstance(error, NoBot):
            await ctx.send("You cannot play against the bot dummy!")
        if isinstance(error, commands.UserNotFound):
            await ctx.send("User not found.")
        if isinstance(error, SameUser):
            await ctx.send("You can't play against yourself!")
        if isinstance(error, AlreadyPlaying):
            await ctx.send("That person is already playing!")

    @c4accept.error
    async def on_c4accept_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("An internal error has occured.")
        if isinstance(error, NotInvited):
            await ctx.send(f'<@{ctx.message.author.id}>, you are not invited to any game.')

    @c4drop.error
    async def on_c4drop_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("An internal error has occured.")
        if isinstance(error, NoGame):
            await ctx.send(f'<@{ctx.message.author.id}>, you are not in any game.')
        if isinstance(error, NoValidSpot):
            await ctx.send(f'<@{ctx.message.author.id}>, please select a valid spot.')
        if isinstance(error, NotYourTurn):
            await ctx.send(f"<@{ctx.message.author.id}>, it's not your turn yet.")
        if isinstance(error, ColumnFull):
            await ctx.send(f"<@{ctx.message.author.id}>, that column is full. Please select another one.")

class NoBot(commands.CommandError):
    def __init__(self, server, *args, **kwargs):
        self.server = server
        super().__init__(*args, **kwargs)

class SameUser(commands.CommandError):
    def __init__(self, server, *args, **kwargs):
        self.server = server
        super().__init__(*args, **kwargs)

class AlreadyPlaying(commands.CommandError):
    def __init__(self, server, *args, **kwargs):
        self.server = server
        super().__init__(*args, **kwargs)


class NotInvited(commands.CommandError):
    def __init__(self, server, *args, **kwargs):
        self.server = server
        super().__init__(*args, **kwargs)

class NoGame(commands.CommandError):
    def __init__(self, server, *args, **kwargs):
        self.server = server
        super().__init__(*args, **kwargs)

class NoValidSpot(commands.CommandError):
    def __init__(self, server, *args, **kwargs):
        self.server = server
        super().__init__(*args, **kwargs)

class NotYourTurn(commands.CommandError):
    def __init__(self, server, *args, **kwargs):
        self.server = server
        super().__init__(*args, **kwargs)

class ColumnFull(commands.CommandError):
    def __init__(self, server, *args, **kwargs):
        self.server = server
        super().__init__(*args, **kwargs)

async def setup(bot):
    await bot.add_cog(connect4(bot))