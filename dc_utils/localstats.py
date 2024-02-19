from datetime import datetime

import discord
from discord import Embed

from functions.db_operate.db_firstjoin import get_whitelisted_players, get_playtime
from functions.misc import seconds_to_hms
from functions.steam.steam import convert_steamid, get_steam_profile_url
from tqdm import tqdm


async def get_playtime_rank(channel) -> None:
    embeds = []
    datas = []

    names_id = get_whitelisted_players()

    progress_bar = tqdm(total=len(names_id), desc="Updating Playtime Ranking...", )
    for user in names_id:
        progress_bar.update(1)

        playtime = get_playtime(user['steamid'])
        steamid64 = convert_steamid(user['steamid'], 64)
        url = get_steam_profile_url(steamid64)

        datas.append([user['name'], steamid64, playtime, url])
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
