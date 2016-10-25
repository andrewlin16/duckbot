from discord.ext.commands import Bot

LENNY = '( ͡° ͜ʖ ͡°)'
GIFF = '༼ つ ◕_◕ ༽つ'
DISAPPROVAL = 'ಠ_ಠ'
DONGER = 'ヽ༼ຈل͜ຈ༽ﾉ'


def register(bot: Bot):
    @bot.command(pass_context=True, help=LENNY)
    async def lenny(ctx, x=None, y=None):
        await bot.say(LENNY)

    @bot.command(pass_context=True, help=GIFF)
    async def giff(ctx, x=None, y=None):
        await bot.say(GIFF)

    @bot.command(pass_context=True, help=DISAPPROVAL)
    async def disapproval(ctx, x=None, y=None):
        await bot.say(DISAPPROVAL)

    @bot.command(pass_context=True, help=DONGER)
    async def donger(ctx, x=None, y=None):
        await bot.say(DONGER)
