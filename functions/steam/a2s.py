from valve.source import a2s
from config import SERVER_LIST


def fetch_online_player(ip: str, port: int) -> tuple:
    try:
        with a2s.ServerQuerier((ip, port)) as server:
            info = server.info()
            return info['player_count'], info['max_players']
    except Exception as e:
        print("Error fetching online player: ", e)


if __name__ == "__main__":
    s = SERVER_LIST[0]
    print(type(s.ip), type(s.port))
    rs = fetch_online_player(s.ip, s.port)
    print(rs)
    pass
