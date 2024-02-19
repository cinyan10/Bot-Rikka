import discord
from discord import Embed, Message
from discord.ext import commands
from configs.discord import GOKZCN_CHANNEL_ID
from dc_utils.gokzcn import gokzcn_rank
from dc_utils.leaderboard import update_playtime_rank_7am
from dc_utils.localstats import get_playtime_rank


class Leaderboards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gokzcn_channel = bot.get_channel(GOKZCN_CHANNEL_ID)
        self.playtime_channel = bot.get_channel()

    @commands.Cog.listener()
    async def on_ready(self):
        await update_playtime_rank_7am(self.playtime_channel)

    @commands.hybrid_command()
    @commands.has_permissions(administrator=True)
    async def update_gokzcn_rank(self, ctx):
        """update the gokzcn_rank in channel"""
        channel = self.bot.get_channel(GOKZCN_CHANNEL_ID)

        send_ms: Message = await ctx.send(embed=Embed(title="Loading...", description=f"this will take a while...", color=0x60FFFF))
        try:
            if channel is None:
                await ctx.send(f"Channel with ID {GOKZCN_CHANNEL_ID} not found.")
                return

            embeds = gokzcn_rank()
            if embeds:
                await channel.purge(limit=None)

            for embed in embeds:
                await channel.send(embed=embed)

            await send_ms.edit(embed=Embed(title="Done", description=f"Ranking send in {channel.name}", color=0x60FFFF))

        except Exception as e:
            await send_ms.edit(embed=Embed(title="Error", description=f"{e}", color=0x60FFFF))

    @commands.hybrid_command()
    @commands.has_permissions(administrator=True)
    async def update_playtime_rank(self, ctx):
        ms = await ctx.send(embed=Embed(title="Loading ranking", description=f"this will take a while...",
                                        color=discord.Color.blue()))

        await get_playtime_rank(self.playtime_channel)
        await ms.edit(embed=Embed(title="Done",
                                  description=f"updated in {self.playtime_channel.name}",
                                  color=discord.Color.green()))


async def setup(bot: commands):
    await bot.add_cog(Leaderboards(bot))
