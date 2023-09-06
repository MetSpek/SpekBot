import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import check, Context
from helpers import errorhandling
import data.token as TOKEN
import io
import asyncio
from typing import Literal, Optional
import db as db

intents = discord.Intents.default()

bot = commands.Bot(command_prefix=commands.when_mentioned, description='''All spek bot commands''', intents=intents)

cogs_list = [
    'user',
    'connect4',
    'doubleornothing',
    'spekroulette' ,
    'dailyspekpot',
    'misc'
]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(bot.command_prefix)
    # print('------')
    # try:
    #     await bot.tree.sync(guild=discord.Object(id=1117500597269172265))
    #     print(f"synced command(s)!")
    #     print("!!!DO NOT FORGET TO START THE WAMPSERVER!!!")
    # except Exception as e:
    #     print(e)


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

@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

@bot.command()
@commands.is_owner()
async def admin(ctx: commands.Context, action: str, account: int, amount: int):
    user = await bot.fetch_user(account)
    if db.userExists(account):
        match action:
            case 'gsc':
                await db.giveCoins(account, amount)
                await ctx.send(f'Gave **{user}** {amount} SpekCoins')
    else:
        await ctx.send(f'{user} has no account')

asyncio.run(main())