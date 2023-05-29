import discord
from discord.ext import commands
import data.token as TOKEN
import io
import asyncio
import os

description = '''All spek bot commands'''


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=f"<@{1095362700617461930}>" +  " ", description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(bot.command_prefix)
    print('------')

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