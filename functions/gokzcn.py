import discord
import requests
from discord import Embed
from functions.database import discord_id_to_steamid
from functions.steam import convert_steam_id


def get_gokzcn_info(discord_id=None, mode='kzt', steamid=None):
    player_data = None
    if steamid is None:
        steamid = discord_id_to_steamid(discord_id)
    steamid64 = convert_steam_id(steamid, 'steamid64')
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
    content = (
        f'Mode: {mode.upper()}\n'
        f'Rank: {player_data["ranking"]}\n'
        f'Skill Score: {player_data["point_skill"]}\n'
    )

    info_embed = Embed(title=f"bilibili: {player_data['bili_name']}", description=content, colour=discord.Colour.yellow(), url=bili_url)
    info_embed.set_author(name=player_data['name'], icon_url=player_data['avatar'], url=player_data['url'])

    return info_embed


def get_discord_role_from_data(skill_score, ranking):
    if ranking <= 10:
        return "Legend"
    elif skill_score >= 8.0:
        return "Master"
    elif skill_score >= 7.5:
        return "Professional"
    elif skill_score >= 7.0:
        return "Expert"
    elif skill_score >= 6.0:
        return "Skilled"
    elif skill_score >= 5.0:
        return "Intermediate"
    elif skill_score >= 4.0:
        return "Beginner"
    else:
        return "New"


async def assign_role_to_user(guild, discord_id, role_name):
    member = guild.get_member(discord_id)
    if not member:
        print(f"Member with ID {discord_id} not found.")
        return

    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        print(f"Role '{role_name}' not found.")
        return

    await member.add_roles(role)


if __name__ == "__main__":
    pass
