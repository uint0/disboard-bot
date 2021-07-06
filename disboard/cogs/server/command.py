import logging

import discord
import discord.ext.commands as commands

import util.azure
import util.discord

import cogs.server.converter as converter
import handlers.server.exceptions as server_exceptions
import config


NO_SUCH_SERVER_MSG = "No such server. Find available servers with !server list"
USAGE_MSG = "Usage: !server <status|start|deallocate|metrics|list|help> [server_name]"

logger = logging.getLogger(__name__)

def get_status_color(status_code):
    if status_code == "PowerState/deallocated":
        return 0xff0000
    elif status_code == "PowerState/running":
        return 0x00ff00
    return 0x4f545c


class ServerCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @util.discord.require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    async def server(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(USAGE_MSG)

    @server.command()
    @util.discord.require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    @util.discord.raises_exception(server_exceptions.ServerForbiddenException)
    async def status(self, ctx, server: converter.ServerConverter):
        if not server:
            return await ctx.send(NO_SUCH_SERVER_MSG)

        logger.info("user %s:[%s] requested status for %s", ctx.message.author, ctx.message.author.id, server)

        async with util.azure.aio_resource(server):
            status = await server.get_status()

        embed = discord.Embed(
            title=server.name,
            description=f"{server.resource_names.group}/{server.resource_names.name}",
            color=get_status_color(status.status_code)
        )
        embed.set_author(name="Azure Compute")
        embed.set_thumbnail(url="https://symbols.getvecta.com/stencil_27/102_vm-symbol.3da37253c9.png")

        embed.add_field(
            name="Status",
            value=status.status_name,
            inline=True
        )
        embed.add_field(
            name="Status Time",
            value=str(status.status_time).rsplit('.', 1)[0] if status.status_time is not None else '-',
            inline=True
        )
        embed.add_field(
            name="Game",
            value=server.meta.get('game'),
            inline=True
        )
        embed.add_field(
            name="Owner",
            value=', '.join(server.meta.get('owner')),
            inline=True
        )
    
        embed.set_footer(text=f"!server status {server.called_name}")
        
        await ctx.send(embed=embed)


    @server.command()
    @util.discord.require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    @util.discord.raises_exception(server_exceptions.ServerForbiddenException)
    async def start(self, ctx, server: converter.ServerConverter):
        if not server:
            return await ctx.send(NO_SUCH_SERVER_MSG)
        
        logger.info("user %s:[%s] requested start for %s", ctx.message.author, ctx.message.author.id, server)
        msg = await ctx.reply(f"Starting server {server}...")

        async with util.azure.aio_resource(server):
            waiter = await server.start()
            await waiter.result()

        await msg.reply('Server start request complete.')


    @server.command(aliases=['stop'])
    @util.discord.require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    @util.discord.raises_exception(server_exceptions.ServerForbiddenException)
    async def deallocate(self, ctx, server: converter.ServerConverter):
        if not server:
            return await ctx.send(NO_SUCH_SERVER_MSG)
        
        logger.info("user %s:[%s] requested deallocate for %s", ctx.message.author, ctx.message.author.id, server)
        msg = await ctx.reply(f"Deallocating server {server}...")

        async with util.azure.aio_resource(server):
            waiter = await server.stop()
            await waiter.result()

        await msg.reply('Server deallocation request complete.')
    
    @server.command(name='list')
    @util.discord.require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    async def _list(self, ctx):
        await ctx.send(f"Available Servers: {', '.join(config.server.list_servers())}")

    @server.command()
    @util.discord.require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    async def help(self, ctx):
        await ctx.send(USAGE_MSG)
