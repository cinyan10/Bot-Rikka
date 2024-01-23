from discord.ext import commands


class Jumpstats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Jumpstats Cog loaded")


async def setup(bot):
    await bot.add_cog(Jumpstats(bot))
