import requests
from config import *
import xml.etree.ElementTree as element_tree  # NOQA


def get_steam_username(steamid64):
    # Replace with your Steam Web API key
    api_key = STEAM_API_KEY

    # Define the Steam Web API URL
    api_url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steamid64}"

    try:
        # Send a GET request to the Steam Web API
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            player_info = data["response"]["players"][0]

            # Extract and return the player's username (personaname)
            username = player_info.get("personaname")
            return username

        else:
            print(f"Error: HTTP {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None


# Function to get Steam user's profile picture by their SteamID64
def get_steam_pfp(steamid64):
    # Construct the API Request URL
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
    parameters = {
        'key': STEAM_API_KEY,  # Your Steam Web API key
        'steamids': steamid64  # The SteamID64 of the user
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


def convert_steamid(source_id, target_type):
    """
    Converts between SteamID, SteamID32, and SteamID64.

    :param source_id: The source SteamID in any format.
    :param target_type: The target format type ('steamid', 'steamid32', 'steamid64').
    :return: The converted SteamID in the target format.
    """
    source_id = str(source_id)

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


def is_user_in_steam_group(steamid64):
    page = 1
    while True:
        group_url = f"{GROUP_URL}&p={page}"
        try:
            response = requests.get(group_url)
            if response.status_code != 200:
                print(f"Failed to retrieve group members, status code: {response.status_code}")
                return False

            root = element_tree.fromstring(response.content)
            members = root.find('members')

            if members is None:
                print("Members list not found in XML.")
                return False

            for member in members:
                if member.text == steamid64:
                    return True

            # Check if there's a next page
            nextPage = root.find('nextPage')
            if nextPage is None or nextPage.text == "":
                break

            page += 1

        except requests.RequestException as e:
            print(f"Error making request: {e}")
            return False
        except element_tree.ParseError as e:
            print(f"XML Parsing Error: {e}")
            return False

    return False


if __name__ == '__main__':
    group_url = "https://steamcommunity.com/groups/axekz/memberslistxml/?xml=1"
    steamid64 = '76561199022242128'  # Replace with an actual SteamID64
    if is_user_in_steam_group(steamid64):
        print("User is in the group.")
    else:
        print("User is not in the group.")
