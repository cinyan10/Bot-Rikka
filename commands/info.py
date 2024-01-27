import discord
from discord import Embed
from discord.ext import commands
from dc_utils.firstjoin import find_player
from dc_utils.info import set_bili, set_steam, set_wl_role
from dc_utils.setting import set_language, set_kz_mode
from functions.database import reset_user_steam, discord_id_to_steamid
from functions.embed_content import user_info
from functions.globalapi.kz_global_stats import KzGlobalStats
from functions.gokzcn import get_gokzcn_info
from pymysql.err import IntegrityError

from functions.steam import convert_steamid


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def info(self, ctx, member: discord.Member = None, steamid: str = None):
        """Show your or other's information"""
        discord_id = member.id if member else ctx.author.id
        result = user_info(discord_id, steamid)
        await ctx.send(embed=result)

    @commands.hybrid_command()
    async def bind_steam(self, ctx, steamid: str):
        """Bind your steamid, steamid can be any type (except: [U:X:XXXXXX])"""
        steamid = convert_steamid(steamid, "steamid")

        # Bind steamid
        try:
            set_steam(ctx, steamid)
            await ctx.send('Steam ID bound successfully!')
        except IntegrityError as e:
            # Check for duplicate entry error
            if 'Duplicate entry' in str(e) and 'steamid_32' in str(e):
                await ctx.send('This Steam ID is already bound to another user.')
            else:
                await ctx.send('An error occurred while binding the Steam ID.')
        except Exception as e:
            await ctx.send(f'An unexpected error occurred: {e}')

        # Set Whitelisted Role
        try:
            await set_wl_role(ctx, steamid=steamid)
        except Exception as e:
            await ctx.send(f'An unexpected error occurred: {e}')

    @commands.hybrid_command()
    async def reset_steam(self, ctx):
        """Resets the steamid"""
        user_id = ctx.author.id
        reset_user_steam(user_id)
        await ctx.send('Your Steam ID has been reset.')

    @commands.hybrid_command()
    async def gokzcn(self, ctx, member: discord.Member = None, steamid: str = None, mode: str = 'kzt'):
        """Show your gokz.cn info"""
        discord_id = member.id if member else ctx.author.id
        if steamid is None:
            steamid = discord_id_to_steamid(discord_id)
        result = get_gokzcn_info(discord_id=discord_id, mode=mode, steamid=steamid)
        embed_info = result['embed']
        await ctx.send(embed=embed_info)

    @commands.hybrid_command()
    async def find(self, ctx, name: str):
        """find a player by name"""
        await find_player(ctx, name)

    @commands.hybrid_command(name="setting")
    async def setting(self, ctx, language=None, kz_mode=None):
        """
        settings
        """
        if language:
            await set_language(ctx, language)
        if kz_mode:
            await set_kz_mode(ctx, kz_mode)

    @commands.hybrid_command()
    async def bind_bili(self, ctx, bili_uid):
        """Set your Bilibili UID"""
        rs = set_bili(ctx, bili_uid)
        await ctx.send(embed=Embed(title="bind_bili", description=rs, colour=discord.Colour.green()))

    @commands.hybrid_command(name="get_role")
    async def get_role(self, ctx):
        """Get the whitelisted role if you are"""
        discord_id = ctx.author.id
        steamid = discord_id_to_steamid(discord_id)
        await set_wl_role(ctx, steamid=steamid)

    @commands.hybrid_command(name="kz")
    async def kz(self, ctx, steamid=None):
        ms = await ctx.send(embed=Embed(title="KZ Stats Loading..."))
        if steamid:
            steamid64 = convert_steamid(steamid, "steamid64")
        else:
            discord_id = ctx.author.id
            steamid = discord_id_to_steamid(discord_id)
            steamid64 = convert_steamid(steamid, "steamid64")
        try:
            embed = KzGlobalStats(steamid64).embed_stats()
        except Exception as e:
            embed = Embed(title="Error!", description=str(e), colour=discord.Colour.red())
        await ms.edit(embed=embed)


async def setup(bot):
    await bot.add_cog(Info(bot))
