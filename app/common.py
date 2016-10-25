import random

from discord.ext.commands import Context

rand = random.SystemRandom()


def display_name(ctx: Context) -> str:
    return ctx.message.author.nick or ctx.message.author.name
