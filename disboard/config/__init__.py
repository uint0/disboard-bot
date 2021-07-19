import os, os.path

from .discord import DiscordConfig
from .azure import AzureConfig
from .webapp import WebAppConfig
from .plt import PltConfig
from .server import ServerConfig
from .minecraft import MinecraftConfig


def _get_conf_file(name):
    return os.path.join(os.environ.get('DISBOARD_CONF_DIR', '../config'), name)


discord = DiscordConfig()
azure = AzureConfig()
webapp = WebAppConfig()
plt = PltConfig()
minecraft = MinecraftConfig(_get_conf_file('minecraft.json'))
server = ServerConfig(_get_conf_file('servers.json'))
