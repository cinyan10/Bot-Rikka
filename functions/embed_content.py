import discord
from discord import Embed
from functions.database import *
from functions.steam import *
from functions.kreedz import *
from functions.date_time import *
from functions.database import *


def user_info(discord_id) -> discord.Embed:

    steamid = retrieve_steam_id(discord_id)
    steamid64 = steamid_to_steamid64(steamid)
    steamid32 = steamid64_to_steamid32(steamid64)

    name = get_steam_user_name(steamid)
    joindate = format_string_to_datetime(retrieve_join_date(steamid))
    lastseen = format_string_to_datetime(retrieve_last_seen(steamid))
    pfp_url = get_steam_pfp(steamid64)
    profile_url = get_steam_profile_url(steamid64)
    kzgoeu_url = get_kzgoeu_profile_url(steamid)
    country = get_steam_user_country(steamid64).lower()
    total_playtime = get_total_playtime(steamid32)

    content = (
        f":flag_{country}: **{name}**\n"
        f"**steamID**: `{steamid}`\n"
        f"**steamID64**: `{steamid64}`\n"
        f"**First Join**: {joindate}\n"
        f"**Last Seen**: {lastseen}\n"
        f"**Playtime**: {total_playtime}\n"
    )

    embed = Embed(
        title=f"Info",
        description=content,
        colour=discord.Colour.blue(),
    )
    embed.set_author(name=f"{name}", icon_url=pfp_url, url=profile_url)
    embed.url = kzgoeu_url
    embed.set_image(url=pfp_url)

    return embed


def get_jstop(limit: int, mode: str) -> discord.Embed:
    content = query_jumpstats_top(limit, mode)
    embed = Embed(
        title="JUMPSTATS TOP" + mode.upper(),
        description=content,
        colour=discord.Colour.green()
    )

    return embed