import discord
from discord.ext import commands
from discord import app_commands
from helpers import checks
import db as db
import random

async def lobbyEmbed(user):
    embed = discord.Embed(title=f'Daily SpekPot!')
    embed.set_thumbnail(url=user.avatar)
    embed.add_field(name='How to play?', value=f'TBD')
    embed.add_field(name='Times left today', value=await db.checkDailySpekPot(user.id), inline=False)
    view = startButton(user)
    view.timeout = None 
    return embed, view

async def gameEmbed(user):
    embed = discord.Embed(title=f'Daily SpekPot!')
    embed.set_thumbnail(url=user.avatar)
    embed.add_field(name='Rewards', value=f'TBD')
    return embed


class startButton(discord.ui.View):
    def __init__(self, user):
        self.user = user
        super().__init__()
    
    @discord.ui.button(label="start", style=discord.ButtonStyle.green)
    async def start(self, interaction: discord.Interaction, button: discord.Button):
        embed = await gameEmbed(self.user)
        await interaction.response.edit_message(embed=embed,view=None)


class dailyspekpot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("DailySpekPot commands are online!")
 
    @checks.has_started()
    @app_commands.command(name="dailyspekpot", description="Play your own daily Spekpot!")
    async def dailyspekpot(self, interaction: discord.Interaction):
        
        if await db.checkDailySpekPot(interaction.user.id) <= 0:
            await interaction.response.send_message('You already played 3 times this day!', ephemeral=True)
            return

        embed = await lobbyEmbed(interaction.user)
        await interaction.response.send_message(embed=embed[0], view=embed[1], ephemeral=True)

async def setup(bot):
    await bot.add_cog(dailyspekpot(bot))