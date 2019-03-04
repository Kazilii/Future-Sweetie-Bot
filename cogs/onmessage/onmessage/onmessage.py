import time
from redbot.core import commands
from redbot.core import checks
from redbot.core import Config
from discord import Game
from discord import TextChannel as Channel
from random import randint as RNG


class OnMessage(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.mayo = False
		self.start_time = None
		self.joined = True
		self.joined_time = None
		self.nodupe = False
		self.config = Config.get_conf(self, identifier=91349673171775488)

		default_global = {
			'reactions': {
				'why not?': ':wynaut:364952371593478144'
			},
			'eh': ['eh!', 'eh?', 'eh!~~', 'eh?~~', 'eh!*', 'eh?*', 'eh!_', 'eh?_'],
			'canada': ['canadia', 'tim hortons', 'bags of milk', 'bag of milk', 'Techdisk', 'Cynder']
		}

		default_guild = {
			'reactionconf': {
				'enabled': False,
				'guildonly': False
			},
			'reactions': {

			},
			'disabled_channels': {

			}
		}

		self.config.register_global(**default_global)
		self.config.register_guild(**default_guild)

	@commands.guild_only()
	@commands.group()
	async def react(self, ctx):
		pass

	@react.command()
	@checks.mod()
	async def toggle(self, ctx):
		"""Toggle the auto react system on the server."""
		if await self.config.guild(ctx.guild).get_raw('reactionconf', 'enabled'):
			value = False
		else:
			value = True

		await self.config.guild(ctx.guild).set_raw('reactionconf', 'enabled', value=value)
		await ctx.send('Auto Reacts toggled. Current status: {}'.format(value))

	@react.command()
	@checks.mod()
	async def blockchannel(self, ctx, channel: Channel):
		"""Disable autoreacts in the specified channel."""
		guild = self.config.guild(ctx.guild)
		channels = list(await guild.get_raw('disabled_channels'))
		if channel.id in channels:
			await ctx.send('Channel already blocked. Use `^react unblockchannel` to remove it from the block list.')
			return
		channels.append(channel.id)
		await guild.set_raw('disabled_channels', value=channels)
		await ctx.send('Done.')

	@react.command()
	@checks.mod()
	async def unblockchannel(self, ctx, channel: Channel):
		"""Remove channel from the block list."""
		guild = self.config.guild(ctx.guild)
		channels = list(await guild.get_raw('disabled_channels'))
		if channel.id not in channels:
			await ctx.send('Channel not blocked.')
			return
		counter = 0
		for chan in channels:
			if channel.id == chan:
				channels.pop(counter)
				return
			counter = counter + 1
		await ctx.send('Channel not blocked.')

	@react.command()
	@checks.mod()
	async def toggleglobal(self, ctx):
		"""Toggle whether or not default auto reacts are enabled."""
		if await self.config.guild(ctx.guild).get_raw('reactionconf', 'guildonly'):
			value = False
		else:
			value = True

		await self.config.guild(ctx.guild).set_raw('reactionconf', 'guildonly', value=value)
		await ctx.send('Default reactions status: {}'.format(value))

	def check(self, user, author):
		return user == author

	@react.command()
	@checks.is_owner()
	async def addglobal(self, ctx, *, phrase):
		"""Adds a global auto reaction for the given phrase."""
		msg = await ctx.send('Please react to this message with the emoji you want to autoreact with.')

		reaction, user = await self.bot.wait_for('reaction_add', timeout=60)

		if self.check(user, ctx.author):
			try:
				await ctx.message.add_reaction(reaction.emoji)
			except:
				await ctx.send(
					"I don't have access to that emoji, please add it to this server, or another server that I'm in.")
				return
			await self.config.set_raw('reactions', phrase, value=str(reaction.emoji).strip('<').strip('>'))
			await ctx.send('Reaction for\n~~~~~~\n{phrase}\n~~~~~~\nset to\n~~~~~~\n{emoji}'.format(phrase=phrase,
																									emoji=reaction.emoji))
		else:
			await ctx.send("Couldn't find a reaction, please try again.")

	@react.command()
	@checks.mod()
	async def add(self, ctx, *, phrase):
		"""Adds an auto reaction to the server for the given phrase."""
		msg = await ctx.send('Please react to this message with the emoji you want to autoreact with.')

		reaction, user = await self.bot.wait_for('reaction_add', timeout=60)

		if self.check(user, ctx.author):
			try:
				await ctx.message.add_reaction(reaction.emoji)
			except:
				await ctx.send(
					"I don't have access to that emoji, please add it to this server, or another server that I'm in.")
				return
			await self.config.guild(ctx.guild).set_raw('reactions', phrase,
													   value=str(reaction.emoji).strip('<').strip('>'))
			await ctx.send('Reaction for\n~~~~~~\n{phrase}\n~~~~~~\nset to\n~~~~~~\n{emoji}'.format(phrase=phrase,
																									emoji=reaction.emoji))
		else:
			await ctx.send("Couldn't find a reaction, please try again.")

	@react.command()
	@checks.mod()
	async def remove(self, ctx, *, phrase):
		"""Remove an auto reaction."""
		reactions = self.config.guild(ctx.guild).get_raw('reactions')

		for x in await reactions:
			if phrase == x:
				await self.config.guild(ctx.guild).clear_raw('reactions', x)
				await ctx.send('Reaction phrase removed.')
				return
		await ctx.send('Reaction phrase not found. Use `^react list` to see all reaction phrases.')

	@react.command()
	@checks.mod()
	async def list(self, ctx):
		"""List all guild specific auto reactions."""
		reactions = self.config.guild(ctx.guild)
		stri = "```\n"
		num = 1
		for x in await reactions.get_raw('reactions'):
			stri = stri + "{num}) {phrase} | {emoji}\n".format(num=num, phrase=x,
															   emoji=await reactions.get_raw('reactions', x))
			num = num + 1
		stri = stri + "```"
		await ctx.send(stri)

	@react.command()
	@checks.is_owner()
	async def listglobal(self, ctx):
		"""List all autoreacts in the global pool."""
		reactions = self.config
		stri = "```\n"
		num = 1
		for x in await reactions.get_raw('reactions'):
			stri = stri + "{num}) {phrase} | {emoji}\n".format(num=num, phrase=x,
															   emoji=await reactions.get_raw('reactions', x))
			num = num + 1
		stri = stri + "```"
		try:
			await ctx.send(stri)
		except:
			with open('globalreacts.txt', 'w') as file:
				file.write(stri)
				ctx.send(file=file)

	def statuscheck(self, message):
		if message.guild.get_member(self.bot.user.id).activity is not None:
			return True
		else:
			return False

	async def on_message(self, message):
		if message.guild is None:
			return
		if message.author == self.bot.user:
			return

		if not self.statuscheck(message):
			game = Game(name='^help')
			await self.bot.change_presence(activity=game)

		channel = message.channel
		author = message.author
		mayoyes = 'is mayonnaise an instrument'
		mayoyesalt = 'is mayo an instrument'
		content = message.content.lower()

		guild = self.config.guild(message.guild)
		glob = self.config

		if content.startswith(mayoyes.lower()) or content.startswith(mayoyesalt.lower()):
			self.mayo = True
			self.start_time = time.time()
			await message.channel.send('No {}. Mayonnaise is not an instrument.'.format(author.mention))

		if (content.startswith('raises'.lower()) or content.startswith('_raises'.lower()) or content.startswith(
				'*raises'.lower())) and (self.mayo == True):
			if time.time() - self.start_time < 30:
				self.mayo = False
				self.start_time = None
				await message.channel.send('Horseradish is not an instrument either.')
			else:
				self.start_time = None
				self.mayo = False

		if not await guild.get_raw('reactionconf', 'enabled'):
			return

		if await guild.get_raw('reactionconf', 'guildonly'):
			for x in await glob.reactions():
				if x in message.content:
					await message.add_reaction(await glob.get_raw('reactions', x))

			for x in await glob.eh():
				if message.content.casefold().endswith(x.casefold()):
					chance = RNG(0, 100)
					if chance < 10:
						await message.add_reaction(':timhortons:365313496872779776')
					else:
						await message.add_reaction('\U0001F341')

			for x in await glob.canada():
				if x.casefold() in message.content.casefold():
					chance = RNG(0, 100)
					if chance < 10:
						await message.add_reaction(':timhortons:365313496872779776')
					else:
						await message.add_reaction('\U0001F341')

		for x in await guild.get_raw('reactions'):
			if x.lower() in message.content.lower():
				await message.add_reaction(await guild.get_raw('reactions', x))
