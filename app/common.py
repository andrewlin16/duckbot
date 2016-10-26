import random

from discord.ext.commands import Context

rand = random.SystemRandom()


def is_direct_message(ctx: Context) -> bool:
    return ctx.message.channel.is_private
