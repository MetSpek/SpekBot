import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import data.data as saveFile

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=f"<@{1095362700617461930}>" +  " ", description='''All spek bot commands''', intents=intents)

data = saveFile.data

class user(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("User commands are online!")

    @bot.command(name="save")
    async def savedata(self, ctx):
        if ctx.message.author.id == 243763234685976577:
            saveFile.saveData()
            await ctx.send(f"Data saved", ephemeral=True)
        else:
            await ctx.send(f"You cannot save...", ephemeral=True)


    @bot.tree.command(name="arcadestart", description="Start your arcade account")
    async def arcadestart(self, interaction: discord.Interaction):
        if str(interaction.user.id) in data:
            await interaction.response.send_message(f"You already started your arcade account!", ephemeral=True)
            return
    
        data[str(interaction.user.id)] = {
            'balance' : 0
        }

        print(data)
        await interaction.response.send_message(f"You started your arcade account and now can play the games!", ephemeral=True)

    @bot.tree.command(name="arcadebalance", description="Check your balance")
    async def arcadebalance(self, interaction: discord.Interaction):
        if not str(interaction.user.id) in data:
            await interaction.response.send_message(f"You have not started with this bot. Use /arcadeStart to start with the Spek Arcade!", ephemeral=True)
            return

        userData = data[str(interaction.user.id)]
        if userData:
            embed = discord.Embed(title=f"{interaction.user.name}'s balance")
            embed.set_thumbnail(url=interaction.user.avatar)
            embed.add_field(name="SpekCoins", value=f"{userData['balance']}", inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"Can't find user")

async def setup(bot):
    await bot.add_cog(user(bot))