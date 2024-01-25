import random
from datetime import datetime

import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot

from config import TEST_CHANNEL_ID


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name} (ID: {self.bot.user.id})')
        await self.bot.tree.sync()
        await self.bot.get_channel(TEST_CHANNEL_ID).send(embed=Embed(
            description="I'm successfully started!!", colour=discord.Colour.green(), timestamp=datetime.now()))

    @commands.hybrid_command()
    async def ping(self, ctx):
        """Pings the bot"""
        responses = ["meow~", "Itami~ >.<", "What's the matter, gosyujinnsama?", "pong~", "UwU", "don't poke me, plz T^T"]
        result = random.choice(responses)
        await ctx.send(result)

    @commands.hybrid_command()
    @commands.has_permissions(administrator=True)
    async def sync(self, ctx):
        await self.bot.tree.sync()
        await ctx.send("Sync completed!")


async def setup(bot):
    await bot.add_cog(Basic(bot))
