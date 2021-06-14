import discord.ext.commands as commands

import handlers.server.server as server_handler
import handlers.server.exceptions as server_exceptions

class ServerConverter(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            return server_handler.Server(argument)
        except server_exceptions.ServerNotConfiguredException:
            return None
