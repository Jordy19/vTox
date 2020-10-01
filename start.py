# Project vTox

import asyncio
import threading
import time

from utils import bot, conf, log


class vTox():
    """vTox"""

    def __init__(self):
        """Constructor."""
        self.bot = bot.DiscordBot(self, conf.get())
        self.loop = asyncio.get_event_loop()
        self.log = log.LogHandler()
        self.config = conf.get()

    def disconnect(self):
        """Disconnect ourself from Discord"""
        self.bot.logout()
        
    def run(self):
        """This function is called for initialization."""
        token = self.config["token"]
        self.loop.create_task(self.bot.start(token))
        try:
            self.loop.run_forever()
        finally:
            self.loop.stop()

if __name__ == "__main__":
    logger = log.LogHandler()
    logger.info("Initializing vTox...")
    try:
        __import__("discord")
    except ImportError:
        print("Failure, discord.py not found.")
        print("vTox requires https://github.com/Rapptz/discord.py to work.")
    engine = vTox()
    engine.init()
