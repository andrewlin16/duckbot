import re

from discord.ext.commands import Bot

from common import rand, display_name


def register(bot: Bot):
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
            range_regex = re.compile('\d+-\d+')
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

        await bot.delete_message(ctx.message)
        await bot.say(
            format_string % (display_name(ctx), lower_bound, upper_bound,
                             rand.randint(lower_bound, upper_bound)))
