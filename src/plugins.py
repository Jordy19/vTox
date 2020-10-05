# Plugin System for vTox (using discord.py:cogs)

import discord.ext.commands.errors

import src.log

class Plugin():
    """ 
        Plugin System using discord.py:cogs
    """

    def __init__(self, bot):
        """
            Constructor.
        """
        self.bot = bot
        self.core = ["owner", "plugin"]
        self.path = "plugins.{}.plugin"

    def load(self, name, core=False):
        """Loads cog extensions
        
        Args:
            name: A plugin name
            core: <optional> True if the plugin is a core plugin
        """
        if core == True:
            path = f"src.commands.{name}"
        else:
            name = name.title()
            path = self.path.format(name)
        try:
            self.bot.load_extension(path.format(name))
        except ModuleNotFoundError as e: 
            self.bot.log.error(f"[{self.bot.user}/{name}] I'm unable to load this module: {e}")
            self.bot.plugin_list["available"].append(name)   
        else:
            if not core:
                if name in self.bot.plugin_list["available"]:
                    self.bot.plugin_list["available"].remove(name)
                else:
                    pass
                self.bot.plugin_list["loaded"].append(name)
            else:
                pass

    def unload(self, name):
        """Unloads cog extensions

        Args:
            name: A plugin name
        """
        if name not in self.bot.plugin_list['loaded']:
            raise PluginNotLoaded(f"The plugin {name} is not loaded.")
        else:
            name = name.title()
            path = self.path.format(name)
            try:
                self.bot.unload_extension(path)
            except discord.ext.commands.errors.ExtensionNotLoaded:
                raise PluginNotLoaded(f"The plugin {name} is not loaded.")
            else:
                self.bot.plugin_list["loaded"].remove(name)
                self.bot.plugin_list["available"].append(name)   



    def load_from_config(self, config):
        """
            Loads all the config specified in the auto_load config list
            This function is ran at initalization.
        Args:
            config: the bot configuration in dict format
        """
        # First, load the core commands.
        core_plugins = []
        for plugin in self.core:
            core_plugins.append(plugin)
            self.load(plugin, core=True)
        # Second, load the plugins listed in 'auto_load'.
        for plugin in config["auto_load_plugins"]:
            self.load(plugin)
        self.bot.log.debug(f"Core Plugins: ({len(core_plugins)}): {', '.join(core_plugins)}")
        self.bot.log.info(f"Plugins loaded({len(self.bot.plugin_list['loaded'])}): {', '.join(self.bot.plugin_list['loaded'])}")

class PluginNotLoaded(Exception):
    """The plugin is not loaded."""
    def __init__(self, message):
        super().__init__(message)

class PluginAlreadyLoaded(Exception):
    """The plugin is already loaded"""
    def __init__(self, message):
        super().__init__(message)
