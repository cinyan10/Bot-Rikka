from discord.ext import commands
from functions.query import *


class ServerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        pass

    @commands.hybrid_command()
    async def server(self, ctx, content: str = None):
        # ... implementation ...
        pass

    @commands.hybrid_command()
    async def servers(self, ctx):
        # ... implementation ...
        pass


def setup(bot):
    bot.add_cog(ServerCommands(bot))
