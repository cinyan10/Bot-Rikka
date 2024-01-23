from discord.ext import commands


class JumpStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="hello")
    async def ljpb(self, ctx, mode='kzt', steamid=None):
        """
        Get your lj pb or other's lj pb
        """
        result = get_ljpb(ctx, mode, steamid)
        await ctx.send(embed=result)

    @commands.Cog.listener()
    async def on_ready(self):
        print("JumpStats Cog loaded")


def setup(bot):
    bot.add_cog(JumpStats(bot))
