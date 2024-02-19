from datetime import datetime

import discord

from discord import Embed
from tqdm import tqdm

from functions.db_operate.db_firstjoin import get_whitelisted_players
from functions.gokzcn import fetch_playerdata
from functions.steam.steam import convert_steamid


# [[steamid, name, skill, cnRank]]


def gokzcn_rank(mode='kzt') -> list[Embed]:
    embeds = []
    players: list = get_whitelisted_players()
    ranking = []

    pbar = tqdm(total=len(players), desc='Updating gokz.cn Ranking')
    for player in players:
        pbar.update(1)

        steamid64 = convert_steamid(player['steamid'], 'steamid64')
        data = fetch_playerdata(steamid64, mode=mode)
        if data:
            info = [data['name'], data['ranking'], data['point_skill'], data['url']]
            ranking.append(info)
    pbar.close()

    ranking = sorted(ranking, key=lambda x: x[2], reverse=True)
    chunk_size = 20
    sublists = [ranking[i:i + chunk_size] for i in range(0, len(ranking), chunk_size)]
    count = 0

    for sublist in sublists[:5]:
        content = ''
        for player in sublist:
            count += 1
            content += f'{count}. [**{player[0]}**]({player[3]}) - Skill: **{player[2]}** - cnRank: **{player[1]}**\n'
        embeds.append(Embed(description=content, colour=discord.Colour.blue()))

    embeds[0].title = "SERVER GOKZ.CN RANKING"
    embeds[-1].timestamp = datetime.now()

    return embeds


if __name__ == '__main__':

    pass
