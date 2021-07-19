import json


class MinecraftConfig:
    def __init__(self, servers_conf_file):
        self._conf_path = servers_conf_file
        self._config = {}

        self.load_from_file()
    
    def load_from_file(self):
        with open(self._conf_path) as f:
            config = json.load(f)
        self._config = config
        
    def get_server(self, name):
        return self._config[name]
