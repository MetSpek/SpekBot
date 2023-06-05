import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import check, Context
import data.token as TOKEN
import io
import asyncio
import os
import json 

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=f"<@{1095362700617461930}>" +  " ", description='''All spek bot commands''', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(bot.command_prefix)
    print('------')
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command(s)!")
    except Exception as e:
        print(e)


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
    bot.help_command = NewHelp()
    await bot.start(TOKEN.TOKEN)

class NewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page)
            await destination.send(embed=emby)


asyncio.run(main())