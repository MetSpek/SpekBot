import discord
from discord.ext import commands
from discord import app_commands
from helpers import checks
import db as db


class user(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("User commands are online!")

    
    @app_commands.command(name="arcadestart", description="Start your arcade account")
    async def arcadestart(self, interaction: discord.Interaction):
        if db.userExists(interaction.user.id):
            await interaction.response.send_message(f"You already started your arcade account!", ephemeral=True)
            return
        
        await db.createUser(interaction.user.id)

        if db.userExists(interaction.user.id):
            await interaction.response.send_message(f"You started your arcade account and now you can play the games!", ephemeral=True)
        else:
            await interaction.response.send_message(f"There was an error creating your account, please try again later.", ephemeral=True)

    @checks.has_started()
    @app_commands.command(name="arcadebalance", description="Check your balance")
    async def arcadebalance(self, interaction: discord.Interaction):
        user = await db.getUserStat(interaction.user.id)
        embed = discord.Embed(title=f"{interaction.user.name}'s balance")
        embed.set_thumbnail(url=interaction.user.avatar)
        balance = int(user['BALANCE'])
        embed.add_field(name="SpekCoins", value=f"{f'{balance:,}'}", inline=False)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(user(bot))