import yaml


class ConfigHandler():
    """Config Handler"""

    def _get(self):
        with open('config.yml', 'r') as f:
            self.config = yaml.load(f, Loader=yaml.BaseLoader)
            return self.config

def get():
    return ConfigHandler()._get()
