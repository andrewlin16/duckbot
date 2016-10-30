import re

from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

from common import rand, is_direct_message

RANGE_REGEX = re.compile('\d+-\d+')


class General:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def roll(self, ctx: Context, x=None, y=None):
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
            if RANGE_REGEX.match(x):
                range_split = x.split('-')
                lower_bound = int(range_split[0])
                upper_bound = int(range_split[1])
            else:
                upper_bound = int(x)

        lower_bound = max(lower_bound, 1)
        upper_bound = max(lower_bound, upper_bound)

        num_digits = len(str(upper_bound))

        reply_end = ('(%d-%d): **%0' + str(num_digits) + 'd**') % \
                    (lower_bound, upper_bound,
                     rand.randint(lower_bound, upper_bound))

        if is_direct_message(ctx):
            reply_start = 'You rolled'
        else:
            await self.bot.delete_message(ctx.message)
            reply_start = '**%s** rolls' % ctx.message.author.display_name

        await self.bot.say('%s %s' % (reply_start, reply_end))


def setup(bot: Bot):
    bot.add_cog(General(bot))
