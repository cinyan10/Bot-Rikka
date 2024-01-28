import discord
import requests
from discord import Embed

from config import STEAMID64, STEAM_API_KEY


def get_steam_profile_info(steamid64):
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={STEAM_API_KEY}&steamids={steamid64}"

    try:
        response = requests.get(url)
        data = response.json()

        # Check if the response contains the player data
        if 'response' in data and 'players' in data['response']:
            player_data = data['response']['players'][0]

            name = player_data['personaname']
            avatar_url = player_data['avatarfull']
            profile_url = player_data['profileurl']

            return name, avatar_url, profile_url
        else:
            return None, None, None

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None, None, None


def embed_set_author_steam(embed: discord.Embed, steamid64):
    name, avatar_url, profile_url = get_steam_profile_info(steamid64)

    embed.set_author(name=name, url=profile_url, icon_url=avatar_url)

    return embed


def embed_user_steam(steamid64):
    name, avatar_url, profile_url = get_steam_profile_info(steamid64)

    embed = Embed()
    embed.set_author(name=name, url=profile_url, icon_url=avatar_url)

    return embed


if __name__ == '__main__':

    name, avatar_url, profile_url = get_steam_profile_info(STEAMID64)

    if name:
        print(f"Steam Name: {name}")
        print(f"Avatar URL: {avatar_url}")
        print(f"Profile URL: {profile_url}")
    else:
        print("Failed to retrieve Steam profile information.")
