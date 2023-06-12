import discord
from discord.ext import commands
from discord import app_commands
import db as db

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=f"<@{1095362700617461930}>" +  " ", description='''All spek bot commands''', intents=intents)

class NotStarted(app_commands.AppCommandError):
    pass

def has_started():
    def predicate(interaction: discord.Interaction):
        if db.userExists(interaction.user.id):
            return True
        else:
            raise NotStarted(interaction)
    return app_commands.check(predicate)