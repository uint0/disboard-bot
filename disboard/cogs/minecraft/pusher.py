import discord
import discord.ext.commands as commands


class MinecraftPusher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.push_server_activity)
    
    async def get_server_activity(self):
        pass