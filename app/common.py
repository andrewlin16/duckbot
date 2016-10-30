import random

import discord
from discord.ext.commands import Bot, Context

rand = random.SystemRandom()


def is_direct_message(ctx: Context) -> bool:
    return ctx.message.channel.is_private


def get_invite_url(bot: Bot) -> str:
    permissions = discord.Permissions.text()
    return discord.utils.oauth_url(bot.client_id, permissions=permissions)
