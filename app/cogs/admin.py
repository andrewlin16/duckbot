import logging

from discord.ext import commands
from discord.ext.commands import Bot, Context

import checks

logger = logging.getLogger(__name__)


class Admin:
    """Commands for use by a server admin"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.group(pass_context=True, hidden=True)
    async def admin(self, ctx: Context):
        cmd = ctx.invoked_subcommand or ctx.subcommand_passed
        logger.info('%s called admin command %s' % (ctx.message.author, cmd))

    @admin.command()
    @checks.is_owner()
    async def example(self):
        await self.bot.say("I'm an example admin command")


def setup(bot: Bot):
    bot.add_cog(Admin(bot))
