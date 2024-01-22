import requests
from config import *


# Function to get Steam user's profile picture by their SteamID64
def get_steam_pfp(steam_id64):
    # Construct the API Request URL
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
    parameters = {
        'key': STEAM_API_KEY,  # Your Steam Web API key
        'steamids': steam_id64  # The SteamID64 of the user
    }

    # Make the API Call
    response = requests.get(url, params=parameters)

    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        # Parse the JSON Response for the profile picture URL
        players = data.get('response', {}).get('players', [])
        if players:
            return players[0].get('avatarfull', 'No avatar URL found')
        else:
            return 'No players data found'
    else:
        return f'Error: {response.status_code}'


def convert_steamid_to_steamid64(steamid):
    """
    Converts a STEAM_X:Y:Z format SteamID into a SteamID64.

    :param steamid: A SteamID in the format of STEAM_X:Y:Z
    :return: A SteamID64
    """
    # Split the SteamID into its parts
    parts = steamid.split(':')
    # Convert parts to integers
    y = int(parts[1])
    z = int(parts[2])
    # Use the conversion formula
    steamid64 = z * 2 + y + 76561197960265728
    return steamid64


def get_steam_profile_url(steamid64):
    """
    Constructs the URL to a Steam user's profile page using their SteamID64.

    :param steamid64: A SteamID64 of the user
    :return: The URL to the user's Steam profile page
    """
    base_url = "https://steamcommunity.com/profiles/"
    return f"{base_url}{steamid64}"


if __name__ == '__main__':
    steamid = 'STEAM_1:0:530988200'  # Replace this with the actual SteamID
    steamid64 = convert_steamid_to_steamid64(steamid)
    profile_url = get_steam_profile_url(steamid64)
    print(profile_url)
