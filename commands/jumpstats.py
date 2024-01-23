from discord.ext import commands


class Jumpstats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="hello")
    async def ljpb(self, ctx, mode='kzt', steamid=None):
        """
        Get your lj pb or other's lj pb
        """
        await ctx.send('')

    @commands.Cog.listener()
    async def on_ready(self):
        print(" Cog loaded")


def setup(bot):
    bot.add_cog((bot))
