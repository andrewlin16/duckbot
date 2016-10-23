import discord
import duckbot_settings
import random
from discord.ext import commands

_DESCRIPTION = '''quack'''

bot = commands.Bot(command_prefix='/', description=_DESCRIPTION)

@bot.event
async def on_ready():
	print('logged in: %s (%s)' % (bot.user.name, bot.user.id))
	
	oauth_url = discord.utils.oauth_url(duckbot_settings.CLIENT_ID, permissions=discord.Permissions.text())
	print('invite me: %s' % oauth_url)

	print('Channels:')

	channels = bot.get_all_channels()
	for channel in channels:
		print('%s (%s)' % (channel.name, channel.id))
		if channel.name == 'botspam':
			await bot.send_message(channel, 'quack!! (ready to roll)')

@bot.command()
async def roll():
	await bot.say('pretending to roll')

bot.run(duckbot_settings.TOKEN)
