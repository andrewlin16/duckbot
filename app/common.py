import random
import string

from discord.ext.commands import Context

rand = random.SystemRandom()


def display_name(ctx: Context) -> string:
    return ctx.message.author.nick or ctx.message.author.name
