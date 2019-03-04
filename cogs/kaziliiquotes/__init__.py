from .kaziliiquotes import KaziliiQuotes


def setup(bot):
	bot.add_cog(KaziliiQuotes(bot))
