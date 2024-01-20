from valve.source import a2s

servers = [
    ['43.139.56.16', 10001],
    ['43.139.56.16', 10002],
    ['43.139.56.16', 10003],
    ['43.139.56.16', 10004],
    ['43.139.56.16', 10005],
    ['43.139.56.16', 10006],
    ['43.138.126.94', 10001],
    ['43.138.126.94', 10002],
    ['43.138.126.94', 10003],
    ['43.138.126.94', 10004],
    ['43.138.126.94', 10005],
    ['43.138.126.94', 10006],
]

servers_dict = {
    '广州1': ['43.139.56.16', 10001],
    '广州2': ['43.139.56.16', 10002],
    '广州3': ['43.139.56.16', 10003],
    '广州4': ['43.139.56.16', 10004],
    '广州5': ['43.139.56.16', 10005],
    '广州6': ['43.139.56.16', 10006],
    '北京1': ['43.138.126.94', 10001],
    '北京2': ['43.138.126.94', 10002],
    '北京3': ['43.138.126.94', 10003],
    '北京4': ['43.138.126.94', 10004],
    '北京5': ['43.138.126.94', 10005],
    '北京6': ['43.138.126.94', 10006],
}


def format_duration(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes)}:{int(seconds)} "


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
                print(f"{player['name']} - Time: {format_duration(player['duration'])}")
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
                content += f"{player['name']} - Time: {format_duration(player['duration'])}"

        return content
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    server_ip = "43.139.56.16"
    server_port = 10003  # Default CS:GO port is usually 27015

    query_csgo_server(server_ip, server_port)
