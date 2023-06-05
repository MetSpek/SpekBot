import json
import discord
from discord.ext import commands
from discord import app_commands

with open('data/save.json') as json_file:
    data = json.load(json_file)

def saveData():
    with open('data/save.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
