import datetime


class LogHandler():

    def __init__(self, plugin_name=""):
        """"Constructor.
        
        Args:
            plugin_name: The name of the plugin
        """
        self.plugin = plugin_name
        self.now = datetime.datetime.now()
        self.timestamp = self.now.strftime("%b-%d-%Y (%H:%M:%S)")

    def _getFormat(self, message):
        """Returns the string format.
        
        Args: 
            message: The message
        
        """
        if self.plugin:
            return f"{self.timestamp} {self.plugin}: {message}"
        else:
            return f"{self.timestamp}: {message}"

    def info(self, message):
        """Prints the INFO log text.
        
        Args: 
            message: A string containing text.

        """
        text_format = self._getFormat(message)
        print(f"{'INFO':5} {text_format} {message}")

    def error(self, message):
        """Prints the ERROR log text.

        Args: 
            message: A string containing text.
        """
        text_format = self._getFormat(message)
        print(f"{'ERROR':5} {text_format} {message}")

    def debug(self, message):
        """Prints the DEBUG log text.
        
        Args: 
            message: A string containing text.
        """
        text_format = self._getFormat(message)
        print(f"{'DEBUG':5} {text_format} {message}")