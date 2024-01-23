from discord.ext import commands


class Jumpstats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Jumpstats Cog loaded")


def setup(bot):
    bot.add_cog(Jumpstats(bot))
