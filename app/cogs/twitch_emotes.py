from io import BytesIO
import requests

from discord.ext import commands
from discord.ext.commands import Bot

TWITCH_EMOTES_API = 'https://twitchemotes.com/api_cache/v2/global.json'


class TwitchEmotes:

    def __init__(self, bot: Bot):
        self.bot = bot

        r = requests.get(TWITCH_EMOTES_API)
        emote_data = r.json()

        emote_template = emote_data['template']['small']
        emote_ids = {name: info['image_id'] for name, info in
                     emote_data['emotes'].items()}
        emote_cache = {}

        @bot.listen('on_message')
        async def respond(message):
            if message.author == bot.user:
                return

            text = message.content

            if text in emote_ids:
                if text not in emote_cache:
                    url = emote_template.replace('{image_id}',
                                                 str(emote_ids[text]))

                    emote_img = requests.get(url).content
                    emote_cache[text] = emote_img

                data = BytesIO(emote_cache[text])
                filename = '%s.png' % text
                await bot.send_file(message.channel, data, filename=filename)


def setup(bot: Bot):
    bot.add_cog(TwitchEmotes(bot))
