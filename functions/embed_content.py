import discord
from discord import Embed
from functions.database import *
from functions.steam import *
from functions.kreedz import *


def user_info(discord_id) -> discord.Embed:

    steamid = retrieve_steam_id(discord_id)
    steamid64 = convert_steamid_to_steamid64(steamid)

    name = retrieve_user_name(steamid)
    join_date = retrieve_join_date(steamid)
    last_seen = retrieve_last_seen(steamid)
    pfp_url = get_steam_pfp(steamid64)
    profile_url = get_steam_profile_url(steamid64)
    kzgoeu_url = get_kzgoeu_profile_url(steamid)

    embed = Embed(
        title="Info",
        description="",
        colour=discord.Colour.green()
    )
    embed.set_author(name=name, icon_url=pfp_url, url=profile_url)
    embed.url = kzgoeu_url

    return embed
