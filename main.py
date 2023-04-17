# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
import random
import data.pokemondata as pokemondata
import data.token as TOKEN

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


@bot.command()
async def open(ctx, case):
    """Adds two numbers together."""
    if pokemondata.all_cases[case]:
        await ctx.send(f'GOT POKEMON = {pokemondata.all_pokemon[len(pokemondata.all_pokemon) - 1]} from {case}')


bot.run(TOKEN.TOKEN)