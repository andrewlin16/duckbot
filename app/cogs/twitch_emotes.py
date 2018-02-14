from io import BytesIO
import logging
import re
import requests

from discord.ext import commands
from discord.ext.commands import Bot

TWITCH_EMOTE_TEMPLATE = 'https://static-cdn.jtvnw.net/emoticons/v1/{image_id}/1.0'
NUM_FFZ_EMOTES = 100

TWITCH_EMOTES_API = 'https://twitchemotes.com/api_cache/v3/global.json'
BTTV_EMOTES_API = 'https://api.betterttv.net/emotes'
FFZ_EMOTES_API = 'https://api.frankerfacez.com/v1/emoticons?per_page=%d&sort=count-desc' % NUM_FFZ_EMOTES

logger = logging.getLogger(__name__)


class TwitchEmotes:

    def __init__(self, bot: Bot):
        self.bot = bot
        emote_cache = {}

        # Resolve vanilla Twitch emotes via Twitchemotes.com
        r = requests.get(TWITCH_EMOTES_API)
        ttv_emote_data = r.json()
        ttv_emotes = {
            name: (TWITCH_EMOTE_TEMPLATE.replace(
                '{image_id}', str(info['id'])), 'png')
            for name, info in ttv_emote_data.items()
        }

        logger.info('Got %d Twitch emotes from Twitchemotes.com API' %
                    len(ttv_emotes))
        logger.info('Using template: %s' % TWITCH_EMOTE_TEMPLATE)

        # Resolve BetterTTV emotes
        r = requests.get(BTTV_EMOTES_API)
        bttv_emote_data = r.json()

        bttv_emotes = {
            data['regex']: ('https:' + data['url'], data['imageType'])
            for data in bttv_emote_data['emotes']
        }

        logger.info('Got %d BTTV emotes from BetterTTV emotes API' %
                    len(bttv_emotes))

        # Resolve FrankerFaceZ emotes
        r = requests.get(FFZ_EMOTES_API)
        ffz_emote_data = r.json()

        ffz_emotes = {}
        # Note: iterating manually in case of multiple emotes defined for 1 name
        for data in ffz_emote_data['emoticons']:
            name = data['name']
            if name not in ffz_emotes:
                ffz_emotes[name] = ('https:' + data['urls']['1'], 'png')

        logger.info('Got %d FFZ emotes from FrankerFaceZ API' % len(ffz_emotes))

        # Merge all emotes (do note that order is important for priority)
        # Priority: TTV > BTTV > FFZ
        emotes = {**ffz_emotes, **bttv_emotes, **ttv_emotes}
        logger.info('Total of %d emotes' % len(emotes))

        @bot.listen('on_message')
        async def respond(message):
            if message.author == bot.user:
                return

            emote = self.find_emote(emotes, message.content)

            if emote is not None:
                text, url, extension = emote
                if text not in emote_cache:
                    logger.info('Fetching emote %s from %s' % (text, url))

                    emote_img = requests.get(url).content
                    emote_cache[text] = emote_img

                filename = '%s.%s' % (text, extension)
                with BytesIO(emote_cache[text]) as data:
                    await bot.send_file(message.channel, data,
                                        filename=filename)

    def find_emote(self, emote_dict, text):
        for emote in emote_dict:
            if re.findall(r'\b%s$' % re.escape(emote), text):
                url, extension = emote_dict[emote]
                return (emote, url, extension)
        return None


def setup(bot: Bot):
    bot.add_cog(TwitchEmotes(bot))
