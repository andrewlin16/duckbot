from io import BytesIO
import logging
import requests

from discord.ext import commands
from discord.ext.commands import Bot

TWITCH_EMOTES_API = 'https://twitchemotes.com/api_cache/v2/global.json'
BTTV_EMOTES_API = 'https://api.betterttv.net/emotes'


logger = logging.getLogger(__name__)


class TwitchEmotes:

    def __init__(self, bot: Bot):
        self.bot = bot
        emote_cache = {}

        r = requests.get(TWITCH_EMOTES_API)
        ttv_emote_data = r.json()

        ttv_emote_template = ttv_emote_data['template']['small']
        ttv_emotes = {
            name: (ttv_emote_template.replace(
                '{image_id}', str(info['image_id'])), 'png')
            for name, info in ttv_emote_data['emotes'].items()
        }

        logger.info('Got %d Twitch emotes from Twitchemotes.com API' %
                    len(ttv_emotes))
        logger.info('Using template: %s' % ttv_emote_template)

        r = requests.get(BTTV_EMOTES_API)
        bttv_emote_data = r.json()

        bttv_emotes = {
            data['regex']: ('https:' + data['url'], data['imageType'])
            for data in bttv_emote_data['emotes']
        }

        logger.info('Got %d BTTV emotes from BetterTTV emotes API' %
                    len(bttv_emotes))

        emotes = {**ttv_emotes, **bttv_emotes}

        logger.info('Total of %d Twitch + BTTV emotes' % len(emotes))

        @bot.listen('on_message')
        async def respond(message):
            if message.author == bot.user:
                return

            text = message.content

            if text in emotes:
                if text not in emote_cache:
                    url = emotes[text][0]
                    logger.info('Fetching emote %s from %s' % (text, url))

                    emote_img = requests.get(url).content
                    emote_cache[text] = emote_img

                filename = '%s.%s' % (text, emotes[text][1])
                with BytesIO(emote_cache[text]) as data:
                    await bot.send_file(message.channel, data,
                                        filename=filename)


def setup(bot: Bot):
    bot.add_cog(TwitchEmotes(bot))
