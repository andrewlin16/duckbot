import discord
import duckbot_settings
import os
import random
import re
from discord.ext import commands

_DESCRIPTION = '''quack'''

bot = commands.Bot(command_prefix='/', description=_DESCRIPTION)
rand = random.SystemRandom()

range_regex = re.compile('\d+-\d+')


@bot.command(pass_context=True)
async def roll(ctx, bound1=None, bound2=None):
    lower_bound = 1
    upper_bound = 100

    if bound2 is not None:
        lower_bound = int(bound1)
        upper_bound = int(bound2)
    elif bound1 is not None:
        if (range_regex.match(bound1)):
            range_split = bound1.split('-')
            lower_bound = int(range_split[0])
            upper_bound = int(range_split[1])
        else:
            upper_bound = int(bound1)

    lower_bound = max(lower_bound, 1)
    upper_bound = max(lower_bound, upper_bound)

    num_digits = len(str(upper_bound))
    format_string = '**%s** rolls (%d-%d): **%0' + str(num_digits) + 'd**'

    display_name = ctx.message.author.nick or ctx.message.author.name

    await bot.say(format_string % (display_name, lower_bound, upper_bound,
                                   rand.randint(lower_bound, upper_bound)))


@bot.command()
async def dbg(expr):
    if 'ALLOW_EVAL' in os.environ and os.environ['ALLOW_EVAL']:
        try:
            await bot.say('`%s`' % eval(expr))
        except Exception as e:
            await bot.say('%s: `%s`' % (type(e), e))
    else:
        await bot.say('Sorry, no eval!')


@bot.event
async def on_ready():
    print('logged in: %s (%s)' % (bot.user.name, bot.user.id))

    oauth_url = discord.utils.oauth_url(
        duckbot_settings.CLIENT_ID, permissions=discord.Permissions.text())
    print('invite me: %s' % oauth_url)

bot.run(duckbot_settings.TOKEN)
