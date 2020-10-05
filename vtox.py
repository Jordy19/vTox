# Project vTox

import asyncio
import sys
import threading
import time

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from src import conf, log, plugin


class vTox(commands.Bot):
    """
        A class that inherit the commands.Bot class. 
    """

    def __init__(self, engine, config):
        """Constructor.
        
        Args:
            server: The Engine() class from start.py
            config: A dict with the bot configuration values. (config.yml)
        """
        super(vTox, self).__init__(command_prefix="!", owner_id=int(config["owner"]))
        self.log = log.Log(config["username"], config["debug_mode"])
        self.engine = engine
        self.config = config
        # Plugin loading requires 'self'.
        self.plugin = plugin.Plugin(self)
        # self.config = config

    async def on_ready(self):
        """Event from discord.py that gets triggered when the Discord bot is ready."""
        await self.change_presence(activity=discord.Game(name="Powered by vTox."))
        self.log.info(f"Connected to Discord (Bot owner: {self.config['owner']})")
        # Load the plugins from our config file.
        self.plugin.load_from_config(self.config)
        # Retriev the plugin list.
        plugin_list = self.plugin.get_list()
        self.log.info(f"Plugins available ({len(plugin_list['available'])}): {', '.join(plugin_list['available'])}")
        self.log.info(f"Plugins loaded ({len(plugin_list['loaded'])}): {', '.join(plugin_list['loaded'])}")
        if len(plugin_list['loaded']) == 0:
            self.log.info("There are no plugins loaded, the bot will be terminated.")
            await self.logout()
            sys.exit()


class Engine():
    """vTox Engine"""

    def __init__(self):
        """Constructor."""
        self.bot = vTox(self, conf.get())
        self.loop = asyncio.get_event_loop()
        self.config = conf.get()

    def disconnect(self):
        """Disconnect ourself from Discord"""
        self.bot.logout()
        
    def init(self):
        """This function is called for initialization."""
        token = self.config["token"]
        self.loop.create_task(self.bot.start(token))
        try:
            self.loop.run_forever()
        finally:
            self.loop.stop()

if __name__ == "__main__":
    logger = log.Log()
    logger.info("Initializing vTox.")
    try:
        __import__("discord")
    except ImportError:
        print("Failure, discord.py not found.")
        print("vTox requires https://github.com/Rapptz/discord.py to work.")
    engine = Engine()
    engine.init()
