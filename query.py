from valve.source import a2s
from servers import *


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

        content = (f"Server: {info['server_name']}"
                   f"\nMap: {info['map']}"
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

        content = (f"[{info['server_name']}](https://redirect.axekz.com/{server.id}):"
                   f" {info['map']}"
                   f" Players: {info['player_count']}/{info['max_players']}\n")
        if players:
            for player in players['players']:
                content += f"{player['name']}\t"
        content += "\n"
        return content
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    rs = format_seconds(5656)
    print(rs)
