import logging

from discord import User
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

logger = logging.getLogger(__name__)


class PollState:

    def __init__(self, owner: User, question: str, answers):
        self.original_message = None
        self.owner = owner
        self.question = question
        self.answers = [{'name': answer, 'count': 0} for answer in answers]
        self.voters = set()

    def __str__(self):
        return '{}\n{}'.format(
            self.question,
            '\n'.join(['{}. {} - {}'.format(i + 1, ans['name'], ans['count'])
                       for i, ans in enumerate(self.answers)])
        )


class Poll:

    def __init__(self, bot):
        self.bot = bot
        self.current_polls = {}

    @commands.group(pass_context=True)
    async def poll(self, ctx: Context):
        """Poll
        """
        logger.info('/poll received')

    @poll.command(pass_context=True)
    async def start(self, ctx: Context, question=None, *answers):
        if question is None:
            return  # TODO handle spurious /poll

        if ctx.message.channel in self.current_polls:
            return  # TODO handle chan already has poll

        current_poll = PollState(ctx.message.author, question, answers)

        self.current_polls[ctx.message.channel] = current_poll

        message = await self.bot.say(current_poll)
        current_poll.original_message = message

    @poll.command(pass_context=True)
    async def stop(self, ctx: Context):
        if ctx.message.channel not in self.current_polls:
            await self.bot.say('No poll currently running in channel')
            return

        current_poll = self.current_polls[ctx.message.channel]
        if (ctx.message.author is current_poll.owner or
                ctx.message.author.permissions_in(ctx.message.channel).manage_messages()):
            self.current_polls.pop(ctx.message.channel)

            await self.bot.say(current_poll)

    @commands.command(pass_context=True)
    async def vote(self, ctx: Context, ans_num: int):
        if ctx.message.channel not in self.current_polls:
            await self.bot.say('No poll currently running in channel')
            return

        current_poll: PollState = self.current_polls[ctx.message.channel]
        author = ctx.message.author

        if author in current_poll.voters:
            return

        if 1 <= ans_num <= len(current_poll.answers):
            current_poll.answers[ans_num - 1]['count'] += 1
            current_poll.voters.add(author)
            await self.bot.edit_message(current_poll.original_message, str(current_poll))
            await self.bot.reply('vote has been counted')


def setup(bot: Bot):
    bot.add_cog(Poll(bot))
