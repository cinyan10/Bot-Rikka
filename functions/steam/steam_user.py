import discord
import requests
from discord import Embed

from config import STEAM_API_KEY


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


def check_vac_bans(steamid64):
    api_key = STEAM_API_KEY

    url = f"https://api.steampowered.com/ISteamUser/CheckPlayerBans/v1/?key={api_key}&steamids={steamid64}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        bans = data.get("players", [])

        if bans:
            for ban in bans:
                game = ban.get("AppName", "Unknown Game")
                days_since_last_ban = ban.get("DaysSinceLastBan", 0)
                num_bans = ban.get("NumberOfVACBans", 0)

                print(f"Game: {game}")
                print(f"Days Since Last Ban: {days_since_last_ban}")
                print(f"Number of VAC Bans: {num_bans}")
        else:
            print("No VAC bans found for this user.")
    else:
        print("Failed to fetch VAC ban information.")

# Replace with the user's SteamID64


if __name__ == '__main__':
    user_steamid64 = "76561198083328612"
    check_vac_bans(user_steamid64)
    pass
