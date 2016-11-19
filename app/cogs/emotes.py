from discord.ext import commands
from discord.ext.commands import Bot

DISAPPROVAL = 'ಠ_ಠ'
DONGER = 'ヽ༼ຈل͜ຈ༽ﾉ'
GIFF = '༼ つ ◕_◕ ༽つ'
LENNY = '( ͡° ͜ʖ ͡°)'


class Emotes:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help=DISAPPROVAL)
    async def disapproval(self):
        await self.bot.say(DISAPPROVAL)

    @commands.command(help=DONGER)
    async def donger(self):
        await self.bot.say(DONGER)

    @commands.command(help=GIFF)
    async def giff(self):
        await self.bot.say(GIFF)

    @commands.command(help=LENNY)
    async def lenny(self):
        await self.bot.say(LENNY)


def setup(bot: Bot):
    bot.add_cog(Emotes(bot))
