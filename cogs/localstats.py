from discord.ext import commands
from dc_utils.jumpstats import *
from functions.database import discord_id_to_steamid


class LocalStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("LocalStats Cog loaded")

    @commands.hybrid_command(name="ljpb")
    async def ljpb(self, ctx, kz_mode='kzt', steamid=None, is_block_jump=False):
        discord_id = ctx.author.id
        if steamid is None:
            steamid = discord_id_to_steamid(discord_id)

        rs = embed_ljpb(kz_mode, steamid, is_block_jump)
        await ctx.send(embed=rs)


async def setup(bot):
    await bot.add_cog(LocalStats(bot))
