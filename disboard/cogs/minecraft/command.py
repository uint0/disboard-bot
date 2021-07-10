import discord
import discord.ext.commands as commands

import config


def get_server_icon(server_type: str):
    return {
        'fabric': 'https://avatars.githubusercontent.com/u/21025855'
    }.get(server_type)


class MinecraftCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = None

    async def player_connection(
        self,
        connection_type: str,
        player_name: str,
        server_name: str,
        server_type: str
    ):
        if connection_type == "connect":
            descriptor = "joined"
            color      = 0x00ff00
            footer     = "addict"
        elif connection_type == "disconnect":
            descriptor = "left"
            color      = 0xff0000
            footer     = "no u"

        embed = discord.Embed(
            title=f"{player_name} {descriptor} the game",
            color=color
        )
        embed.set_author(name=server_name.title(), icon_url=get_server_icon(server_type))
        embed.set_footer(text=footer)

        await self.send_message(embed=embed)

    
    async def send_message(self, *args, **kwargs):
        if self.channel is None:
            self.channel = self.bot.get_channel(config.discord.DISCORD_CHANNEL_MINECRAFT)
        await self.channel.send(*args, **kwargs)