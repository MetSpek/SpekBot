import discord
from discord.ext import commands
from discord import app_commands
from helpers import checks
import db as db
import random

class misccommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("MiscCommands commands are online!")

    @checks.has_started()
    @app_commands.command(name="roll", description="Roll all kinds of dice!")
    @app_commands.describe(dice = "The dice you want to roll [number]d[number]")
    async def rolldice(self, interaction: discord.Interaction, dice : str):
        if not 'd' in dice:
            await self.on_roll_command_error(interaction, 'input')
            return
        
        splitted_values = dice.split('d')

        if splitted_values[0] == '':
            splitted_values[0] = '1'
        
        if splitted_values[1] == '':
            await self.on_roll_command_error(interaction, 'input')
            return

        if not splitted_values[0].isdigit() or not splitted_values[1].isdigit():
            await self.on_roll_command_error(interaction, 'input')
            return

        if int(splitted_values[0]) > 100 or int(splitted_values[1]) > 100:
            await self.on_roll_command_error(interaction, 'number')

        rolled_values = ""
        total_value = 0

        for x in range(0, int(splitted_values[0])):
            random_value = random.randint(1, int(splitted_values[1]))
            total_value += random_value

            if int(splitted_values[0]) > 1:
                if x == int(splitted_values[0]) - 1:
                    rolled_values += f"{random_value} = **{total_value}**" 
                else:
                    rolled_values += f"{random_value} + "
            
        await interaction.response.send_message(f"<@{interaction.user.id}> rolled: **{total_value}**\n ({dice}) \n{rolled_values}")
        
    async def on_roll_command_error(self, interaction: discord.Interaction, type):
        match type:
            case 'input':
                await interaction.response.send_message("Please enter a valid value '[number of dice]d[sides of the die]'.", ephemeral=True)
            case 'number':
                await interaction.response.send_message("The maximum value is 100.", ephemeral=True)
            case other:
                await interaction.response.send_message("A command error has occured, please contact the developer.", ephemeral=True)

    @checks.has_started()
    @app_commands.command(name="invite", description="Get the link to add Spek Arcade to your own server!")
    async def spekinvite(self, interaction: discord.Interaction):
        embed = discord.Embed(title='Want to add SpekBot to your own server?')
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(name='Invite Bot', value="[add here](https://discord.com/api/oauth2/authorize?client_id=1095362700617461930&permissions=28582941293655&scope=bot)")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(misccommands(bot))