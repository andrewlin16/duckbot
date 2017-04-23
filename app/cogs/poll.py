import logging

from discord import User
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

logger = logging.getLogger(__name__)


class PollState:
    """State of a single poll.

     Attributes
    -----------
    owner : User
        Owner of this poll.
    question : str
        The poll question.
    answers : List[str]
        List of answers.
    voters : Set[User]
        Voters who have already voted in this poll.
    original_message: Message
        The message sent by the bot when the poll was started showing the state
        of the poll. It will be updated continuously as the poll as answered.
    """

    def __init__(self, owner: User, question: str, answers):
        self.owner = owner
        self.question = question
        self.answers = [{'name': answer, 'count': 0} for answer in answers]
        self.voters = set()
        self.original_message = None

    def __str__(self):
        answer_list = [
            '{}. {} - {} vote(s)'.format(i + 1, ans['name'], ans['count'])
            for i, ans in enumerate(self.answers)
        ]

        return '**POLL**: {}\n\n{}'.format(
            self.question, '\n'.join(answer_list))

    def end_result_str(self):
        max_votes = max(self.answers, key=lambda ans: ans['count'])['count']
        answer_list = [
            '{0}{1}. {2} - {3} vote(s){0}'.format(
                '**' if ans['count'] == max_votes else '',
                i + 1, ans['name'], ans['count'])
            for i, ans in enumerate(self.answers)
        ]

        return '**POLL RESULTS**: {}\n\n{}'.format(
            self.question, '\n'.join(answer_list))


class Poll:
    """Commands to create and manage polls."""

    def __init__(self, bot):
        self.bot = bot
        self.current_polls = {}

    @commands.group(pass_context=True)
    async def poll(self, ctx: Context):
        """Poll
        """
        if ctx.invoked_subcommand is None:
            await self.bot.say('Unknown poll command.')

    @poll.command(pass_context=True)
    async def start(self, ctx: Context, question=None, *answers):
        """Start a poll

        Syntax:
            /poll "This is the question" "Answer 1" "Answer 2"
        """
        if question is None:
            await self.bot.reply('your poll needs a question.')
            return

        if len(answers) < 1:
            await self.bot.reply('your poll needs answers.')
            return

        channel = ctx.message.channel
        if channel in self.current_polls:
            await self.bot.reply('there is already a poll running in here.')
            return

        current_poll = PollState(ctx.message.author, question, answers)

        self.current_polls[channel] = current_poll

        message = await self.bot.say(current_poll)
        current_poll.original_message = message
        await self.bot.pin_message(message)

    @poll.command(pass_context=True, aliases=['end'])
    async def stop(self, ctx: Context):
        """Stop the current poll.

        Must be poll owner or have the Manage Messages permission for channel.
        """
        channel = ctx.message.channel
        if channel not in self.current_polls:
            await self.bot.reply('there is no poll currently running in here.')
            return

        current_poll = self.current_polls[channel]
        author = ctx.message.author
        if (author is current_poll.owner or
                author.permissions_in(channel).manage_messages()):
            self.current_polls.pop(channel)

            await self.bot.unpin_message(current_poll.original_message)
            await self.bot.say(current_poll.end_result_str())

    @commands.command(pass_context=True)
    async def vote(self, ctx: Context, ans_num=None):
        """Vote for an answer. Must be an answer number."""
        channel = ctx.message.channel
        if channel not in self.current_polls:
            await self.bot.reply('there is no poll currently running in here.')
            return

        current_poll: PollState = self.current_polls[channel]

        if ans_num is None:
            await self.bot.reply('your vote must be between {}-{}.'.format(
                1, len(current_poll.answers)))
            return

        try:
            ans_num = int(ans_num)
        except ValueError:
            await self.bot.reply('your vote must be between {}-{}.'.format(
                1, len(current_poll.answers)))
            return

        author = ctx.message.author
        if author in current_poll.voters:
            await self.bot.reply('you have already voted in this poll.')
            return

        if 1 <= ans_num <= len(current_poll.answers):
            current_poll.answers[ans_num - 1]['count'] += 1
            current_poll.voters.add(author)
            await self.bot.edit_message(current_poll.original_message,
                                        str(current_poll))
            await self.bot.reply('your vote has been counted.')
        else:
            await self.bot.reply('your vote must be between {}-{}.'.format(
                1, len(current_poll.answers)))


def setup(bot: Bot):
    bot.add_cog(Poll(bot))
