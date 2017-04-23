import argparse
import logging

from discord.ext import commands

import config
from common import get_invite_url

_DEFAULT_BOT_NAME = 'duckbot'
_DESCRIPTION = '''quack'''

default_cogs = [
    'admin',
    'emotes',
    'general',
    'owner',
    'poll',
    'twitch_emotes',
]


def setup_logging() -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s [%(name)s]: %(message)s')

    # Log WARNING to 'discord.log'
    file_handler = logging.FileHandler(filename='discord.log', encoding='utf-8',
                                       mode='a')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
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

    bot = commands.Bot(command_prefix='/', description=_DESCRIPTION)

    botname = args.botname
    if botname not in config.bots:
        if len(config.bots) == 1:
            botname = next(iter(config.bots.keys()))
        else:
            raise Exception('Bot config for "%s" not found.' % botname)

    bot_info = config.bots[botname]
    bot.client_id = bot_info['client_id']
    token = bot_info['token']

    cog_list = bot_info['cogs'] if 'cogs' in bot_info else default_cogs

    # Register commands to bot
    for cog in cog_list:
        bot.load_extension('cogs.' + cog)
        logger.info('Loaded extension: %s' % cog)

    @bot.event
    async def on_ready():
        logger.info('Ready')
        logger.info('--------------------')
        logger.info('logged in: %s (%s)' % (bot.user.name, bot.user.id))
        logger.info('invite me: %s' % get_invite_url(bot))
        logger.info('--------------------')
        logger.info('Connected to servers:')
        for server in bot.servers:
            logger.info('    ' + str(server))

    bot.run(token)


if __name__ == '__main__':
    main()
