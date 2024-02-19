from datetime import datetime

import discord
from discord import Embed

from functions.db_operate.db_firstjoin import get_whitelisted_players, get_playtime, get_playtimes
from functions.misc import seconds_to_hms
from functions.steam.steam import convert_steamid, get_steam_username, get_steam_profile_url
from tqdm import tqdm

from functions.steam.steam_user import get_steam_user_details


async def get_playtime_rank(channel) -> None:
    embeds = []
    steamids = get_whitelisted_players()

    datas = []
    steamid_playtimes = get_playtimes(steamids)

    progress_bar = tqdm(total=len(steamids), desc="Updating Playtime Ranking...", )
    for user in steamid_playtimes:
        progress_bar.update(1)

        steamid64 = convert_steamid(user['steamid'], 64)
        details = get_steam_user_details(steamid64)

        name = details['personaname']
        url = details['profileurl']

        datas.append([name, steamid64, user['playtime'], url])
    progress_bar.close()

    datas = sorted(datas, key=lambda x: x[2], reverse=True)
    chunk_size = 20
    sublists = [datas[i:i + chunk_size] for i in range(0, len(datas), chunk_size)]
    count = 0

    for sublist in sublists[:5]:
        content = ''
        for player in sublist:
            if player[2] != 0:
                hours, minutes, seconds = seconds_to_hms(player[2])
                count += 1
                content += f'{count}. [**{player[0]}**]({player[3]}) ----  **{hours}h {minutes}m {seconds}s**\n'
        embeds.append(Embed(description=content, colour=discord.Colour.blue()))

    embeds[0].title = 'Playtime Ranking'
    embeds[-1].timestamp = datetime.now()

    if embeds:
        await channel.purge(limit=None)
    for embed in embeds:
        await channel.send(embed=embed)


if __name__ == '__main__':
    pass
