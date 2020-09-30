import sys

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from utils.log import LogHandler

class DiscordBot(commands.Bot):
    """
        Main client for vTox.
    """

    def __init__(self, server, config):
        super(DiscordBot, self).__init__(command_prefix="!", owner_id=int(config["owner"]))
        self.log = LogHandler(config["username"])
        self.config = config
        self.server = server
        self.plugins = {}
        self.plugin_list = {"available": [], "loaded": []}

        # Plugin loader
        for plugin in self.config["auto_load_plugins"]:
            plugin_path = f"plugins.{plugin}.plugin"
            self.plugin_list["available"].append(plugin)
            try:
                self.load_extension(plugin_path)
                self.plugin_list["loaded"].append(plugin)
            except Exception as e:
                self.log.error(f"[{self.user}/{plugin}] I'm unable to load this module: {e}")

    async def on_ready(self):
        self.log = LogHandler()
        await self.change_presence(activity=discord.Game(name="Powered by vTox."))
        self.log.info(f"Connected to Discord (Bot owner: {self.config['owner']})")
        self.log.info(f"Plugins available ({len(self.plugin_list['available'])}): {', '.join(self.plugin_list['available'])}")
        self.log.info(f"Plugins loaded ({len(self.plugin_list['loaded'])}): {', '.join(self.plugin_list['loaded'])}")
        if len(self.plugin_list['loaded']) == 0:
            self.log.info("There are no plugins loaded, the bot will be terminated.")
            await self.logout()
            sys.exit()