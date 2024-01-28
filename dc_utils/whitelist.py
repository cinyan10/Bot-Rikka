import discord.ext.commands
import requests

from functions.database import discord_id_to_steamid
from functions.steam.steam import convert_steamid


async def get_whitelisted(bot: discord.ext.commands.Bot, ctx):
    user_id = ctx.author.id
    steamid = discord_id_to_steamid(user_id)
    steamid64 = convert_steamid(steamid, 'steamid64')

    # Check if the player has been banned by VAC or multiple games
