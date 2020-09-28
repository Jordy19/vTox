import datetime


class LogHandler():

    def __init__(self, plugin_name="", message=""):
        self.plugin = plugin_name
        self.now = datetime.datetime.now()
        self.timestamp = self.now.strftime("%b-%d-%Y (%H:%M:%S)")
        # Todo Find a better way to do this.
        if self.plugin == "":
            self.format = f"{self.timestamp}: {message}"
        else:
            self.format = f"{self.timestamp} {self.plugin}: {message}"

    def info(self, message):
        print(f"{'INFO':5} {self.format} {message}")

    def error(self, message):
        print(f"{'ERROR':5} {self.format} {message}")

    def debug(self, message):
        print(f"{'DEBUG':5} {self.format} {message}")