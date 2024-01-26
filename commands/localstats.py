import discord
from discord.ext import commands
from dc_utils.jumpstats import *
from functions.database import discord_id_to_steamid
from functions.db_operate.discord import get_kz_mode


class LocalStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ljpb")
    async def ljpb(self, ctx, kz_mode=None, steamid=None, is_block_jump=False):
        """get your or other's long jump personal best!!"""
        discord_id = ctx.author.id
        if steamid is None:
            steamid = discord_id_to_steamid(discord_id)
        if kz_mode is None:
            kz_mode = get_kz_mode(discord_id)

        rs = embed_ljpb(kz_mode, steamid, is_block_jump)
        await ctx.send(embed=rs)

    @commands.hybrid_command(name="jspb")
    async def jspb(self, ctx, kz_mode=None, steamid=None):
        """get your or other's jumpstats"""
        discord_id = ctx.author.id
        if steamid is None:
            steamid = discord_id_to_steamid(discord_id)
        if kz_mode is None:
            kz_mode = get_kz_mode(discord_id)

        rs = embed_jspb(kz_mode, steamid)
        await ctx.send(embed=rs)

    def get_discord_id(mention):
        try:
            # Extract the user ID from the mention
            user_id = int(mention[3:-1])  # Extract the user ID from the mention string
            return user_id
        except (ValueError, IndexError):
            # Handle exceptions if the mention format is invalid
            return None

    # Example usage
    mention = "@he/him"
    discord_id = get_discord_id(mention)

    if discord_id is not None:
        print(f"User ID: {discord_id}")
    else:
        print("Invalid mention format.")


async def setup(bot):
    await bot.add_cog(LocalStats(bot))
