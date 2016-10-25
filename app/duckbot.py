import argparse

import discord
from discord.ext import commands

import config
from cmd import general, emotes


def parse_arguments():
    parser = argparse.ArgumentParser(description="quack")
    parser.add_argument('-b', '--botname',
                        required=True,
                        choices=config.bots.keys(),
                        help="Name of bot in config file")
    return parser.parse_args()


args = parse_arguments()

bot_info = config.bots[args.botname]
CLIENT_ID = bot_info['client_id']
TOKEN = bot_info['token']

_DESCRIPTION = '''quack'''

bot = commands.Bot(command_prefix='/', description=_DESCRIPTION)

# Register commands to bot
general.register(bot)
emotes.register(bot)


@bot.event
async def on_ready():
    print('logged in: %s (%s)' % (bot.user.name, bot.user.id))

    oauth_url = discord.utils.oauth_url(
        CLIENT_ID, permissions=discord.Permissions.text())
    print('invite me: %s' % oauth_url)


bot.run(TOKEN)
