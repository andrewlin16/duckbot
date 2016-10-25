import argparse
import random
import re

import discord
from discord.ext import commands

import config


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
rand = random.SystemRandom()

range_regex = re.compile('\d+-\d+')


@bot.command(pass_context=True)
async def roll(ctx, x=None, y=None):
    """Rolls a random number.

    Options:
    • "/roll": Rolls 1-100.
    • "/roll [x]": Rolls 1-x.
    • "/roll [x] [y]" or "/roll [x]-[y]": Rolls x-y.
    """
    lower_bound = 1
    upper_bound = 100

    if y is not None:
        lower_bound = int(x)
        upper_bound = int(y)
    elif x is not None:
        if range_regex.match(x):
            range_split = x.split('-')
            lower_bound = int(range_split[0])
            upper_bound = int(range_split[1])
        else:
            upper_bound = int(x)

    lower_bound = max(lower_bound, 1)
    upper_bound = max(lower_bound, upper_bound)

    num_digits = len(str(upper_bound))
    format_string = '**%s** rolls (%d-%d): **%0' + str(num_digits) + 'd**'

    display_name = ctx.message.author.nick or ctx.message.author.name

    await bot.delete_message(ctx.message)
    await bot.say(format_string % (display_name, lower_bound, upper_bound,
                                   rand.randint(lower_bound, upper_bound)))


@bot.event
async def on_ready():
    print('logged in: %s (%s)' % (bot.user.name, bot.user.id))

    oauth_url = discord.utils.oauth_url(
        CLIENT_ID, permissions=discord.Permissions.text())
    print('invite me: %s' % oauth_url)


bot.run(TOKEN)
