import argparse
import logging

import discord
from discord.ext import commands

import config
from cmd import general, emotes

_DEFAULT_BOT_NAME = 'duckbot'
_DESCRIPTION = '''quack'''


def setup_logging() -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s [%(name)s]: %(message)s)')

    # Log WARNING to 'discord.log'
    file_handler = logging.FileHandler(filename='discord.log', encoding='utf-8',
                                       mode='w')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.WARNING)
    logger.addHandler(file_handler)

    # Log INFO to stderr
    stderr_handler = logging.StreamHandler()
    stderr_handler.setLevel(logging.INFO)
    stderr_handler.setFormatter(formatter)
    logger.addHandler(stderr_handler)

    return logger


def parse_arguments():
    parser = argparse.ArgumentParser(description="quack")
    parser.add_argument('-b', '--botname',
                        choices=config.bots.keys(),
                        default=_DEFAULT_BOT_NAME,
                        help="Name of bot in config file")
    return parser.parse_args()


def main():
    logger = setup_logging()

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
        logger.info('Ready')
        print('--------------------')
        print('logged in: %s (%s)' % (bot.user.name, bot.user.id))

        oauth_url = discord.utils.oauth_url(
            client_id, permissions=discord.Permissions.text())
        print('invite me: %s' % oauth_url)
        print('--------------------')

    bot.run(token)


if __name__ == '__main__':
    main()
