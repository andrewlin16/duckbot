import logging

from discord import ClientException
from discord.ext import commands
from discord.ext.commands import Bot, Context
from discord.ext.commands import UserInputError

import checks

logger = logging.getLogger(__name__)


class Admin:
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.group(pass_context=True, hidden=True)
    async def extension(self, ctx: Context):
        logger.info('%s called admin command %s' % (ctx.message.author, ctx.invoked_subcommand))

    @extension.command()
    @checks.is_owner()
    async def load(self, cog: str):
        try:
            self.bot.load_extension('cogs.' + cog)
            logger.info('Loaded extension: %s' % cog)
            await self.bot.say('**[Admin]** Loaded extension: %s' % cog)
        except UserInputError:
            await self.bot.say("**[Admin]** incorrect arguments")
        except ClientException:
            await self.bot.say("**[Admin]** Extension could not be loaded")

    @extension.command()
    @checks.is_owner()
    async def unload(self, cog: str):
        try:
            self.bot.unload_extension('cogs.' + cog)
            logger.info('Unloaded extension: %s' % cog)
            await self.bot.say('**[Admin]** Unloaded extension: %s' % cog)
        except UserInputError:
            await self.bot.say("**[Admin]** incorrect arguments")

    @extension.command()
    @checks.is_owner()
    async def reload(self, cog: str):
        try:
            self.bot.unload_extension('cogs.' + cog)
            self.bot.load_extension('cogs.' + cog)
            logger.info('Reloaded extension: %s' % cog)
            await self.bot.say('**[Admin]** Reloaded extension: %s' % cog)
        except UserInputError:
            await self.bot.say("**[Admin]** incorrect arguments")
        except ClientException:
            await self.bot.say("**[Admin]** Extension could not be loaded")


def setup(bot: Bot):
    bot.add_cog(Admin(bot))
