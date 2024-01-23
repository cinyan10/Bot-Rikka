from discord.ext import commands


class UtilityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def bind_steam(self, ctx, steamid: str):
        # ... implementation ...
        pass

    @commands.hybrid_command()
    async def reset_steam(self, ctx):
        # ... implementation ...
        pass

    @commands.hybrid_command()
    async def gokzcn(self, ctx, steamid: str = None, mode: str = 'kzt'):
        # ... implementation ...
        pass

    @commands.hybrid_command()
    async def info(self, ctx, steamid: str = None):
        # ... implementation ...
        pass

    @commands.hybrid_command()
    async def find(self, ctx, name: str):
        # ... implementation ...
        pass


def setup(bot):
    bot.add_cog(UtilityCommands(bot))
