import argparse

import discord
from discord.ext import commands

import config
from cmd import general, emotes


_DEFAULT_BOT_NAME = 'duckbot'
_DESCRIPTION = '''quack'''


def parse_arguments():
    parser = argparse.ArgumentParser(description="quack")
    parser.add_argument('-b', '--botname',
                        choices=config.bots.keys(),
                        default=_DEFAULT_BOT_NAME,
                        help="Name of bot in config file")
    return parser.parse_args()


def main():
    args = parse_arguments()

    botname = args.botname
    if botname not in config.bots:
        if len(config.bots) == 1:
            botname = next(iter(config.bots.keys()))
        else:
            raise Exception('Bot config for "%s" not found.' % botname)

    bot_info = config.bots[botname]
    client_id = bot_info['client_id']
    token = bot_info['token']

    bot = commands.Bot(command_prefix='/', description=_DESCRIPTION)

    # Register commands to bot
    general.register(bot)
    emotes.register(bot)

    @bot.event
    async def on_ready():
        print('logged in: %s (%s)' % (bot.user.name, bot.user.id))

        oauth_url = discord.utils.oauth_url(
            client_id, permissions=discord.Permissions.text())
        print('invite me: %s' % oauth_url)

    bot.run(token)


if __name__ == '__main__':
    main()
