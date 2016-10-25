from discord.ext.commands import Bot

from common import display_name

LENNY = '( ͡° ͜ʖ ͡°)'
GIFF = '༼ つ ◕_◕ ༽つ'
DISAPPROVAL = 'ಠ_ಠ'
DONGER = 'ヽ༼ຈل͜ຈ༽ﾉ'

FORMAT_STRING = '**%s** says: %s'


def register(bot: Bot):
    @bot.command(pass_context=True, help=LENNY)
    async def lenny(ctx, x=None, y=None):
        await bot.delete_message(ctx.message)
        await bot.say(FORMAT_STRING % (display_name(ctx), LENNY))

    @bot.command(pass_context=True, help=GIFF)
    async def giff(ctx, x=None, y=None):
        await bot.delete_message(ctx.message)
        await bot.say(FORMAT_STRING % (display_name(ctx), GIFF))

    @bot.command(pass_context=True, help=DISAPPROVAL)
    async def disapproval(ctx, x=None, y=None):
        await bot.delete_message(ctx.message)
        await bot.say(FORMAT_STRING % (display_name(ctx), DISAPPROVAL))

    @bot.command(pass_context=True, help=DONGER)
    async def donger(ctx, x=None, y=None):
        await bot.delete_message(ctx.message)
        await bot.say(FORMAT_STRING % (display_name(ctx), DONGER))
