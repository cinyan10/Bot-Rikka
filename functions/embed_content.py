import discord
from discord import Embed
from functions.database import *
from functions.steam import *
from functions.kreedz import *
from functions.date_time import *


def user_info(discord_id) -> discord.Embed:

    steamid = retrieve_steam_id(discord_id)
    steamid64 = convert_steamid_to_steamid64(steamid)

    name = retrieve_user_name(steamid)
    joindate = format_string_to_datetime(retrieve_join_date(steamid))
    lastseen = format_string_to_datetime(retrieve_last_seen(steamid))
    pfp_url = get_steam_pfp(steamid64)
    profile_url = get_steam_profile_url(steamid64)
    kzgoeu_url = get_kzgoeu_profile_url(steamid)
    country = get_steam_user_country(steamid64).lower()

    content = (
        f":flag_{country}: **{name}**\n"
        f"**steamID**: `{steamid}`\n"
        f"**steamID64**: `{steamid64}`\n"
        f"**First join**: {joindate}\n"
        f"**Last seen**: {lastseen}\n"
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
