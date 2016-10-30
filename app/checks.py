from discord.ext import commands

import config


def is_owner():
    def predicate(author_id):
        try:
            return config.owner_id == author_id
        except NameError:
            return False

    return commands.check(lambda ctx: predicate(ctx.message.author.id))
