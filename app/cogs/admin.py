from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

import checks


class Admin:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def my_id(self, ctx: Context):
        """Temporary command to show off checks.is_owner"""
        await self.bot.say(ctx.message.author.id)


def setup(bot: Bot):
    bot.add_cog(Admin(bot))
