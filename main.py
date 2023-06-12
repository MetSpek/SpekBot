import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import check, Context
from helpers import errorhandling
import data.token as TOKEN
import io
import asyncio
import os
import json 

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=f"<@{1095362700617461930}>" +  " ", description='''All spek bot commands''', intents=intents)

cogs_list = [
    'user',
    'connect4',
    'doubleornothing',
    'spekroulette' 
]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(bot.command_prefix)
    print('------')
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command(s)!")
        print("!!!DO NOT FORGET TO START THE WAMPSERVER!!!")
    except Exception as e:
        print(e)


async def main():
    for cog in cogs_list:
        await bot.load_extension(f'cogs.{cog}')
    bot.help_command = NewHelp()
    bot.tree.on_error = errorhandling.on_tree_error
    await bot.start(TOKEN.TOKEN)

class NewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page)
            await destination.send(embed=emby)


asyncio.run(main())