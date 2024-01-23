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


def get_steam_profile_url(steamid64):
    """
    Constructs the URL to a Steam user's profile page using their SteamID64.

    :param steamid64: A SteamID64 of the user
    :return: The URL to the user's Steam profile page
    """
    base_url = "https://steamcommunity.com/profiles/"
    return f"{base_url}{steamid64}"


def get_steam_user_country(steamid64):
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
    params = {
        'key': STEAM_API_KEY,
        'steamids': steamid64
    }

    response = requests.get(url, params=params)
    data = response.json()

    try:
        country = data['response']['players'][0]['loccountrycode']
        return country
    except (KeyError, IndexError):
        return "black"


def steamid32_to_steamid64(steamid32):
    """
    Converts a SteamID32 to a SteamID64.

    :param steamid32: A SteamID32 (a 32-bit integer)
    :return: A SteamID64 (a 64-bit integer)
    """
    steamid64_base = 76561197960265728
    steamid32_int = int(steamid32)
    steamid64 = steamid32_int + steamid64_base
    return steamid64


def steamid64_to_steamid32(steamid64):
    """
    Converts a SteamID64 to a SteamID32.

    :param steamid64: A SteamID64 (a 64-bit integer)
    :return: A SteamID32 (a 32-bit integer)
    """
    steamid64_base = 76561197960265728
    steamid32 = steamid64 - steamid64_base
    return steamid32


def steamid64_to_steamid(steamid64):
    """
    Converts a SteamID64 to a STEAM_X:Y:Z format SteamID.

    :param steamid64: A SteamID64
    :return: A SteamID in the format of STEAM_X:Y:Z
    """
    steamid64_base = 76561197960265728
    z = (steamid64 - steamid64_base) // 2
    y = (steamid64 - steamid64_base) % 2
    return f"STEAM_1:{y}:{z}"


def steamid_to_steamid64(steamid):
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


def steamid32_to_steamid(steamid32):
    steamid64 = steamid32_to_steamid64(steamid32)
    steamid = steamid64_to_steamid(steamid64)
    return steamid


def steamid_to_steamid32(steamid):
    steamid64 = steamid_to_steamid64(steamid)
    steamid32 = steamid32_to_steamid64(steamid64)
    return steamid32


def convert_steam_id(source_id, target_type):
    """
    Converts between SteamID, SteamID32, and SteamID64.

    :param source_id: The source SteamID in any format.
    :param target_type: The target format type ('steamid', 'steamid32', 'steamid64').
    :return: The converted SteamID in the target format.
    """
    def steamid_to_steamid64(steamid):
        parts = steamid.split(':')
        y = int(parts[1])
        z = int(parts[2])
        return z * 2 + y + 76561197960265728

    def steamid64_to_steamid(steamid64):
        steamid64_base = 76561197960265728
        z = (steamid64 - steamid64_base) // 2
        y = (steamid64 - steamid64_base) % 2
        return f"STEAM_1:{y}:{z}"

    def steamid32_to_steamid64(steamid32):
        return steamid32 + 76561197960265728

    def steamid64_to_steamid32(steamid64):
        return steamid64 - 76561197960265728

    # Format source SteamID if it starts with STEAM_0
    if source_id.startswith("STEAM_0"):
        source_id = "STEAM_1" + source_id[7:]

    # Detect source SteamID format
    if ':' in source_id:  # STEAM_X:Y:Z format
        source_format = 'steamid'
        steamid64 = steamid_to_steamid64(source_id)
    elif source_id.isdigit():
        if len(source_id) > 10:  # SteamID64 format
            source_format = 'steamid64'
            steamid64 = int(source_id)
        else:  # SteamID32 format
            source_format = 'steamid32'
            steamid64 = steamid32_to_steamid64(int(source_id))
    else:
        raise ValueError("Invalid SteamID format")

    # Convert to target format
    if target_type == 'steamid':
        return steamid64_to_steamid(steamid64) if source_format != 'steamid' else source_id
    elif target_type == 'steamid32':
        return steamid64_to_steamid32(steamid64) if source_format != 'steamid32' else int(source_id)
    elif target_type == 'steamid64':
        return steamid64 if source_format != 'steamid64' else int(source_id)
    else:
        raise ValueError("Invalid target format type")


if __name__ == '__main__':
    # Example usage
    source_id = '76561199022242128'  # This can be any of SteamID, SteamID32, or SteamID64
    target_type = 'steamid64'  # Can be 'steamid', 'steamid32', or 'steamid64'
    converted_id = convert_steam_id(source_id, target_type)
    print(converted_id)
