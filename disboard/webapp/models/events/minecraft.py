import enum

import pydantic

class MinecraftPlayerConnectionEventType(str, enum.Enum):
    CONNECT = 'connect'
    DISCONNECT = 'disconnect'

class MinecraftServerType(str, enum.Enum):
    PAPER = "paper"
    FABRIC = "fabric"
    VANILLA = "vanilla"


class MinecraftServerInfo(pydantic.BaseModel):
    name: str
    type: MinecraftServerType


class MinecraftPlayerConnectionEvent(pydantic.BaseModel):
    server_info: MinecraftServerInfo
    player_name: str
    connection_event_type: MinecraftPlayerConnectionEventType
