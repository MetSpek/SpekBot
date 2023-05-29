import discord
from discord.ext import commands
import random
import Pokemon.pokemondata as pokemondata
import Pokemon.choosepokemon as choosepokemon


async def openCase(ctx, *args):
    case = ' '.join(args)
    case.lower()
    if case == "s":
        case = "standard"

    pokemon = choosepokemon.choose_pokemon(case)
    if pokemon["secondary_type"] != "":
        types = pokemon["primary_type"] + "/" + pokemon["secondary_type"]
    else:
        types = pokemon["primary_type"]

   
    match pokemon["rarity"]:
        case "common":
            rarity_colour = discord.Color.light_grey()
        case "uncommon":
            rarity_colour = discord.Color.blue()
        case "rare":
            rarity_colour = discord.Color.purple()
        case "legendary":
            rarity_colour = discord.Color.red()
        case "mythical":
            rarity_colour = discord.Color.gold()

    file = discord.File(f'Pokemon/images/normal/{pokemon["id"]}.png', filename="image.png")
    embed = discord.Embed(title=f'#{pokemon["id"]} — {pokemon["name"]}',colour=rarity_colour)
    embed.set_thumbnail(url="attachment://image.png")
    embed.add_field(name="", value=f'**Type:** {types} \n **Total IV:** {pokemon["iv_total"]}% \n **Worth:** {pokemon["worth"]}pbc', inline=False)
    await ctx.send(file=file, embed=embed)

