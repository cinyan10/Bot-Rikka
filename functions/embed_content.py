from datetime import datetime

import discord
from discord import Embed

from functions.database import get_steam_user_name, retrieve_join_date, retrieve_last_seen, \
    get_country_from_steamid32, query_jumpstats_top
from functions.db_operate.db_discord import discord_id_to_steamid
from functions.db_operate.db_firstjoin import get_playtime
from functions.globalapi.kzgoeu import get_kzgoeu_profile_url
from functions.misc import format_string_to_datetime, get_country_code, seconds_to_hms
from functions.steam.steam import convert_steamid, get_steam_pfp, get_steam_profile_url
from functions.steam.steam_user import get_steam_user_details


async def user_info(ctx, discord_id=None, steamid=None) -> None:

    if steamid is None:
        steamid = discord_id_to_steamid(discord_id)
    else:
        steamid = convert_steamid(steamid)

    if steamid is None:
        ctx.send(embed=Embed(title="Error!",
                             description="Query Steam error. Please ensure you have bound your Steam ID",
                             color=0xff0f0f,
                             timestamp=datetime.now()))
        return

    steamid64 = convert_steamid(steamid, 64)
    steamid32 = convert_steamid(steamid, 32)

    joindate = format_string_to_datetime(retrieve_join_date(steamid))
    lastseen = format_string_to_datetime(retrieve_last_seen(steamid))

    # kzgoeu_url = get_kzgoeu_profile_url(steamid)

    user = get_steam_user_details(steamid64)
    name = user['personaname']
    pfp_url = user['avatarfull']
    profile_url = user['profileurl']

    country_emoji = ':flag_' + get_country_code(get_country_from_steamid32(steamid32)).lower() + ':'

    playtime = get_playtime(steamid)
    hours, minutes, seconds = seconds_to_hms(playtime)

    content = (
        f"{country_emoji}: **{name}**\n"
        f"**steamID**: `{steamid}`\n"
        f"**steamID64**: `{steamid64}`\n"
        f"**First Join**: {joindate}\n"
        f"**Last Seen**: {lastseen}\n"
        f"**Playtime**: {hours}h, {minutes}m, {seconds}s,\n"
    )

    embed = Embed(
        title=f"Profile",
        description=content,
        colour=discord.Colour.blue(),
    )
    embed.set_author(name=f"{name}", icon_url=pfp_url, url=profile_url)
    embed.url = profile_url
    embed.set_image(url=pfp_url)

    await ctx.send(embed=embed)


def get_jstop(limit: int, mode: str) -> discord.Embed:
    content = query_jumpstats_top(limit, mode)
    embed = Embed(
        title="JUMPSTATS TOP " + mode.upper(),
        description=content,
        colour=discord.Colour.green()
    )

    return embed
