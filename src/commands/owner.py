import discord
from discord.ext import commands


class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.info = {
            "name": "",
            "desc": "Owner related commands",
            "authors": "Jordy19",
            "version": "1.0"
        }

def setup(bot):
    bot.add_cog(Owner(bot))