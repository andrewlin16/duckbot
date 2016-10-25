from discord.ext.commands import Bot

LENNY = '( ͡° ͜ʖ ͡°)'
GIFF = '༼ つ ◕_◕ ༽つ'
DISAPPROVAL = 'ಠ_ಠ'
DONGER = 'ヽ༼ຈل͜ຈ༽ﾉ'


def register(bot: Bot):
    @bot.command(help=LENNY)
    async def lenny():
        await bot.say(LENNY)

    @bot.command(help=GIFF)
    async def giff():
        await bot.say(GIFF)

    @bot.command(help=DISAPPROVAL)
    async def disapproval():
        await bot.say(DISAPPROVAL)

    @bot.command(help=DONGER)
    async def donger():
        await bot.say(DONGER)
