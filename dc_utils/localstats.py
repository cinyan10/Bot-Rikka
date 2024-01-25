
import discord
from discord import Embed
from functions.steam import *
from functions.database import get_total_playtime
from functions.db_operate.firstjoin import get_whitelisted_players
from functions.steam import convert_steamid


def get_playtime_rank() -> list[Embed]:
    embeds = []
    steamids = get_whitelisted_players()

    datas = []
    count = 0
    for steamid in steamids:
        count = count + 1
        print(f"{count}/{len(steamids)} {steamid}")
        steamid32 = convert_steamid(steamid, 'steamid32')
        steamid64 = convert_steamid(steamid, 'steamid64')
        playtime = get_total_playtime(steamid32)
        name = get_steam_username(steamid64)
        url = get_steam_profile_url(steamid64)
        datas.append([name, steamid64, playtime, url])

    datas = sorted(datas, key=lambda x: x[2][0] * 3600 + x[2][1] * 60 + x[2][2], reverse=True)
    chunk_size = 20
    sublists = [datas[i:i + chunk_size] for i in range(0, len(datas), chunk_size)]
    count = 0

    for sublist in sublists:
        content = ''
        for player in sublist:
            count += 1
            content += f'[**{count}. {player[0]}**]({player[3]}) - Play Time: **{player[2][0]}h, {player[2][1]}m, {player[2][2]}s**\n'
        embeds.append(Embed(description=content, colour=discord.Colour.blue()))

    return embeds


if __name__ == '__main__':
    rs = get_playtime_rank()
    print(rs)
