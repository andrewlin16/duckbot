import logging
import datetime

from discord import User
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

logger = logging.getLogger(__name__)

# Time where poll can only be closed by owner or channel managers
DEFAULT_LOCK_TIME = datetime.timedelta(hours=6)


class PollState:
    """State of a single poll.

     Attributes
    -----------
    owner : User
        Owner of this poll.
    question : str
        The poll question.
    choices : List[str]
        List of choices.
    voters : Set[User]
        Voters who have already voted in this poll.
    original_message: Message
        The message sent by the bot when the poll was started showing the state
        of the poll. It will be updated continuously as votes are submitted.
    """

    def __init__(self, owner: User, question: str, choices):
        self.owner = owner
        self.question = question
        self.choices = [{'name': choice, 'count': 0} for choice in choices]
        self.voters = set()
        self.original_message = None
        self.start_time = datetime.datetime.now()

    def __str__(self):
        choice_list = [
            '{}. {} - {} vote(s)'.format(i + 1, ans['name'], ans['count'])
            for i, ans in enumerate(self.choices)
        ]

        return '{}\n\n{}'.format(self.question, '\n'.join(choice_list))

    def end_result_str(self):
        max_votes = max(self.choices, key=lambda ans: ans['count'])['count']
        choice_list = [
            '{0}{1}. {2} - {3} vote(s){0}'.format(
                '**' if ans['count'] == max_votes else '',
                i + 1, ans['name'], ans['count'])
            for i, ans in enumerate(self.choices)
        ]

        return '**POLL RESULTS**: {}\n\n{}'.format(
            self.question, '\n'.join(choice_list))

    def get_validated_choice(self, ans_num):
        try:
            ans_num = int(ans_num)
            return ans_num if 1 <= ans_num <= len(self.choices) else None
        except (TypeError, ValueError):
            return None

    def has_already_voted(self, user):
        return user in self.voters

    def has_lock_expired(self):
        return datetime.datetime.now() - self.start_time > DEFAULT_LOCK_TIME


class Poll:
    """Commands to create and manage polls."""

    def __init__(self, bot):
        self.bot = bot
        self.current_polls = {}

    @commands.group(pass_context=True)
    async def poll(self, ctx: Context):
        """Group of commands for poll management"""
        if ctx.invoked_subcommand is not None:
            return

        channel = ctx.message.channel
        if channel in self.current_polls:
            await self.bot.say('Current poll: {}'.format(
                self.current_polls[channel]))
        else:
            await self.bot.say('There is no poll currently running.')

    @poll.command(pass_context=True)
    async def start(self, ctx: Context, question=None, *choices):
        """Start a poll.

        Syntax:
            /poll start "This is the question" "Choice 1" "Choice 2"
        """
        if question is None:
            await self.bot.reply('your poll needs a question.')
            return

        if len(choices) < 1:
            await self.bot.reply('your poll needs choices.')
            return

        channel = ctx.message.channel
        if channel in self.current_polls:
            await self.bot.reply('there is already a poll running in here.')
            return

        current_poll = PollState(ctx.message.author, question, choices)

        self.current_polls[channel] = current_poll

        message = await self.bot.say('**POLL**: {}'.format(current_poll))
        current_poll.original_message = message
        await self.bot.pin_message(message)

    @poll.command(pass_context=True, aliases=['end'])
    async def stop(self, ctx: Context):
        """Stop the current poll.

        When the poll is locked, only the poll owner or users who have the 
        Manage Messages permission for the channel can stop the poll.
        """
        channel = ctx.message.channel
        if channel not in self.current_polls:
            await self.bot.reply('there is no poll currently running in here.')
            return

        current_poll = self.current_polls[channel]
        author = ctx.message.author
        if not (author == current_poll.owner or
                author.permissions_in(channel).manage_messages or
                current_poll.has_lock_expired()):
            await self.bot.reply("you can't end this poll yet.")
            return

        self.current_polls.pop(channel)
        await self.bot.unpin_message(current_poll.original_message)
        await self.bot.say(current_poll.end_result_str())

    @commands.command(pass_context=True)
    async def vote(self, ctx: Context, ans_num=None):
        """Vote for a choice. Must be a choice number."""
        channel = ctx.message.channel
        if channel not in self.current_polls:
            await self.bot.reply('there is no poll currently running in here.')
            return

        current_poll = self.current_polls[channel]

        ans_num = current_poll.get_validated_choice(ans_num)
        if ans_num is None:
            await self.bot.reply('your vote must be between {}-{}.'.format(
                1, len(current_poll.choices)))
            return

        author = ctx.message.author
        if current_poll.has_already_voted(author):
            await self.bot.reply('you have already voted in this poll.')
            return

        current_poll.choices[ans_num - 1]['count'] += 1
        current_poll.voters.add(author)
        await self.bot.edit_message(current_poll.original_message,
                                    str(current_poll))
        await self.bot.reply('your vote has been counted.')


def setup(bot: Bot):
    bot.add_cog(Poll(bot))
