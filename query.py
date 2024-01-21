from valve.source import a2s


def format_seconds(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours >= 10:
        return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
    elif hours >= 1:
        return "{}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
    else:
        return "{:02}:{:02}".format(int(minutes), int(seconds))


def query_csgo_server(ip, port):
    try:
        with a2s.ServerQuerier((ip, port)) as server:
            info = server.info()
            players = server.players()

        print(f"Server Info:")
        print(f"Server Name: {info['server_name']}")
        print(f"Map: {info['map']}")
        print(f"Players: {info['player_count']}/{info['max_players']}")

        if players:
            print("\nPlayer List:")
            for player in players['players']:
                print(f"{player['name']} - Time: {format_seconds(player['duration'])}")
    except Exception as e:
        print(f"Error: {e}")


def query_server(ip, port):
    try:
        with a2s.ServerQuerier((ip, port)) as server:
            info = server.info()
            players = server.players()

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


def query_server_basic(ip, port):
    try:
        with a2s.ServerQuerier((ip, port)) as server:
            info = server.info()
            players = server.players()

        content = (f"[{info['server_name']}](https://redirect.axekz.com/):"
                   f" {info['map']}"
                   f" Players: {info['player_count']}/{info['max_players']}\n")
        # if players:
        #     content += "\nPlayer List:"
        #     for player in players['players']:
        #         content += f"\n{player['name']}\t - Time: {format_duration(player['duration'])}"
        return content
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    rs = format_seconds(5656)
    print(rs)
