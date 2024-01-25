from datetime import datetime

import discord
from discord import Embed
from functions.db_operate.firstjoin import *
from functions.gokzcn import fetch_playerdata


# [[steamid, name, skill, cnRank]]


def gokzcn_rank(mode='kzt') -> Embed:
    players: list = get_whitelisted_players()
    ranking = []

    count = 0
    for steamid in players:
        count += 1
        print("loading", count, '/', len(players))
        steamid64 = convert_steamid(steamid, 'steamid64')
        data = fetch_playerdata(steamid64, mode=mode)
        if data:
            info = [data['name'], data['ranking'], data['point_skill'], data['url']]
            ranking.append(info)

    ranking = sorted(ranking, key=lambda x: x[2], reverse=True)

    content = ''
    count = 0
    for player in ranking[:30]:
        count += 1
        content += f'[**{count}. {player[0]}**]({player[3]}) - Skill: **{player[2]}** - cnRank: **{player[1]}**\n'

    rank_embed = Embed(title="SERVER GOKZ.CN Ranking", description=content, colour=discord.Colour.blue(), timestamp=datetime.now())

    return rank_embed


if __name__ == '__main__':
    gokzcn_rank()
