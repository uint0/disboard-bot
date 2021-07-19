import json

class ServerConfig:
    def __init__(self, config_file):
        self._file_path = config_file
        self._alias_map = {}
        self._config    = {}

        self.load_from_file()
    

    def load_from_file(self):
        with open(self._file_path) as f:
            config = json.load(f)
        
        new_alias_map  = {}
        new_config_map = {}
        for server in config['servers']:
            server_def = {
                'resource': server['resource'],
                'perms':    server['perms'],
                'meta':     server['meta'],
                'name':     server['name']
            }

            for alias in server.get('aliases', []):
                new_alias_map[alias.lower()] = server['name']
            new_alias_map[server['name'].lower()] = server['name']

            new_config_map[server['name']] = server_def

        self._alias_map = new_alias_map
        self._config = new_config_map
    

    def get_server(self, name):
        try:
            server_name = self._alias_map[name.lower()]
            return self._config[server_name]
        except KeyError:
            return None
    
    def list_servers(self):
        return list(self._config.keys())
