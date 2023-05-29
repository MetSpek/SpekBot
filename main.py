# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
import data.token as TOKEN
import io
import aiohttp

import Pokemon.pokemon as pokemon

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=f"<@{1095362700617461930}>" +  " ", description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(bot.command_prefix)
    print('------')

@bot.command(name="open", aliases=['o'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def open(ctx, *args):
    await pokemon.openCase(ctx, *args)

@open.error
async def on_open_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("An unknown error has occured.")
    if isinstance(error, commands.CommandOnCooldown):
	    await ctx.send(f"You have to wait {round(error.retry_after, 2)} seconds to open another case")

bot.run(TOKEN.TOKEN)