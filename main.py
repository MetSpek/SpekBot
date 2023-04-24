# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
import random
import data.pokemondata as pokemondata
import data.token as TOKEN
import data.choosepokemon as choosepokemon

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
async def open(ctx, *args):

    case = ' '.join(args)
    case.lower()
    if case == "s":
        case = "standard"

    pokemon = choosepokemon.choose_pokemon(case)
    
    if pokemon["secondary_type"] != "":
        types = pokemon["primary_type"] + "/" + pokemon["secondary_type"]
    else:
        types = pokemon["primary_type"]

    file = discord.File(f'data/images/normal/1.png', filename="image.png")
    embed = discord.Embed(title=f'#{pokemon["id"]} — {pokemon["name"]}',colour=discord.Colour.random())
    embed.set_thumbnail(url="attachment://image.png")
    embed.add_field(name="", value=f'**Type:** {types} \n **Total IV:** {pokemon["iv_total"]}% \n **Worth:** {pokemon["worth"]}pbc', inline=False)
    await ctx.send(file=file, embed=embed)

@open.error
async def on_open_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("An unknown error has occured.")


bot.run(TOKEN.TOKEN)