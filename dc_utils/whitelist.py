import asyncio

import discord.ext.commands
from discord import Embed

from dc_utils.info import set_wl_role
from functions.database import discord_id_to_steamid
from functions.db_operate.db_firstjoin import update_whitelist_status
from functions.globalapi.kz_global_stats import KzGlobalStats
from functions.steam.steam import convert_steamid, is_in_group
from functions.steam.steam_user import check_steam_bans


async def get_whitelisted(ctx):
    user_id = ctx.author.id
    steamid = discord_id_to_steamid(user_id)
    steamid64 = convert_steamid(steamid, 'steamid64')

    # Check if the player has been banned by VAC or multiple games
    ban_status = check_steam_bans(steamid64)
    if ban_status['vac_banned']:
        return await ctx.send(embed=Embed(title="You have been banned by VAC!!!", colour=discord.Colour.red()))
    elif ban_status['game_ban_count'] > 1:
        return await ctx.send(embed=Embed(title=f"You have been banned by {ban_status['game_ban_count']} games!!!", colour=discord.Colour.red()))
    else:
        await ctx.send(embed=Embed(title=f"You haven't been banned", colour=discord.Colour.green()))

    # Check if the player is in steam group
    is_group = is_in_group(steamid64)

    await asyncio.sleep(2)

    print(is_group)
    if is_group:
        await ctx.send(embed=Embed(title=f"You're In the Steam Group", colour=discord.Colour.green()))
    else:
        await ctx.send(embed=Embed(title=f"You haven't join in Steam Group yet!", colour=discord.Colour.red()))

    await asyncio.sleep(2)

    # Check if the player got enough pts
    for i in range(3):
        stats = KzGlobalStats(steamid64, i)
        if stats.is_reach_pts():
            await ctx.send(embed=Embed(title=f"You reached 50k pts!!", colour=discord.Colour.green()))
            update_whitelist_status(steamid)
            await ctx.send(embed=Embed(title=f"Added you to the whitelist", colour=discord.Colour.green()))
            await set_wl_role(ctx, steamid64)
            break
        await asyncio.sleep(2)

    await ctx.send(embed=Embed(title=f"You Didn't reach 50k pts!!", colour=discord.Colour.red()))
