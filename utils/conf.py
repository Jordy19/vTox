import yaml


class ConfigHandler():
    """Config Handler"""

    def _get(self):
        """Returns the YAML config files in dict format."""
        with open('config.yml', 'r') as f:
            self.config = yaml.load(f, Loader=yaml.BaseLoader)
            return self.config

def get():
    """Returns the value received from _get()"""
    return ConfigHandler()._get()
