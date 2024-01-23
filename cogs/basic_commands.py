import random
from discord.ext import commands
from config import TEST_CHANNEL_ID


class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name}')
        print("basic_commands cog loaded")

        async def sync():
            """s"""
            await self.bot.tree.sync()
            await self.bot.get_channel(TEST_CHANNEL_ID).send(content="Sync completed!")

        await sync()

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
