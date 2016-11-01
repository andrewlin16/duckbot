import logging

from discord import ClientException
from discord.ext import commands
from discord.ext.commands import Bot, Context
from discord.ext.commands import UserInputError

import checks

logger = logging.getLogger(__name__)


class Owner:
    """Commands for use by the owner of the bot"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.group(pass_context=True, hidden=True)
    async def extension(self, ctx: Context):
        """Group of commands for runtime extension management"""
        cmd = ctx.invoked_subcommand or ctx.subcommand_passed
        logger.info('%s called owner command %s' % (ctx.message.author, cmd))

    @extension.command()
    @checks.is_owner()
    async def load(self, cog: str):
        try:
            self.bot.load_extension('cogs.' + cog)
            logger.info('Loaded extension: %s' % cog)
            await self.bot.say('**[Owner]** Loaded extension: %s' % cog)
        except UserInputError:
            await self.bot.say("**[Owner]** Incorrect arguments")
        except ClientException:
            await self.bot.say("**[Owner]** Extension could not be loaded")

    @extension.command()
    @checks.is_owner()
    async def unload(self, cog: str):
        try:
            self.bot.unload_extension('cogs.' + cog)
            logger.info('Unloaded extension: %s' % cog)
            await self.bot.say('**[Owner]** Unloaded extension: %s' % cog)
        except UserInputError:
            await self.bot.say("**[Owner]** Incorrect arguments")

    @extension.command()
    @checks.is_owner()
    async def reload(self, cog: str):
        try:
            self.bot.unload_extension('cogs.' + cog)
            self.bot.load_extension('cogs.' + cog)
            logger.info('Reloaded extension: %s' % cog)
            await self.bot.say('**[Owner]** Reloaded extension: %s' % cog)
        except UserInputError:
            await self.bot.say("**[Owner]** Incorrect arguments")
        except ClientException:
            await self.bot.say("**[Owner]** Extension could not be loaded")


def setup(bot: Bot):
    bot.add_cog(Owner(bot))
