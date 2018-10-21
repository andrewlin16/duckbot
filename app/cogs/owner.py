import logging
import subprocess
import sys

from discord import ClientException
from discord.ext import commands
from discord.ext.commands import Bot, Context
from discord.ext.commands import UserInputError

import checks

logger = logging.getLogger(__name__)


class Owner:
    """Commands for use by the owner of the bot"""

    SAY_PREFIX = "[Owner] "

    def __init__(self, bot: Bot):
        self.bot = bot

    async def say(self, s: str):
        await self.bot.say(Owner.SAY_PREFIX + s)

    @commands.command(hidden=True)
    @checks.is_owner()
    async def upgrade(self):
        """Upgrade the bot by pulling from git origin and restarting (not included)"""
        await self.say("Upgrading the bot")
        subprocess.run("git pull origin master".split(" "))
        sys.exit(0)

    @commands.group(pass_context=True, hidden=True)
    @checks.is_owner()
    async def cog(self, ctx: Context):
        """Group of commands for runtime cog management"""
        cmd = ctx.invoked_subcommand or ctx.subcommand_passed
        logger.info("%s called Owner command: %s" % (ctx.message.author, cmd))

    @cog.command()
    async def load(self, cog: str):
        try:
            self.bot.load_extension("cogs." + cog)
            logger.info("Loaded cog: %s" % cog)
            await self.say("Loaded cog: %s" % cog)
        except UserInputError:
            await self.say("Incorrect arguments")
        except (ClientException, ImportError):
            await self.say("Cog could not be loaded")

    @cog.command()
    async def unload(self, cog: str):
        if cog == "owner":
            await self.say("Don't be a dummy")
            return
        try:
            self.bot.unload_extension("cogs." + cog)
            logger.info("Unloaded cog: %s" % cog)
            await self.say("Unloaded cog: %s" % cog)
        except UserInputError:
            await self.say("Incorrect arguments")

    @cog.command()
    async def reload(self, cog: str):
        try:
            self.bot.unload_extension("cogs." + cog)
            self.bot.load_extension("cogs." + cog)
            logger.info("Reloaded cog: %s" % cog)
            await self.say("Reloaded cog: %s" % cog)
        except UserInputError:
            await self.say("Incorrect arguments")
        except (ClientException, ImportError):
            await self.say("Cog could not be loaded")


def setup(bot: Bot):
    bot.add_cog(Owner(bot))
