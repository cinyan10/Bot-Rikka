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
    joindate = formatted_datetime(retrieve_join_date(steamid))
    lastseen = formatted_datetime(retrieve_last_seen(steamid))
    pfp_url = get_steam_pfp(steamid64)
    profile_url = get_steam_profile_url(steamid64)
    kzgoeu_url = get_kzgoeu_profile_url(steamid)

    embed = Embed(
        title="Info",
        description=f"First join: <t:{timestamp}>\nLast seen: <t:{timestamp}>",
        colour=discord.Colour.green()
    )
    embed.set_author(name=name, icon_url=pfp_url, url=profile_url)
    embed.url = kzgoeu_url
    embed.set_image(url=pfp_url)
    embed.set_footer()

    return embed
