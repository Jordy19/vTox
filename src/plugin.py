# Plugin System for vTox (using discord.py:cogs)

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
        self.list = {"available": [], "loaded": []}

    def get_list(self):
        """Returns the self.list dictionary."""
        return self.list

    def load(self, name, core=False):
        """Loads cog extensions
        
        Args:
            name: A plugin name
        """
        if core == True:
            path = f"src.commands.{name}"
        else:
            path = self.path.format(name)
        print(path)
        # self.bot.load_extension(path.format(name))
        self.list["available"].append(name)   
        # except self.log.error(f"[{self.user}/{plugin}] I'm unable to load this module: {e}")
        return True

    def load_from_config(self, config):
        """
            Loads all the config specified in the auto_load config list
            This function is ran at initalization.
        Args:
            config: the bot configuration in dict format
        """
        # First, load the core commands.
        for plugin in self.core:
            self.load(plugin, core=True)
        # Second, load the plugins listed in 'auto_load'.
        for plugin in config["auto_load_plugins"]:
            self.load(plugin)         