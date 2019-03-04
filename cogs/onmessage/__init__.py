from .onmessage import OnMessage


def setup(bot):
	bot.add_cog(OnMessage(bot))
