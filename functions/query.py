from discord import Embed
from valve.source import a2s

from config import MAP_TIERS, SERVER_LIST
from functions.servers import *
import requests


# Functions
def format_seconds(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours >= 10:
        return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
    elif hours >= 1:
        return "{}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
    else:
        return "{:02}:{:02}".format(int(minutes), int(seconds))


async def query_server_embed(server: Server, bot=None) -> Embed:
    try:
        with a2s.ServerQuerier((server.ip, server.port)) as s:
            info = s.info()
            players = s.players()
            try:
                tier = MAP_TIERS[info['map']]
            except Exception:
                tier = 'T0'

            players_str = ''
            for player in players['players']:
                players_str += f"\n{player['name']} - {format_seconds(player['duration'])}"

            embed = Embed(
                title=f'{info['map']} - T{tier}',
                description=players_str,
                color=0x58b9ff,
            )

            embed.set_author(name=f"{info['server_name']}    {info['player_count']}/{info['max_players']}")
            embed.url = f'http://redirect.axekz.com/{server.id}'
            embed.set_image(url=f"https://raw.githubusercontent.com/KZGlobalTeam/map-images/master/images/{info['map']}.jpg")

            # edit channel name
            if bot:
                channel = bot.get_channel(server.channel_id)
                await channel.edit(name=f"{server.name_short}│{info['player_count']}／{info['max_players']}")

            return embed
    except Exception as e:
        print(f"Error: {e}")
        return Embed(title="Error")


def query_server_details(server: Server) -> str:  # NOQA
    try:
        with a2s.ServerQuerier((server.ip, server.port)) as s:
            info = s.info()
            players = s.players()
            try:
                tier = MAP_TIERS[info['map']]
            except Exception:
                tier = 'T0'

        content = (f"Server: {info['server_name']}"
                   f"\nMap: {info['map']} T{tier}"
                   f"\nPlayers: {info['player_count']}/{info['max_players']}")
        if players:
            content += "\nPlayer List:"
            for player in players['players']:
                content += f"\n{player['name']}\t - Time: {format_seconds(player['duration'])}"

        return content
    except Exception as e:
        print(f"Error: {e}")


def query_server_simple(server):  # NOQA
    try:
        with a2s.ServerQuerier((server.ip, server.port)) as s:
            info = s.info()
            players = s.players()
            try:
                tier = MAP_TIERS[info['map']]
            except Exception:
                tier = 'T0'
        content = (f"[**AXE GOKZ {server.name_short[:2]}#{server.name_short[2]}**](http://redirect.axekz.com/{server.id}):  "
                   f"*{info['map']}* "
                   f'**T{tier}**  '
                   f"{info['player_count']}/{info['max_players']}\n")

        if players:
            players_str = ''
            for player in players['players']:
                content += f"`{player['name']}`  "
                players_str += f"`{player['name'].replace('`', '')}`"
            if players_str != '':
                content += "\n"
        return content
    except Exception as e:
        print(f"Error: {e}")
        return ""


def fetch_map_tier(map_name: str):
    try:
        response = requests.get('https://kztimerglobal.com/api/v2.0/maps/name/' + map_name)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the response as JSON (assuming the API returns JSON)
            data = response.json()
            return data['difficulty']
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None


def query_all_servers() -> str:
    info_data = ''
    for s in SERVER_LIST:
        info_data += query_server_simple(s)

    return info_data


if __name__ == "__main__":
    rs = query_all_servers()
    print(rs, type(rs))
