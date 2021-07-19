import os


class DiscordConfig:
    DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']

    DISCORD_CHANNEL_AZURE = os.environ['DISCORD_CHANNEL_AZURE']
    DISCORD_CHANNEL_MINECRAFT = int(os.environ['DISCORD_CHANNEL_MINECRAFT'])
