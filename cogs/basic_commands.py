import random
from discord.ext import commands


class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def ping(self, ctx):
        responses = ["meow~", "Itami~ >.<", "What's the matter, gosyujinnsama?", "pong~", "UwU", "don't poke me, plz T^T"]
        result = random.choice(responses)
        await ctx.send(result)

    @commands.hybrid_command()
    @commands.has_permissions(administrator=True)
    async def sync(self, ctx):
        await self.bot.tree.sync()
        await ctx.send("Sync completed!")


def setup(bot):
    bot.add_cog(BasicCommands(bot))
