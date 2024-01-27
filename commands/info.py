import discord
from discord import Embed
from discord.ext import commands
from dc_utils.firstjoin import find_player
from dc_utils.info import set_bili, set_steam
from dc_utils.setting import set_language, set_kz_mode
from functions.database import reset_user_steam, discord_id_to_steamid
from functions.embed_content import user_info
from functions.gokzcn import get_gokzcn_info
from pymysql.err import IntegrityError


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def bind_steam(self, ctx, steamid: str):
        """Bind your steamid, steamid can be any type (except: [U:X:XXXXXX])"""
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

    @commands.hybrid_command()
    async def reset_steam(self, ctx):
        """Resets the steamid"""
        user_id = ctx.author.id
        reset_user_steam(user_id)
        await ctx.send('Your Steam ID has been reset.')

    @commands.hybrid_command()
    async def gokzcn(self, ctx, steamid: str = None, mode: str = 'kzt'):
        """Show your gokz.cn info"""
        discord_id = ctx.author.id
        if steamid is None:
            steamid = discord_id_to_steamid(discord_id)
        result = get_gokzcn_info(discord_id=discord_id, mode=mode, steamid=steamid)
        embed_info = result['embed']
        await ctx.send(embed=embed_info)

    @commands.hybrid_command()
    async def info(self, ctx, steamid: str = None):
        """Show your information"""
        discord_id = ctx.author.id
        result = user_info(discord_id, steamid)
        await ctx.send(embed=result)

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
        discord_id = ctx.author.id
        rs = set_bili(ctx, bili_uid)
        await ctx.send(embed=Embed(title="bind_bili", description=rs, colour=discord.Colour.green()))


async def setup(bot):
    await bot.add_cog(Info(bot))
