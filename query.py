import sys

from valve.source import a2s
from servers import *
import requests


def format_seconds(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours >= 10:
        return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
    elif hours >= 1:
        return "{}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
    else:
        return "{:02}:{:02}".format(int(minutes), int(seconds))


def query_server(server: Server):   # NOQA
    try:
        with a2s.ServerQuerier((server.ip, server.port)) as s:
            info = s.info()
            players = s.players()
            tier = fetch_map_tier(info['map'])

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


def query_server_basic(server):     # NOQA
    try:
        with a2s.ServerQuerier((server.ip, server.port)) as s:
            info = s.info()
            players = s.players()
            # tier = fetch_map_tier(info['map'])

        content = (f"[{server.name_short[:2]}#{server.name_short[2]}](http://redirect.axekz.com/{server.id}):  "
                   f"{info['map']} "
                   f"{info['player_count']}/{info['max_players']}\n")
        if players:
            players_str = ''
            for player in players['players']:
                players_str += f"{player['name']}  "
                content += f"{player['name']}  "
            if players_str != '':
                content += "\n"
        return content
    except Exception as e:
        print(f"Error: {e}")


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


if __name__ == "__main__":
    print(fetch_map_tier('kz_p1'))
