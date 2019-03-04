from redbot.core import commands
from redbot.core import checks
from redbot.core import Config
from discord import Member
from discord import TextChannel
from discord import File
from random import choice as RNG

PATH = "/home/dawn/bots/sweetiebot/media/"

class Kazicustom(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.config = Config.get_conf(self, identifier=724)
		default_global = {
			'barrel': {
				'objects': ['another barrel!* Uh... right, well...',
							'a katana!* Oh my, that looks sharp!',
							'a kazoo!* Oh! Oh! I love this instrument!',
							'a warm plate of spaghetti!* Oooh, yum!',
							'a miniature robotic dog!* Awww... how adorable!',
							'a miniaturized Avali mech!* Hmm, this can\'t possibly be dangerous!',
							"{author}!*",
							"{user}!*",
							"a plush version of {author}!* Neato!",
							"a plush version of {user}!* Neato!",
							"a medpack! Practical!*",
							"the Source Code:tm:!*",
							"a Katamary Demacy!*",
							"a Roomba!*",
							"Applejack's Hat!* Stylish!",
							"Twilight's favorite book!* Make sure you return it by the schedule time!",
							"a mango!* Yum!",
							"the King of all Cosmos!* Uh oh.",
							"a muffin!* Yum!",
							"Celestia's favorite banana!* Mmmmyou like bananas?",
							"Pinkie Pie's Party Cannon!* Let's get this party started!",
							"the Master Sword!* Now it's time to rush Agahnim!",
							"five arrows!?* Aw come on!",
							"a one up mushroom!*",
							"vines!*",
							"a wall of text!* TL;DR Something brain related.",
							"an Estus Flask!* Make sure you visit a bonfire to fill it!",
							"a Final Smash Orb!* What power does it hold?",
							"the MLP Show Bible!* Oooh! This should be a good read!"],
				'response': ['*rumages through Kazilii\'s barrel and pulls out {object} Here you go {user}!',
							 "*digs around in Kazilii's barrel and finds {object} Here you go {user}! Have fun!",
							 "*searches through Kazilii's barrel and finds {object} Here you go {user}!",
							 "*pokes around in Kazilii's barrel and pulls out {object} Here you go {user}! Enjoy!"]
			}
		}
		self.config.register_global(**default_global)

	@commands.command()
	async def barrel(self, ctx, user: Member = None):
		"""Have Sweetie Bot dig around in Kazilii's mysterious Barrel! Who knows what you might get? Specify a user to give them an item instead."""

		obj = RNG(await self.config.barrel.get_raw('objects'))
		resp = RNG(await self.config.barrel.get_raw('response'))
		author = ctx.author
		if user is not None:
			await ctx.send(resp.format(object=obj, user=user.display_name, author=author.display_name))
		else:
			await ctx.send(resp.format(object=obj, user=author.display_name, author=author.display_name))

	@commands.command()
	async def boop(self, ctx, user: Member = None):
		"""Boop someone!"""
		author = ctx.author
		if user == self.bot.user:
			await ctx.send('*boops Sweetie Bo-*\n...\nHey, wait a second!')
		elif user is not None:
			await ctx.send("*boops {}*".format(user.display_name))
		else:
			await ctx.send('*boops {}*'.format(author.display_name))

	@commands.group(hidden=True)
	async def use(self, ctx):
		pass
		#TODO Add the use command, similar to the barrel command

	@commands.command()
	@checks.mod()
	async def say(self, ctx, channel: TextChannel, *, text):
		"""Say something in the specified channel, great for pranks!"""
		await channel.send(text)

	@commands.command()
	async def platinum(self, ctx):
		fp = RNG([PATH + 'platinum1.jpg', PATH + 'platinum2.png'])
		await ctx.send(file=File(fp=fp))

	@commands.command()
	async def sleep(self, ctx, user: Member=None):
		"You should reall be sleeping right now!"

		author = ctx.author.display_name

		if user is not None:
			user = user.display_name
		else:
			user = author
		await ctx.send(RNG(['***NO {user}! WHAT ARE YOU DOING!? GO TO SLEEP! GOSH!***'.format(user=user.upper()),
							'***NO {user}, GO TO SLEEP, JEEZ, WHY ARE YOU STILL UP!?***'.format(user=user.upper())]))

	@commands.command(hidden=True)
	async def kazilii(self, ctx):
		await ctx.send(ctx.guild.get_member(99716967107149824).avatar_url)

	@commands.command(hidden=True)
	async def cutepone(self, ctx):
		try:
			starlight = ctx.guild.get_member(167798987078762497)
			await ctx.send(starlight.avatar_url)
		except:
			await ctx.send('Cute pone isn\'t here!')