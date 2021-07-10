import logging

import discord
import discord.ext.commands

import cogs.server.command
import cogs.cost.command
import cogs.minecraft.command
import config


logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")
logging.getLogger('azure').setLevel(logging.ERROR)
logging.getLogger('discord').setLevel(logging.ERROR)


bot = discord.ext.commands.Bot(command_prefix='!')
bot.add_cog(cogs.server.command.ServerCommand(bot))
bot.add_cog(cogs.cost.command.CostCommand(bot))
bot.add_cog(cogs.minecraft.command.MinecraftCommand(bot))


if __name__ ==  "__main__":
    bot.run(config.discord.DISCORD_BOT_TOKEN)