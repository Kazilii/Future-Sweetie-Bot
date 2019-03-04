from redbot.core import commands
from redbot.core import checks
from redbot.core import Config
from discord import Member
from discord import Embed
from discord import File
from random import randint
import re
from typing import Union
from urlextract import URLExtract
from .imagemanip import isurlimage

ID = 0
PATH = "/home/dawn/bots/sweetiebot/media/"

class KaziliiQuotes(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.config = Config.get_conf(self, identifier=7651)
		default_guild = {
			"quotes": []
		}

		self.config.register_guild(**default_guild)

	def isimagequote(self, quote):
		"""Checks to see if the quote contains images and returns a list of those images, otherwise returns false."""
		extractor = URLExtract()
		urls = extractor.find_urls(quote)
		images = []
		if len(urls) > 0:
			for url in urls:
				if isurlimage(url):
					images.append(url)
			return images
		else:
			return False

	@commands.guild_only()
	@commands.group(name='quote', invoke_without_command=True)
	async def _quote(self, ctx, *, id_or_author: Union[Member, int, str] = None):
		"""Get a quote, use `$help quote` for additional commands"""
		guild = self.config.guild(ctx.guild)
		default_avatar = 'https://discordapp.com/assets/dd4dbc0016779df1378e7812eabaa04d.png'
		quotes = list(await guild.quotes())
		color = 0x67c4e2

		if len(quotes) == 0:
			await ctx.send('No quotes found on this server!\nDisplaying help info...')
			await ctx.send_help()
			return

		if id_or_author == 'me' or id_or_author == 'myself':
			id_or_author = ctx.author

		if id_or_author is not None:

			if type(id_or_author) is Member:
				qid = 0
				nquotes = []
				for quote in quotes:
					if quotes[qid]['author_id'] is not None:
						if int(quotes[qid]['author_id']) == int(id_or_author.id):
							nquotes.append((qid, quotes[qid]))
					qid = qid + 1
				if len(nquotes) == 0:
					await ctx.send('No quotes with that author found.')
					return
				nqid = randint(0, len(nquotes) - 1)
				quote = nquotes[nqid][1]['text']
				author_name = nquotes[nqid][1]['author_name']
				author_id = nquotes[nqid][1]['author_id']
				added_by = nquotes[nqid][1]['added_by']
				added_name = nquotes[nqid][1]['added_name']
				qid = nquotes[nqid][0]

			if type(id_or_author) is int:
				try:
					qid = id_or_author - 1
					quote = quotes[qid]['text']
					author_name = quotes[qid]['author_name']
					author_id = quotes[qid]['author_id']
					added_by = quotes[qid]['added_by']
					added_name = quotes[qid]['added_name']
				except IndexError:
					await ctx.send('Quote not found. Highest quote ID is {}'.format(len(quotes)))

			if type(id_or_author) is str:
				qid = 0
				nquotes = []
				for quote in quotes:
					if quotes[qid]['author_name'] == id_or_author:
						nquotes.append((qid, quotes[qid]))
					qid = qid + 1
				if len(nquotes) == 0:
					await ctx.send('No quotes with that author found.')
					return
				nqid = randint(0, len(nquotes) - 1)
				quote = nquotes[nqid][1]['text']
				author_name = nquotes[nqid][1]['author_name']
				author_id = nquotes[nqid][1]['author_id']
				added_by = nquotes[nqid][1]['added_by']
				added_name = nquotes[nqid][1]['added_name']
				qid = nquotes[nqid][0]

		else:
			qid = randint(0, len(quotes) - 1)
			quote = quotes[qid]['text']
			author_name = quotes[qid]['author_name']
			author_id = quotes[qid]['author_id']
			added_by = quotes[qid]['added_by']
			added_name = quotes[qid]['added_name']

		embed = Embed(title=author_name, color=color)
		if author_id is not None:
			author_id = int(author_id)
		if added_by is not None:
			added_by = int(added_by)
		if self.memberinserver(ctx, author_id):
			embed = Embed(title=self.id2display_name(ctx, author_id), color=color)
			embed.set_thumbnail(url=self.id2avatarurl(ctx, author_id))
		else:
			embed = Embed(title=author_name, color=color)
			embed.set_thumbnail(url=default_avatar)

		if self.isimagequote(quote):
			images = self.isimagequote(quote)
			iid = 0
			if len(images) > 1:
				for image in images:
					#if iid == 0:
					#	pass
					#else:
					embed.add_field(name='IMAGE URL', value=image, inline=True)
					iid = iid + 1
			embed.set_image(url=images[0])

		embed.add_field(name="Quote", value=quote, inline=True)
		embed.add_field(name='ID', value=str(qid + 1), inline=False)
		embed.set_author(name='Kazilii Quotes System', icon_url='https://cdn.discordapp.com/avatars/493917745415716896/b717e5442f824019f38014e8ec4dd70d.png')
		if self.memberinserver(ctx, added_by):
			embed.set_footer(text="Added by: " + self.id2display_name(ctx, added_by), icon_url=self.id2avatarurl(ctx, added_by))
		else:
			embed.set_footer(text="Added by: " + added_name, icon_url=default_avatar)
		await ctx.send(embed=embed)
		return

	#@_quote.command(hidden=True)
	#async def fix(self, ctx):
	#	guild = self.config.guild(ctx.guild)
	#	qid = 0
	#	quotes = list(await guild.quotes())
	#	for quote in quotes:
	#		try:
	#			quote['added_name']
	#		except:
	#			quote['added_name'] = 'Unknown'
	#	await guild.quotes.set(quotes)
	#	await ctx.send('Done')


	@_quote.command()
	@checks.mod()
	async def edit(self, ctx, quote_id: int, quote, *, author: Union[Member, str] = None):
		"""edit a quote"""
		qid = quote_id - 1
		guild = self.config.guild(ctx.guild)
		quotes = list(await guild.quotes())
		if author is not None:
			if type(author) == str:
				author_name = author.strip('\t\n\r\x0b\x0c-–—')
				author_id = None
			elif type(author) == Member:
				author_name = author.display_name
				author_id = author.id
			else:
				await ctx.send('Invalid author')
				return
		else:
			author_id = None

		try:
			keknut = quotes[qid]

			if '"' not in ctx.message.content:
				await ctx.send("I'm sorry! I can't add that quote as it's invalid! You probably forgot your quotation marks!\n"
							   "Here's an example quote:\n"
							   "^quote add \"Cake is == Pie!\" {}".format(ctx.bot.mention))
				return


			if author is not None:
				quotes[qid]['author_name'] = author_name
				quotes[qid]['author_id'] = author_id
			quotes[qid]['text'] = quote

			await guild.quotes.set(quotes)
			await ctx.send('Quote Edited! ID: {}'.format(qid + 1))

		except:
			await ctx.send('That quote doesn\'t exist.')
			return


	@_quote.command()
	async def add(self, ctx, quote: str, *, author: Union[Member, str] = None):
		"""Add a quote!"""
		guild = self.config.guild(ctx.guild)
		if author is not None:
			if type(author) == str:
				author_name = author.strip('\t\n\r\x0b\x0c-–—')
				author_id = None
			elif type(author) == Member:
				author_name = author.display_name
				author_id = author.id
			else:
				await ctx.send('Invalid author')
				return
		else:
			author_id = None
			author_name = "Unknown"

		if '"' not in ctx.message.content:
			await ctx.send("I'm sorry! I can't add that quote as it's invalid! You probably forgot your quotation marks!\n"
						   "Here's an example quote:\n"
						   "^quote add \"Cake is == Pie!\" {}".format(ctx.bot.mention))
			return

		quotes = list(await guild.quotes())
		quotes.append({
			'author_id': author_id,
			'author_name': author_name,
			'text': quote,
			'added_by': ctx.author.id,
			'added_name': ctx.author.display_name
		})
		await guild.quotes.set(quotes)
		await ctx.send('Quote added! ID: {}'.format(len(list(await guild.quotes()))))

	@_quote.command()
	@checks.mod_or_permissions(manage_messages=True)
	async def remove(self, ctx, quote_id: int):
		"""Remove a quote by ID"""
		guild = self.config.guild(ctx.guild)
		quotes = list(await guild.quotes())
		qid = quote_id - 1
		quotes.pop(qid)
		await guild.quotes.set(quotes)
		await ctx.send('Quote removed!')

	@_quote.command()
	async def lastquoteid(self, ctx):
		"""Shows the ID for the last quote added"""
		guild = self.config.guild(ctx.guild)
		quotes = list(guild.quotes())
		await ctx.send('ID: {}'.format(len(quotes)))

	@commands.command(hidden=True)
	async def coo(self, ctx, test: Union[Member, str]):
		await ctx.send(type(test))

	@_quote.command()
	async def list(self, ctx):
		"""Get a list of all quotes for this server in a text file."""
		guild = self.config.guild(ctx.guild)
		quotes = list(await guild.quotes())
		stri = "```\n"
		qid = 1
		for x in quotes:
			if x['author_id'] is not None:
				if self.memberinserver(ctx, int(x['author_id'])):
					authorname = self.id2display_name(ctx, int(x['author_id']))
				else:
					authorname = x['author_name']
			else:
				authorname = x['author_name']
			stri = stri + "~~~~~~~~~~~~\n{QID})   {QUOTE}   | {AUTHORNAME}\n~~~~~~~~~~~~\n\n".format(QID=qid, QUOTE=x['text'], AUTHORNAME=authorname)
			qid = qid + 1
		stri = stri + '```'
		with open(PATH + 'quotes.txt', 'w') as outfile:
			outfile.write(stri)
		await ctx.send(file=File(fp=PATH + 'quotes.txt', filename='quotes.txt'))

	@commands.command()
	@checks.is_owner()
	async def clearquotes(self, ctx):
		await self.config.guild(ctx.guild).clear()
		await ctx.send('Quotes Cleared')

	def memberinserver(self, ctx, id):
		try:
			ctx.guild.get_member(int(id)).display_name
			return True
		except:
			return False

	def id2display_name(self, ctx, id):
		return ctx.guild.get_member(int(id)).display_name

	def id2avatarurl(self, ctx, id):
		return ctx.guild.get_member(int(id)).avatar_url

	def mention2member(self, ctx, user):
		return ctx.guild.get_member(int(re.sub('[<@!>]', '', user)))

	def ismember(self, ctx, user):
		try:
			ctx.guild.get_member(int(re.sub('[<@!>]', '', user)))
			return True
		except:
			return False