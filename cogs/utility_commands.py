from discord.ext import commands

from dc_utils.firstjoin import find_player
from functions.database import reset_user_steam, bind_user_steam, discord_id_to_steamid
from functions.embed_content import user_info
from functions.gokzcn import get_gokzcn_info, assign_role_to_user, get_discord_role_from_data
from config import GUILD_ID
from pymysql.err import IntegrityError


class UtilityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def bind_steam(self, ctx, steamid: str):
        """Bind your steamid, steamid can be any type"""
        user_id = ctx.author.id
        try:
            bind_user_steam(user_id, steamid, ctx)
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
        player_data = result['player_data']

        guild = self.bot.get_guild(GUILD_ID)
        skill_score = player_data['point_skill']
        ranking = player_data['ranking']
        role_name = get_discord_role_from_data(skill_score, ranking)

        await assign_role_to_user(guild, discord_id, role_name)
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


def setup(bot):
    bot.add_cog(UtilityCommands(bot))
