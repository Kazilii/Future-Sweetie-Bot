from redbot.core import commands
from redbot.core import checks
from redbot.core import Config
from discord import Forbidden
from discord import Colour



class KaziColors(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.config = Config.get_conf(self, identifier=384)
		default_guild = {
			"roles": {}
		}
		self.config.register_guild(**default_guild)


	def serverhasrole(self, role, server):
		for r in server.roles:
			if r.name.lower() == role.lower():
				return True
		return False

	@commands.guild_only()
	@commands.group(aliases=['ccr'], name='color')
	async def _color(self, ctx):
		"""Custom self assignable roles!"""
		pass

	@_color.command(aliases=['create'])
	@checks.mod_or_permissions(manage_roles=True)
	async def add(self, ctx, html_color: Colour, *, name):
		"""Add/Create a custom role for the server"""
		guild = self.config.guild(ctx.guild)

		if self.serverhasrole(name, ctx.guild):
			for x in ctx.guild.roles:
				if x.name.lower() == name.lower():
					await guild.set_raw('colors', x.name, 'id', value=x.id)
					await guild.set_raw('colors', x.name, 'deletable', value=False)
					await ctx.send('Role added to role list.')
					return
		else:
			role = await ctx.guild.create_role(name=name, reason='KaziColors - Self Assignable Role', color=html_color)
			await guild.set_raw('colors', name, 'id', value=role.id)
			await guild.set_raw('colors', name, 'deletable', value=True)
			await ctx.send('Role created and added to role list.')
			return

	@_color.command(aliases=['del', 'delete'])
	@checks.mod_or_permissions(manage_roles=True)
	async def remove(self, ctx, *, name):
		"""Remove a role from the role list. If role was created by these commands, delete it from the server."""
		guild = self.config.guild(ctx.guild)

		if self.serverhasrole(name, ctx.guild):
			for x in ctx.guild.roles:
				if x.name.lower() == name.lower():
					if await guild.get_raw('colors', x.name, 'deletable'):
						await x.delete()
						await guild.clear_raw('colors', name)
						await ctx.send('Role removed and deleted.')
						return
					else:
						await guild.clear_raw('colors', name)
						await ctx.send('Role removed, but not deleted.')
						return
			await ctx.send('Role does not exist to me.')
			return
		await ctx.send('Role does not exist to the server.')
		return

	@_color.command()
	async def iam(self, ctx, *, role):
		"""Give yourself a role from the server."""
		guild = self.config.guild(ctx.guild)
		donator = False
		if ctx.guild.id == "91349673171775488":
			for r in ctx.author.roles:
				if r.name.lower() == "donators":
					donator = True
				if r.name.lower() == 'staff':
					donator = True
			if not donator:
				await ctx.send("I'm sorry! This feature is only for Donators!")
				return

		if self.serverhasrole(role, ctx.guild):
			for x in await guild.get_raw('colors'):
				if x.lower() == role.lower():
					for r in ctx.author.roles:
						if x.lower() == r.name.lower():
							await ctx.send('You already have that role!')
							return
					try:

						for a in await guild.get_raw('colors'):
							for b in ctx.author.roles:
								if b.name.lower() == a.lower():
									await ctx.author.remove_roles(b)

						await ctx.author.add_roles(ctx.guild.get_role(await guild.get_raw('colors', x, 'id')), reason='KaziColors - Self Assignable Role')
						await ctx.send('Role applied!')
						return
					except Forbidden:
						await ctx.send('I do not have permissions to give that role. Please give me permissions to manage roles.')
						return
			await ctx.send('I can not give that role.')
			return
		else:
			await ctx.send('Role does not exist on this server.')
			return

	@_color.command()
	async def iamnot(self, ctx, *, role):
		"""Remove a role from yourself"""
		guild = self.config.guild(ctx.guild)
		if self.serverhasrole(role, ctx.guild):
			for x in await guild.get_raw('colors'):
				if x.lower() == role.lower():
					for r in ctx.author.roles:
						if x.lower() == r.name.lower():
							try:
								await ctx.author.remove_roles(ctx.guild.get_role(await guild.get_raw('colors', x, 'id')), reason='KaziColors - Self Assignable Role')
								await ctx.send('Role removed!')
								return
							except Forbidden:
								await ctx.send('I do not have permissions to remove that role. Please give me permissions to manage roles.')
					await ctx.send('You do not have that role.')
					return
			await ctx.send('That role does not exist to me.')
			return
		await ctx.send('That role does not exist to the server.')

	@_color.command()
	async def list(self, ctx):
		"""List all self asignable roles"""
		guild = self.config.guild(ctx.guild)

		stri = ""

		for x in sorted(await guild.get_raw('colors')):
			for y in ctx.guild.roles:
				if x.lower() == y.name.lower():
					stri = stri + '{}\n'.format(y.mention)

		await ctx.send(stri)
