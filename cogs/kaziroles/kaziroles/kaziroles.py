from redbot.core import commands
from redbot.core import checks
from redbot.core import Config
from discord import Forbidden



class KaziRoles(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.config = Config.get_conf(self, identifier=1580414)
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
	@commands.group(aliases=['cr'], name='role')
	async def _role(self, ctx):
		"""Custom self assignable roles!"""
		pass

	@_role.command(aliases=['create'])
	@checks.mod_or_permissions(manage_roles=True)
	async def add(self, ctx, group, *, name):
		"""Add/Create a custom role for the server"""
		guild = self.config.guild(ctx.guild)

		if self.serverhasrole(name, ctx.guild):
			for x in ctx.guild.roles:
				if x.name.lower() == name.lower():
					await guild.set_raw('roles', x.name, 'id', value=x.id)
					await guild.set_raw('roles', x.name, 'group', value=group)
					await guild.set_raw('roles', x.name, 'deletable', value=False)
					await ctx.send('Role added to role list.')
					return
		else:
			role = await ctx.guild.create_role(name=name, reason='KaziRoles - Self Assignable Role')
			await guild.set_raw('roles', name, 'id', value=role.id)
			await guild.set_raw('roles', name, 'deletable', value=True)
			await guild.set_raw('roles', name, 'group', value=group)
			await ctx.send('Role created and added to role list.')
			return

	@_role.command(aliases=['del', 'delete'])
	@checks.mod_or_permissions(manage_roles=True)
	async def remove(self, ctx, *, name):
		"""Remove a role from the role list. If role was created by these commands, delete it from the server."""
		guild = self.config.guild(ctx.guild)

		if self.serverhasrole(name, ctx.guild):
			for x in ctx.guild.roles:
				if x.name.lower() == name.lower():
					if await guild.get_raw('roles', x.name, 'deletable'):
						await x.delete()
						await guild.clear_raw('roles', name)
						await ctx.send('Role removed and deleted.')
						return
					else:
						await guild.clear_raw('roles', name)
						await ctx.send('Role removed, but not deleted.')
						return
			await ctx.send('Role does not exist to me.')
			return
		await ctx.send('Role does not exist to the server.')
		return

	@_role.command()
	async def iam(self, ctx, *, role):
		"""Give yourself a role from the server."""
		guild = self.config.guild(ctx.guild)
		if self.serverhasrole(role, ctx.guild):
			for x in await guild.get_raw('roles'):
				if x.lower() == role.lower():
					for r in ctx.author.roles:
						if x.lower() == r.name.lower():
							await ctx.send('You already have that role!')
							return
					try:
						await ctx.author.add_roles(ctx.guild.get_role(await guild.get_raw('roles', x, 'id')), reason='KaziRoles - Self Assignable Role')
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

	@_role.command()
	async def iamnot(self, ctx, *, role):
		"""Remove a role from yourself"""
		guild = self.config.guild(ctx.guild)
		if self.serverhasrole(role, ctx.guild):
			for x in await guild.get_raw('roles'):
				if x.lower() == role.lower():
					for r in ctx.author.roles:
						if x.lower() == r.name.lower():
							try:
								await ctx.author.remove_roles(ctx.guild.get_role(await guild.get_raw('roles', x, 'id')), reason='KaziRoles - Self Assignable Role')
								await ctx.send('Role removed!')
								return
							except Forbidden:
								await ctx.send('I do not have permissions to remove that role. Please give me permissions to manage roles.')
					await ctx.send('You do not have that role.')
					return
			await ctx.send('That role does not exist to me.')
			return
		await ctx.send('That role does not exist to the server.')

	@_role.command()
	async def list(self, ctx):
		"""List all self asignable roles"""
		guild = self.config.guild(ctx.guild)
		stri = "```\n"
		tuplels = []
		for x in await guild.get_raw('roles'):
			tuplels.append((await guild.get_raw('roles', x, 'group'), x))

		# g('Species', 'Unicorn')
		# gr('Test', 'Tester')
		# ('Test', 'Other Test')
		# ('Species', 'Pegasus')
		# ('Other', 'Other')

		# "```\n"
		# "[Species]"
		# "Unicorn"
		# "

		added = []

		def check(name):
			for l in added:
				if l == name:
					return True
			return False

		for g in tuplels:
			for gr in tuplels:
				if gr[0] == g[0]:
					if '[{}]'.format(g[0]) in stri:
						if check(gr[1]):
							pass
						else:
							stri = stri + "{}\n".format(gr[1])
							added.append(gr[1])
					else:
						stri = stri + "\n[{}]\n".format(g[0])
						if check(gr[1]):
							pass
						else:
							stri = stri + "{}\n".format(gr[1])
							added.append(gr[1])
		stri = stri + '```'
		await ctx.send(stri)
