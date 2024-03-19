from steam import Steam
from configs.steam import STEAM_API_KEY, STEAMID64

steam = Steam(STEAM_API_KEY)
user = steam.users.get_owned_games(STEAMID64)
print(user)
