import discord
from discord.ext import commands
from discord import app_commands
from helpers import checks
import db as db
import random

costs = 100

active_players = {}

async def addActivePlayer(id):
    active_players[str(id)] = {
        'value' : costs
    }

async def makeEmbed(user):
    embed = discord.Embed(title=f"Double or Nothing!")
    embed.set_thumbnail(url=user.avatar)
    embed.add_field(name="Current Value:", value=f"{active_players[str(user.id)]['value']} SpekCoins")
    return embed

async def tryDouble(user, interaction: discord.Interaction):
    current_value = active_players[str(user.id)]['value']
    chance = random.randint(1,2)
    match chance:
        case 1:
            active_players[str(user.id)]['value'] = current_value * 2
            view = playButton(user.id)
            embed = await makeEmbed(user)
            embed.add_field(name="Value Doubled!",  value=f"", inline=False)
            await interaction.response.edit_message(embed = embed, view=view)
        case 2:
            view = startButton(user.id)
            embed = discord.Embed(title=f"Double or Nothing!")
            embed.set_thumbnail(url=user.avatar)
            embed.add_field(name="You Lost...", value=f"You can try again")
            await interaction.response.edit_message(embed=embed, view=view)
            return

class startButton(discord.ui.View):
    def __init__(self, user):
        self.user = user
        super().__init__()

    @discord.ui.button(label="start game", style=discord.ButtonStyle.green)
    async def start(self, interaction: discord.Interaction, button: discord.Button):
        if self.user != interaction.user.id:
            await interaction.response.send_message("This is not your instance of Double or Nothing!", ephemeral=True)
            return
    
        if not await db.removeCoins(interaction.user.id, costs):
            await interaction.response.send_message("You do not have enough SpekCoins to play this!", ephemeral=True)
            return

        await addActivePlayer(interaction.user.id)
        view = playButton(interaction.user.id)
        await interaction.response.edit_message(embed=await makeEmbed(interaction.user), view=view)
    
class playButton(discord.ui.View):
    def __init__(self, user):
        self.user = user
        super().__init__()

    @discord.ui.button(label="double", style=discord.ButtonStyle.green)
    async def double(self, interaction: discord.Interaction, button: discord.Button):
        if self.user != interaction.user.id:
            await interaction.response.send_message("This is not your instance of Double or Nothing!", ephemeral=True)
            return

        await tryDouble(interaction.user, interaction)

    @discord.ui.button(label="cash out", style=discord.ButtonStyle.red)
    async def csah(self, interaction: discord.Interaction, button: discord.Button):
        if self.user != interaction.user.id:
            await interaction.response.send_message("This is not your instance of Double or Nothing!", ephemeral=True)
            return
    
        view = startButton(interaction.user.id)
        embed = discord.Embed(title=f"Double or Nothing!")
        embed.set_thumbnail(url=interaction.user.avatar)
        embed.add_field(name="You won", value=f"{active_players[str(interaction.user.id)]['value']} SpekCoins, congrats!")
        await interaction.response.edit_message(embed=embed, view=view)
        await db.giveCoins(interaction.user.id, active_players[str(interaction.user.id)]['value'])


class DoN(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("DoubleOrNothing commands are online!")
    
    @checks.has_started()
    @app_commands.command(name="doublenothing", description="Play the double or nothing game")
    async def doublenothing(self, interaction: discord.Interaction):
        view = startButton(interaction.user.id)
        embed = discord.Embed(title=f"Double or Nothing!")
        embed.set_thumbnail(url=interaction.user.avatar)
        embed.add_field(name="How to play?", value=f"When you click the 'start' button, you pay {costs} SpekCoins and start with a value of 10 and can choose to try to double it and have a chance to lose all. Use the 'check out' button to checkout the current value", inline=False)
        embed.add_field(name="Price:", value="100 SpekCoins")
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(DoN(bot))