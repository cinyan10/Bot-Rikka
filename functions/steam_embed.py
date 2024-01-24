from datetime import date, datetime, timedelta, time
from decimal import Decimal
from typing import Tuple, Any, Set, Dict

import discord
from discord import Embed
from functions.database import get_steam_user_name
from functions.steam import *


def steam_embed(steamid, title=None, description=None, timestamp=None):
    steamid64 = convert_steamid(steamid, 'steamid64')
    embed = Embed(
        colour=discord.Colour.blue(),
        title=title,
        description=description,
        timestamp=timestamp,
    )

    profile_url = get_steam_profile_url(steamid64)
    pfp_url = get_steam_pfp(steamid64)
    username = get_steam_username(steamid64)
    embed.set_author(name=username, icon_url=pfp_url, url=profile_url)

    return embed


if __name__ == '__main__':
    pass
