import discord
import requests
from discord import Embed, File, Message

from functions.database import discordid_to_steamid
from functions.steam import steamid_to_steamid64


def get_gokzcn_info(discord_id=None, mode='kzt', steamid=None):
    player_data = None
    if steamid is None:
        steamid = discordid_to_steamid(steamid)
    steamid64 = steamid_to_steamid64(steamid)
    gokzcn_url = f"http://gokz.cn/api/rankings?page_size=1&search_text={steamid64}&mode={mode}"
    response = requests.get(gokzcn_url)

    if response.status_code == 200:
        try:
            player_data = response.json()['data']['list'][0]  # Parse JSON data
        except ValueError:
            print("Failed to parse JSON")
    else:
        print(f"Failed to retrieve data: {response.status_code}")

    bili_url = f"https://space.bilibili.com/{player_data['bili_id']}"
    content = (f'Rank: {player_data["ranking"]}\n'
               f'Skill Score: {player_data["point_skill"]}\n')

    info_embed = Embed(title=f"bilibili: {player_data['bili_name']}", description=content, colour=discord.Colour.yellow(), url=bili_url)
    info_embed.set_author(name=player_data['name'], icon_url=player_data['avatar'], url=player_data['url'])

    return info_embed


if __name__ == "__main__":
    rs = get_gokzcn_info(steamid='STEAM_1:0:530988200')
    print(rs)

