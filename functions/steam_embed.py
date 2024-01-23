import discord
from discord import Embed
from functions.database import get_steam_user_name
from functions.steam import *


def steam_embed(steamid, title=None, description=None, timestamp=None) -> Embed:
    steamid = convert_steamid(steamid, 'steamid')
    embed = Embed(
        colour=discord.Colour.blue(),
        title=title,
        description=description,
        timestamp=timestamp,
    )

    profile_url = get_steam_profile_url(steamid)
    pfp_url = get_steam_pfp(steamid)
    username = get_steam_user_name(steamid)
    embed.set_author(name=username, icon_url=pfp_url, url=profile_url)

    return embed
