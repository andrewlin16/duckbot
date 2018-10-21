from discord.ext import commands

import config


def is_owner():
    def predicate(author_id):
        try:
            return author_id in config.owner_ids
        except NameError:
            return False

    return commands.check(lambda ctx: predicate(ctx.message.author.id))
